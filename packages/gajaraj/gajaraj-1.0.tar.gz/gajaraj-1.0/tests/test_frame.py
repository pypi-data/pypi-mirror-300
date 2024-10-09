# tests/test_frame.py

from gajaraj.frame import DataFrame

def test_select():
    df = DataFrame(["A", "B", "C"], [[1, 2, 3], [4, 5, 6]])
    selected = df.select("A", "C")
    assert selected.columns == ["A", "C"]
    assert selected.data == [[1, 3], [4, 6]]  # Check selected data

def test_fillna():
    df = DataFrame(["A", "B"], [[1, None], [None, 3]])
    filled = df.fillna(0)
    assert filled.data == [[1, 0], [0, 3]]
