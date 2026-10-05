# task_tracker/database.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Task


class Database:
    """Handles all MongoDB operations for the task tracker."""

    def __init__(self, db_name="task_tracker_db"):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client[db_name]
        self.tasks = self.db["tasks"]

    def _doc_to_task(self, doc):
        """Convert a MongoDB document to a Task object."""
        task = Task(
            title=doc["title"],
            priority=doc.get("priority", "Medium"),
            description=doc.get("description", ""),
            due_date=doc.get("due_date"),
        )
        task.is_complete = doc.get("is_complete", False)
        task.created_at = doc.get("created_at")
        task._id = doc["_id"]
        return task

    # --- CREATE ---
    def add_task(self, task):
        result = self.tasks.insert_one(task.to_dict())
        task._id = result.inserted_id
        return task

    # --- READ ---
    def get_all(self):
        return [self._doc_to_task(d) for d in self.tasks.find()]

    def get_by_id(self, task_id):
        try:
            doc = self.tasks.find_one({"_id": ObjectId(task_id)})
        except Exception:
            return None
        return self._doc_to_task(doc) if doc else None

    def search(self, keyword):
        docs = self.tasks.find({"title": {"$regex": keyword, "$options": "i"}})
        return [self._doc_to_task(d) for d in docs]

    def filter_by_status(self, is_complete):
        docs = self.tasks.find({"is_complete": is_complete})
        return [self._doc_to_task(d) for d in docs]

    def filter_by_priority(self, priority):
        docs = self.tasks.find({"priority": priority})
        return [self._doc_to_task(d) for d in docs]

    # --- UPDATE ---
    def update_task(self, task_id, fields):
        try:
            result = self.tasks.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": fields}
            )
        except Exception:
            return False
        return result.modified_count > 0

    def mark_complete(self, task_id):
        return self.update_task(task_id, {"is_complete": True})

    # --- DELETE ---
    def delete_task(self, task_id):
        try:
            result = self.tasks.delete_one({"_id": ObjectId(task_id)})
        except Exception:
            return False
        return result.deleted_count > 0

    def count(self):
        return self.tasks.count_documents({})

    def close(self):
        self.client.close()