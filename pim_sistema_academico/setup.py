from setuptools import setup
from Cython.Build import cythonize

setup(
    name="media_cython",
    ext_modules=cythonize("media_cython.pyx"),
)
