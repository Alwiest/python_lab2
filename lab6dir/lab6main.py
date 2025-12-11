"""
Сравнение времени работы рекурсивной и нерекурсивной реализации построения бинарного дерева.

Вариант №12:
    root = 12
    height = переменная (для тестов)
    left_leaf = root ** 3
    right_leaf = (root * 2) - 1
"""

from typing import Any, Callable, Dict
import timeit
import matplotlib.pyplot as plt


# Рекурсивный вариант
def build_tree_recursive(
    height: int,
    root: Any,
    left_branch: Callable[[Any], Any] = lambda x: x ** 3,
    right_branch: Callable[[Any], Any] = lambda x: (x * 2) - 1
) -> Dict[str, Any]:
    """
    Рекурсивно строит бинарное дерево заданной высоты.

    Args:
        height (int): высота дерева.
        root (Any): значение корневого узла.
        left_branch (Callable): формула для левого потомка.
        right_branch (Callable): формула для правого потомка.

    Returns:
        Dict[str, Any]: дерево в виде словаря.
    """
    if height < 1:
        raise ValueError("Высота дерева должна быть >= 1")

    if height == 1:
        return {"value": root, "left": None, "right": None}

    left_value = left_branch(root)
    right_value = right_branch(root)

    return {
        "value": root,
        "left": build_tree_recursive(height - 1, left_value, left_branch, right_branch),
        "right": build_tree_recursive(height - 1, right_value, left_branch, right_branch)
    }


# Нерекурсивный вариант
def build_tree_iterative(
    height: int,
    root: Any,
    left_branch: Callable[[Any], Any] = lambda x: x ** 3,
    right_branch: Callable[[Any], Any] = lambda x: (x * 2) - 1
) -> Dict[str, Any]:
    """
    Строит бинарное дерево нерекурсивным способом (через очередь).

    Args:
        height (int): высота дерева.
        root (Any): значение корневого узла.
        left_branch (Callable): формула для левого потомка.
        right_branch (Callable): формула для правого потомка.

    Returns:
        Dict[str, Any]: дерево в виде словаря.
    """
    if height < 1:
        raise ValueError("Высота дерева должна быть >= 1")

    tree = {"value": root, "left": None, "right": None}
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


# Сравнение времени работы
def compare_time(max_height: int = 10, repeats: int = 10) -> None:
    """
    Сравнивает время работы рекурсивного и нерекурсивного подходов при разных высотах дерева.
    Строит график зависимости времени от высоты.

    Args:
        max_height (int): максимальная высота дерева для теста.
        repeats (int): количество повторов каждого замера.
    """
    heights = list(range(1, max_height + 1))
    recursive_times = []
    iterative_times = []

    for h in heights:
        rec_time = timeit.timeit(
            lambda: build_tree_recursive(h, 12),
            number=repeats
        )
        iter_time = timeit.timeit(
            lambda: build_tree_iterative(h, 12),
            number=repeats
        )
        recursive_times.append(rec_time)
        iterative_times.append(iter_time)

    # Построение графика
    plt.figure(figsize=(8, 5))
    plt.plot(heights, recursive_times, marker="o", label="Рекурсивная реализация")
    plt.plot(heights, iterative_times, marker="s", label="Нерекурсивная реализация")
    plt.title("Сравнение времени построения бинарного дерева (вариант №12)")
    plt.xlabel("Высота дерева")
    plt.ylabel(f"Время выполнения ({repeats} повторов)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Вывод результатов в консоль
    print("Высота | Рекурсивная (сек) | Нерекурсивная (сек)")
    print("-----------------------------------------------")
    for h, r, i in zip(heights, recursive_times, iterative_times):
        print(f"{h:6d} | {r:18.6f} | {i:19.6f}")

    # Итоговый вывод
    avg_ratio = sum(r / i for r, i in zip(recursive_times, iterative_times)) / len(heights)
    print("\nВывод:")
    if avg_ratio > 1.1:
        print("→ Нерекурсивный метод быстрее в среднем примерно в {:.1f} раз.".format(avg_ratio))
    elif avg_ratio < 0.9:
        print("→ Рекурсивный метод быстрее в среднем примерно в {:.1f} раз.".format(1 / avg_ratio))
    else:
        print("→ Время работы обоих подходов примерно одинаково.")


# -----------------------------
# Точка входа
# -----------------------------
if __name__ == "__main__":
    compare_time(max_height=10, repeats=100)
