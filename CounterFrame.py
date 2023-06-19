import customtkinter


class CounterFrame(customtkinter.CTkFrame):
    def __init__(self, task, master, **kwargs):
        super().__init__(master, **kwargs)
        self.task = task

        self.add_button = customtkinter.CTkButton(self, text="", height=9, width=30, command=self.add_button_callback)
        self.add_button.grid(row=0, column=0)

        self.counter_entry = customtkinter.CTkEntry(self, height=12, width=30, font=('', 14))
        self.counter_entry.grid(row=1, column=0)
        self.counter_entry.insert(0, self.task.counter)
        self.counter_entry.bind("<FocusOut>", self.counter_changed)

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

    def counter_changed(self, event=None):
        self.task.counter = int(self.counter_entry.get())
