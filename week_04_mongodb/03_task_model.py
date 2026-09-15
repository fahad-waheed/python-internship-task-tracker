# week_04_mongodb/03_task_model.py
from datetime import datetime
from pymongo import MongoClient


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
        """Convert the Task object to a dictionary for MongoDB storage."""
        return {
            "title": self.title,
            "priority": self.priority,
            "description": self.description,
            "due_date": self.due_date,
            "is_complete": self.is_complete,
            "created_at": self.created_at,
        }

    def show_info(self):
        """Print the task details."""
        status = "✅ Done" if self.is_complete else "⏳ Pending"
        print(f"{status} | [{self.priority}] {self.title}")
        if self.description:
            print(f"         {self.description}")


class TaskRepository:
    """Handles all database operations for Task objects."""

    def __init__(self, db):
        self.collection = db["tasks_v2"]  # separate collection to avoid conflicts

    def save(self, task):
        """Save a Task object to the database."""
        result = self.collection.insert_one(task.to_dict())
        print(f"💾 Saved: '{task.title}' (ID: {result.inserted_id})")
        return result.inserted_id

    def get_all(self):
        """Retrieve all tasks as Task objects."""
        tasks = []
        for doc in self.collection.find():
            task = Task(
                title=doc["title"],
                priority=doc.get("priority", "Medium"),
                description=doc.get("description", ""),
                due_date=doc.get("due_date"),
            )
            task.is_complete = doc.get("is_complete", False)
            task.created_at = doc.get("created_at")
            tasks.append(task)
        return tasks

    def count(self):
        """Return the number of tasks in the database."""
        return self.collection.count_documents({})

    def clear(self):
        """Remove all tasks (for testing)."""
        self.collection.delete_many({})
        print("🧹 All tasks cleared.")


if __name__ == "__main__":
    from pymongo import MongoClient

    # Connect and set up
    client = MongoClient("localhost", 27017)
    db = client["internship_db"]
    repo = TaskRepository(db)

    # Start fresh
    repo.clear()

    # Create some tasks using the Task class
    print("\n--- Creating tasks ---")
    task1 = Task("Learn MongoDB", priority="High", description="Study CRUD and schemas")
    task2 = Task("Practice PyMongo", priority="Medium")
    task3 = Task("Build a task tracker", priority="High", description="Final project")

    # Save them to the database
    repo.save(task1)
    repo.save(task2)
    repo.save(task3)

    # Read them back
    print(f"\n--- Fetching all tasks (Total: {repo.count()}) ---")
    for task in repo.get_all():
        task.show_info()

    client.close()