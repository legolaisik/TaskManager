import customtkinter
from CounterFrame import CounterFrame


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
            self.counter.bind("<Button-1>", self.focus_event)

        if not self.task.deadline is None:
            self.column += 1
            self.grid_columnconfigure(self.column, weight=1)
            self.task_deadline = customtkinter.CTkLabel(self, height=30, text_color="#D10031",
                                                        font=('', 14), text=self.task.deadline)
            self.task_deadline.grid(row=0, column=self.column - 1, padx=10)
            self.task_deadline.bind("<Button-1>", self.focus_event)

        self.column += 1
        self.grid_columnconfigure(self.column, weight=1)
        self.delete_task_button = customtkinter.CTkButton(self, text_color='red', text="X",
                                                          height=30, width=10, fg_color='#DBDBDB')
        self.delete_task_button.grid(row=0, column=self.column - 1, padx=(10, 0))

        self.column += 1
        self.grid_columnconfigure(self.column, weight=1)
        self.edit_task_button = customtkinter.CTkButton(self, text_color='black', text="E",
                                                        height=30, width=10, fg_color='#DBDBDB')
        self.edit_task_button.grid(row=0, column=self.column - 1, padx=(0, 10))

        self.bind("<Button-1>", self.focus_event)
        self.task_label.bind("<Button-1>", self.focus_event)

    def focus_event(self, event=None):
        self.focus()