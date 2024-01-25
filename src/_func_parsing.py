import ast
from collections import defaultdict


def generate_function_ast(code: str) -> ast.FunctionDef | None:
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
    params = []
    param_types = []
    for arg in function_ast.args.args:
        params.append(arg.arg)
        param_type = None

        # FIXME: this work for List[int], but not List[List[int]] or more
        # (i.e. 2055) arg.annotation.value.id does not exist
        # will need to travel down until find .id
        if arg.annotation and hasattr(arg.annotation, 'id'):
            param_type = arg.annotation.id
        elif arg.annotation:
            param_type = f'{arg.annotation.value.id}[{arg.annotation.slice.id}]'

        param_types.append(param_type)

    return params, param_types


def get_rtype(function_ast: ast.FunctionDef) -> str | None:
    rtype = None
    # FIXME: see above
    if function_ast.returns and hasattr(function_ast.returns, 'id'):
        rtype = function_ast.returns.id
    elif function_ast.returns:
        rtype = f'{function_ast.returns.value.id}[{function_ast.returns.slice.id}]'
    return rtype


def _add_pass_to_functions(class_src: str) -> str:
    lines = class_src.split('\n')
    modified_lines = []

    for i, line in enumerate(lines):
        modified_lines.append(line)

        if line.strip().startswith('def'):
            # account for class offset
            indent = 4 + len(line) - len(line.lstrip())
            indented_pass = ' ' * indent + 'pass'
            modified_lines.append(indented_pass)

    return '\n'.join(modified_lines)
