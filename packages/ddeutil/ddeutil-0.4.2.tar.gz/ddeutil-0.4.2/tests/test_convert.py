import pytest
from ddeutil.core import convert as cc


def test_str2bool():
    assert not cc.str2bool()

    for _string in ["true", "True", "1", "Y", "y", "yes", "Yes", "o", "O"]:
        assert cc.str2bool(_string)

    for _string in ["false", "False", "0", "N", "n", "no", "No", "x", "X"]:
        assert not cc.str2bool(_string)

    assert not cc.str2bool("Nop", force_raise=False)


def test_str2bool_raise():
    with pytest.raises(ValueError):
        cc.str2bool("Nop")


def test_str2list():
    assert cc.str2list() == []
    assert cc.str2list('["a", "b", "c"]') == ["a", "b", "c"]
    assert cc.str2list('["d""]', force_raise=False) == ['["d""]']
    assert cc.str2list('"d""]', force_raise=False) == ['"d""]']

    with pytest.raises(ValueError):
        cc.str2list('["d""]')

    with pytest.raises(ValueError):
        cc.str2list('"d""]')


def test_str2dict():
    assert cc.str2dict() == {}
    assert cc.str2dict('{"a": 1, "b": 2, "c": 3}') == {"a": 1, "b": 2, "c": 3}
    assert cc.str2dict('{"d""', force_raise=False) == {0: '{"d""'}
    assert cc.str2dict('{"d"}', force_raise=False) == {0: '{"d"}'}

    with pytest.raises(ValueError):
        cc.str2dict('{"d""')

    with pytest.raises(ValueError):
        cc.str2dict('{"d"}')


def test_str2int_float():
    assert cc.str2int_float() == 0
    assert cc.str2int_float("+3") == 3
    assert cc.str2int_float("-5.00") == -5.0
    assert cc.str2int_float("-3.01") == -3.01
    assert cc.str2int_float("[1]") == "[1]"
    assert cc.str2int_float("x0", force_raise=False) == "x0"

    with pytest.raises(ValueError):
        cc.str2int_float("x0", force_raise=True)


def test_must_list():
    assert cc.must_list("[1, 2, 3]") == [1, 2, 3]
    assert cc.must_list() == []
    assert cc.must_list([1, "foo"]) == [1, "foo"]


def test_must_bool():
    assert cc.must_bool("1")
    assert not cc.must_bool(0)
    assert not cc.must_bool("[1, 2, 'foo']")
    assert not cc.must_bool(None)


def test_str2any():
    assert cc.str2any(22) == 22
    assert cc.str2any("1245") == 1245
    assert cc.str2any('"string"') == "string"
    assert cc.str2any("[1, 2, 3]") == [1, 2, 3]
    assert cc.str2any('{"key": "value"}') == {"key": "value"}
    assert cc.str2any("1245.123") == 1245.123
    assert cc.str2any("True")
    assert cc.str2any("[1, 2") == "[1, 2"
    assert cc.str2any("1.232.1") == "1.232.1"


def test_revert_args():
    assert cc.revert_args(
        "value", 1, name="demo", _dict={"k1": "v1", "k2": "v2"}
    ) == (("value", 1), {"name": "demo", "_dict": {"k1": "v1", "k2": "v2"}})
    assert cc.revert_args(1, 2, 3) == ((1, 2, 3), {})
    assert cc.revert_args(foo="bar") == ((), {"foo": "bar"})


def test_str2args():
    assert cc.str2args("'value', 1, name='demo'") == (
        ("value", 1),
        {"name": "demo"},
    )
    assert cc.str2args("'value', 1, '[1, 3, \"foo\"]'") == (
        ("value", 1, '[1, 3, "foo"]'),
        {},
    )
