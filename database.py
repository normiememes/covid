import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import get_logger

logger = get_logger()

DB_DRIVER = os.getenv("DB_DRIVER")
ENV = os.getenv("ENV")

engine = None


class DatabaseDriverException(Exception):
    pass


if DB_DRIVER == "sqlite":
    logger.info("Using sqlite")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
elif DB_DRIVER == "mysql+pymysql":
    logger.info("Using mysql+pymysql database driver")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    if ENV == "docker-compose":
        connection_string = f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        # Used for connecting to gcp cloud sql
        # Found here: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/cloud-sql/mysql/sqlalchemy/main.py

        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        connection_string = URL(
            drivername=DB_DRIVER,
            username=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            query={"unix_socket": f"/cloudsql/{DB_HOST}"},
        )

    # The SQLAlchemy engine will help manage interactions, including automatically
    # managing a pool of connections to your database
    engine = create_engine(
        connection_string,
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        pool_recycle=1800,  # 30 minutes
    )

    if not database_exists(engine.url):
        create_database(engine.url)

else:
    raise DatabaseDriverException

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
