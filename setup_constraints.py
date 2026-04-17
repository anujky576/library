from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'library_management')

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]

print("Setting up MongoDB Constraints and Indexes...\n")

# ====== 1. UNIQUE INDEXES ======
print("1️⃣ Creating Unique Indexes...")

# Unique index on serial_number in books collection
try:
    db.books.create_index("serial_number", unique=True)
    print("   ✅ Unique index created on books.serial_number")
except Exception as e:
    print(f"   ⚠️ Unique index on books.serial_number: {e}")

# Unique index on email in borrowers collection
try:
    db.borrowers.create_index("email", unique=True)
    print("   ✅ Unique index created on borrowers.email")
except Exception as e:
    print(f"   ⚠️ Unique index on borrowers.email: {e}")

# ====== 2. SCHEMA VALIDATION ======
print("\n2️⃣ Adding Schema Validation...")

# Validation for books collection
books_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["serial_number", "title", "author", "publication"],
        "properties": {
            "_id": {"bsonType": "objectId"},
            "serial_number": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "author": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "publication": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "quantity": {
                "bsonType": "int",
                "minimum": 1,
                "description": "must be an integer >= 1"
            },
            "borrower_id": {
                "bsonType": ["objectId", "null"],
                "description": "references borrowers._id or null if available"
            },
            "issue_date": {
                "bsonType": ["date", "null"],
                "description": "issue date or null"
            },
            "due_date": {
                "bsonType": ["date", "null"],
                "description": "due date or null"
            }
        }
    }
}

# Validation for borrowers collection
borrowers_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email"],
        "properties": {
            "_id": {"bsonType": "objectId"},
            "name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                "description": "must be a valid email and is required"
            }
        }
    }
}

try:
    db.command("collMod", "books", validator=books_schema)
    print("   ✅ Schema validation applied to books collection")
except Exception as e:
    print(f"   ⚠️ Schema validation for books: {e}")

try:
    db.command("collMod", "borrowers", validator=borrowers_schema)
    print("   ✅ Schema validation applied to borrowers collection")
except Exception as e:
    print(f"   ⚠️ Schema validation for borrowers: {e}")

# ====== 3. INDEXES FOR PERFORMANCE ======
print("\n3️⃣ Creating Performance Indexes...")

# Index on borrower_id for faster lookups
try:
    db.books.create_index("borrower_id")
    print("   ✅ Index created on books.borrower_id")
except Exception as e:
    print(f"   ⚠️ Index on books.borrower_id: {e}")

# Compound index for availability queries
try:
    db.books.create_index([("borrower_id", 1), ("serial_number", 1)])
    print("   ✅ Compound index created on (borrower_id, serial_number)")
except Exception as e:
    print(f"   ⚠️ Compound index: {e}")

# Index on issue_date and due_date for range queries
try:
    db.books.create_index([("due_date", 1)])
    print("   ✅ Index created on books.due_date")
except Exception as e:
    print(f"   ⚠️ Index on books.due_date: {e}")

print("\n" + "="*50)
print("✅ MongoDB Constraints Setup Complete!")
print("="*50)

# Show all indexes
print("\n📊 Created Indexes:")
for collection_name in ["books", "borrowers"]:
    collection = db[collection_name]
    indexes = collection.list_indexes()
    print(f"\n{collection_name}:")
    for index in indexes:
        print(f"  - {index['name']}: {index['key']}")

client.close()
