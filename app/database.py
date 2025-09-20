import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env faylını yüklə
load_dotenv()

# Ətraf mühit dəyişəni oxu
DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     # Əgər .env tapılmazsa, SQLite fallback
#     DATABASE_URL = "sqlite:///./test.db"

# Engine yarat
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Session yarat
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model bazası üçün
Base = declarative_base()



