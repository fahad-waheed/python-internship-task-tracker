# task_tracker/app.py
from database import Database
from models import Task


db = Database()


def header(title):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)


def print_tasks(tasks):
    if not tasks:
        print("  (no tasks)")
        return
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task}")


def add_task():
    header("Add New Task")
    title = input("Title: ").strip()
    if not title:
        print("❌ Title cannot be empty.")
        return

    priority = input("Priority [Low/Medium/High] (default Medium): ").strip() or "Medium"
    if priority not in ["Low", "Medium", "High"]:
        print("❌ Invalid priority. Using 'Medium'.")
        priority = "Medium"

    description = input("Description (optional): ").strip()

    task = Task(title=title, priority=priority, description=description)
    db.add_task(task)
    print(f"✅ Task added: {task}")


def list_all():
    header("All Tasks")
    print_tasks(db.get_all())


def list_pending():
    header("Pending Tasks")
    print_tasks(db.filter_by_status(False))


def list_complete():
    header("Completed Tasks")
    print_tasks(db.filter_by_status(True))


def search_tasks():
    header("Search Tasks")
    keyword = input("Enter keyword: ").strip()
    if not keyword:
        print("❌ Empty keyword.")
        return
    print_tasks(db.search(keyword))


def mark_complete():
    header("Mark Task as Complete")
    task_id = input("Enter task ID: ").strip()
    if db.mark_complete(task_id):
        print("✅ Task marked complete.")
    else:
        print("❌ Task not found or already complete.")


def delete_task():
    header("Delete Task")
    task_id = input("Enter task ID: ").strip()
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return
    if db.delete_task(task_id):
        print("✅ Task deleted.")
    else:
        print("❌ Task not found.")


def list_ids():
    header("Task IDs")
    tasks = db.get_all()
    if not tasks:
        print("  (no tasks)")
        return
    for task in tasks:
        print(f"  {task._id}  →  {task.title}")


def menu():
    while True:
        print("\n" + "=" * 50)
        print("       📝  TASK TRACKER")
        print("=" * 50)
        print(f"  Total tasks: {db.count()}")
        print("-" * 50)
        print("  1. Add a new task")
        print("  2. List all tasks")
        print("  3. List pending tasks")
        print("  4. List completed tasks")
        print("  5. Search tasks by title")
        print("  6. Show all task IDs")
        print("  7. Mark a task as complete")
        print("  8. Delete a task")
        print("  0. Exit")
        print("-" * 50)

        choice = input("Choose an option: ").strip()

        if choice == "1":   add_task()
        elif choice == "2": list_all()
        elif choice == "3": list_pending()
        elif choice == "4": list_complete()
        elif choice == "5": search_tasks()
        elif choice == "6": list_ids()
        elif choice == "7": mark_complete()
        elif choice == "8": delete_task()
        elif choice == "0":
            print("\n👋 Goodbye!")
            db.close()
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()