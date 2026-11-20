import bisect


class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"


def _build(values, start, end):
    if start > end:
        return None
    middle = (start + end) // 2
    return Node(
        values[middle],
        _build(values, start, middle - 1),
        _build(values, middle + 1, end),
    )


def insort_sorted(values):
    result = []
    for value in values:
        bisect.insort(result, value)
    return result


def make_tree(values) -> Node:
    values = insort_sorted(values)
    return _build(values, 0, len(values) - 1)


def _render(node):
    label = str(node.value)
    width = len(label)
    if node.left is None and node.right is None:
        return [label], width, width // 2
    if node.right is None:
        lines, n, x = _render(node.left)
        first = (x + 1) * " " + (n - x - 1) * "_" + label
        second = x * " " + "/" + (n - x - 1 + width) * " "
        rest = [line + width * " " for line in lines]
        return [first, second] + rest, n + width, n + width // 2
    if node.left is None:
        lines, n, x = _render(node.right)
        first = label + x * "_" + (n - x) * " "
        second = (width + x) * " " + "\\" + (n - x - 1) * " "
        rest = [width * " " + line for line in lines]
        return [first, second] + rest, n + width, width // 2
    left, n, x = _render(node.left)
    right, m, y = _render(node.right)
    first = (x + 1) * " " + (n - x - 1) * "_" + label + y * "_" + (m - y) * " "
    second = x * " " + "/" + (n - x - 1 + width + y) * " " + "\\" + (m - y - 1) * " "
    left = left + [n * " "] * (len(right) - len(left))
    right = right + [m * " "] * (len(left) - len(right))
    rest = [a + width * " " + b for a, b in zip(left, right)]
    return [first, second] + rest, n + m + width, n + width // 2


def pretty_print(node):
    if node is None:
        print("(empty)")
        return
    lines, _, _ = _render(node)
    for line in lines:
        print(line.rstrip())
