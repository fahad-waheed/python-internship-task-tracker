# week_03_oop/01_classes_basics.py

class Task:
    """A simple class representing a task in our tracker."""

    def __init__(self, title, priority):
        self.title = title
        self.priority = priority
        self.is_complete = False  # default value

    def mark_complete(self):
        """Mark the task as done."""
        self.is_complete = True

    def show_info(self):
        """Print the task details."""
        status = "Done" if self.is_complete else "Pending"
        print(f"Task: {self.title}")
        print(f"Priority: {self.priority}")
        print(f"Status: {status}")
        print("-" * 30)


# --- Testing the class ---
if __name__ == "__main__":
    task1 = Task("Learn OOP", "High")
    task2 = Task("Write documentation", "Low")

    task1.show_info()
    task2.show_info()

    # Mark the first task as complete
    print("Marking task 1 as complete...\n")
    task1.mark_complete()

    task1.show_info()