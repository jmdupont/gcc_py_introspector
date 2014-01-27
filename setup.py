#from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name='gcc.introspector',
    version='0.0.1',
    author='James Michael DuPont',
    author_email='jamesmikedupont@gmail.com',
    packages=['gcc.introspector', 'gcc.introspector.test'],
    scripts=['bin/tu_parser.py'],
    url='https://github.com/h4ck3rm1k3/gcc_py_introspector',
    license='LICENSE.txt',
    description='GCC TU parser',
    long_description=open('README.md').read(),
    #install_requires=[    ],

    tests_requires = ['ply.lex'],
    setup_requires = ['ply'],
    
    test_suite = 'nose.collector'
)

