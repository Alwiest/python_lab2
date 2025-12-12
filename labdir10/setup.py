from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "cython_integrate",
        ["cython_integrate.pyx"],
        extra_compile_args=['-O3'],
        language="c",
    )
]

setup(
    name="lab10_integrate",
    version="1.0",
    description="Cython модуль для численного интегрирования",
    ext_modules=cythonize(extensions,
                         compiler_directives={
                             'language_level': "3",
                             'boundscheck': False,
                             'wraparound': False,
                         },
                         annotate=True),
    zip_safe=False,
)