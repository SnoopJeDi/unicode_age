from Cython.Build import cythonize
from setuptools import setup


setup(
    ext_modules=cythonize("src/unicode_age.pyx"),
)
