def test_import():
    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.xterm import XTerm as a
    from trame_xterm.widgets.xterm import XTerm as b

    assert dir(a) == dir(b)
