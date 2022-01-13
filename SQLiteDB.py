import sqlite3
import threading


class SQLiteDB:
    def __init__(self, name):
        self.name = name
        self.connection = sqlite3.connect(f'{self.name}.db', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.lock = threading.Lock()

    def execute(self, query):
        with self.lock:
            with self.connection:
                self.cursor.execute(query)

    def fetch_all(self):
        with self.lock:
            result = [dict(row) for row in self.cursor.fetchall()]

        return result

    def fetch_one(self):
        with self.lock:
            result = self.cursor.fetchone()[0]

        return result
