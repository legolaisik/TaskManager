import customtkinter
from Task import Task


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