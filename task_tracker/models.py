# task_tracker/models.py
from datetime import datetime


class Task:
    """Represents a single task in the task tracker."""

    def __init__(self, title, priority="Medium", description="", due_date=None):
        self.title = title
        self.priority = priority
        self.description = description
        self.due_date = due_date
        self.is_complete = False
        self.created_at = datetime.now()

    def to_dict(self):
        """Convert to a dictionary for MongoDB storage."""
        return {
            "title": self.title,
            "priority": self.priority,
            "description": self.description,
            "due_date": self.due_date,
            "is_complete": self.is_complete,
            "created_at": self.created_at,
        }

    def status(self):
        """User-facing status."""
        return "Complete" if self.is_complete else "Pending"

    def __str__(self):
        return f"[{self.status()}] {self.title} ({self.priority})"