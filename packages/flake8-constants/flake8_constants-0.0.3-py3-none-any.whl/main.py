import ast
from typing import Any, Generator, Set, Tuple, Union, Dict, List
from typing_extensions import Final
import argparse


class ConstantModificationChecker:
    name: Final[str] = "flake8-constants"
    version: Final[str] = "0.0.3"

    DEFAULT_NON_MODIFYING_METHODS: Final[Set[str]] = {
        "get",
        "keys",
        "values",
        "items",
        "copy",
        "deepcopy",
        "encode",
        "decode",
        "deepcopy",
        "__getitem__",
        "__len__",
        "__iter__",
        "__contains__",
    }

    def __init__(self, tree: ast.AST):
        self.tree: ast.AST = tree
        self.constants: Dict[str, Set[str]] = {"": set()}  # Global scope
        self.scope_stack: List[str] = [""]  # Start in global scope
        self.non_modifying_methods: Set[str] = self.DEFAULT_NON_MODIFYING_METHODS.copy()

    def run(self) -> Generator[Tuple[int, int, str, type], Any, None]:
        yield from self.visit_node(self.tree)

    def visit_node(
        self, node: ast.AST
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            self.scope_stack.append(node.name)
            self.constants.setdefault(self.current_scope(), set())

            for item in node.body:
                yield from self.visit_node(item)

            self.scope_stack.pop()
            return

        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            yield from self.check_assignment(node)
        elif isinstance(node, ast.AugAssign):
            yield from self.check_aug_assignment(node)
        elif isinstance(node, ast.Call):
            yield from self.check_call(node)

        for child in ast.iter_child_nodes(node):
            yield from self.visit_node(child)

    def current_scope(self) -> str:
        return ".".join(self.scope_stack)

    def check_assignment(
        self, node: Union[ast.Assign, ast.AnnAssign]
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and target.id.isupper():
                current_scope = self.current_scope()
                if target.id in self.constants[current_scope]:
                    yield (
                        node.lineno,
                        node.col_offset,
                        f"C001 Reassignment of constant '{target.id}' in scope '{current_scope}'",
                        type(self),
                    )
                else:
                    self.constants[current_scope].add(target.id)
                    # Check if the constant is a mutable type
                    if isinstance(node, ast.Assign):
                        value = node.value
                    elif isinstance(node, ast.AnnAssign):
                        value = node.value
                    else:
                        continue

                    if isinstance(value, (ast.List, ast.Dict, ast.Set)):
                        yield (
                            node.lineno,
                            node.col_offset,
                            f"C006 Constant '{target.id}' is defined as a mutable type",
                            type(self),
                        )

            elif isinstance(target, ast.Attribute) and target.attr.isupper():
                if isinstance(target.value, ast.Name) and target.value.id == "self":
                    class_scope = ".".join(self.scope_stack[:-1])
                    if class_scope in self.constants and target.attr in self.constants[class_scope]:
                        yield (
                            node.lineno,
                            node.col_offset,
                            f"C002 Modification of class constant '{target.attr}'",
                            type(self),
                        )
                    else:
                        self.constants[class_scope].add(target.attr)

    def check_aug_assignment(
        self, node: ast.AugAssign
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
            yield (
                node.lineno,
                node.col_offset,
                f"C003 Augmented assignment to constant '{node.target.id}' in scope '{self.current_scope()}'",
                type(self),
            )
        elif isinstance(node.target, ast.Attribute) and node.target.attr.isupper():
            if (
                isinstance(node.target.value, ast.Name)
                and node.target.value.id == "self"
            ):
                class_scope = ".".join(self.scope_stack[:-1])
                if (
                    class_scope in self.constants
                    and node.target.attr in self.constants[class_scope]
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        f"C004 Augmented assignment to class constant '{node.target.attr}'",
                        type(self),
                    )

    def check_call(
        self, node: ast.Call
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if isinstance(node.func, ast.Attribute) and isinstance(
            node.func.value, ast.Name
        ):
            if (
                node.func.value.id.isupper()
                and node.func.attr not in self.non_modifying_methods
            ):
                yield (
                    node.lineno,
                    node.col_offset,
                    f"C005 Potential modification of constant '{node.func.value.id}' through method call in scope '{self.current_scope()}'",
                    type(self),
                )

    @classmethod
    def add_options(cls, parser: Any) -> None:
        try:
            parser.add_option(
                "--non-modifying-methods",
                default=",".join(cls.DEFAULT_NON_MODIFYING_METHODS),
                parse_from_config=True,
                comma_separated_list=True,
                help="Comma-separated list of methods considered non-modifying",
            )
        except argparse.ArgumentError:
            pass

    @classmethod
    def parse_options(cls, options: Any) -> None:
        cls.non_modifying_methods = set(options.non_modifying_methods)


def plugin(tree: ast.AST) -> Generator[Tuple[int, int, str, type], Any, None]:
    return ConstantModificationChecker(tree).run()
