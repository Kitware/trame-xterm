from termcolor import colored
from trame_client.widgets.core import AbstractElement

from .. import module

__ALL__ = ["XTerm", "colored"]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


# Expose your vue component(s)
class XTerm(HtmlElement):
    _next_id = 0

    def __init__(self, **kwargs):
        XTerm._next_id += 1
        ref_name = f"trame_xterm_{XTerm._next_id}"
        self.__ref = kwargs.get("ref", ref_name)

        super().__init__(
            "x-term",
            **kwargs,
        )
        self._attributes["ref"] = f'ref="{self.__ref}"'
        self._attr_names += [
            ("options", ":options"),
            ("listen", ":listen"),
        ]
        self._event_names += [
            "bell",
            "binary",
            "cursorMove",
            "input",
            "key",
            "lineFeed",
            "render",
            "writeParsed",
            "resize",
            "scroll",
            "selectionChange",
            "titleChange",
        ]

    def blur(self):
        self.server.js_call(self.__ref, "blur")

    def focus(self):
        self.server.js_call(self.__ref, "focus")

    def resize(self, columns, rows):
        self.server.js_call(self.__ref, "resize", columns, rows)

    def register_marker(self, cursor_y_offset):
        self.server.js_call(self.__ref, "registerMarker", cursor_y_offset)

    def clear_selection(self):
        self.server.js_call(self.__ref, "clearSelection")

    def select(self, column, row, length):
        self.server.js_call(self.__ref, "select", column, row, length)

    def select_all(self):
        self.server.js_call(self.__ref, "selectAll")

    def select_lines(self, start, end):
        self.server.js_call(self.__ref, "selectLines", start, end)

    def scroll_lines(self, amount):
        self.server.js_call(self.__ref, "scrollLines", amount)

    def scroll_pages(self, page_count):
        self.server.js_call(self.__ref, "scrollPages", page_count)

    def scroll_top(self):
        self.server.js_call(self.__ref, "scrollToTop")

    def scroll_bottom(self):
        self.server.js_call(self.__ref, "scrollToBottom")

    def scroll_to_line(self, line):
        self.server.js_call(self.__ref, "scrollToLine", line)

    def clear(self):
        self.server.js_call(self.__ref, "clear")

    def write(self, data):
        self.server.js_call(self.__ref, "write", data)

    def writeln(self, data=""):
        self.server.js_call(self.__ref, "writeln", data)

    def write_colored(self, text, color=None, on_color=None, attrs=None):
        self.write(colored(text, color, on_color, attrs))

    def writeln_colored(self, text, color=None, on_color=None, attrs=None):
        self.writeln(colored(text, color, on_color, attrs))

    def paste(self, data):
        self.server.js_call(self.__ref, "paste", data)

    def refresh(self, start, end):
        self.server.js_call(self.__ref, "refresh", start, end)

    def clear_texture_atlas(self):
        self.server.js_call(self.__ref, "clearTextureAtlas")

    def reset(self):
        self.server.js_call(self.__ref, "reset")
