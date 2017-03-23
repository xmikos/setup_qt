#!/usr/bin/env python

from setuptools import setup

setup(
    name='setup_qt',
    version='1.0.0',
    description='Compile Qt resource files, UI files and translations in setup.py',
    long_description=open('README.rst').read(),
    author='Michal Krenek (Mikos)',
    author_email='m.krenek@gmail.com',
    url='https://github.com/xmikos/setup_qt',
    license='MIT',
    py_modules=['setup_qt'],
    install_requires=[
        'setuptools',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Framework :: Setuptools Plugin',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Software Distribution',
    ]
)
