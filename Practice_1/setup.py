# pylint: disable=C0114

from distutils.core import setup
from Cython.Build import cythonize

# setup.py build_ext --inplace
setup(

    name='manual_array',
    ext_modules=cythonize("my_array.pyx"),
)
