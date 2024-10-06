# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Some trivial tests for the trivial repr handler."""

from __future__ import annotations

import pathlib
import typing

import pytest

import trivrepr


if typing.TYPE_CHECKING:
    from typing import Final


STR_HELLO: Final = "hello"
"""The string to test with."""

NUM_SMALL: Final = 17
"""The test value before incrementing."""

NUM_LARGE: Final = 18
"""The test value after incrementing."""

PATH_NONE: Final = "/nonexistent"
"""The path to test with."""


class NoJson(trivrepr.TrivialRepr):
    """A trivial test class that does not provide the `.to_json()` method."""

    def __init__(self, tag: str, value: int) -> None:
        """Construct a `NoJson` object with the specified values."""
        super().__init__()
        self.tag = tag
        self.value = value


class Base(trivrepr.TrivialReprWithJson):
    """A test class."""

    def __init__(self, num: int) -> None:
        """Store a number into an object."""
        super().__init__()
        self.num = num

    def increment(self) -> None:
        """Increment the stored number."""
        self.num += 1

    def query(self) -> int:
        """Return the stored number."""
        return self.num


class Derived(Base):
    """Another test class."""

    def __init__(self, num: int, stri: str) -> None:
        """Store a number and a string into an object."""
        super().__init__(num)
        self.stri = stri

    def trim(self) -> None:
        """Remove whitespace from the start and end of the string."""
        self.stri = self.stri.strip()

    def announce(self) -> str:
        """Return the string and the number."""
        return f"{self.stri}: {self.num}"


class Complex(trivrepr.TrivialReprWithJson):
    """A class with various subobjects."""

    def __init__(  # noqa: PLR0913,PLR0917
        self,
        base: Base,
        derived: Derived,
        list_base: list[Base],
        dict_derived: dict[str, Derived],
        set_int: set[int],
        dict_str: dict[str, str],
        path: pathlib.Path,
    ) -> None:
        """Initialize the complex class."""
        super().__init__()
        self.base = base
        self.derived = derived
        self.list_base = list_base
        self.dict_derived = dict_derived
        self.set_int = set_int
        self.dict_str = dict_str
        self.path = path


class KWOnlyArgs(trivrepr.TrivialReprWithJson):
    """A class with keyword-only arguments in the constructor."""

    def __init__(
        self,
        name: str = STR_HELLO,
        *,
        flag: bool = False,
        value: int = NUM_SMALL,
    ) -> None:
        """Initialize the keyword-only arguments test class."""
        self.name = name
        self.flag = flag
        self.value = value


def test_base() -> None:
    """Test the handling of the base class."""
    noj: Final = NoJson(STR_HELLO, NUM_LARGE)

    rep_noj: Final = repr(noj)
    assert f"tag={STR_HELLO!r}" in rep_noj
    assert f"value={NUM_LARGE}" in rep_noj

    base: Final = Base(NUM_SMALL)
    assert base.query() == NUM_SMALL

    rep_17: Final = repr(base)
    assert rep_17.startswith("Base(")
    assert f"num={NUM_SMALL}" in rep_17
    assert "," not in rep_17

    base.increment()
    assert base.query() == NUM_LARGE

    rep_18: Final = repr(base)
    assert rep_18.startswith("Base(")
    assert f"num={NUM_LARGE}" in rep_18
    assert "," not in rep_18


def test_derived() -> None:
    """Test the handling of the derived class."""
    untrimmed: Final = " hi \t"
    trimmed: Final = untrimmed.strip()

    derived: Final = Derived(NUM_SMALL, untrimmed)
    assert derived.query() == NUM_SMALL
    assert derived.announce() == untrimmed + f": {NUM_SMALL}"

    rep_17: Final = repr(derived)
    assert rep_17.startswith("Derived(")
    assert f"num={NUM_SMALL}" in rep_17
    assert f"stri={untrimmed!r}" in rep_17
    assert len(rep_17.split(", ")) == len(("num", "stri"))

    derived.increment()
    derived.trim()
    assert derived.query() == NUM_LARGE
    assert derived.announce() == trimmed + f": {NUM_LARGE}"

    rep_18: Final = repr(derived)
    assert rep_18.startswith("Derived(")
    assert f"num={NUM_LARGE}" in rep_18
    assert f"stri={trimmed!r}" in rep_18
    assert len(rep_18.split(", ")) == len(("num", "stri"))


def test_to_json() -> None:
    """Test the to_json() method."""
    noj: Final = NoJson(STR_HELLO, NUM_LARGE)
    with pytest.raises(AttributeError):
        noj.to_json()  # type: ignore[attr-defined]  # this is the whole point

    base: Final = Base(42)
    assert base.to_json() == {"num": 42}

    base.increment()
    assert base.to_json() == {"num": 43}

    derived: Final = Derived(616, "  stuff  ")
    assert derived.to_json() == {"num": 616, "stri": "  stuff  "}

    derived.increment()
    assert derived.to_json() == {"num": 617, "stri": "  stuff  "}

    derived.trim()
    assert derived.to_json() == {"num": 617, "stri": "stuff"}

    iset: Final = {2, -1, 15}
    sdict: Final = {"the quick": "brown fox", "jumped over": "the lazy dog"}
    cpx: Final = Complex(
        base,
        derived,
        [base],
        {"first": derived},
        iset,
        sdict,
        pathlib.Path(PATH_NONE),
    )
    assert cpx.to_json() == {
        "base": {"num": 43},
        "derived": {"num": 617, "stri": "stuff"},
        "list_base": [{"num": 43}],
        "dict_derived": {"first": {"num": 617, "stri": "stuff"}},
        "path": PATH_NONE,
        "set_int": sorted(iset),
        "dict_str": sdict,
    }


def test_kwonly() -> None:
    """Test the to_json() method on a class with keyword-only init arguments."""
    kwo: Final = KWOnlyArgs()
    assert kwo.to_json() == {
        "name": STR_HELLO,
        "flag": False,
        "value": NUM_SMALL,
    }
