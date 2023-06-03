import customtkinter
import sqlite3


class Task:
    def __init__(self, title, counter=None, deadline=None):
        if len(title) < 60:
            self.title = title
        else:
            self.title = title[:60]

        self.counter = counter

        if deadline is None:
            self.deadline = deadline
        elif len(deadline) < 20:
            self.deadline = deadline
        else:
            self.deadline = deadline[:20]


class CounterFrame(customtkinter.CTkFrame):
    def __init__(self, task, master, **kwargs):
        super().__init__(master, **kwargs)
        self.task = task

        self.add_button = customtkinter.CTkButton(self, text="", height=9, width=30, command=self.add_button_callback)
        self.add_button.grid(row=0, column=0)

        self.counter_entry = customtkinter.CTkEntry(self, height=12, width=30, font=('', 14))
        self.counter_entry.grid(row=1, column=0)
        self.counter_entry.insert(0, self.task.counter)

        self.sub_button = customtkinter.CTkButton(self, text="", height=9, width=30, command=self.sub_button_callback)
        self.sub_button.grid(row=3, column=0)

    def add_button_callback(self):
        self.task.counter += 1
        self.counter_entry.delete(0, "end")
        self.counter_entry.insert(0, self.task.counter)

    def sub_button_callback(self):
        self.task.counter -= 1
        self.counter_entry.delete(0, "end")
        self.counter_entry.insert(0, self.task.counter)


class TaskFrame(customtkinter.CTkFrame):
    def __init__(self, task, id, master, **kwargs):
        super().__init__(master, **kwargs)
        self.task = task
        self.id = id
        self.column = 2

        self.grid_columnconfigure(self.column, weight=1)

        self.task_label = customtkinter.CTkLabel(self, height=30, font=('', 16),
                                                 text=str(self.id + 1) + ". " + self.task.title)
        self.task_label.grid(row=0, column=0, padx=10, columnspan=2)

        if not self.task.counter is None:
            self.column += 1
            self.grid_columnconfigure(self.column, weight=1)
            self.counter = CounterFrame(master=self, width=30, task=self.task)
            self.counter.grid(row=0, column=self.column - 1)

        if not self.task.deadline is None:
            self.column += 1
            self.grid_columnconfigure(self.column, weight=1)
            self.task_deadline = customtkinter.CTkLabel(self, height=30, text_color="#D10031",
                                                        font=('', 14), text=self.task.deadline)
            self.task_deadline.grid(row=0, column=self.column - 1, padx=10)

        self.column += 1
        self.grid_columnconfigure(self.column, weight=1)
        self.delete_task_button = customtkinter.CTkButton(self, text_color='red', text="X",
                                                          height=30, width=20, fg_color='#DBDBDB')
        self.delete_task_button.grid(row=0, column=self.column - 1, padx=10)


class TasksListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, tasks=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.task_frames = []

        self.update_tasks(tasks)

    def update_tasks(self, tasks):
        for task_frame in self.task_frames:
            task_frame.destroy()
        self.task_frames.clear()
        for i, task in enumerate(tasks):
            self.task_frames.append(TaskFrame(master=self, task=task, id=i))
            self.task_frames[i].grid(row=i, column=0, pady=5, sticky="nw")
            self.task_frames[i].delete_task_button.bind('<Button-1>', self.delete_task)

    def delete_task(self, event):
        button = event.widget.master
        task_frame = button.master
        self.task_frames.remove(task_frame)
        canvas = self.master
        frame = canvas.master
        app = frame.master
        app.remove_task(task_frame.task)
        task_frame.destroy()



class CreateTaskWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_task = None

        self.title("CreateTask")

        self.grid_columnconfigure(2, weight=1)

        self.task_title_entry = customtkinter.CTkEntry(self, width=300, placeholder_text="Название новой задачи")
        self.task_title_entry.grid(row=0, column=0, pady=(20, 10), columnspan=2)

        self.task_deadline_entry = customtkinter.CTkEntry(self, width=150,
                                                          placeholder_text="Дедлайн задачи (не обязательно)")
        self.task_deadline_entry.grid(row=1, column=0, padx=10, pady=10)

        self.task_counter_checkbox = customtkinter.CTkCheckBox(self, width=150, text="Трекер")
        self.task_counter_checkbox.grid(row=1, column=1, padx=10, pady=10)

        self.create_task_button = customtkinter.CTkButton(self, text="Добавить",
                                                          command=self.create_task_button_callback)
        self.create_task_button.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="ew")

        self.cancel_button = customtkinter.CTkButton(self, text="Отмена",
                                                     command=self.cancel_button_callback)
        self.cancel_button.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="ew")

        self.bind('<Return>', self.create_task_button_callback)
        self.bind('<M2-Up>', self.task_counter_checkbox.toggle)
        self.bind('<Escape>', self.cancel_button_callback)

    def create_task_button_callback(self, event=None):
        title = self.task_title_entry.get()
        deadline = self.task_deadline_entry.get()

        if deadline == "":
            deadline = None

        if self.task_counter_checkbox.get():
            counter = 0
        else:
            counter = None

        self.new_task = Task(title, counter, deadline)
        self.destroy()

    def cancel_button_callback(self, event=None):
        self.destroy()

    def get_new_task(self):
        self.grab_set()
        self.wait_window()
        return self.new_task


class App(customtkinter.CTk):
    tasks = []

    def __init__(self):
        super().__init__()

        self.connect_sql("tasks.db")

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.create_task_window = None
        self.title("TaskManager")
        self.geometry("500x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3)

        self.create_task_button = customtkinter.CTkButton(self, text="Добавить задачу",
                                                          command=self.open_create_task_window)
        self.create_task_button.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.tasks_list_frame = TasksListFrame(master=self, height=350, tasks=self.tasks)
        self.tasks_list_frame.grid(row=1, column=0, padx=20, pady=(10, 20), rowspan=2, sticky="news")

        self.bind('<Return>', self.open_create_task_window)

    def close(self):
        self.save_sql()
        self.destroy()

    def save_sql(self):
        for task in self.tasks:
            tracker = "null" if task.counter is None else f'{task.counter}'
            deadline = "deadline IS null" if task.deadline is None else f'deadline="{task.deadline}"'
            self.cur_db.execute(f'''UPDATE tasks 
                                    SET tracker={tracker} 
                                    WHERE title='{task.title}'
                                    AND {deadline}''')
            self.con.commit()

    def open_create_task_window(self, event=None):
        if self.create_task_window is None or not self.create_task_window.winfo_exists():
            self.create_task_window = CreateTaskWindow(self)
            new_task = self.create_task_window.get_new_task()
            if not new_task is None:
                self.append_task(new_task)
        else:
            self.create_task_window.focus()

    def append_task(self, task):
        self.tasks.append(task)
        self.tasks_list_frame.update_tasks(self.tasks)
        self.append_sql(task)

    def remove_task(self, task):
        self.remove_sql(task)
        self.tasks.remove(task)
        self.tasks_list_frame.update_tasks(self.tasks)

    def remove_sql(self, task):
        tracker = "tracker IS null" if task.counter is None else f'tracker={task.counter}'
        deadline = "deadline IS null" if task.deadline is None else f'deadline="{task.deadline}"'
        self.cur_db.execute(f'''DELETE FROM tasks 
                            WHERE title='{task.title}' 
                            AND {tracker}
                            AND {deadline}''')
        self.con.commit()

    def append_sql(self, task):
        tracker = "null" if task.counter is None else f'{task.counter}'
        deadline = "null" if task.deadline is None else f'"{task.deadline}"'
        self.cur_db.execute(f'''INSERT INTO tasks (title, tracker, deadline) VALUES
                            ('{task.title}', {tracker}, {deadline})''')
        self.con.commit()

    def connect_sql(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur_db = self.con.cursor()

        self.cur_db.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name= "tasks" ''')
        if self.cur_db.fetchone() is None:
            self.cur_db.execute(''' CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title varchar(60) not null,
                                    tracker int,
                                    deadline varchar(20)) ''')

        self.cur_db.execute(''' SELECT * FROM tasks ''')
        for t in self.cur_db.fetchall():
            self.tasks.append(Task(t[1], t[2], t[3]))


app = App()
app.mainloop()
