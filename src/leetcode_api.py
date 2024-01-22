import requests
from cookies import get_leetcode_session

PROBLEM_API = 'https://leetcode.com/api/problems/all/'
GRAPHQL_API = 'https://leetcode.com/graphql'


def fetch_problems() -> list:
    response = requests.get(PROBLEM_API)
    data = response.json()

    problems = []
    for item in data['stat_status_pairs']:
        stat = item['stat']
        num = stat['frontend_question_id']
        title = stat['question__title']
        slug = stat['question__title_slug']

        problems.append((num, title, slug))

    return problems

def query_graphql():
    token = get_leetcode_session()
    pass
