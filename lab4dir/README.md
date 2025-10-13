# Реализация функций
```
def fact_recursive(n: int) -> int:
    """Вычисление факториала рекурсивно."""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n: int) -> int:
    """Вычисление факториала через цикл (итеративно)."""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
```

# Бенчмарк с timeit
```
import timeit
import matplotlib.pyplot as plt

def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее минимальное время выполнения func на наборе данных."""
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)

# фиксированный набор чисел для тестирования
test_data = list(range(10, 300, 10))

# собираем результаты
res_recursive = [benchmark(fact_recursive, [n], number=1000, repeat=5) for n in test_data]
res_iterative = [benchmark(fact_iterative, [n], number=1000, repeat=5) for n in test_data]
```
# Построение графика
```
plt.plot(test_data, res_recursive, label="Рекурсивный", color='blue')
plt.plot(test_data, res_iterative, label="Итеративный", color='red')
plt.xlabel("n")
plt.ylabel("Время выполнения (сек)")
plt.title("Сравнение рекурсивного и итеративного факториала")
plt.legend()
plt.grid(True)
plt.show()
```
# Выводы
Итеративная реализация работает заметно быстрее рекурсивной, особенно на больших n, включая lru_cache.
Рекурсивная реализация замедляется из-за временных расходов на вызовы функций и использование стека.
Сложность обеих функций O(n), но для использования на больших числах лучше итеративный подход.

<img width="951" height="731" alt="image" src="https://github.com/user-attachments/assets/4e541b81-8e70-4ccb-992f-feb6d88e6ef6" />
<img width="945" height="714" alt="image" src="https://github.com/user-attachments/assets/d0b5dad2-220c-4b42-aea5-15cc0bf2ed65" />

<img width="939" height="708" alt="image" src="https://github.com/user-attachments/assets/e6b907cd-5bd6-467b-bbfb-460f1e4b0a1f" />
<img width="951" height="731" alt="image" src="https://github.com/user-attachments/assets/4e541b81-8e70-4ccb-992f-feb6d88e6ef6" />
<img width="939" height="708" alt="image" src="https://github.com/user-attachments/assets/e6b907cd-5bd6-467b-bbfb-460f1e4b0a1f" />
