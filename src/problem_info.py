import leetcode_api
from problem_index import ProblemIndex
from parsing import extract_fields


def get_problem(num: int) -> dict | None:
    with ProblemIndex() as db:
        problem = db.select_problem(num)

        if problem is None:
            print(f'Could not find {num}')
            return None

    problem_info = leetcode_api.fetch_problem_info(problem['slug'])
    synced_code = leetcode_api.fetch_synced_code(problem['question_id'])

    fields = extract_fields(problem_info, synced_code)
    return fields


def update_problem_listing():
    problems = leetcode_api.fetch_problems()

    with ProblemIndex() as db:
        db.update_problems(problems)
