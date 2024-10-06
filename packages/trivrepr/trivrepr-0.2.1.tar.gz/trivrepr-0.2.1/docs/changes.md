<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the parse-stages project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2024-10-05

### Fixes

- Also support keyword-only arguments to `__init__()`

## [0.2.0] - 2024-10-05

### Semi-incompatible changes

- Drop Python 2.x support
- Drop Python 3.5 - 3.7 support
- Declare support for Python 3.9 to 3.13

### Fixes

- Do not unconditionally expect the `inspect` module to have a `getargspec()`
  function; recent versions of Python 3.x do not have one

### Additions

- Add the `TrivialReprWithJson` class providing the `.to_json()` method to
  recursively generate a dictionary from the object's properties
- Add a Nix expression for running the unit tests suite
- Add some MkDocs/Markdown-based documentation and update the metadata links
- Test suite:
    - add tags to the Tox environments for `tox-stages` invocation
    - add lower and upper version constraints for the environment dependencies
    - add the "reuse" test environment to check the SPDX tags
    - add the "ruff" test environment replacing the "pep8" and "pylint" ones
    - add a manually-invoked "pyupgrade" test environment

### Other changes

- Switch from `setuptools` to `hatchling` and a PEP 518 build
- Reformat the source code using `ruff`
- Drop the `news.py` changelog extractor, we switched to `mkdocs`
- Switch to yearless copyright notices
- Switch to SPDX copyright and license tags
- Minor refactoring inspired by suggestions from Ruff
- Use `Final` type qualifiers for single-assignment variables
- Test suite:
    - list the environment names one per line
    - drop the "pep8" and "pylint" test environment in favor of the "ruff" one
    - DRY: keep the list of Python files and directories into a variable
    - move the `mypy` configuration to the `pyproject.toml` file

## [0.1.1] - 2019-03-07

### Additions

- Add the `news.py` tool for preparing the distribution changelog
- Use `setuptools-git` to include more files in the sdist tarball

### Fixes

- Correct the project's homepage URL

## [0.1.0] - 2019-03-06

### Started

- Initial public release

[Unreleased]: https://gitlab.com/ppentchev/trivrepr/-/compare/0.2.1...master
[0.2.1]: https://gitlab.com/ppentchev/trivrepr/-/compare/0.2.0...0.2.1
[0.2.0]: https://gitlab.com/ppentchev/trivrepr/-/compare/0.1.1...0.2.0
[0.1.1]: https://gitlab.com/ppentchev/trivrepr/-/compare/0.1.0...0.1.1
[0.1.0]: https://gitlab.com/ppentchev/trivrepr/-/tags/0.1.0
