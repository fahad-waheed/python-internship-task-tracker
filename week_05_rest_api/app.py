# week_05_rest_api/app.py

# --- Imports (all built-in Python modules) ---
from http.server import HTTPServer, BaseHTTPRequestHandler # this creates actual web server
from urllib.parse import urlparse
import json

# --- MongoDB ---
from pymongo import MongoClient  # connecting to mongodb
from bson.objectid import ObjectId # mongo uses obid

# --- MongoDB setup ---
client = MongoClient("localhost", 27017) # connect mongo to a localhost
db = client["internship_db"] #create a database 
tasks_collection = db["api_tasks"] # collection to store tasks


# --- Helper: convert MongoDB task to clean JSON-friendly dict ---
def format_task(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "priority": task.get("priority", "Medium"),
        "is_complete": task.get("is_complete", False),
    }


# --- The Request Handler ---
class TaskAPIHandler(BaseHTTPRequestHandler):

    # --- Helper: send a JSON response ---
    def send_json(self, data, status=200):
        # Send status code
        self.send_response(status)
        # Send headers
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # Send body (JSON formatted)
        self.wfile.write(json.dumps(data).encode("utf-8"))

    # --- Helper: read the request body ---
    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body)


    # ==========================================
    # GET — Read tasks
    # ==========================================
    def do_GET(self):
        path = urlparse(self.path).path

        # Route: GET / → welcome message
        if path == "/":
            self.send_json({"message": "Task Tracker API is running 🚀"})
            return

        # Route: GET /tasks → list all tasks
        if path == "/tasks":
            tasks = [format_task(t) for t in tasks_collection.find()]
            self.send_json({"count": len(tasks), "tasks": tasks})
            return

        # Route: GET /tasks/<id> → get one task
        if path.startswith("/tasks/"):
            task_id = path.split("/tasks/")[1]
            try:
                task = tasks_collection.find_one({"_id": ObjectId(task_id)})
            except Exception:
                self.send_json({"error": "Invalid task ID"}, 400)
                return

            if not task:
                self.send_json({"error": "Task not found"}, 404)
                return

            self.send_json(format_task(task))
            return

        # If no route matched
        self.send_json({"error": "Route not found"}, 404)


    # ==========================================
    # POST — Create a task
    # ==========================================
    def do_POST(self):
        path = urlparse(self.path).path

        # Route: POST /tasks → create new task
        if path == "/tasks":
            data = self.read_body()

            # Validation
            if not data or "title" not in data:
                self.send_json({"error": "Title is required"}, 400)
                return

            # Build the new task
            new_task = {
                "title": data["title"],
                "priority": data.get("priority", "Medium"),
                "is_complete": False,
            }

            # Save to MongoDB
            result = tasks_collection.insert_one(new_task)
            new_task["_id"] = result.inserted_id

            # Return 201 Created
            self.send_json(format_task(new_task), 201)
            return

        self.send_json({"error": "Route not found"}, 404)


    # ==========================================
    # PUT — Update a task
    # ==========================================
    def do_PUT(self):
        path = urlparse(self.path).path

        # Route: PUT /tasks/<id>
        if path.startswith("/tasks/"):
            task_id = path.split("/tasks/")[1]
            data = self.read_body()

            if not data:
                self.send_json({"error": "No update data"}, 400)
                return

            try:
                result = tasks_collection.update_one(
                    {"_id": ObjectId(task_id)},
                    {"$set": data}
                )
            except Exception:
                self.send_json({"error": "Invalid task ID"}, 400)
                return

            if result.matched_count == 0:
                self.send_json({"error": "Task not found"}, 404)
                return

            updated = tasks_collection.find_one({"_id": ObjectId(task_id)})
            self.send_json(format_task(updated))
            return

        self.send_json({"error": "Route not found"}, 404)


    # ==========================================
    # DELETE — Remove a task
    # ==========================================
    def do_DELETE(self):
        path = urlparse(self.path).path

        # Route: DELETE /tasks/<id>
        if path.startswith("/tasks/"):
            task_id = path.split("/tasks/")[1]

            try:
                result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
            except Exception:
                self.send_json({"error": "Invalid task ID"}, 400)
                return

            if result.deleted_count == 0:
                self.send_json({"error": "Task not found"}, 404)
                return

            self.send_json({"message": "Task deleted"})
            return

        self.send_json({"error": "Route not found"}, 404)


# --- Run the server ---
if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), TaskAPIHandler)
    print("🚀 Task Tracker API running at http://127.0.0.1:8000")
    print("   Press Ctrl+C to stop.\n")
    server.serve_forever()