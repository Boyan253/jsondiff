import jsondiff


def test_no_differences():
    assert list(jsondiff.walk({"a": 1}, {"a": 1})) == []

def test_changed_value():
    diffs = list(jsondiff.walk({"a": 1}, {"a": 2}))
    assert diffs == [("~", "a", 1, 2)]


def test_added_and_removed_keys():
    diffs = list(jsondiff.walk({"a": 1}, {"b": 2}))
    kinds = sorted(d[0] for d in diffs)
    assert kinds == ["+", "-"]

def test_nested_paths_are_dotted():
    diffs = list(jsondiff.walk({"a": {"b": 1}}, {"a": {"b": 2}}))
    assert diffs[0][1] == "a.b"
