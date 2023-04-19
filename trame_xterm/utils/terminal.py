import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import logging
import asyncio


def handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:  # pylint: disable=broad-except
        logging.exception("Exception raised by task = %r", task)


class Terminal:
    def __init__(self, cmd, write_fn, reset_fn):
        self._cmd = cmd
        self.fd = None
        self.child_pid = None
        self.write_fn = write_fn
        self.reset_fn = reset_fn
        self._task = None

    def set_size(self, cols, rows):
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def input(self, data):
        if self.fd is not None:
            os.write(self.fd, data.encode())

    async def _monitor_output(self):
        max_read_bytes = 1024 * 20
        while True:
            await asyncio.sleep(0.01)
            if self.fd is not None:
                timeout_sec = 0
                (data_ready, _, _) = select.select([self.fd], [], [], timeout_sec)
                if data_ready:
                    output = os.read(self.fd, max_read_bytes).decode(errors="ignore")
                    self.write_fn(output)

    def start(self):
        if self.child_pid:
            # Do not start it twice
            return

        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            subprocess.run(self._cmd)
        else:
            self.fd = fd
            self.child_pid = child_pid
            self.set_size(50, 50)
            self._task = asyncio.create_task(self._monitor_output())
            self._task.add_done_callback(handle_task_result)
