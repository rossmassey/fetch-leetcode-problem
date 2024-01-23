import re
import html
from collections import namedtuple

def extract_fields(problem_info: dict, synced_code: dict) -> dict:
    content = split_content(problem_info['content'])
    fields = {
        'num': problem_info['questionFrontendId'],
        'title': problem_info['title'],
        'slug': problem_info['titleSlug'],
        'difficulty': problem_info['difficulty'],
        'description': content.description,
        'examples': extract_examples(content.examples),
        'constraints': extract_constraints(content.constraints),
        'code_snippet': extract_python_snippet(problem_info['codeSnippets']),
    }

    return fields

def split_content(content: str) -> namedtuple:
    # fix weird symbols
    content = html.unescape(content)

    # leetcode use non-breaking space (nbsp) to delimit sections
    sections = content.split('<p>\xa0</p>')

    ContentSections = namedtuple('ContentSections', 
                                 'description examples constraints')
    
    ContentSections.description = sections[0]
    ContentSections.examples = sections[1]
    ContentSections.constraints = sections[2]

    return ContentSections

def extract_python_snippet(snippets: dict) -> dict:
    python_filter = lambda snippet: snippet['lang'] == 'Python3'
    python_snippet = filter(python_filter, snippets)

    return next(python_snippet)['code']

def extract_constraints(constraints_section: str) -> list:
    return re.findall(r'<li>(.*?)</li>', constraints_section)

def extract_examples(examples_section: str) -> str:
    # TODO extract description, img, [input], output 
    return examples_section


def html_to_rst(content: str) -> str:
    # TODO copy clean_html function
    pass
