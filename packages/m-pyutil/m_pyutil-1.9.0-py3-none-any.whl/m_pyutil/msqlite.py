import os
import sqlite3
from sqlite3 import Connection

DEFAULT_DB_FILE = 'sqlite.db'


def get_conn(f: str = DEFAULT_DB_FILE) -> Connection:
    os.makedirs('tmp', exist_ok=True)
    return sqlite3.connect(f'tmp/{f}')


def create(sql: str, f: str = DEFAULT_DB_FILE):
    return save(sql=sql, f=f)


def drop(sql: str, f: str = DEFAULT_DB_FILE):
    return save(sql=sql, f=f)


def save(sql: str, params: list = None, f: str = DEFAULT_DB_FILE) -> int:
    while True:
        with get_conn(f) as conn:
            # noinspection PyBroadException
            try:
                cur = conn.execute(sql, params or [])
                conn.commit()
                return cur.rowcount
            except Exception as e:
                if 'database is locked' in str(e):
                    continue
                raise e


def select(sql: str, params: list = None, f: str = DEFAULT_DB_FILE) -> list:
    with get_conn(f) as conn:
        return conn.execute(sql, params or []).fetchall()


def select_one(sql: str, params: list = None, f: str = DEFAULT_DB_FILE) -> tuple:
    with get_conn(f) as conn:
        return conn.execute(sql, params or []).fetchone()
