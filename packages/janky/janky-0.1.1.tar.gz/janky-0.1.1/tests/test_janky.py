from janky import jank, JankLevel

test_strings = ["Testing String", "Hello World", "abcdefghijklmnopqrstuvwxyz"]


def test_no_jank():
    for string in test_strings:
        assert jank(string, JankLevel.NONE) == string


def test_min_jank():
    for string in test_strings:
        assert len(jank(string, JankLevel.MINIMAL)) == len(string)
        assert jank(string, JankLevel.MINIMAL) != string


def test_jank():
    for string in test_strings:
        assert len(jank(string)) == len(string)
        assert jank(string) != string
