


def extract_fields(problem_info: dict) -> dict:
    fields = {}
    fields['code_snippet'] = extract_code_snippet(problem_info)




    return fields

def extract_code_snippet(problem_info: dict) -> dict:
    python_filter = lambda snippet: snippet['lang'] == 'Python3'
    python_snippet = filter(python_filter, problem_info['codeSnippets'])
    return next(python_snippet)['code']