import leetcode_api
from problem_index import ProblemIndex
from parsing import extract_fields


def get_problem(num: int) -> dict | None:
    with ProblemIndex() as db:
        problem = db.select_problem(num)
        if problem is None:
            print(f'Could not find {num}')
            return None
        
    slug = problem['slug']
    question_id = problem['question_id']


    problem_info = leetcode_api.fetch_problem_info(slug)
    synced_code = leetcode_api.fetch_synced_code(question_id)

    fields = extract_fields(problem_info, synced_code)
    return {**fields, **synced_code} if synced_code else fields


def update_problem_listing():
    with ProblemIndex() as db:
        problems = leetcode_api.fetch_problems()
        db.update_problems(problems)


# update_problem_listing()
info = get_problem(130)

for key, value in info.items():
    print(f'{key:<{15}} {value}')
