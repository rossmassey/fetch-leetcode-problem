def extract_fields(problem_info: dict, synced_code: dict) -> dict:
    fields = {
        'num': problem_info['questionFrontendId'],
        'title': problem_info['title'],
        'slug': problem_info['titleSlug'],
        'difficulty': problem_info['difficulty'],
        'code_snippet': extract_python_snippet(problem_info)
    }

    return fields


def extract_python_snippet(problem_info: dict) -> dict:
    python_filter = lambda snippet: snippet['lang'] == 'Python3'
    python_snippet = filter(python_filter, problem_info['codeSnippets'])
    return next(python_snippet)['code']
