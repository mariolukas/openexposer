import os

from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy

from grslicer import VERSION


dev_mode = os.path.exists('dev')

if dev_mode:
    from Cython.Distutils import build_ext

    print('Development mode: Compiling Cython modules from .pyx sources.')
    sources = ["grslicer/util/cynp.pyx"]

else:
    from distutils.command.build_ext import build_ext

    print('Distribution mode: Compiling Cython generated .c sources.')
    sources = ["grslicer/util/cynp.c"]

ext = Extension("grslicer/util/cynp", sources=sources, language="c", include_dirs=[numpy.get_include()])

setup(
    name="GRSlicer",
    version=VERSION,
    author='Gregor Ratajc',
    author_email='me@gregorratajc.com',
    url='https://github.com/greginvm/grslicer',
    packages=find_packages(),
    ext_modules=[ext],
    scripts=['run.py'],
    tests_require=['pytest'],
    cmdclass={
        'build_ext': build_ext},
)