from datastore import Datastore
from leetcode_api import fetch_problems


def get_problem(num: int) -> dict | None:
    with Datastore('problems.db', 'schema.sql') as db:
        slug = db.select_problem(num)
        if slug is None:
            print(f'Could not find {num}')
            return None



    # fetch problem info
    # parse problem info
    # return


def update_problems():
    with Datastore('problems.db', 'schema.sql') as db:
        problems = fetch_problems()
        db.update_problems(problems)


