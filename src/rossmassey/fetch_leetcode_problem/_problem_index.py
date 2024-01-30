"""
Database for storing leetcode problem num, title, slug, and question id

Implements context manager protocol with sqlite3
"""
import os
import sqlite3

from ._util import absolute_path

# sqlite3 database file store location
DB_PATH = 'problems.db'

# path to SQL script that creates `problems` table
SCHEMA_PATH = 'schema.sql'


class ProblemIndex:
    """
    Manages a database connection to store and retrieve LeetCode problems info

    GraphQL queries require a title-slug and question-id separate from the
    frontend id/number. Leetcode has a public listing of all problems, but
    fetching + scanning that is slow. Instead, cache the results so that
    operation is not repeated.
    """
    def __init__(self):
        """
        Initialize database connection and creates database/table if it
        doesn't exist.
        """
        self.db_path = absolute_path(DB_PATH)
        self.schema_path = absolute_path(SCHEMA_PATH)
        self.conn = None

        if not os.path.exists(self.db_path):
            self._init_db()

    def __enter__(self):
        """
        Opens database connection.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes database connection.
        """
        if self.conn:
            self.conn.close()

    def _init_db(self):
        """
        Creates database and table.
        """
        try:
            with open(self.schema_path, 'r') as file:
                schema = file.read()
        except FileNotFoundError:
            print(f'Could not find schema file: {self.schema_path}')
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)

    def _query(self, stmt: str, params: tuple) -> sqlite3.Row:
        """
        Executes a query.

        Args:
            stmt (str): SQL statement to execute
            params (tuple): associated parameters
            want_value (bool): if True, return query result

        Returns:
            sqlite3.Row: query result (if want_value)
        """
        with self.conn as transaction:
            cursor = transaction.cursor()
            cursor.execute(stmt, params)
            return cursor.fetchone()

    def update_problems(self, problems: list):
        """
        Updates the problems table with the given problems.

        Args:
            problems: list of problems to insert
        """
        for problem in problems:
            self.insert_problem(*problem)

    def insert_problem(self, num: str, title: str, slug: str, question_id: str):
        """
        Inserts a problem into the problems table.

        Args:
            num (str): problem number
            title (str): problem title
            slug (str): problem title slug
            question_id (str): problem internal id
        """
        stmt = 'INSERT OR REPLACE INTO problems (num, title, slug, question_id) VALUES (?, ?, ?, ?)'
        self._query(stmt, (num, title, slug, question_id))

    def select_problem(self, num: int) -> sqlite3.Row:
        """
        Selects a problem from the problems table.

        Args:
            num (int): problem number

        Returns:
            sqlite3.Row: row containing the problem's num, title, slug, and question id
        """
        stmt = 'SELECT * FROM problems WHERE num = ?'
        return self._query(stmt, (num,))

    def count_problems(self) -> sqlite3.Row:
        """
        Counts the number of problems in the problems table.

        Returns: 
            int: count of problems
        """
        stmt = 'SELECT COUNT(*) FROM problems'
        return self._query(stmt, ())
