from ddeutil.core import splitter as sp


def test_rsplit():
    assert ["foo", "bar"] == sp.must_rsplit(
        "foo bar", maxsplit=2, mustsplit=False
    )
