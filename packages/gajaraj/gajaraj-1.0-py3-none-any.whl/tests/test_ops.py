# tests/test_ops.py

from gajaraj.frame import DataFrame
from gajaraj.ops import group_by

def test_group_by():
    df = DataFrame(["A", "B"], [[1, 2], [1, 3], [2, 4]])
    grouped = group_by(df, "A", lambda x: sum(row[1] for row in x))
    assert grouped.data == [[1, 5], [2, 4]]  # Sum of B for each unique A
