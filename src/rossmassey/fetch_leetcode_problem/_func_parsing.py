"""
Functions for parsing leetcode code snippet
"""
import ast
from collections import defaultdict


def generate_function_ast(code: str) -> ast.FunctionDef | None:
    """
    Generates abstract syntax tree (ast) from code

    Args:
        code (str): class source code

    Returns:
        ast.FunctionDef: function ast for the leetcode problem
    """
    tree = ast.parse(_add_pass_to_functions(code))

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
    """
    Gets function parameters and types

    Args:
        function_ast (ast.FunctionDef): function ast

    Returns:
        tuple: list of parameters and ist of types
    """
    params = []
    param_types = []

    for arg in function_ast.args.args:
        params.append(arg.arg)
        param_types.append(_parse_annotation(arg.annotation))

    return params, param_types


def get_rtype(function_ast: ast.FunctionDef) -> str | None:
    """
    Gets function return type

    Args:
        function_ast (ast.FunctionDef): function ast

    Returns:
        str: the return type of the function
    """
    return _parse_annotation(function_ast.returns)


def _add_pass_to_functions(class_src: str) -> str:
    """
    Adds `pass` to each function in class source code to allow for ast parsing

    Args:
        class_src: source code of class

    Returns: source code with `pass` added to each function
    """
    lines = class_src.split('\n')
    modified_lines = []

    for line in lines:
        modified_lines.append(line)

        if line.strip().startswith('def'):
            # account for class offset
            indent = 4 + len(line) - len(line.lstrip())
            indented_pass = ' ' * indent + 'pass'
            modified_lines.append(indented_pass)

    return '\n'.join(modified_lines)


def _parse_annotation(node: ast.arg.annotation) -> str:
    """
    Converts the annotation binary tree to a string

    Travels down recursively, don't expect many levels...

    Args:
        ast.arg.annotation: the annotation object

    Returns:
        str: the annotation string
    """
    if isinstance(node, ast.Name):
        return node.id

    elif isinstance(node, ast.Subscript):
        return f"{node.value.id}[{_parse_annotation(node.slice)}]"
