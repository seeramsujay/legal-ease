"""
Build script for Cython-compiled C-extensions in Legal-Ease.
Provides ultra-fast clause alignment, Levenshtein calculation, and token matching.
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import os

ext_modules = [
    Extension(
        "legal_ease.fast_ops",
        sources=["src/legal_ease/fast_ops.pyx"],
        extra_compile_args=["-O3", "-march=native", "-ffast-math"],
    )
]

setup(
    name="legal-ease-accelerated",
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "nonecheck": False,
        },
    ),
)
