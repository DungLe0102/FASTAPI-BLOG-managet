from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# kết nối database
engine = create_engine(DATABASE_URL)

# session làm việc với DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base model
Base = declarative_base()


# dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()