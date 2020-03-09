import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import get_logger

logger = get_logger()

DB_DRIVER = os.getenv("DB_DRIVER", None)

if DB_DRIVER == "mysql+pymysql":
    logger.info("Using mysql+pymysql database driver")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # [START cloud_sql_mysql_sqlalchemy_create]
    # The SQLAlchemy engine will help manage interactions, including automatically
    # managing a pool of connections to your database
    engine = create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        URL(
            drivername=DB_DRIVER,
            username=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            query={"unix_socket": "/cloudsql/{}".format(DB_HOST)},
        ),
        # ... Specify additional properties here.
        # [START_EXCLUDE]
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        pool_recycle=1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
        # [END_EXCLUDE]
    )
    # [END cloud_sql_mysql_sqlalchemy_create]

    if not database_exists(engine.url):
        create_database(engine.url)
else:
    logger.info("Using sqlite")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
