import functools
import importlib.abc
import importlib.machinery
import importlib.util
import sys
import types
from collections.abc import Callable


class _LazyStaticFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self) -> None:
        self._funcs: dict[str, Callable[[], object]] = {}

    def find_spec(
            self,
            fullname: str,
            path: object,
            target: object = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if fullname in self._funcs:
            return importlib.util.spec_from_loader(fullname, self)
        else:
            return None

    def create_module(self, spec: object) -> None:
        return None

    def exec_module(self, mod: types.ModuleType) -> None:
        mod.V = self._funcs[mod.__name__]()  # type: ignore[attr-defined]


@functools.cache
def _insert_finder() -> _LazyStaticFinder:
    finder = _LazyStaticFinder()
    sys.meta_path.append(finder)
    return finder


def lazy[T](f: Callable[[], T]) -> T:
    name = f'{__name__}___{f.__module__}___{f.__name__}'.replace('.', '__')

    g: dict[str, T] = {}
    exec(f'lazy from {name} import V', g)

    _insert_finder()._funcs[name] = f

    return g['V']
