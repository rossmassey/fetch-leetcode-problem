import os
import sqlite3


class Datastore:
    def __init__(self, db_path, schema_path):
        self.db_path = db_path
        self.schema_path = schema_path
        self.conn = None

        if not os.path.exists(db_path):
            self._init_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def _init_db(self):
        try:
            with open(self.schema_path, 'r') as file:
                schema = file.read()
        except FileNotFoundError:
            print(f'Could not find schema file: {self.schema_path}')
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)

    def _query(self, stmt, params, want_value=False):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(stmt, params)

            if want_value:
                return cursor.fetchone()

    def insert_problem(self, num, title, slug):
        stmt = 'INSERT INTO problems (num, title, slug) VALUES (?, ?, ?)'
        self._query(stmt, (num, title, slug))

    def select_problem(self, num):
        stmt = 'SELECT * FROM problems WHERE num = ?'
        return self._query(stmt, (num, ), want_value=True)
