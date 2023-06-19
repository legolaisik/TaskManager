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
