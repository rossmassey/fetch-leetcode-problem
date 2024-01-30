"""
Gets problem information from leetcode. Stores problem num, title, slug,
question id in sqlite3 database.
"""
from . import _leetcode_api
from ._parsing import extract_fields
from ._problem_index import ProblemIndex
from ._util import absolute_path


def get_problem(num: int) -> dict | None:
    """
    Gets problem info for problem number

    Searches local sqlite3 database for problem slug and question id,
    uses those to query leetcode GraphQL API for problem info and synced
    code.

    Returned fields include:

    .. code-block:: none

        num (int): leetcode problem number
        title (str): problem title
        slug (str): problem slug
        difficulty (str): problem difficulty
        description (str): problem description
        examples (list[dict]): problem examples
        constraints (list[str]): problem constraints
        code_snippet (str): problem code snippet
        code (str): synced code
        func (dict): function info

    Args:
        num (int): leetcode problem number

    Returns:
        dict: problem info fields
    """
    with ProblemIndex() as db:
        problem = db.select_problem(num)

    if problem is None:
        print(f'Could not find {num}')
        return None

    problem_info = _leetcode_api.fetch_problem_info(problem['slug'])
    synced_code = _leetcode_api.fetch_synced_code(problem['question_id'])

    fields = extract_fields(problem_info, synced_code)
    return fields


def update_problem_listing():
    """
    Fetches all leetcode problems title, slug, and question id and stores
    in local sqlite3 database.
    """
    problems = _leetcode_api.fetch_problems()

    with ProblemIndex() as db:
        db.update_problems(problems)


def count_problems() -> int:
    """
    Counts the number of problems stored in local sqlite3 database

    Returns:
        int: number of problems
    """
    with ProblemIndex() as db:
        count = db.count_problems()

    return count['COUNT(*)']


def load_cookie(cookie_path: str = None):
    """
    Change cookie path from default

    Params:
        cookie_path (str): new cookie.txt path
    """
    if cookie_path is None:
        # assume cookies.txt located in src directory
        cookie_path = absolute_path('cookies.txt')

    _leetcode_api.set_cookie(cookie_path)
