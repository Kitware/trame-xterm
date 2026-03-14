from trame_xterm.widgets.xterm import *  # noqa: F403


def initialize(server):
    from trame_xterm import module

    server.enable_module(module)
