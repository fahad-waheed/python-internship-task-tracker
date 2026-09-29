# week_07_api_validation/validation.py

from pymongo import MongoClient
from bson.objectid import ObjectId


# --- MongoDB setup ---
client = MongoClient("localhost", 27017)
db = client["internship_db"]
tasks = db["validated_tasks"]


# --- Validation functions ---
def validate_title(title):
    """Return an error message if title is invalid, else None."""
    if not title:
        return "Title is required"
    if not isinstance(title, str):
        return "Title must be text"
    if len(title.strip()) == 0:
        return "Title cannot be empty"
    if len(title) > 100:
        return "Title must be under 100 characters"
    return None


def validate_priority(priority):
    """Return an error message if priority is invalid, else None."""
    if priority not in ["Low", "Medium", "High"]:
        return "Priority must be Low, Medium, or High"
    return None


# --- Safe create function ---
def create_task(title, priority="Medium"):
    """Create a task only if validation passes."""
    # Validate title
    error = validate_title(title)
    if error:
        print(f"❌ Error: {error}")
        return None

    # Validate priority
    error = validate_priority(priority)
    if error:
        print(f"❌ Error: {error}")
        return None

    # All good — save it
    task = {"title": title.strip(), "priority": priority, "is_complete": False}
    result = tasks.insert_one(task)
    print(f"✅ Created task: '{task['title']}' ({priority})")
    return result.inserted_id


# --- Safe get function ---
def get_task(task_id):
    """Get a task by ID with error handling."""
    try:
        task = tasks.find_one({"_id": ObjectId(task_id)})
    except Exception:
        print("❌ Error: Invalid ID format")
        return None

    if not task:
        print("❌ Error: Task not found")
        return None

    print(f"✅ Found: {task['title']} ({task['priority']})")
    return task


# --- Safe delete function ---
def delete_task(task_id):
    """Delete a task with error handling."""
    try:
        result = tasks.delete_one({"_id": ObjectId(task_id)})
    except Exception:
        print("❌ Error: Invalid ID format")
        return False

    if result.deleted_count == 0:
        print("❌ Error: Task not found")
        return False

    print("✅ Task deleted")
    return True


# --- Test everything ---
if __name__ == "__main__":
    print("--- Testing validation and error handling ---\n")

    # Clean up old test data
    tasks.delete_many({})

    print("1. Valid task:")
    create_task("Finish report", "High")

    print("\n2. Missing title:")
    create_task("", "High")

    print("\n3. Invalid priority:")
    create_task("Buy groceries", "Urgent")

    print("\n4. Title too long:")
    create_task("x" * 150, "Low")

    print("\n5. Valid task again:")
    task_id = create_task("Learn MongoDB", "Medium")

    print("\n6. Get valid task:")
    get_task(task_id)

    print("\n7. Get with bad ID:")
    get_task("not-a-real-id")

    print("\n8. Get non-existent task:")
    get_task("000000000000000000000000")

    print("\n9. Delete valid task:")
    delete_task(task_id)

    print("\n10. Delete same task again (should fail):")
    delete_task(task_id)

    print("\n--- Done ---")