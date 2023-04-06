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

    await PROC.wait()
    print("Process is done...")


async def handle_stdout(process):
    async for data in process.stdout:
        print("out", data)
        ctrl.write(data)


async def handle_stderr(process):
    async for data in process.stderr:
        print("err", data)


async def on_input(data):
    PROC.stdin.write(bytes(data, "utf-8"))
    await PROC.stdin.drain()


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
