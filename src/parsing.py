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
    }

    return fields


def format_and_split_content(content: str) -> namedtuple:
    # leetcode use non-breaking space (nbsp) to delimit sections
    sections = content.split('<p>&nbsp;</p>')

    # convert to rst
    sections = [html_to_rst(html.unescape(section)) for section in sections]

    ContentSections = namedtuple('ContentSections',
                                 'description examples constraints')

    ContentSections.description = sections[0]
    ContentSections.examples = sections[1]
    ContentSections.constraints = sections[2]

    print(ContentSections.examples)

    return ContentSections


def extract_python_snippet(snippets: dict) -> dict:
    python_filter = lambda snippet: snippet['lang'] == 'Python3'
    python_snippet = filter(python_filter, snippets)

    return next(python_snippet)['code']


def extract_constraints(constraints_section: str) -> list:
    return re.findall(r'<li>(.*?)</li>', constraints_section)


def extract_examples(examples_section: str) -> list:
    examples = []

    # Split the text into sections
    sections = re.split(r'\*\*Example \d+:\*\*', examples_section)
    counter = 1

    patterns = {
        'input': r'\*\*Input:\*\* ([^\n]+)',
        'output': r'\*\*Output:\*\* ([^\n]+)',
        'img': r'\.\. image:: ([^\n]+)',
        'explanation': r'\*\*Explanation:\*\*([\s\S]+?)(?=</pre>|$)'
    }

    for section in sections[1:]:  # Skip the first split as it's empty
        example = {
            'n': counter,
            'input': None, 'output': None, 'img': None, 'explanation': None
        }

        for key, pattern in patterns.items():
            if match := re.search(pattern, section):
                example[key] = match.group(1)

        # if input_match := re.search(r'\*\*Input:\*\* ([^\n]+)', section):
        #     example['input'] = input_match.group(1)
        #
        # if output_match := re.search(r'\*\*Output:\*\* ([^\n]+)', section):
        #     example['output'] = output_match.group(1)
        #
        # if img_match := re.search(r'\.\. image:: ([^\n]+)', section):
        #     example['img'] = img_match.group(1)

        examples.append(example)
        counter += 1

    return examples


def html_to_rst(text: str) -> str:
    """
    convert html tags to rst syntax

    Parameters:
        text (str): HTML formatted text

    Returns:
        str: rst formatted text
    """
    replacements = [
        {  # code pattern
            'pattern': r'<code>([\s\S]*?)</code>',
            'repl': r'``\1``'
        },
        {  # superscript pattern
            'pattern': r'<sup>(.*?)</sup>',
            'repl': r'^\1'
        },
        {  # bold pattern
            'pattern': r'<strong(?: [^>]*)?>(.*?)</strong>',
            'repl': r'**\1**'
        },
        {  # italic pattern
            'pattern': r'<em>(.*?)</em>',
            'repl': r'\1'
        },
        {  # paragraph pattern
            'pattern': r'<p>(.*?)</p>',
            'repl': r'\1'
        },
        {  # img pattern
            'pattern': r'<img alt="" src="(.*?)" style=".*?" />',
            'repl': '.. image:: \\1\n'
        },
        {  # for examples to work
            'pattern': r'true',
            'repl': 'True'
        },
        {
            'pattern': r'false',
            'repl': 'False'
        },
    ]

    for replacement in replacements:
        text = re.sub(replacement['pattern'], replacement['repl'], text)

    return text

    # code_pattern = r'<code>([\s\S]*?)</code>'
    # superscript_pattern = r'<sup>(.*?)</sup>'
    # bold_pattern = r'<strong(?: [^>]*)?>(.*?)</strong>'
    # italics_pattern = r'<em>(.*?)</em>'
    # paragraph_pattern = r'<p>(.*?)</p>'
    # img_pattern = r'<img alt="" src="(.*?)" style=".*?" />'
    #
    # text = re.sub(code_pattern, r'``\1``', text)
    # text = re.sub(superscript_pattern, r'^\1', text)
    # text = re.sub(bold_pattern, r'**\1**', text)
    # text = re.sub(italics_pattern, r'\1', text)  # remove italics
    # text = re.sub(paragraph_pattern, r'\1', text)
    # text = re.sub(img_pattern, ".. image:: \\1\n", text)

    # for examples to work
    # text = re.sub(r'true', 'True', text)
    # text = re.sub(r'false', 'False', text)

    return text
