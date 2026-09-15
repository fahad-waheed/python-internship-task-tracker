# week_04_mongodb/01_crud_operations.py
from pymongo import MongoClient

# 1. Connect to the local MongoDB instance
client = MongoClient('localhost', 27017)

# 2. Access a database (created automatically if it doesn't exist)
db = client['internship_db']

# 3. Access a collection (like a table in SQL)
tasks_collection = db['tasks']

# --- CREATE ---
print("--- CREATE: Inserting tasks ---")
task1 = {"title": "Learn MongoDB", "priority": "High", "is_complete": False}
task2 = {"title": "Practice CRUD", "priority": "Medium", "is_complete": False}

result = tasks_collection.insert_one(task1)
print(f"Inserted task with ID: {result.inserted_id}")

tasks_collection.insert_one(task2)

# --- READ ---
print("\n--- READ: Finding all tasks ---")
for task in tasks_collection.find():
    print(task)

# --- UPDATE ---
print("\n--- UPDATE: Marking 'Learn MongoDB' as complete ---")
tasks_collection.update_one(
    {"title": "Learn MongoDB"},
    {"$set": {"is_complete": True}}
)

# --- DELETE ---
print("\n--- DELETE: Removing 'Practice CRUD' ---")
tasks_collection.delete_one({"title": "Practice CRUD"})

# --- VERIFY ---
print("\n--- FINAL STATE ---")
for task in tasks_collection.find():
    print(task)