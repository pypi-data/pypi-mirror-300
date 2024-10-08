import ast

import pytest

from main import ConstantModificationChecker, plugin


def run_checker(code):
    tree = ast.parse(code.strip())
    checker = ConstantModificationChecker(tree)
    return list(checker.run())


def test_error_messages():
    code = """
MAX_VALUE = 100
MAX_VALUE = 200
"""
    results = run_checker(code)
    assert len(results) == 1
    assert "C001 Reassignment of constant 'MAX_VALUE'" in results[0][2]


@pytest.mark.parametrize(
    "code,expected_errors,expected_lines,expected_codes",
    [
        (
            """
MAX_VALUE = 100
MAX_VALUE = 200
CONSTANT_LIST = ['a', 'b', 'c']
CONSTANT_LIST.append('d')
normal_var = 10
normal_var = 20
""",
            2,
            [2, 4],
            ["C001", "C005"],
        ),
        (
            """
MAX_VALUE = 100
print(MAX_VALUE)
CONSTANT_LIST = ['a', 'b', 'c']
print(CONSTANT_LIST)
""",
            0,
            [],
            [],
        ),
        (
            """
max_value = 100
max_value = 200
constant_list = ['a', 'b', 'c']
constant_list.append('d')
""",
            0,
            [],
            [],
        ),
        (
            """
class PermissionsBase:
    LIST = Permission()
    GET = Permission()

class AssignmentPermissions(PermissionsBase):
    LIST = Permission(user_types=(...))
    GET = Permission(user_types=(...))
""",
            0,
            [],
            [],
        ),
        (
            """
MAPPING = {
    'type1': 'desc1',
    'type2': 'desc2'
}
value = MAPPING.get('type1')
""",
            0,
            [],
            [],
        ),
        (
            """
CONSTANT = 100
CONSTANT += 1
""",
            1,
            [2],
            ["C003"],
        ),
        (
            """
CONSTANT: int = 100
CONSTANT = 200
""",
            1,
            [2],
            ["C001"],
        ),
        (
            """
CONSTANT = [1, 2, 3]
CONSTANT.extend([4, 5])
""",
            1,
            [2],
            ["C005"],
        ),
        (
            """
class MyClass:
    CONSTANT = 100

    def method(self):
        self.CONSTANT = 200
""",
            1,
            [5],
            ["C002"],
        ),
    ],
)
def test_constant_modification(code, expected_errors, expected_lines, expected_codes):
    results = run_checker(code)
    assert (
        len(results) == expected_errors
    ), f"Expected {expected_errors} errors, got {len(results)} - {results}"
    if results:
        assert [
            result[0] for result in results
        ] == expected_lines, (
            f"Expected lines {expected_lines}, got {[result[0] for result in results]}"
        )
        assert [
            result[2][:4] for result in results
        ] == expected_codes, f"Expected codes {expected_codes}, got {[result[2][:4] for result in results]}"


def test_multiple_assignments():
    code = """
CONSTANT1 = CONSTANT2 = 100
CONSTANT1 = 200
"""
    results = run_checker(code)
    assert len(results) == 1
    assert "C001 Reassignment of constant 'CONSTANT1'" in results[0][2]


def test_method_call_on_constant():
    code = """
CONSTANT_DICT = {'key': 'value'}
CONSTANT_DICT.update({'new_key': 'new_value'})
"""
    results = run_checker(code)
    assert len(results) == 1
    assert "C005 Potential modification of constant 'CONSTANT_DICT'" in results[0][2]


def test_constant_in_different_scopes():
    code = """
GLOBAL_CONSTANT = 100

def func1():
    FUNC_CONSTANT = 200
    FUNC_CONSTANT = 300

class MyClass:
    CLASS_CONSTANT = 400
    
    def method(self):
        self.CLASS_CONSTANT = 500
"""
    results = run_checker(code)
    assert len(results) == 2, f"Expected 2 errors, got {len(results)} - {results}"
    assert (
        "C001 Reassignment of constant 'FUNC_CONSTANT' in scope '.func1'"
        in results[0][2]
    ), results
    assert (
        "C002 Modification of class constant 'CLASS_CONSTANT'" in results[1][2]
    ), results


def test_plugin_function():
    code = """
CONSTANT = 100
CONSTANT = 200
"""
    tree = ast.parse(code)
    results = list(plugin(tree))
    assert len(results) == 1
    assert "C001 Reassignment of constant 'CONSTANT'" in results[0][2]


def test_add_options():
    class MockParser:
        def __init__(self):
            self.options = []

        def add_option(self, *args, **kwargs):
            self.options.append((args, kwargs))

    parser = MockParser()
    ConstantModificationChecker.add_options(parser)
    assert len(parser.options) == 1
    option_args, option_kwargs = parser.options[0]

    assert "--non-modifying-methods" in option_args
    assert option_kwargs["default"] == ",".join(
        ConstantModificationChecker.DEFAULT_NON_MODIFYING_METHODS
    )
    assert option_kwargs["parse_from_config"] is True
    assert option_kwargs["comma_separated_list"] is True
    assert "help" in option_kwargs


def test_parse_options():
    class MockOptions:
        def __init__(self):
            self.non_modifying_methods = ["method1", "method2"]

    options = MockOptions()
    original_methods = ConstantModificationChecker.DEFAULT_NON_MODIFYING_METHODS.copy()

    try:
        ConstantModificationChecker.parse_options(options)
        assert ConstantModificationChecker.non_modifying_methods == set(
            ["method1", "method2"]
        )
    finally:
        # Restore the original default methods after the test
        ConstantModificationChecker.non_modifying_methods = original_methods


def test_default_non_modifying_methods():
    expected_default_methods = {
        "get",
        "keys",
        "values",
        "items",
        "copy",
        "deepcopy",
        "__getitem__",
        "__len__",
        "__iter__",
        "__contains__",
    }
    assert (
        ConstantModificationChecker.DEFAULT_NON_MODIFYING_METHODS
        == expected_default_methods
    )


def test_async_function():
    code = """
async def async_func():
    ASYNC_CONSTANT = 100
    ASYNC_CONSTANT = 200
"""
    results = run_checker(code)
    assert len(results) == 1
    assert (
        "C001 Reassignment of constant 'ASYNC_CONSTANT' in scope '.async_func'"
        in results[0][2]
    )


def test_nested_scopes():
    code = """
def outer():
    OUTER_CONSTANT = 100
    def inner():
        INNER_CONSTANT = 200
        INNER_CONSTANT = 300
    OUTER_CONSTANT = 400
"""
    results = run_checker(code)
    assert len(results) == 2
    assert (
        "C001 Reassignment of constant 'INNER_CONSTANT' in scope '.outer.inner'"
        in results[0][2]
    )
    assert (
        "C001 Reassignment of constant 'OUTER_CONSTANT' in scope '.outer'"
        in results[1][2]
    )


def test_class_method_constant():
    code = """
class TestClass:
    @classmethod
    def class_method(cls):
        CLASS_METHOD_CONSTANT = 100
        CLASS_METHOD_CONSTANT = 200
"""
    results = run_checker(code)
    assert len(results) == 1
    assert (
        "C001 Reassignment of constant 'CLASS_METHOD_CONSTANT' in scope '.TestClass.class_method'"
        in results[0][2]
    )


def test_augmented_assignment_in_class():
    code = """
class TestClass:
    CLASS_CONSTANT = 100
    
    def method(self):
        self.CLASS_CONSTANT += 1
"""
    results = run_checker(code)
    assert len(results) == 1
    assert (
        "C004 Augmented assignment to class constant 'CLASS_CONSTANT'" in results[0][2]
    )


def test_non_modifying_method_call():
    code = """
CONSTANT_DICT = {'key': 'value'}
value = CONSTANT_DICT.get('key')
"""
    results = run_checker(code)
    assert len(results) == 0


def test_annotated_assignment():
    code = """
ANNOTATED_CONSTANT: int = 100
ANNOTATED_CONSTANT = 200
"""
    results = run_checker(code)
    assert len(results) == 1
    assert "C001 Reassignment of constant 'ANNOTATED_CONSTANT'" in results[0][2]
