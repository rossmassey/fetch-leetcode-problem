import os
import sqlite3
from util import absolute_path

DB_PATH = 'problems.db'
SCHEMA_PATH = 'schema.sql'


class ProblemIndex:
    def __init__(self):
        self.db_path = absolute_path(DB_PATH)
        self.schema_path = absolute_path(SCHEMA_PATH)
        self.conn = None

        if not os.path.exists(self.db_path):
            self._init_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
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

    def update_problems(self, problems):
        for problem in problems:
            self.insert_problem(*problem)

    def insert_problem(self, num, title, slug, question_id):
        stmt = 'INSERT OR REPLACE INTO problems (num, title, slug, question_id) VALUES (?, ?, ?, ?)'
        self._query(stmt, (num, title, slug, question_id))

    def select_problem(self, num):
        stmt = 'SELECT * FROM problems WHERE num = ?'
        return self._query(stmt, (num,), want_value=True)
