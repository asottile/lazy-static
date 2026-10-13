import types

from testing import example


def test_1(capsys):
    assert capsys.readouterr().out == ''
    assert type(example.__dict__['for_test_1']) is types.LazyImportType  # type: ignore[attr-defined]  # noqa: E501

    assert example.for_test_1 == 5

    assert capsys.readouterr().out == 'computing\n'
    assert type(example.__dict__['for_test_1']) is int


def test_2(capsys):
    assert capsys.readouterr().out == ''
    assert type(example.__dict__['for_test_2']) is types.LazyImportType  # type: ignore[attr-defined]  # noqa: E501

    assert example.for_test_2 == 6

    assert capsys.readouterr().out == 'computing\n'
    assert type(example.__dict__['for_test_2']) is int
