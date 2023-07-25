#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='drawwithplt',
    version="0.3.1",
    description=(
        'More EASY to Draw SCI figure with PIL'
    ),
    # long_description=open('README.rst').read(),
    author='liftes',
    author_email='21121598@bjtu.edu.cn',
    maintainer='liftes',
    maintainer_email='21121598@bjtu.edu.cn',
    license='BSD License',
    # packages=find_packages(),
    py_modules=["drawwithplt"],
    platforms=["all"],
    url='https://github.com/liftes/PythonDraw',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'scipy',
        'matplotlib',
        'seaborn',
        'numpy',
    ]
)