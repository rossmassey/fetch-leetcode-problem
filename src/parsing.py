import re
import html
from collections import namedtuple
from typing import List


def extract_fields(problem_info: dict, synced_code: dict) -> dict:
    content = format_and_split_content(problem_info['content'])

    fields = {
        'num': problem_info['questionFrontendId'],
        'title': problem_info['title'],
        'slug': problem_info['titleSlug'],
        'difficulty': problem_info['difficulty'],
        'description': content.description,
        'examples': extract_examples(content.examples),
        'constraints': extract_constraints(content.constraints),
        'code_snippet': extract_python_snippet(problem_info['codeSnippets']),
        'code': synced_code['code'] if synced_code else None
    }

    return fields


def format_and_split_content(content: str) -> namedtuple:
    # leetcode use non-breaking space (nbsp) to delimit sections
    sections = content.split('<p>&nbsp;</p>')

    # convert to rst
    sections = [html_to_rst(html.unescape(section)) for section in sections]

    # leetcode has 3 sections in content
    Content = namedtuple('Content',
                         'description examples constraints')

    return Content(sections[0], sections[1], sections[2])

def html_to_rst(text: str) -> str:
    patterns = {
        # code
        r'<code>([\s\S]*?)</code>': r'``\1``',
        # superscript
        r'<sup>(.*?)</sup>': r'^\1',
        # bold
        r'<strong(?: [^>]*)?>(.*?)</strong>': r'**\1**',
        # italics (remove)
        r'<em>(.*?)</em>': r'*\1*',
        # paragraph (remove)
        r'<p>(.*?)</p>': r'\1',
        # img
        r'<img alt="" src="(.*?)" style=".*?" />': r'.. image:: \1\n',
        # for examples to work
        r'true': r'True',
        r'false': r'False',
    }

    for pattern, repl in patterns.items():
        text = re.sub(pattern, repl, text)

    return text


def extract_python_snippet(snippets: dict) -> dict:
    python_snippet = (
        snippet['code'] for snippet in snippets
        if snippet['lang'] == 'Python3'
    )
    return next(python_snippet, None)


def extract_constraints(constraints_section: str) -> list:
    return re.findall(r'<li>(.*?)</li>', constraints_section)


def extract_examples(examples_section: str) -> list:
    patterns = {
        'input': r'\*\*Input:\*\* ([^\n]+)',
        'output': r'\*\*Output:\*\* ([^\n]+)',
        'img': r'\.\. image:: ([^\n]+)',
        'explanation': r'\*\*Explanation:\*\*([\s\S]+?)(?=</pre>|$)'
    }

    example_list = re.split(r'\*\*Example \d+:\*\*', examples_section)
    example_list = example_list[1:]  # first split is empty so drop

    examples = []
    for n, example in enumerate(example_list, 1):
        data = {
            'n': n,
            'input': None, 'output': None, 'img': None, 'explanation': None
        }

        for key, pattern in patterns.items():
            if match := re.search(pattern, example):
                data[key] = match.group(1)

        examples.append(data)

    return examples
