# week_06_testing/task_manager.py
from pymongo import MongoClient
from bson.objectid import ObjectId


class TaskManager:
    """Handles all task-related operations with MongoDB."""

    def __init__(self, db_name="internship_db_test"):
        # Connect to MongoDB
        self.client = MongoClient("localhost", 27017)
        self.db = self.client[db_name]
        self.collection = self.db["tasks"]

    # --- CREATE ---
    def create_task(self, title, priority="Medium"):
        """Insert a new task and return it."""
        task = {
            "title": title,
            "priority": priority,
            "is_complete": False,
        }
        result = self.collection.insert_one(task)
        task["_id"] = result.inserted_id
        return task

    # --- READ ---
    def get_task(self, task_id):
        """Find a task by its ID."""
        return self.collection.find_one({"_id": ObjectId(task_id)})

    def get_all_tasks(self):
        """Return all tasks."""
        return list(self.collection.find())

    def search_by_title(self, text):
        """Find tasks whose title contains 'text' (case-insensitive)."""
        return list(self.collection.find({"title": {"$regex": text, "$options": "i"}}))

    def search_by_priority(self, priority):
        """Find tasks with a given priority."""
        return list(self.collection.find({"priority": priority}))

    def count_tasks(self):
        """Return the total number of tasks."""
        return self.collection.count_documents({})

    # --- UPDATE ---
    def update_task(self, task_id, fields):
        """Update a task's fields. Returns True if a task was modified."""
        result = self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": fields}
        )
        return result.modified_count > 0

    def mark_complete(self, task_id):
        """Shortcut to mark a task as complete."""
        return self.update_task(task_id, {"is_complete": True})

    # --- DELETE ---
    def delete_task(self, task_id):
        """Delete a task. Returns True if a task was deleted."""
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    def clear_all(self):
        """Remove all tasks (used in tests)."""
        self.collection.delete_many({})

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()