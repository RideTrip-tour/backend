import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

# DATABASE
DATABASE_DIALECT = os.getenv("DATABASE_DIALECT", "postgresql")
DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "asyncpg")
DATABASE_NAME = os.getenv("POSTGRES_DB", "rtt_test")
DATABASE_USER = os.getenv("POSTGRES_USER", "admin_test")
DATABASE_PASS = os.getenv("POSTGRES_PASSWORD", "postgre_admin")
DATABASE_HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_PORT = os.getenv("POSTGRES_PORT", 5432)
DATABASE_URL = URL.create(
    drivername=f"{DATABASE_DIALECT}+{DATABASE_DRIVER}",
    username=DATABASE_USER,
    password=DATABASE_PASS,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)
