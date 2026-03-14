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
import asyncio
import time

from trame.app import TrameApp
from trame.decorators import life_cycle
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import xterm


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class StyleGenerator:
    STYLES = (
        bcolors.OKBLUE,
        bcolors.OKCYAN,
        bcolors.WARNING,
        bcolors.FAIL,
        bcolors.BOLD,
        bcolors.UNDERLINE,
    )

    def __init__(self):
        self._idx = 0
        self._size = len(self.STYLES)

    def next(self):
        self._idx = (self._idx + 1) % self._size
        return self.STYLES[self._idx]


class OutputWindow(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.styles = StyleGenerator()
        self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Read-Only XTerm")

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="h-100 pa-0"):
                    xterm.XTerm(
                        ctx_name="term",
                        options="{ disableStdin: 1 }",
                        listen="[]",
                    )
            with self.ui.toolbar:
                v3.VSpacer()
                v3.VBtn("Clear", classes="mx-1", click=self.ctx.term.clear)
                v3.VBtn("Reset", classes="mx-1", click=self.ctx.term.reset)
                v3.VBtn("Top", classes="mx-1", click=self.ctx.term.scroll_top)
                v3.VBtn("Bottom", classes="mx-1", click=self.ctx.term.scroll_bottom)

    @life_cycle.server_ready_task
    async def print_time(self, **_):
        while True:
            await asyncio.sleep(0.5)
            self.ctx.term.writeln(
                f"{bcolors.OKGREEN} Time is:{bcolors.ENDC} {self.styles.next()}{time.time()}{bcolors.ENDC}"
            )

    @life_cycle.client_connected
    def client_connected(self, *_):
        self.ctx.term.writeln_colored(
            "Welcome to xterm", "red", "on_green", ["bold", "underline"]
        )
        self.ctx.term.write(
            "".join(
                [
                    xterm.colored("Red ", "red", "on_blue", ["bold"]),
                    xterm.colored("Green ", "green", "on_light_grey", ["underline"]),
                ]
            )
        )
        self.ctx.term.writeln()


def main():
    app = OutputWindow()
    app.server.start()


if __name__ == "__main__":
    main()
