# tests/test_init.py

import gajaraj as gj

def test_imports():
    # Test if DataFrame is accessible
    from gajaraj.frame import DataFrame
    assert DataFrame is not None

    # Test if I/O functions are accessible
    assert gj.read_csv is not None
    assert gj.to_csv is not None
    assert gj.read_json is not None
    assert gj.read_excel is not None

    # Test if operations are accessible
    assert gj.group_by is not None
    assert gj.apply is not None
    assert gj.merge is not None
