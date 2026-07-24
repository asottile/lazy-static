import types

import pytest

import lazy_static
from testing import example


def test_1(capsys):
    assert capsys.readouterr().out == ''
    assert type(example.__dict__['for_test_1']) is types.LazyImportType  # type: ignore[attr-defined]  # noqa: E501

    assert example.for_test_1 == 5

    assert capsys.readouterr().out == 'computing\n'
    assert type(example.__dict__['for_test_1']) is int


def test_importer_defer():
    assert lazy_static._insert_finder().find_spec('does-not-exist', []) is None

    with pytest.raises(ModuleNotFoundError):
        __import__('does-not-exist')
