import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,				
                     "packages": ["pygame", "sys","socket", "random", "pickle", "time"],
                     "excludes": ["scipy", "tkinter", "numpy", "test", "multiprocessing"]}

base = None
'''if sys.platform == "win32":
    base = "Win32GUI"''' #Uncomment to make the console disappear.

setup(name="M711Dimension",
      version="1.0",
      description="M711Dimension - Client",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="client.py", base=base)])