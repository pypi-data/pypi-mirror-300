# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Helper module for constructing repr() strings.

The trivrepr module contains the TrivialRepr class that may be
derived from to provide an implementation of __repr__() for
simple classes that have all their attributes passed directly to
the constructor.

    import trivrepr

    class KeyValue(trivrepr.TrivialRepr):
        def __init__(self, key, value, more='hi'):
            super(KeyValue, self).__init__()
            self.key = key
            self.value = value
            self.more = more

    kv = KeyValue(key='key', value='val')
    print(repr(kv))

This program will output:

    KeyValue(key='key', value='val', more='hi')

The `TrivialReprWithJson` class adds a `.to_json()` method that returns
the same fields that `__repr__()` will output as a dictionary.

The trivrepr module is fully typed.
"""

from __future__ import annotations

import inspect
import pathlib
import types
import typing


if typing.TYPE_CHECKING:
    from typing import Any, Final


VERSION: Final = "0.2.0"


def _to_json(obj: Any) -> Any:  # noqa: ANN401
    """Provide a dictionary describing an object's properties."""
    if isinstance(getattr(obj, "to_json", None), types.MethodType):
        return obj.to_json()

    if isinstance(obj, dict):
        return {name: _to_json(value) for (name, value) in obj.items()}

    if isinstance(obj, set):
        return sorted(_to_json(value) for value in obj)

    if isinstance(obj, list):
        return [_to_json(value) for value in obj]

    if isinstance(obj, pathlib.Path):
        return str(obj)

    # Eh, well... let us hope it is one of the base types.
    return obj


class TrivialRepr:
    """Helper class that generates a repr() string.

    Derived classes should take care that all arguments to the __init__()
    method correspond to object attributes with exactly the same names.
    """

    def __repr__(self) -> str:
        """Provide a Python-esque representation of the object."""
        attrlist: Final = inspect.getfullargspec(self.__init__).args[1:]  # type: ignore[misc]
        attrs: Final = ", ".join(f"{name}={getattr(self, name)!r}" for name in attrlist)
        return f"{type(self).__name__}({attrs})"


class TrivialReprWithJson(TrivialRepr):
    """Helper class that also provides a `.to_json()` method."""

    def to_json(self) -> dict[str, Any]:
        """Provide a dictionary describing the object's properties.

        Any property value that is an object implementing a `.to_json()`
        method will have this method invoked to obtain the dictionary value.
        Dictionaries, lists, and sets will be recursively descended into
        (set elements are also sorted); `pathlib.Path` objects will be
        converted into strings. Any other objects are stored as they are.
        """
        attrlist: Final = inspect.getfullargspec(self.__init__).args[1:]  # type: ignore[misc]
        return {name: _to_json(getattr(self, name)) for name in attrlist}
