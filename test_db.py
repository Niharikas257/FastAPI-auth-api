# app/test_db.py
from app.database import SessionLocal

try:
    db = SessionLocal()
    print("✅ Connected to PostgreSQL successfully!")
    db.close()
except Exception as e:
    print("❌ Connection failed:", e)
