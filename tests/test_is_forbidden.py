from ..py_to_rpy import _is_forbidden


def test_is_forbidden_allowed():
    dummy_line = 'Hello world'

    assert not _is_forbidden(dummy_line)


def test_is_forbidden_forbidden():
    dummy_line = "import renpy.exports as renpy"

    assert _is_forbidden(dummy_line)


def test_is_forbidden_forbidden_whitespace():
    dummy_line = "                   import renpy.exports as renpy"

    assert _is_forbidden(dummy_line)
