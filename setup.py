# Настройки для сборки программы в файл exe

from cx_Freeze import setup, Executable
import sys, os, xlwt

# stderr = sys.stderr
# sys.stderr = open(os.devnull, 'w')

build_exe_options = {"packages": ["xlwt"]}

setup(
    name = "k2_82",
    version = "0.3.2",
    description = "k2_82",
    options = {"build_exe": build_exe_options},
    executables = [Executable("k2_82.py", base='Win32GUI')]
)