import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env
load_dotenv()

# Step 1: Check if DATABASE_URL is loaded
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL is missing! Check your .env file.")
    exit(1)
else:
    print(f"✅ DATABASE_URL found: {DATABASE_URL}")

# Step 2: Try connecting to the database
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Failed to connect to the database!")
    print(f"Error: {e}")
