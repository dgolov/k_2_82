# Настройки для сборки программы в файл exe

from cx_Freeze import setup, Executable
from settings import *

import sys, os, xlwt, PyQt5


# stderr = sys.stderr
# sys.stderr = open(os.devnull, 'w')

includes = ["xlwt",]

excludes = [
    'logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml', 'pydoc', 'doctest', 'argparse', 'datetime',
    'zipfile', 'subprocess', 'pickle', 'threading', 'locale', 'calendar', 'functools', 'weakref', 'tokenize', 'base64',
    'gettext', 'heapq', 're', 'bz2', 'fnmatch', 'getopt', 'reprlib', 'string', 'stringprep', 'quopri', 'copy', 'imp'
]

build_exe_options = {"packages": includes}

setup(
    name="k2_82",
    version=VERSION,
    description="k2_82",
    options={"build_exe": build_exe_options},
    executables=[Executable("k2_82.py", base='Win32GUI')]
)
