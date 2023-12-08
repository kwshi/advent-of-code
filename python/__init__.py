# BOTH this file and the one under `_test` are needed in order for pytest to allow
# relative imports of `ks` in `_test`; this is because we want pytest to follow the
# "test modules inside packages" mode/layout, which requires `__init__.py`s at
# every level (starting from the test modules) up to the "package root":

# > pytest will find foo/bar/tests/test_foo.py and realize it is part of a package given that there’s an __init__.py file in the same folder. It will then search upwards until it can find the last folder which still contains an __init__.py file in order to find the package root (in this case foo/). To load the module, it will insert root/ to the front of sys.path (if not there already) in order to load test_foo.py as the module foo.bar.tests.test_foo.

# references:
# <https://stackoverflow.com/questions/50174130/how-do-i-pytest-a-project-using-pep-420-namespace-packages>
# <https://docs.pytest.org/en/6.2.x/pythonpath.html#test-modules-conftest-py-files-inside-packages>
