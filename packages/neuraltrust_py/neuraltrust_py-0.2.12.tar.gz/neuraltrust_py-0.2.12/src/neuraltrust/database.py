import os
from dotenv import load_dotenv
from contextlib import contextmanager
from psycopg import Connection
from psycopg_pool import ConnectionPool

load_dotenv()

class DatabaseManager:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            cls._pool = ConnectionPool(
                min_size=1,
                max_size=10,  # Adjust this number based on your needs
                conninfo=" ".join([
                    f"dbname={os.environ.get('POSTGRES_DATABASE')}",
                    f"user={os.environ.get('POSTGRES_USER')}",
                    f"password={os.environ.get('POSTGRES_PASSWORD')}",
                    f"host={os.environ.get('POSTGRES_URL')}",
                    f"port={os.environ.get('POSTGRES_PORT', 5432)}"
                ])
            )
        return cls._pool

    @classmethod
    @contextmanager
    def get_connection(cls):
        pool = cls.get_pool()
        with pool.connection() as conn:
            yield conn

    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.close()
            cls._pool = None