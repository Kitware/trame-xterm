#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
#     "trame-vuetify",
#     "trame-xterm",
# ]
# ///
#
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import client, xterm
from trame.widgets import vuetify3 as v3


class MultiShell(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._term_idx = 0
        self._build_ui()
        self.add_terminal()

    def _build_ui(self):
        self.state.term_names = []
        # Need to register it since its usage is deferred
        xterm.initialize(self.server)

        with SinglePageLayout(self.server) as self.ui:
            with self.ui.toolbar.clear() as toolbar:
                toolbar.density = "compact"
                v3.VSelect(
                    prepend_icon="mdi-console",
                    append_icon="mdi-plus",
                    click_append=self.add_terminal,
                    v_model=("next_shell", "/bin/zsh"),
                    items=(
                        "shells",
                        [
                            {"title": "bash", "value": "/bin/bash"},
                            {"title": "zsh", "value": "/bin/zsh"},
                            {"title": "python3", "value": "/usr/bin/python3"},
                        ],
                    ),
                    density="compact",
                    classes="mx-2",
                    variant="flat",
                    hide_details=True,
                    style="max-width: 205px; margin-left: 10px;",
                )

                v3.VSpacer()
                with v3.VTabs(v_model=("active_term", None)):
                    v3.VTab("{{ name }}", v_for="name, idx in term_names", key="idx")
                v3.VSpacer()
                v3.VSelect(
                    v_model="active_theme",
                    items=("theme_names", xterm.THEME_NAMES),
                    density="compact",
                    variant="flat",
                    hide_details=True,
                    style="max-width: 300px;",
                )
            with self.ui.content:
                with v3.VContainer(fluid=True, classes="fill-height pa-0"):
                    with v3.VTabsWindow(
                        v_model="active_term",
                        classes="h-100",
                        style="width: 100%;",
                    ):
                        with v3.VTabsWindowItem(
                            v_for="name, idx in term_names",
                            key="idx",
                            classes="h-100",
                        ):
                            client.ServerTemplate(name=("name",))

    def add_terminal(self):
        self._term_idx += 1
        new_name = f"{self._term_idx}: {self.state.next_shell.split('/').pop()}"

        self.state.term_names.append(new_name)
        self.state.dirty("term_names")
        self.state.active_term = self._term_idx - 1

        with DivLayout(self.server, template_name=new_name) as ui:
            ui.root.style = "width: 100%; height: 100%;"
            xterm.XTerm(
                shell=[self.state.next_shell],
                theme_name=("active_theme", "Floraverse"),
            )


def main():
    app = MultiShell()
    app.server.start()


if __name__ == "__main__":
    main()
