import math


def integrate_cython_pure(func, double a, double b, int n_iter=1000):
    cdef double h = (b - a) / n_iter
    cdef double total = 0.0
    cdef int i
    cdef double x_left, x_right, x_mid

    for i in range(n_iter):
        x_left = a + i * h
        x_right = x_left + h
        x_mid = (x_left + x_right) / 2
        total += func(x_mid) * h

    return total


def integrate_cython_optimized(func, double a, double b, int n_iter=1000):
    cdef double h = (b - a) / n_iter
    cdef double total = 0.0
    cdef int i
    cdef double x_mid

    for i in range(n_iter):
        x_mid = a + (i + 0.5) * h
        total += func(x_mid)

    return total * h


def integrate_cython(f, a, b, n_iter=1000):
    return integrate_cython_optimized(f, a, b, n_iter)