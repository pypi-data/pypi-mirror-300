import json
from collections.abc import Mapping, Sequence


def get_structure(var, _seen=None, _level=0, pretty: bool = False):
    """
    Recursively builds a structure representation of a variable, handling circular references.

    Args:
        var: The variable to analyze.
        _seen: A set of object IDs that have already been visited (used for detecting circular references).
        _level: The current level of recursion (used for formatting).
        pretty (bool): If True, format with new lines and indents. If False, compact formatting.

    Returns:
        str: A string representing the structure of the variable.
    """
    if _seen is None:
        _seen = set()

    if id(var) in _seen:
        return '"<Circular Reference>"'

    _seen.add(id(var))

    indent = ' ' * (_level * 4) if pretty else ''
    newline = '\n' if pretty else ''
    sep = ', ' if not pretty else ',\n'

    if isinstance(var, Mapping):
        items = []
        for k, v in var.items():
            item = f'{indent if pretty else ""}"{k}": {
                get_structure(v, _seen, _level + 1, pretty)}'
            items.append(item)
        return f'{{{newline}{sep.join(items)}{newline}{indent}}}'
    elif isinstance(var, tuple):
        items = [f'{indent if pretty else ""}{get_structure(
            i, _seen, _level + 1, pretty)}' for i in var]
        return f'({newline}{sep.join(items)}{newline}{indent})'
    elif isinstance(var, list):
        items = [f'{indent if pretty else ""}{get_structure(
            i, _seen, _level + 1, pretty)}' for i in var]
        return f'[{newline}{sep.join(items)}{newline}{indent}]'
    else:
        return json.dumps(type(var).__name__)


def print_structure(var, pretty: bool = False):
    """
    Prints the structure of any variable, handling circular references.

    Args:
        var: The variable to analyze.
        pretty (bool): If True, format with new lines and indents. If False, compact formatting.
    """
    print(get_structure(var, pretty=pretty))
