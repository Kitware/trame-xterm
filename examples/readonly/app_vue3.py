import asyncio
import time

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout

from trame.widgets import vuetify3, xterm

server = get_server()
server.client_type = "vue3"
state, ctrl = server.state, server.controller


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


styles = [
    bcolors.OKBLUE,
    bcolors.OKCYAN,
    bcolors.WARNING,
    bcolors.FAIL,
    bcolors.BOLD,
    bcolors.UNDERLINE,
]
style_size = len(styles)


@ctrl.add_task("on_server_ready")
async def print_time(*_, **__):
    style_idx = 0
    while True:
        await asyncio.sleep(0.5)
        style_idx = (style_idx + 1) % style_size
        style = styles[style_idx]
        ctrl.writeln(
            f"{bcolors.OKGREEN} Time is:{bcolors.ENDC} {style}{time.time()}{bcolors.ENDC}"
        )


@ctrl.add("on_client_connected")
def client_connected(*_):
    ctrl.writeln_colored("Welcome to xterm", "red", "on_green", ["bold", "underline"])
    ctrl.write(
        "".join(
            [
                xterm.colored("Red ", "red", "on_blue", ["bold"]),
                xterm.colored("Green ", "green", "on_light_grey", ["underline"]),
            ]
        )
    )
    ctrl.writeln()


with SinglePageLayout(server) as layout:
    layout.title.set_text("Read-Only XTerm")
    with layout.toolbar:
        vuetify3.VSpacer()
        vuetify3.VBtn("Clear", classes="mx-1", click=ctrl.clear)
        vuetify3.VBtn("Reset", classes="mx-1", click=ctrl.reset)
        vuetify3.VBtn("Top", classes="mx-1", click=ctrl.scroll_top)
        vuetify3.VBtn("Bottom", classes="mx-1", click=ctrl.scroll_bottom)

    with layout.content:
        with vuetify3.VContainer(fluid=True, classes="fill-height pa-0"):
            with xterm.XTerm(options="{ disableStdin: 1 }", listen="[]") as term:
                ctrl.clear = term.clear
                ctrl.reset = term.reset
                ctrl.write = term.write
                ctrl.writeln = term.writeln
                ctrl.write_colored = term.write_colored
                ctrl.writeln_colored = term.writeln_colored
                ctrl.scroll_top = term.scroll_top
                ctrl.scroll_bottom = term.scroll_bottom

server.start()
