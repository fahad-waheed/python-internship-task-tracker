# week_04_mongodb/04_query_examples.py
from pymongo import MongoClient, DESCENDING


def main():
    # Connect to the database
    client = MongoClient("localhost", 27017)
    db = client["internship_db"]
    tasks = db["tasks_v2"]  # use the collection from 03_task_model.py

    # Make sure there's data (run 03_task_model.py first if empty)
    if tasks.count_documents({}) == 0:
        print("⚠️  No tasks found. Please run 03_task_model.py first.")
        client.close()
        return

    print("--- 1. Total count ---")
    print(f"Total tasks: {tasks.count_documents({})}\n")

    print("--- 2. Find by priority (High) ---")
    for task in tasks.find({"priority": "High"}):
        print(f"  • {task['title']} — {task['priority']}\n")

    print("--- 3. Find incomplete tasks ---")
    for task in tasks.find({"is_complete": False}):
        print(f"  • {task['title']}\n")

    print("--- 4. Sort by priority (High → Low) ---")
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    # Since MongoDB doesn't sort alphabetically by custom order,
    # we sort by created_at descending as a demo instead
    for task in tasks.find().sort("created_at", DESCENDING):
        print(f"  • {task['title']} ({task['priority']})\n")

    print("--- 5. Count by priority ---")
    for level in ["High", "Medium", "Low"]:
        count = tasks.count_documents({"priority": level})
        print(f"  {level}: {count} task(s)\n")

    print("--- 6. Find one specific task ---")
    task = tasks.find_one({"title": "Learn MongoDB"})
    if task:
        print(f"  Found: {task['title']} — {task.get('description', 'no description')}")

    client.close()


if __name__ == "__main__":
    main()