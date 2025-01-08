# Database Singleton
import sqlite3

from src.backend.config.config import DATABASE_PATH


class Database:
    """Singleton class for managing database connection."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            cls._instance._cursor = cls._instance._connection.cursor()
        return cls._instance

    def execute(self, query, params=()):
        self._cursor.execute(query, params)
        self._connection.commit()

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchone(self):
        return self._cursor.fetchone()

    def close(self):
        self._cursor.close()
        self._connection.close()