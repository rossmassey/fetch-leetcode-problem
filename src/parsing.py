import re
import html
import ast
from collections import namedtuple, defaultdict
from typing import List, Any


def extract_fields(problem_info: dict, synced_code: dict) -> dict:
    content = format_and_split_content(problem_info['content'])
    code_snippet = extract_python_snippet(problem_info['codeSnippets'])

    fields = {
        'num': problem_info['questionFrontendId'],
        'title': problem_info['title'],
        'slug': problem_info['titleSlug'],
        'difficulty': problem_info['difficulty'],
        'description': content.description,
        'examples': extract_examples(content.examples),
        'constraints': extract_constraints(content.constraints),
        'code_snippet': code_snippet,
        'code': synced_code['code'] if synced_code else None,
        'func': extract_function_info(code_snippet)
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


def extract_python_snippet(snippets: dict) -> str | None:
    for snippet in snippets:
        if snippet['lang'] == 'Python3':
            return snippet['code']

    return None


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

    # each example has own data dict
    examples = []
    for n, example in enumerate(example_list, 1):
        data = {
            'n': n,
            'input': None, 'output': None, 'img': None, 'explanation': None
        }

        # extract each pattern
        for key, pattern in patterns.items():
            if match := re.search(pattern, example):
                data[key] = match.group(1)

        examples.append(data)

    return examples


def extract_function_info(code: str) -> dict | None:
    function_ast = generate_function_ast(code)

    if function_ast is None:
        return None

    params, param_types = get_params(function_ast)
    rtype = get_rtype(function_ast)

    return {
        'name': function_ast.name,
        'params': params,
        'param_types': param_types,
        'rtype': rtype
    }


def add_pass_to_functions(class_definition):
    lines = class_definition.split('\n')
    modified_lines = []

    for i, line in enumerate(lines):
        modified_lines.append(line)

        if line.strip().startswith('def'):
            # account for class offset
            indent = 4 + len(line) - len(line.lstrip())
            indented_pass = ' ' * indent + 'pass'
            modified_lines.append(indented_pass)

    return '\n'.join(modified_lines)


def generate_function_ast(code: str) -> ast.FunctionDef | None:
    tree = ast.parse(add_pass_to_functions(code))

    nodes = defaultdict(list)
    for node in ast.walk(tree):
        nodes[node.__class__.__name__].append(node)

    if not nodes['ClassDef'] or not nodes['FunctionDef']:
        return None

    # should only have one class
    class_name = nodes['ClassDef'][0].name

    # skip class based solutions (i.e. 155 - MinStack) for now
    if class_name != 'Solution':
        return None

    # assume there is one function
    return nodes['FunctionDef'][0]


def get_params(function_ast: ast.FunctionDef) -> tuple:
    params = []
    param_types = []
    for arg in function_ast.args.args:
        params.append(arg.arg)
        param_type = None

        if arg.annotation and hasattr(arg.annotation, 'id'):
            param_type = arg.annotation.id
        elif arg.annotation:
            param_type = f'{arg.annotation.value.id}[{arg.annotation.slice.id}]'

        param_types.append(param_type)

    return params, param_types


def get_rtype(function_ast: ast.FunctionDef) -> str | None:
    rtype = None
    if function_ast.returns and hasattr(function_ast.returns, 'id'):
        rtype = function_ast.returns.id
    elif function_ast.returns:
        rtype = f'{function_ast.returns.value.id}[{function_ast.returns.slice.id}]'
    return rtype
