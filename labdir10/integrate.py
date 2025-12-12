import math
import concurrent.futures
import multiprocessing
import timeit


def integrate(f, a, b, n_iter=1000):
    """
    Вычисляет интеграл функции f от a до b методом средних прямоугольников.

    Аргументы:
    f - функция, которую интегрируем (например, math.sin)
    a - начало отрезка (число)
    b - конец отрезка (число)
    n_iter - количество разбиений отрезка (целое число)

    Возвращает:
    Приближенное значение интеграла (число)
    """

    h = (b - a) / n_iter
    total = 0.0

    for i in range(n_iter):
        x_left = a + i * h
        x_right = x_left + h
        x_mid = (x_left + x_right) / 2
        total += f(x_mid) * h

    return total


def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием ThreadPoolExecutor (потоков).

    Аргументы:
    f - функция, интеграл которой вычисляется.
    a - нижний предел интегрирования.
    b - верхний предел интегрирования.
    n_jobs - количество потоков для параллельного выполнения.
    n_iter - общее количество итераций.

    Возвращает:
    Приближенное значение определенного интеграла.
    """
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs)
    step = (b - a) / n_jobs

    futures = []
    for i in range(n_jobs):
        start = a + i * step
        end = a + (i + 1) * step
        futures.append(executor.submit(integrate, f, start, end, n_iter // n_jobs))

    result = 0.0
    for future in concurrent.futures.as_completed(futures):
        result += future.result()

    executor.shutdown()
    return result


def integrate_process(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием ProcessPoolExecutor (процессов).

    Аргументы:
    f - функция, интеграл которой вычисляется.
    a - нижний предел интегрирования.
    b - верхний предел интегрирования.
    n_jobs - количество процессов для параллельного выполнения.
    n_iter - общее количество итераций.

    Возвращает:
    Приближенное значение определенного интеграла.
    """
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs)
    step = (b - a) / n_jobs

    futures = []
    for i in range(n_jobs):
        start = a + i * step
        end = a + (i + 1) * step
        futures.append(executor.submit(integrate, f, start, end, n_iter // n_jobs))

    result = 0.0
    for future in concurrent.futures.as_completed(futures):
        result += future.result()

    executor.shutdown()
    return result


def worker(args):
    """
    Вспомогательная функция для вычисления части интеграла.

    Аргументы:
    args - кортеж (f, start, end, n_iter)

    Возвращает:
    Значение части интеграла.
    """
    f, start, end, n_iter = args
    return integrate(f, start, end, n_iter)


def integrate_processes_mp(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием multiprocessing.Pool.
    Использование multiProcessing будет давать очень близкий результат к noGIL
    noGIL установить не удалось

    Аргументы:
    f - функция, интеграл которой вычисляется.
    a - нижний предел интегрирования.
    b - верхний предел интегрирования.
    n_jobs - количество процессов для параллельного выполнения.
    n_iter - общее количество итераций.

    Возвращает:
    Приближенное значение определенного интеграла.
    """
    step = (b - a) / n_jobs

    tasks = []
    for i in range(n_jobs):
        start = a + i * step
        end = a + (i + 1) * step
        tasks.append((f, start, end, n_iter // n_jobs))

    with multiprocessing.Pool(processes=n_jobs) as pool:
        results = pool.map(worker, tasks)

    return sum(results)


def measure_performance():
    """
    Замеряет время выполнения для разных n_iter.
    """
    print("Замер времени выполнения функции integrate:")
    print("-" * 50)

    n_iter_values = [100, 1000, 10000, 100000, 1000000]

    for n_iter in n_iter_values:
        timer = timeit.Timer(
            stmt="integrate(math.sin, 0, math.pi, n_iter)",
            setup="from __main__ import integrate, math",
            globals={'n_iter': n_iter}
        )

        times = timer.repeat(repeat=5, number=1)
        min_time = min(times)

        result = integrate(math.sin, 0, math.pi, n_iter)

        print(f"n_iter = {n_iter:8d}: время = {min_time:8.4f} сек, "
              f"результат = {result:10.8f}, ошибка = {abs(2 - result):.8f}")

    print("-" * 50)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    measure_performance()