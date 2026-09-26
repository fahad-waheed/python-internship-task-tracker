# week_05_rest_api/test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    print("--- 1. Home ---")
    print(requests.get(f"{BASE_URL}/").json())

    print("\n--- 2. Create a task ---")
    new_task = {"title": "Learn REST API", "priority": "High"}
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    print(response.status_code, response.json())
    task_id = response.json()["id"]

    print("\n--- 3. List all tasks ---")
    print(requests.get(f"{BASE_URL}/tasks").json())

    print("\n--- 4. Get one task ---")
    print(requests.get(f"{BASE_URL}/tasks/{task_id}").json())

    print("\n--- 5. Update the task (mark complete) ---")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json={"is_complete": True})
    print(response.status_code, response.json())

    print("\n--- 6. Delete the task ---")
    print(requests.delete(f"{BASE_URL}/tasks/{task_id}").json())

    print("\n--- 7. Confirm deletion (should be 404) ---")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(response.status_code, response.json())


if __name__ == "__main__":
    main()