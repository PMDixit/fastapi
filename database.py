from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Load environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")  # 'db' is the service name in docker-compose
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()
