from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout

from trame.widgets import vuetify, xterm

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Read-Only XTerm")
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VDivider(vertical=True)
        vuetify.VBtn("Clear", classes="mx-1", click=ctrl.clear)
        vuetify.VBtn("Reset", classes="mx-1", click=ctrl.reset)
        vuetify.VBtn("Top", classes="mx-1", click=ctrl.scroll_top)
        vuetify.VBtn("Bottom", classes="mx-1", click=ctrl.scroll_bottom)

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0"):
            with xterm.XTerm(shell=["/bin/zsh"]) as term:
                ctrl.clear = term.clear
                ctrl.reset = term.reset
                ctrl.scroll_top = term.scroll_top
                ctrl.scroll_bottom = term.scroll_bottom

server.start()
