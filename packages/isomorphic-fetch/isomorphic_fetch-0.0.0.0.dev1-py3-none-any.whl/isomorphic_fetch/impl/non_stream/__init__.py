from sys import modules as sys_modules

if "pyodide" in sys_modules:
    from .pyodide import fetch
else:
    from .non_pyodide import fetch


del sys_modules

__all__ = ["fetch"]
