"""
Программа для генерации бинарного дерева №12.
В корне дерева находится (root). Высота дерева (height) задаётся пользователем.
Для потомков используются правила:
    left = root ** 3
    right = (root * 2) - 1
"""

from typing import Any, Dict, List, Tuple, Optional
import unittest


def gen_bin_tree(height: int = 4,
                 root: int = 12,
                 container: str = "dict") -> Any:
    """
    Рекурсивно генерирует бинарное дерево.

    Args:
        height (int): Высота дерева (по умолчанию 4).
        root (int): Значение корня (по умолчанию 12).
        container (str): Формат представления ("dict", "list" или "tuple").

    Returns:
        Any: Дерево в указанном формате.

    Example:
        >>> gen_bin_tree(2, 12, "dict")
        {'value': 12,
         'left': {'value': 1728, 'left': None, 'right': None},
         'right': {'value': 23, 'left': None, 'right': None}}
    """

    def _build(node_value: int, h: int) -> Any:
        """Вспомогательная рекурсивная функция."""
        if h == 1:
            left = right = None
        else:
            left = _build(node_value ** 3, h - 1)
            right = _build((node_value * 2) - 1, h - 1)

        if container == "dict":
            return {"value": node_value, "left": left, "right": right}
        elif container == "list":
            return [node_value, left, right]
        elif container == "tuple":
            return (node_value, left, right)
        else:
            raise ValueError("Неверный формат контейнера")

    return _build(root, height)


# -------------------
# Тесты
# -------------------
class TestGenBinTree(unittest.TestCase):
    """Тесты для функции gen_bin_tree."""

    def test_height2_dict(self):
        tree = gen_bin_tree(height=2, root=12, container="dict")
        self.assertEqual(tree["value"], 12)
        self.assertEqual(tree["left"]["value"], 1728)   # 12**3
        self.assertEqual(tree["right"]["value"], 23)    # (12*2)-1

    def test_height1_list(self):
        tree = gen_bin_tree(height=1, root=5, container="list")
        self.assertEqual(tree[0], 5)
        self.assertIsNone(tree[1])
        self.assertIsNone(tree[2])

    def test_height2_tuple(self):
        tree = gen_bin_tree(height=2, root=2, container="tuple")
        self.assertEqual(tree[0], 2)
        self.assertEqual(tree[1][0], 8)   # 2**3
        self.assertEqual(tree[2][0], 3)   # (2*2)-1


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
