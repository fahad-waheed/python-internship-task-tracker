# week_04_mongodb/02_database_connection.py
from pymongo import MongoClient


class DatabaseConnection:
    """Handles connection to the MongoDB server."""

    def __init__(self, host="localhost", port=27017, db_name="internship_db"):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """Establish the connection to MongoDB."""
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[self.db_name]
            # Test the connection
            self.client.admin.command("ping")
            print(f"✅ Connected to MongoDB at {self.host}:{self.port}")
            print(f"✅ Using database: {self.db_name}")
            return self.db
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None

    def close(self):
        """Close the connection."""
        if self.client:
            self.client.close()
            print("🔌 Connection closed.")


if __name__ == "__main__":
    # Test the connection
    db_conn = DatabaseConnection()
    db = db_conn.connect()

    if db is not None:
        # List all collections in the database
        print("\nCollections in this database:")
        for name in db.list_collection_names():
            print(f"  - {name}")

    db_conn.close()