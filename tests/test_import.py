def test_import():
    from trame_xterm.widgets.xterm import XTerm  # noqa: F401

    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.xterm import XTerm  # noqa: F401,F811
