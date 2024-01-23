import requests
from cookies import get_leetcode_session_cookie

PROBLEM_API = 'https://leetcode.com/api/problems/all/'
GRAPHQL_API = 'https://leetcode.com/graphql'

COOKIE = get_leetcode_session_cookie('cookies.txt')


def fetch_problems() -> list:
    response = requests.get(PROBLEM_API)
    data = response.json()

    problems = []
    for item in data['stat_status_pairs']:
        stat = item['stat']

        num = stat['frontend_question_id']
        title = stat['question__title']
        slug = stat['question__title_slug']
        question_id = stat['question_id']

        problems.append((num, title, slug, question_id))

    return problems


def _fetch_graphql(payload: dict) -> dict:
    response = requests.post(GRAPHQL_API, json=payload, cookies=COOKIE)
    return response.json()


def fetch_synced_code(question_id: int) -> dict:
    python_language_id = 11  # only get python for now
    payload = {
        "query": """
        query SyncedCode($questionId: Int!, $lang: Int!) {
          syncedCode(questionId: $questionId, lang: $lang) {
            code
          }
        }
        """,
        "variables": {
            "questionId": question_id,
            "lang": python_language_id
        }
    }

    return _fetch_graphql(payload)['data']['syncedCode']


def fetch_problem_info(slug: str) -> dict:
    payload = {
        "query": """
        query questionCustom($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                content
                codeSnippets {
                    lang
                    langSlug
                    code
                }
            }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    }

    return _fetch_graphql(payload)['data']['question']
