from vardiff import VarDiff

def test_compare_equal_values():
    comp = VarDiff()
    assert comp.compare(123, 123) == True

def test_compare_different_values():
    comp = VarDiff()
    result = comp.compare(123, 124)
    assert result == '{\n    "match": false,\n    "value_a": 123,\n    "value_b": 124\n}'

def test_compare_lists():
    comp = VarDiff()
    result = comp.compare([1, 2, 3], [1, 2, 4])
    assert "differences" in result

def test_compare_dicts():
    comp = VarDiff()
    result = comp.compare({"a": 1, "b": 2}, {"a": 1, "b": 3})
    assert "differences" in result
