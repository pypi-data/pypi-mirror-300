<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# trivrepr - a helper for generating repr() strings

\[[Home][ringlet-home] | [GitLab][gitlab] | [PyPI][pypi] | [ReadTheDocs][readthedocs]\]

## Overview

The `trivrepr` module contains the `TrivialRepr` class that may be
derived from to provide an implementation of `__repr__()` for
simple classes that have all their attributes passed directly to
the constructor.

``` py
import trivrepr

class KeyValue(trivrepr.TrivialRepr):
    def __init__(self, key, value, more='hi'):
        super(KeyValue, self).__init__()
        self.key = key
        self.value = value
        self.more = more

kv = KeyValue(key='key', value='val')
print(repr(kv))
```

This program will output:

```
KeyValue(key='key', value='val', more='hi')
```

The `TrivialReprWithJson` class adds a `.to_json()` method that returns
the same fields that `__repr__()` will output as a dictionary.

## Contact

The `trivrepr` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab].
This documentation is hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/trivrepr "The trivrepr GitLab repository"
[pypi]: https://pypi.org/project/trivrepr/ "The trivrepr Python Package Index page"
[readthedocs]: https://trivrepr.readthedocs.io/ "The trivrepr ReadTheDocs page"
[ringlet-home]: https://devel.ringlet.net/devel/trivrepr/ "The Ringlet trivrepr homepage"
