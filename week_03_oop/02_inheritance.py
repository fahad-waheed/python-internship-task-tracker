# week_03_oop/02_inheritance.py

from datetime import date

class Task:
    """Base class for any task."""

    def __init__(self, title):
        self.title = title
        self.is_complete = False

    def mark_complete(self):
        self.is_complete = True

    def show_info(self):
        status = "Done" if self.is_complete else "Pending"
        print(f"[Task] {self.title} - {status}")


class DeadlineTask(Task):
    """A task with a due date. Inherits from Task."""

    def __init__(self, title, due_date):
        # Call the parent class constructor
        super().__init__(title)
        self.due_date = due_date

    def show_info(self):
        """Override the parent method to also show the due date."""
        status = "Done" if self.is_complete else "Pending"
        print(f"[Deadline Task] {self.title} - {status} (Due: {self.due_date})")


# --- Testing inheritance ---
if __name__ == "__main__":
    basic_task = Task("Read Python docs")
    deadline_task = DeadlineTask("Submit weekly report", "2026-09-20")

    basic_task.show_info()
    deadline_task.show_info()

    print("\nMarking both as complete...\n")
    basic_task.mark_complete()
    deadline_task.mark_complete()

    basic_task.show_info()
    deadline_task.show_info()