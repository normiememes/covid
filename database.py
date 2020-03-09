import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import get_logger

logger = get_logger()

if os.getenv("DB_DRIVER") == "mysql+pymysql":
    logger.info("Using mysql SQLALCHEMY_DATABASE_URL")
    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    logger.info(f"{SQLALCHEMY_DATABASE_URL}")

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

    if not database_exists(engine.url):
        create_database(engine.url)
else:
    logger.info("Using sqlite SQLALCHEMY_DATABASE_URL")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
