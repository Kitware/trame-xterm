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
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import xterm


class Shell(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Interactive XTerm")
            self.ui.icon.hide()

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="h-100 pa-0"):
                    xterm.XTerm(
                        ctx_name="xterm",
                        shell=["/bin/zsh"],
                    )

            with self.ui.toolbar as toolbar:
                toolbar.density = "compact"
                v3.VSpacer()
                v3.VDivider(vertical=True)
                v3.VBtn(
                    "Clear",
                    classes="mx-1",
                    variant="flat",
                    click=self.ctx.xterm.clear,
                )
                v3.VBtn(
                    "Reset",
                    classes="mx-1",
                    variant="flat",
                    click=self.ctx.xterm.reset,
                )
                v3.VBtn(
                    "Top",
                    classes="mx-1",
                    variant="flat",
                    click=self.ctx.xterm.scroll_top,
                )
                v3.VBtn(
                    "Bottom",
                    classes="mx-1",
                    variant="flat",
                    click=self.ctx.xterm.scroll_bottom,
                )


def main():
    app = Shell()
    app.server.start()


if __name__ == "__main__":
    main()
