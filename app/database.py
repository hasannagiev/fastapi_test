# Render PostgreSQL üçün DATABASE_URL mühit dəyişəni istifadə edilir
#DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://fastapi_testdb_user:32F78QYjVnThi5AhKCYWbirlaNuOnbTR@localhost:5432/fastapi_testdb")

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

