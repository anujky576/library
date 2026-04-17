from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'library_management')