from collections.abc import Callable


def lazy[T](f: Callable[[], T]) -> T:
    name = f'{__name__}___{f.__module__}___{id(f):x}'

    g: dict[str, T] = {}
    g['_g'] = {'__builtins__': {'__import__': lambda *a, **k: f()}}  # type: ignore[assignment]  # noqa: E501
    exec(f'V = __lazy_import__({name!r}, globals=_g)', g)

    return g['V']
