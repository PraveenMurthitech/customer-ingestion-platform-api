import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor
from app.config.settings import settings


class PostgresPool:
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            cls._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD
            )

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            raise Exception("Pool not initialized")
        return cls._pool.getconn()

    @classmethod
    def release_connection(cls, conn):
        if cls._pool:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        if cls._pool:
            cls._pool.closeall()


# 🔥 THIS is what your DAO actually uses
@contextmanager
def get_db_cursor(dict_cursor: bool = False):
    conn = PostgresPool.get_connection()

    if dict_cursor:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = conn.cursor()

    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        PostgresPool.release_connection(conn)