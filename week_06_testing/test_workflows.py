# week_06_testing/test_workflows.py
import unittest
from task_manager import TaskManager


class TestTaskWorkflows(unittest.TestCase):
    """Tests for all task workflows: insert, update, search, delete."""

    # --- Runs BEFORE each test ---
    def setUp(self):
        # Use a dedicated test database so real data isn't touched
        self.manager = TaskManager(db_name="internship_db_test")
        # Start with a clean slate
        self.manager.clear_all()

    # --- Runs AFTER each test ---
    def tearDown(self):
        self.manager.clear_all()
        self.manager.close()

    # ========================================
    # INSERT WORKFLOW TESTS
    # ========================================
    def test_create_task_inserts_into_db(self):
        """Creating a task should save it to MongoDB."""
        task = self.manager.create_task("Buy groceries", priority="High")

        # Should have an ID
        self.assertIsNotNone(task["_id"])

        # Should be findable in the DB
        found = self.manager.get_task(task["_id"])
        self.assertIsNotNone(found)
        self.assertEqual(found["title"], "Buy groceries")
        self.assertEqual(found["priority"], "High")
        self.assertFalse(found["is_complete"])

    def test_create_multiple_tasks(self):
        """Creating multiple tasks should increment the count."""
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        self.manager.create_task("Task 3")

        self.assertEqual(self.manager.count_tasks(), 3)

    # ========================================
    # UPDATE WORKFLOW TESTS
    # ========================================
    def test_update_task_changes_fields(self):
        """Updating a task should modify the specified fields."""
        task = self.manager.create_task("Old title")

        # Update the title
        success = self.manager.update_task(task["_id"], {"title": "New title"})
        self.assertTrue(success)

        # Verify the change
        updated = self.manager.get_task(task["_id"])
        self.assertEqual(updated["title"], "New title")

    def test_mark_complete(self):
        """mark_complete should set is_complete to True."""
        task = self.manager.create_task("Finish report")

        self.manager.mark_complete(task["_id"])

        updated = self.manager.get_task(task["_id"])
        self.assertTrue(updated["is_complete"])

    # ========================================
    # SEARCH WORKFLOW TESTS
    # ========================================
    def test_search_by_title(self):
        """Search should find tasks by partial title (case-insensitive)."""
        self.manager.create_task("Learn MongoDB")
        self.manager.create_task("Learn Python")
        self.manager.create_task("Buy milk")

        # Search for "learn" — should match 2 tasks
        results = self.manager.search_by_title("learn")
        self.assertEqual(len(results), 2)

    def test_search_by_priority(self):
        """Search should filter tasks by priority."""
        self.manager.create_task("Task A", priority="High")
        self.manager.create_task("Task B", priority="Low")
        self.manager.create_task("Task C", priority="High")

        high_priority = self.manager.search_by_priority("High")
        self.assertEqual(len(high_priority), 2)

    # ========================================
    # DELETE WORKFLOW TESTS
    # ========================================
    def test_delete_task_removes_from_db(self):
        """Deleting a task should remove it from MongoDB."""
        task = self.manager.create_task("Temporary task")
        task_id = task["_id"]

        # Delete it
        success = self.manager.delete_task(task_id)
        self.assertTrue(success)

        # Verify it's gone
        found = self.manager.get_task(task_id)
        self.assertIsNone(found)

    def test_delete_nonexistent_task(self):
        """Deleting a task that doesn't exist should return False."""
        # Use a random valid ObjectId
        from bson.objectid import ObjectId
        fake_id = ObjectId()

        success = self.manager.delete_task(fake_id)
        self.assertFalse(success)


# --- Run tests when executed directly ---
if __name__ == "__main__":
    unittest.main(verbosity=2)