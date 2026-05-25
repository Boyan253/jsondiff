import jsondiff


def test_no_differences():
    assert list(jsondiff.walk({"a": 1}, {"a": 1})) == []

def test_changed_value():
    diffs = list(jsondiff.walk({"a": 1}, {"a": 2}))
    assert diffs == [("~", "a", 1, 2)]
