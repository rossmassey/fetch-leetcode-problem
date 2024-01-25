import html
import re
from collections import namedtuple

from _func_parsing import generate_function_ast, get_params, get_rtype


def extract_fields(problem_info: dict, synced_code: dict) -> dict:
    content = _format_and_split_content(problem_info['content'])
    code_snippet = _extract_python_snippet(problem_info['codeSnippets'])

    fields = {
        'num':          problem_info['questionFrontendId'],
        'title':        problem_info['title'],
        'slug':         problem_info['titleSlug'],
        'difficulty':   problem_info['difficulty'],
        'description':  content.description,
        'examples':     _extract_examples(content.examples),
        'constraints':  _extract_constraints(content.constraints),
        'code_snippet': code_snippet,
        'code':         synced_code['code'] if synced_code else None,
        'func':         _extract_function_info(code_snippet)
    }

    return fields


def _format_and_split_content(content: str) -> namedtuple:
    # leetcode use non-breaking space (nbsp) to delimit sections
    sections = content.split('<p>&nbsp;</p>')

    # convert to rst
    sections = [_html_to_rst(html.unescape(section)) for section in sections]

    # leetcode has 3 sections in content
    Content = namedtuple('Content',
                         'description examples constraints')

    return Content(sections[0], sections[1], sections[2])


def _html_to_rst(text: str) -> str:
    patterns = {
        # html pattern -> rst pattern
        r'<code>([\s\S]*?)</code>':                r'``\1``',
        r'<sup>(.*?)</sup>':                       r'^\1',
        r'<strong(?: [^>]*)?>(.*?)</strong>':      r'**\1**',
        r'<em>(.*?)</em>':                         r'*\1*',
        r'<p>(.*?)</p>':                           r'\1',
        r'<img alt="" src="(.*?)" style=".*?" />': r'.. image:: \1\n',

        # for examples to work  
        r'true':                                   r'True',
        r'false':                                  r'False',
    }

    for pattern, repl in patterns.items():
        text = re.sub(pattern, repl, text)

    return text


def _extract_python_snippet(snippets: dict) -> str | None:
    for snippet in snippets:
        if snippet['lang'] == 'Python3':
            return snippet['code']

    return None


def _extract_constraints(constraints_section: str) -> list:
    return re.findall(r'<li>(.*?)</li>', constraints_section)


def _extract_examples(examples_section: str) -> list:
    patterns = {
        'input':       r'\*\*Input:\*\* ([^\n]+)',
        'output':      r'\*\*Output:\*\* ([^\n]+)',
        'img':         r'\.\. image:: ([^\n]+)',
        'explanation': r'\*\*Explanation:\*\*([\s\S]+?)(?=</pre>|$)',
        'example':     r'\*\*Example \d+:\*\*'
    }

    example_list = re.split(patterns['example'], examples_section)
    example_list = example_list[1:]  # first split is empty so drop

    # each example has own data dict
    examples = []
    for n, example in enumerate(example_list, 1):
        data = {
            'n':     n,
            'input': None, 'output': None, 'img': None, 'explanation': None
        }

        # extract each pattern
        for key, pattern in patterns.items():
            if match := re.search(pattern, example):
                data[key] = match.group(1)

        examples.append(data)

    return examples


def _extract_function_info(code: str) -> dict | None:
    function_ast = generate_function_ast(code)

    if function_ast is None:
        return None

    params, param_types = get_params(function_ast)
    rtype = get_rtype(function_ast)

    return {
        'name':        function_ast.name,
        'params':      params,
        'param_types': param_types,
        'rtype':       rtype
    }
