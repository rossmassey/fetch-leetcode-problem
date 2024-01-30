"""
Functions to fetch data from LeetCode API
"""
import requests

from ._cookies import get_leetcode_session_cookie

PROBLEM_API = 'https://leetcode.com/api/problems/all/'
GRAPHQL_API = 'https://leetcode.com/graphql'

COOKIE = None


def fetch_problems() -> list:
    """
    Fetch all problems from LeetCode API

    Returns:
        list: tuples with num, title, slug, and question id for each problem
    """
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
    """
    Fetch data from LeetCode GraphQL API

    Args:
        payload (dict): json payload to send

    Returns:
        dict: json response
    """
    response = requests.post(GRAPHQL_API, json=payload, cookies=COOKIE)
    return response.json()


def fetch_synced_code(question_id: int) -> dict:
    """
    Fetch synced code from LeetCode GraphQL API

    Args:
        question_id (int): problem question id (not frontend id)

    Returns:
        dict: json response with synced code
    """
    python_language_id = 11  # only get python for now
    payload = {
        "query":     """
        query SyncedCode($questionId: Int!, $lang: Int!) {
          syncedCode(questionId: $questionId, lang: $lang) {
            code
          }
        }
        """,
        "variables": {
            "questionId": question_id,
            "lang":       python_language_id
        }
    }

    return _fetch_graphql(payload)['data']['syncedCode']


def fetch_problem_info(slug: str) -> dict:
    """
    Fetch problem info

    Args:
        slug (str): problem title slug

    Returns:
        dict: json response with problem info
    """
    payload = {
        "query":     """
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


def set_cookie(cookie_path: str):
    global COOKIE
    COOKIE = get_leetcode_session_cookie(cookie_path)
