setup_qt
========

Compile Qt resource files, UI files and translations in setup.py

Can be used with PyQt4, PyQt5, PySide and PySide2. Usage of Qt bindings
wrappers like `Qt.py <https://github.com/mottosso/Qt.py>`_ or
`QtPy <https://github.com/spyder-ide/qtpy>`_ is also supported.

Requirements
------------

- Python >= 3.4
- Setuptools (https://github.com/pypa/setuptools)
- PyQt4 / PyQt5 / PySide / PySide2

Example
-------

**setup.py:**

.. code-block:: python

    from setuptools import setup
    from setup_qt import build_qt
    
    setup(
        name='example',
        version='1.0.0',
        description='setup_qt example',
        author='Monty Python',
        author_email='monty.python@example.com',
        url='https://www.example.com',
        license='MIT',
        packages=['example'],
        package_data={
            'example': [
                '*.ui',
                '*.qrc',
                'languages/*.ts',
                'languages/*.qm',
            ],
        },
        entry_points={
            'gui_scripts': [
                'example=example.__main__:main',
            ],
        },
        install_requires=[
            'PyQt5',
            'Qt.py',
        ],
        options=[
            'build_qt': {
                'packages': ['example'],
                'languages': ['cs'],           # optional
                'languages_dir': 'languages',  # optional ('languages' is default)
                'bindings': 'PyQt5',           # optional ('PyQt5' is default)
                'replacement_bindings': 'Qt',  # optional (for Qt.py wrapper usage)
            },
        ],
        cmdclass={
            'build_qt': build_qt,
        },
    )

**Usage:**
::

    [user@host ~]$ python setup.py build_qt
    running build_qt
    compiling example Qt resource files...
    compiling example Qt UI files...
    updating example Qt translation files...
    compiling example Qt translation files...

Help
----
::

    Options for 'build_qt' command:
      --packages              List of comma separated packages in which to
                              recursively find .qrc, .ui and .ts files
      --languages             List of comma separated translation languages (could
                              be empty)
      --languages-dir         Directory with translation files (could be empty,
                              default is "languages")
      --bindings              Qt binding from which to use pyrcc, pyuic and
                              pylupdate commands (default is PyQt5)
      --replacement-bindings  Qt bindings replacement (e.g. if using wrapper like
                              Qt.py or QtPy)
      --pyrcc                 pyrcc command executable
      --pyuic                 pyuic command executable
      --pylupdate             pylupdate command executable
      --lrelease              lrelease command executable
      --filename-qrc          name template for .py files compiled from .qrc files
      --filename-ui           name template for .py files compiled from .ui files
      --filename-ts           name template for newly created .ts files
