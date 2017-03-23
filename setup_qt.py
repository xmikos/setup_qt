"""Compile Qt resource files, UI files and translations in setup.py

Can be used with PyQt4, PyQt5, PySide and PySide2. Usage of Qt bindings
wrappers like Qt.py or QtPy is also supported.
"""

import pathlib, shutil, re, subprocess
from distutils import log

import setuptools


class build_qt(setuptools.Command):
    description = 'compile Qt resource files, UI files and translations'
    user_options = [
        ('packages=', None, 'List of comma separated packages in which to recursively find .qrc, .ui and .ts files'),
        ('languages=', None, 'List of comma separated translation languages (could be empty)'),
        ('languages-dir=', None, 'Directory with translation files (could be empty, default is "languages")'),
        ('bindings=', None, 'Qt binding from which to use pyrcc, pyuic and pylupdate commands (default is PyQt5)'),
        ('replacement-bindings=', None, 'Qt bindings replacement (e.g. if using wrapper like Qt.py or QtPy)'),
        ('pyrcc=', None, 'pyrcc command executable'),
        ('pyuic=', None, 'pyuic command executable'),
        ('pylupdate=', None, 'pylupdate command executable'),
        ('lrelease=', None, 'lrelease command executable'),
        ('filename-qrc=', None, 'name template for .py files compiled from .qrc files'),
        ('filename-ui=', None, 'name template for .py files compiled from .ui files'),
        ('filename-ts=', None, 'name template for newly created .ts files'),
    ]

    def initialize_options(self):
        self.packages = []
        self.languages = []
        self.languages_dir = 'languages'
        self.bindings = 'PyQt5'
        self.replacement_bindings = ''
        self.pyrcc = 'pyrcc5'
        self.pyuic = 'pyuic5'
        self.pylupdate = 'pylupdate5'
        self.lrelease = 'lrelease'
        self.filename_qrc = 'qrc_{name}.py'
        self.filename_ui = 'ui_{name}.py'
        self.filename_ts = '{package}_{lang}.ts'

    def finalize_options(self):
        if isinstance(self.packages, str):
            self.packages = [p.strip() for p in self.packages.split(',')]
        if isinstance(self.languages, str):
            self.languages = [l.strip() for l in self.languages.split(',')]

    def run(self):
        for package in self.packages:
            package_path = pathlib.Path(package)
            if not package_path.is_dir():
                raise ValueError('Package "{}" not found!'.format(package))

            if self.pyrcc:
                log.info("compiling {} Qt resource files...".format(package))
                for f in package_path.glob('**/*.qrc'):
                    f_compiled = f.with_name(self.filename_qrc.format(name=f.stem))
                    ret = subprocess.call([self.pyrcc, '-o', f_compiled, f])
                    if ret != 0:
                        log.error('error compiling .qrc file: {}'.format(f))

            if self.pyuic:
                log.info("compiling {} Qt UI files...".format(package))
                for f in package_path.glob('**/*.ui'):
                    f_compiled = f.with_name(self.filename_ui.format(name=f.stem))
                    ret = subprocess.call([self.pyuic, '-o', f_compiled, f])
                    if ret != 0:
                        log.error('error compiling .ui file: {}'.format(f))

                    # Replace bindings with replacement_bindings in compiled files
                    if ret == 0 and self.bindings and self.replacement_bindings:
                        # Move original file to backup
                        backup = f_compiled.with_name(f_compiled.name + '.bak')
                        f_compiled.replace(backup)

                        # Write altered content to original file
                        orig_text = backup.open().read()
                        new_text = re.sub('^from {} import'.format(self.bindings),
                                          'from {} import'.format(self.replacement_bindings),
                                          orig_text, flags=re.MULTILINE)
                        with f_compiled.open('w') as fd:
                            fd.write(new_text)

                        # Copy file permissions and attributes and delete backup
                        shutil.copystat(backup, f_compiled)
                        backup.unlink()

            if self.languages and self.pylupdate:
                log.info("updating {} Qt translation files...".format(package))
                languages_path = package_path / self.languages_dir
                if not languages_path.exists():
                    languages_path.mkdir(parents=True)

                py_files = package_path.glob('**/*.py')
                ts_files = package_path.glob('**/*.ts')
                ts_files_defined = [languages_path / self.filename_ts.format(package=package, lang=l)
                                    for l in self.languages]
                ts_files_all = sorted(set(ts_files).union(ts_files_defined))
                ret = subprocess.call([self.pylupdate, *py_files, '-ts', *ts_files_all])
                if ret != 0:
                    log.error('error updating .ts files: {}'.format(', '.join(ts_files_all)))

            if self.languages and self.lrelease:
                log.info("compiling {} Qt translation files...".format(package))
                ts_files = package_path.glob('**/*.ts')
                ret = subprocess.call([self.lrelease, *ts_files])
                if ret != 0:
                    log.error('error compiling .ts files: {}'.format(', '.join(ts_files)))
