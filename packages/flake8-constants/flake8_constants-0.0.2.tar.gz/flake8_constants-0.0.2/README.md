# Flake8 Constants

A Flake8 plugin to detect modifications of constants in Python code, enhancing code quality and preventing unintended behavior.

## Why It's Needed

Constants are meant to be immutable values that don't change throughout the execution of a program. However, Python doesn't have built-in support for true constants, relying on naming conventions (all uppercase) to indicate that a variable should be treated as a constant. This plugin helps enforce these conventions by detecting and reporting attempts to modify constants, which can lead to:

1. Improved code reliability: Preventing accidental modifications of values that should remain constant.
2. Better maintainability: Ensuring that constants are used as intended across the codebase.
3. Clearer intent: Helping developers distinguish between mutable variables and immutable constants.
4. Reduced bugs: Catching potential errors early in the development process.

## Features

- Detects reassignment of constants (variables with all uppercase names)
- Identifies modifications to class constants
- Catches augmented assignments to constants (e.g., `+=`, `-=`)
- Warns about potential modifications through method calls on constants
- Configurable list of non-modifying methods to reduce false positives
- Works across different scopes: global, class, and function levels

## Installation

You can install Flake8 Constants using pip:

```bash
pip install flake8-constants
```

## Usage

Once installed, flake8 will automatically use this plugin. Run flake8 as usual:

```bash
flake8 your_script.py
```

or integrate it into your existing flake8 configuration.

## Configuration

You can configure the plugin by creating a `.flake8` file in your project root and adding the following options:

```ini
[flake8]
ignore = C001,C005
```

This example ignores errors related to constant reassignment and augmented assignments.


## Error Codes

- C001: Reassignment of constant
- C002: Modification of constant in a function
- C003: Modification of constant in a class method
- C004: Modification of constant in a loop
- C005: Modification of constant in a comprehension

## Configuration

No additional configuration is required. The plugin works out of the box with default flake8 settings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.