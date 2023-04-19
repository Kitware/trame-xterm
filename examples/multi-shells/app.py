from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.ui.html import DivLayout

from trame.widgets import vuetify, xterm, client

# Global variable
term_idx = 0

# Trame server + state
server = get_server()
server.client_type = "vue2"
state = server.state

# Need to register it since its usage is deferred
xterm.initialize(server)

# Initial state
state.term_names = []


# Trigger
def add_terminal():
    global term_idx
    term_idx += 1
    new_name = f"{term_idx}: {state.next_shell.split('/').pop()}"

    state.term_names.append(new_name)
    state.dirty("term_names")
    state.active_term = term_idx - 1

    with DivLayout(server, template_name=new_name) as layout:
        layout.root.style = "width: 100%; height: 100%;"
        xterm.XTerm(
            shell=[state.next_shell],
            theme_name=("active_theme", "Floraverse"),
        )


with SinglePageLayout(server) as layout:
    layout.title.hide()

    with layout.icon as icon:
        icon.click = add_terminal
        vuetify.VIcon("mdi-console")

    with layout.toolbar as toolbar:
        toolbar.dense = True
        with vuetify.VTabs(v_model=("active_term", None)):
            vuetify.VTab("{{ name }}", v_for="name, idx in term_names", key="idx")
        vuetify.VSelect(
            v_model="active_theme",
            items=("theme_names", xterm.THEME_NAMES),
            dense=True,
            hide_details=True,
            style="max-width: 150px;",
        )
        vuetify.VSelect(
            v_model=("next_shell", "/bin/zsh"),
            items=(
                "shells",
                [
                    dict(text="bash", value="/bin/bash"),
                    dict(text="zsh", value="/bin/zsh"),
                    dict(text="python3", value="/usr/bin/python3"),
                ],
            ),
            dense=True,
            hide_details=True,
            style="max-width: 150px; margin-left: 10px;",
        )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0"):
            with vuetify.VTabsItems(
                v_model="active_term", classes="fill-height", style="width: 100%;"
            ):
                with vuetify.VTabItem(
                    v_for="name, idx in term_names", key="idx", classes="fill-height"
                ):
                    client.ServerTemplate(name=("name",))

# Run server
add_terminal()
server.start()
