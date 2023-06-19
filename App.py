import customtkinter
import sqlite3
from TasksListFrame import TasksListFrame
from Task import Task
from CreateTaskWindow import CreateTaskWindow


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
