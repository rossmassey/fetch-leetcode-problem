"""
Gets problem information from leetcode. Stores problem num, title, slug,
question id in sqlite3 database.
"""
import _leetcode_api
from _parsing import extract_fields
from _problem_index import ProblemIndex


def get_problem(num: int) -> dict | None:
    """
    Gets problem info for problem number

    Searches local sqlite3 database for problem slug and question id,
    uses those to query leetcode GraphQL API for problem info and synced
    code.

    Returned fields include:
        num (int): leetcode problem number
        title (str): problem title
        slug (str): problem slug
        difficulty (str): problem difficulty
        description (str): problem description
        examples (list): problem examples
        constraints (list): problem constraints
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
