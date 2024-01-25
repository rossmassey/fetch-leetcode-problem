import _leetcode_api
from _parsing import extract_fields
from _problem_index import ProblemIndex


def get_problem(num: int) -> dict | None:
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
    problems = _leetcode_api.fetch_problems()

    with ProblemIndex() as db:
        db.update_problems(problems)


def count_problems() -> int:
    with ProblemIndex() as db:
        count = db.count_problems()

    return count['COUNT(*)']
