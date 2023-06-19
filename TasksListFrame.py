import customtkinter
from TaskFrame import TaskFrame


class TasksListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, tasks=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.task_frames = []

        self.update_tasks(tasks)
        self.bind("<Button-1>", self.focus_event)

    def focus_event(self, event=None):
        self.focus()

    def update_tasks(self, tasks):
        for task_frame in self.task_frames:
            task_frame.destroy()
        self.task_frames.clear()
        for i, task in enumerate(tasks):
            self.task_frames.append(TaskFrame(master=self, task=task, id=i))
            self.task_frames[i].grid(row=i, column=0, pady=5, sticky="nw")
            self.task_frames[i].delete_task_button.bind('<Button-1>', self.delete_task)
            self.task_frames[i].edit_task_button.bind('<Button-1>', self.edit_task)

    def delete_task(self, event):
        button = event.widget.master
        task_frame = button.master
        self.task_frames.remove(task_frame)
        canvas = self.master
        frame = canvas.master
        app = frame.master
        app.remove_task(task_frame.task)
        task_frame.destroy()

    def edit_task(self, event):
        pass
