import leetcode_api
from leetcode_metadata import LeetcodeMetadata


def get_problem(num: int) -> dict | None:
    with LeetcodeMetadata() as db:
        problem = db.select_problem(num)
        slug = problem['slug']
        question_id = problem['question_id']

        if slug is None:
            print(f'Could not find {num}')
            return None

    data = leetcode_api.fetch_problem_info(slug)
    code = leetcode_api.fetch_synced_code(question_id)

    print(data)
    # parse problem info
    # return


def update_problem_listing():
    with LeetcodeMetadata() as db:
        problems = leetcode_api.fetch_problems()
        db.update_problems(problems)


# update_problem_listing()
get_problem(1)
