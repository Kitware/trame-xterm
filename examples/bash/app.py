import asyncio

from trame.app import get_server, asynchronous
from trame.ui.vuetify import SinglePageLayout

from trame.widgets import vuetify, xterm

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

PROC = None


async def create_process():
    global PROC
    PROC = await asyncio.create_subprocess_exec(
        "/bin/bash",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print("Process started", PROC)
    asynchronous.create_task(handle_stdout(PROC))
    asynchronous.create_task(handle_stderr(PROC))

    prepare_for_input()

    # await PROC.wait()
    # print("Process is done...")


async def handle_stdout(process):
    async for data in process.stdout:
        # Adding a '\r' is giving us the right spacing
        data = data.decode("utf-8").replace("\n", "\n\r")
        ctrl.write(data)

    ctrl.writeln()

    prepare_for_input()


async def handle_stderr(process):
    async for data in process.stderr:
        # Adding a '\r' is giving us the right spacing
        data = data.decode("utf-8").replace("\n", "\n\r")
        ctrl.write(data)

    ctrl.writeln()

    prepare_for_input()


async def on_input(data):
    ctrl.write(data)
    if "\r" in data:
        ctrl.writeln()

    data = data.replace("\r", "\n")
    PROC.stdin.write(data.encode("utf-8"))
    await PROC.stdin.drain()


def prepare_for_input():
    ctrl.write(">>> ")


with SinglePageLayout(server) as layout:
    layout.title.set_text("Read-Only XTerm")
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VBtn("Bash", classes="mx-1", click=create_process)
        vuetify.VDivider(vertical=True)
        vuetify.VBtn("Clear", classes="mx-1", click=ctrl.clear)
        vuetify.VBtn("Reset", classes="mx-1", click=ctrl.reset)
        vuetify.VBtn("Top", classes="mx-1", click=ctrl.scroll_top)
        vuetify.VBtn("Bottom", classes="mx-1", click=ctrl.scroll_bottom)

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0"):
            with xterm.XTerm(input=(on_input, "[$event]")) as term:
                ctrl.clear = term.clear
                ctrl.reset = term.reset
                ctrl.write = term.write
                ctrl.writeln = term.writeln
                ctrl.write_colored = term.write_colored
                ctrl.writeln_colored = term.writeln_colored
                ctrl.scroll_top = term.scroll_top
                ctrl.scroll_bottom = term.scroll_bottom

server.start()
