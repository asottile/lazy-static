[![build status](https://github.com/asottile/lazy-static/actions/workflows/main.yml/badge.svg)](https://github.com/asottile/lazy-static/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/lazy-static/main.svg)](https://results.pre-commit.ci/latest/github/asottile/lazy-static/main)

lazy-static
===========

lazy module constants -- think lazy imports but for assignments

roughly named after the (deprecated) rust [crate lazy_static]

[crate lazy_static]: https://docs.rs/lazy_static/latest/lazy_static/

## installation

```bash
pip install lazy-static
```

## why ?

python 3.15 adds [lazy imports] which are neat but are a little too easy to
accidentally make eager.

[lazy imports]: https://peps.python.org/pep-0810/

take this small example for a little wrapper around `pyyaml`:

```python
import functools

lazy import yaml

loads = functools.partial(yaml.load, Loader=yaml.CSafeLoader)
```

did you catch the bug?  yeah that import isn't lazy due to accessing attributes!

it would be great if I could do:

```
lazy loads = functools.partial(yaml.load, Loader=yaml.CSafeLoader)
```

but there's no such thing...[^1] unless...

[^1]: yes yes you can do stuff with `@functools.cache` but that adds an ugly function call!

## Usage

`lazy-static` adds a single api: `@lazy_static.lazy`

taking a simple example:

```python
import argparse
from lazy_static import lazy

@lazy
def computed_once() -> int:
    print('computing!')
    return 5 * 5 * 5

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()  # just for `--help`
    print(f'got {computed_once}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
```

the lazy attribute is deferred when not accessed:

```console
$ python3 t.py --help
usage: t.py [-h]

options:
  -h, --help  show this help message and exit
```

but acts like a normal variable otherwise!

```console
$ python3 t.py
computing!
got 125
```

it even works with static typing!

```diff
$ diff -u t.py.bak t.py
--- t.py.bak    2026-07-24 17:47:14.278681851 -0400
+++ t.py    2026-07-24 17:47:22.759961815 -0400
@@ -10,6 +10,7 @@
     parser = argparse.ArgumentParser()
     parser.parse_args()  # just for `--help`
     print(f'got {computed_once}')
+    reveal_type(computed_once)
     return 0

 if __name__ == '__main__':
```

```console
$ mypy t.py
t.py:13: note: Revealed type is "int"
Success: no issues found in 1 source file
```
___

if we take the earlier example we can define our `loads` partial lazily while
preserving the `lazy` import!


```python
import functools

from lazy_static import lazy
lazy import yaml

@lazy
def loads():
    return functools.partial(yaml.loads, Loader=yaml.CSafeLoader)
```
