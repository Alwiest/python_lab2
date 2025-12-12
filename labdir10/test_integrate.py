from integrate import integrate, integrate_async, integrate_process
from integrate import integrate_processes_mp, worker
try:
    from cython_integrate import integrate_cython
except ImportError:
    from integrate import integrate as integrate_cython
import unittest
import math


class TestIntegrateFirst(unittest.TestCase):
    def test_log2(self):
        result = integrate(math.log2, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate(math.cos, 0, math.pi / 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


class TestIntegrateAsync(unittest.TestCase):
    def test_log2(self):
        result = integrate_async(math.log2, 1, 2, n_iter=1000, n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_async(math.cos, 0, math.pi / 2, n_iter=1000, n_jobs=2)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


class TestIntegrateProcess(unittest.TestCase):
    def test_log2(self):
        result = integrate_process(math.log2, 1, 2, n_iter=1000, n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_process(math.cos, 0, math.pi / 2, n_iter=1000, n_jobs=2)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


class TestIntegrateCython(unittest.TestCase):
    def test_log2(self):
        result = integrate_cython(math.log2, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_cython(math.cos, 0, math.pi / 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


class TestIntegrateNoGIL(unittest.TestCase):
    def test_log2(self):
        result = integrate_processes_mp(math.log2, 1, 2, n_jobs=2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_processes_mp(math.cos, 0, math.pi / 2, n_jobs=2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


def run_all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegrateFirst))
    suite.addTest(unittest.makeSuite(TestIntegrateAsync))
    suite.addTest(unittest.makeSuite(TestIntegrateProcess))
    suite.addTest(unittest.makeSuite(TestIntegrateCython))
    suite.addTest(unittest.makeSuite(TestIntegrateNoGIL))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_all_tests()