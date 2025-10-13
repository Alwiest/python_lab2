import timeit
from typing import Callable, List
import matplotlib.pyplot as plt
import random
from functools import lru_cache


#lru_cache
def fact_recursive(n: int) -> int:
    """
    Вычисляет факториал числа n рекурсивно.

    Args:
        n (int): Целое неотрицательное число.

    Returns:
        int: Факториал числа n.

    Example:
        >>> fact_recursive(5)
        120
    """
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


#lru_cache
def fact_iterative(n: int) -> int:
    """
    Вычисляет факториал числа n итеративно (через цикл).

    Args:
        n (int): Целое неотрицательное число.

    Returns:
        int: Факториал числа n.

    Example:
        >>> fact_iterative(5)
        120
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def benchmark(func: Callable[[int], int], data: List[int], number: int = 1, repeat: int = 5) -> float:
    """
    Выполняет бенчмарк функции func на наборе чисел data и возвращает среднее минимальное время.

    Args:
        func (Callable[[int], int]): Функция для тестирования.
        data (List[int]): Список чисел, на которых будет тестироваться функция.
        number (int, optional): Количество вызовов функции за один прогон. Defaults to 1.
        repeat (int, optional): Сколько раз повторить замер для каждого числа. Defaults to 5.

    Returns:
        float: Среднее минимальное время выполнения функции для всех чисел в data.
    """
    total = 0.0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)


def main() -> None:
    """
    Основная функция: генерирует тестовые данные, выполняет бенчмарк
    для рекурсивной и итеративной реализации факториала и строит графики.

    Returns:
        None
    """
    # фиксированный набор данных
    random.seed(42)
    test_data: List[int] = list(range(10, 300, 10))

    res_recursive: List[float] = []
    res_iterative: List[float] = []

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n], number=10000, repeat=5))
        res_iterative.append(benchmark(fact_iterative, [n], number=10000, repeat=5))

    # Визуализация результатов
    plt.subplot(2, 1, 1)
    plt.plot(test_data, res_recursive, label="Рекурсивный", color='blue')
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Рекурсивный факториал")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(test_data, res_iterative, label="Итеративный", color='red')
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Итеративный факториал")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
