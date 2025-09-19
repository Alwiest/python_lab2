import unittest


def func(num: int, nr_low: int, nr_high: int) -> str:
    """
    Реализация алгоритма бинарного поиска.

    Args:
        num: Искомое число
        nr_low: Нижняя граница диапазона поиска
        nr_high: Верхняя граница диапазона поиска

    Returns:
        Строка с результатом поиска в формате:
        'Игра завершена. Число: X. Итераций: Y'
    """
    iterations = 0
    nr_mid = 0
    low, high = nr_low, nr_high

    while True:
        iterations += 1
        nr_mid = (high - low) // 2 + low
        print(f'Итерация {iterations}. низ: {low}, верх: {high}. Сейчас чекаем: {nr_mid}')

        if nr_mid == num:
            result = f'Игра завершена. Число: {nr_mid}. Итераций: {iterations}'
            print(result)
            return result

        if nr_low > num or nr_high < num:
            break
        if nr_mid < num:
            low = nr_mid + 1
        else:
            high = nr_mid - 1


def main():
    """Основная функция для ввода данных и запуска поиска."""
    try:
        num = int(input())
        nr_low, nr_high = input().split()
        nr_low, nr_high = int(nr_low), int(nr_high)

        result = func(num, nr_low, nr_high)

    except ValueError:
        print("Ошибка: введите корректные числовые значения")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


class TestMath(unittest.TestCase):
    """Тестовый класс для проверки функции бинарного поиска."""

    def test_checker_one(self):
        """Тест для числа 100 в диапазоне 0-100."""
        result = func(100, 0, 100)
        self.assertEqual(result, 'Игра завершена. Число: 100. Итераций: 7')

    def test_checker_two(self):
        """Тест для числа 0 в диапазоне 0-100."""
        result = func(0, 0, 100)
        self.assertEqual(result, 'Игра завершена. Число: 0. Итераций: 6')

    def test_checker_three(self):
        """Тест для числа 50 в диапазоне 0-100."""
        result = func(50, 0, 100)
        self.assertEqual(result, 'Игра завершена. Число: 50. Итераций: 1')

    def test_checker_four(self):
        """Тест для числа 25 в диапазоне 0-50."""
        result = func(25, 0, 50)
        self.assertEqual(result, 'Игра завершена. Число: 25. Итераций: 1')

    def test_checker_five(self):
        """Тест для числа 75 в диапазоне 50-100."""
        result = func(75, 50, 100)
        self.assertEqual(result, 'Игра завершена. Число: 75. Итераций: 1')

    def test_checker_six(self):
        """Тест для числа 1 в диапазоне 1-10."""
        result = func(1, 1, 10)
        self.assertEqual(result, 'Игра завершена. Число: 1. Итераций: 3')

    def test_checker_seven(self):
        """Тест для числа, которое не входит в диапазон"""
        result = func(15, 1, 10)
        self.assertEqual(result, None)


if __name__ == '__main__':
    main()
    unittest.main(argv=[''], verbosity=2, exit=False)

    print(help(func), help(main))