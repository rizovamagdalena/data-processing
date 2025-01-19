# Database Singleton
import sqlite3


class Database:
    """Handles SQLite database connections and operations."""

    def __init__(self, db_name="stock_data.db"):
        self._connection = sqlite3.connect(db_name, check_same_thread=False)
        self._cursor = self._connection.cursor()

    def execute(self, query, params=None):
        """
        Executes a single SQL query.
        :param query: SQL query string
        :param params: Optional parameters for the query
        """
        if params:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)

    def executemany(self, query, param_list):
        """
        Executes a SQL query for multiple sets of parameters.
        :param query: SQL query string
        :param param_list: List of parameter tuples
        """
        self._cursor.executemany(query, param_list)

    def fetchone(self):
        """
        Fetches the next row of a query result.
        """
        return self._cursor.fetchone()

    def fetchall(self):
        """
        Fetches all rows of a query result.
        """
        return self._cursor.fetchall()

    def commit(self):
        """
        Commits the current transaction.
        """
        self._connection.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self._connection.close()
