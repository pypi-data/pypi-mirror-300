# tests/test_io.py

import gajaraj as gj

def test_read_csv():
    df = gj.read_csv("sample.csv")
    assert df.columns == ["Column1", "Column2", "Column3"]
    assert len(df.data) > 0

def test_to_csv():
    df = gj.read_csv("sample.csv")
    gj.to_csv(df, "output.csv")
    df_out = gj.read_csv("output.csv")
    assert df_out.data == df.data
