"""
Модуль для построения бинарного дерева нерекурсивным способом.

Дерево представлено в виде словаря:
{
    "value": <значение узла>,
    "left": <левое поддерево или None>,
    "right": <правое поддерево или None>
}

Пример:
    gen_bin_tree(3, 1, lambda x: x * 2, lambda x: x + 3)
{'value': 1, 'left': {'value': 2, 'left': {...}, 'right': {...}}, 'right': {...}}
"""

from typing import Any, Callable, Dict


def gen_bin_tree(
    height: int,
    root: Any,
    left_branch: Callable[[Any], Any] = lambda x: x ** 3,
    right_branch: Callable[[Any], Any] = lambda x: (x * 2) - 1
) -> Dict[str, Any]:
    """
    Строит бинарное дерево заданной высоты нерекурсивным способом.

    Аргументы:
        height (int): высота дерева (минимум 1).
        root (Any): значение корневого узла.
        left_branch (Callable): функция для вычисления значения левого потомка.
        right_branch (Callable): функция для вычисления значения правого потомка.

    Возвращает:
        Dict[str, Any]: словарь, представляющий бинарное дерево.

    Пример:
        >>> gen_bin_tree(3, 1)
        {'value': 1, 'left': {'value': 1, ...}, 'right': {'value': 1, ...}}
    """
    if height < 1:
        raise ValueError("Высота дерева должна быть >= 1")

    # Создаем корень дерева
    tree = {"value": root, "left": None, "right": None}

    # Очередь для обхода дерева по уровням
    queue = [(tree, 1, root)]

    while queue:
        node, level, value = queue.pop(0)
        if level >= height:
            continue

        left_value = left_branch(value)
        right_value = right_branch(value)

        node["left"] = {"value": left_value, "left": None, "right": None}
        node["right"] = {"value": right_value, "left": None, "right": None}

        queue.append((node["left"], level + 1, left_value))
        queue.append((node["right"], level + 1, right_value))

    return tree


def print_tree(tree: Dict[str, Any], level: int = 0) -> None:
    """
    Выводит бинарное дерево в консоль в виде структуры.

    Аргументы:
        tree (Dict[str, Any]): дерево в виде словаря.
        level (int): текущий уровень (для отступов).
    """
    if tree is None:
        return
    print("  " * level + f"├─ {tree['value']}")
    print_tree(tree["left"], level + 1)
    print_tree(tree["right"], level + 1)


if __name__ == "__main__":
    # Вариант №12:
    # Root = 12; height = 4; left_leaf = root^3; right_leaf = (root*2)-1
    tree = gen_bin_tree(
        height=4,
        root=12,
        left_branch=lambda r: r ** 3,
        right_branch=lambda r: (r * 2) - 1
    )
    print_tree(tree)
