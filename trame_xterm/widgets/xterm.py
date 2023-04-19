import json
from termcolor import colored
from trame_client.widgets.core import AbstractElement
from .. import module

try:
    from ..utils.terminal import Terminal

    TERMINAL_AVAILABLE = True
except ModuleNotFoundError:
    TERMINAL_AVAILABLE = False


__ALL__ = ["XTerm", "colored", "THEME_NAMES"]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


THEME_NAMES = [
    "Night_3024",
    "AdventureTime",
    "Afterglow",
    "AlienBlood",
    "Argonaut",
    "Arthur",
    "AtelierSulphurpool",
    "Atom",
    "Batman",
    "Belafonte_Night",
    "BirdsOfParadise",
    "Blazer",
    "Borland",
    "Bright_Lights",
    "Broadcast",
    "Brogrammer",
    "C64",
    "Chalk",
    "Chalkboard",
    "Ciapre",
    "Cobalt2",
    "Cobalt_Neon",
    "CrayonPonyFish",
    "Dark_Pastel",
    "Darkside",
    "Desert",
    "DimmedMonokai",
    "DotGov",
    "Dracula",
    "Duotone_Dark",
    "ENCOM",
    "Earthsong",
    "Elemental",
    "Elementary",
    "Espresso",
    "Espresso_Libre",
    "Fideloper",
    "FirefoxDev",
    "Firewatch",
    "FishTank",
    "Flat",
    "Flatland",
    "Floraverse",
    "ForestBlue",
    "FrontEndDelight",
    "FunForrest",
    "Galaxy",
    "Github",
    "Glacier",
    "Grape",
    "Grass",
    "Gruvbox_Dark",
    "Hardcore",
    "Harper",
    "Highway",
    "Hipster_Green",
    "Homebrew",
    "Hurtado",
    "Hybrid",
    "IC_Green_PPL",
    "IC_Orange_PPL",
    "IR_Black",
    "Jackie_Brown",
    "Japanesque",
    "Jellybeans",
    "JetBrains_Darcula",
    "Kibble",
    "Later_This_Evening",
    "Lavandula",
    "LiquidCarbon",
    "LiquidCarbonTransparent",
    "LiquidCarbonTransparentInverse",
    "Man_Page",
    "Material",
    "MaterialDark",
    "Mathias",
    "Medallion",
    "Misterioso",
    "Molokai",
    "MonaLisa",
    "Monokai_Soda",
    "Monokai_Vivid",
    "N0tch2k",
    "Neopolitan",
    "Neutron",
    "NightLion_v1",
    "NightLion_v2",
    "Novel",
    "Obsidian",
    "Ocean",
    "OceanicMaterial",
    "Ollie",
    "OneHalfDark",
    "OneHalfLight",
    "Pandora",
    "Paraiso_Dark",
    "Parasio_Dark",
    "PaulMillr",
    "PencilDark",
    "PencilLight",
    "Piatto_Light",
    "Pnevma",
    "Pro",
    "Red_Alert",
    "Red_Sands",
    "Rippedcasts",
    "Royal",
    "Ryuuko",
    "SeaShells",
    "Seafoam_Pastel",
    "Seti",
    "Shaman",
    "Slate",
    "Smyck",
    "SoftServer",
    "Solarized_Darcula",
    "Solarized_Dark",
    "Solarized_Dark_Patched",
    "Solarized_Dark_Higher_Contrast",
    "Solarized_Light",
    "SpaceGray",
    "SpaceGray_Eighties",
    "SpaceGray_Eighties_Dull",
    "Spacedust",
    "Spiderman",
    "Spring",
    "Square",
    "Sundried",
    "Symfonic",
    "Teerb",
    "Terminal_Basic",
    "Thayer_Bright",
    "The_Hulk",
    "Tomorrow",
    "Tomorrow_Night",
    "Tomorrow_Night_Blue",
    "Tomorrow_Night_Bright",
    "Tomorrow_Night_Eighties",
    "ToyChest",
    "Treehouse",
    "Ubuntu",
    "UnderTheSea",
    "Urple",
    "Vaughn",
    "VibrantInk",
    "Violet_Dark",
    "Violet_Light",
    "WarmNeon",
    "Wez",
    "WildCherry",
    "Wombat",
    "Wryan",
    "Zenburn",
    "ayu",
    "deep",
    "idleToes",
]


# Expose your vue component(s)
class XTerm(HtmlElement):
    _next_id = 0

    def __init__(self, shell=None, **kwargs):
        """
        Create an XTerm element

        Argument:

        :param shell: Shell command as an array (i.e. shell=['/bin/bash']). This is not available on Windows.

        Properties:

        :param options: XTerm.js option which are only read at creation. (http://xtermjs.org/docs/api/terminal/interfaces/iterminaloptions/ and http://xtermjs.org/docs/api/terminal/interfaces/iterminalinitonlyoptions/)
        :param listen: Specifies the list of event you aim to listen to. [bell, binary, cursorMove, input, key, lineFeed, render, writeParsed, resize, scroll, selectionChange, titleChange]
        :param theme_name: Name of theme to use. (See THEME_NAMES for the choices)

        Events:

        :param opened: Event trigger when the client side widget is ready.
        :param disposed: Event trigger when the client side widget get removed.
        :param input: Triggered for every user input with content as utf-8 string (onData from xterm.js)
        :param binary: Same as input but using binary rather than string (onBinary from xterm.js)
        :param bell: onBell from xterm.js
        :param cursorMove: onCursorMove from xterm.js
        :param key: onKey from xterm.js
        :param lineFeed: onLineFeed from xterm.js
        :param render: onRender from xterm.js
        :param writeParsed: onWriteParsed from xterm.js
        :param resize: onResize from xterm.js
        :param scroll: onScroll from xterm.js
        :param selectionChange: onSelectionChange from xterm.js
        :param titleChange: onTitleChange from xterm.js

        >>> w = xterm.XTerm(
        ...   options="{ disableStdin: 0 }",
        ...   listen="['input', 'resize']",
        ...   input=(on_input, "[$event]"),
        ...   resize=(on_resize, "[$event]"),
        ... )
        """
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
            ("theme_name", "themeName"),
        ]
        self._event_names += [
            "opened",
            "disposed",
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

        if shell is not None:
            if not TERMINAL_AVAILABLE:
                raise NotImplementedError(
                    "The shell argument is not implemented for Windows"
                )

            self._terminal = Terminal(shell, self.write, self.reset)
            if self.listen is None:
                self.listen = "['input', 'resize']"
            else:
                array = json.loads(self.listen)
                if "input" not in array:
                    array.append("input")
                if "resize" not in array:
                    array.append("resize")
                self.listen = json.dumps(array)

            self.resize = (self._terminal.set_size, "[]", "$event")
            self.input = (self._terminal.input, "[$event]")
            self.opened = self._terminal.start

    def fit(self):
        """Trigger a fit on the available space"""
        self.server.js_call(self.__ref, "fit")

    def use_theme(self, name):
        """Update the theme using a name from THEME_NAMES"""
        self.server.js_call(self.__ref, "updateTheme", name)

    def blur(self):
        """Trigger a blur on the xterm.js widget"""
        self.server.js_call(self.__ref, "blur")

    def focus(self):
        """Trigger a focus on the xterm.js widget"""
        self.server.js_call(self.__ref, "focus")

    def resize(self, columns, rows):
        """
        Trigger a resize on the xterm.js widget

        :param columns: Number of columns
        :param rows: Number of rows
        """
        self.server.js_call(self.__ref, "resize", columns, rows)

    def register_marker(self, cursor_y_offset):
        """
        Trigger a registerMarker on the xterm.js widget

        :param cursor_y_offset: Number lines
        """
        self.server.js_call(self.__ref, "registerMarker", cursor_y_offset)

    def clear_selection(self):
        """Trigger a clearSelection on the xterm.js widget"""
        self.server.js_call(self.__ref, "clearSelection")

    def select(self, column, row, length):
        """
        Trigger a select on the xterm.js widget

        :param column: Start column number
        :param row: Start row/line number
        :param length: Number of char to select
        """
        self.server.js_call(self.__ref, "select", column, row, length)

    def select_all(self):
        """Trigger a selectAll on the xterm.js widget"""
        self.server.js_call(self.__ref, "selectAll")

    def select_lines(self, start, end):
        """
        Trigger a selectLines on the xterm.js widget

        :param start: First line to select
        :param end: Last line to select
        """
        self.server.js_call(self.__ref, "selectLines", start, end)

    def scroll_lines(self, amount):
        """
        Trigger a scrollLines on the xterm.js widget

        :param amount: Jump the amount of lines
        """
        self.server.js_call(self.__ref, "scrollLines", amount)

    def scroll_pages(self, page_count):
        """
        Trigger a scrollPages on the xterm.js widget

        :param page_count: Scroll the number of page provided
        """
        self.server.js_call(self.__ref, "scrollPages", page_count)

    def scroll_top(self):
        """Trigger a scrollToTop on the xterm.js widget"""
        self.server.js_call(self.__ref, "scrollToTop")

    def scroll_bottom(self):
        """Trigger a scrollToBottom on the xterm.js widget"""
        self.server.js_call(self.__ref, "scrollToBottom")

    def scroll_to_line(self, line):
        """
        Trigger a scrollToLine on the xterm.js widget

        :param line: Line number to scroll to
        """
        self.server.js_call(self.__ref, "scrollToLine", line)

    def clear(self):
        """Trigger a clear on the xterm.js widget"""
        self.server.js_call(self.__ref, "clear")

    def write(self, data):
        """
        Trigger a write on the xterm.js widget

        :param data: UTF-8 encoded string
        """
        self.server.js_call(self.__ref, "write", data)

    def writeln(self, data=""):
        """
        Trigger a writeln on the xterm.js widget

        :param data: UTF-8 encoded string
        """
        self.server.js_call(self.__ref, "writeln", data)

    def write_colored(self, text, color=None, on_color=None, attrs=None):
        """
        Trigger a write on the xterm.js widget using the colored Python library

        :param text: Text to color
        :param color: Foreground color (black, red, green, yellow, blue, magenta, cyan, light_gray, dark_gray, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, grey_0, navy_blue, dark_blue, blue_3a, blue_3b, blue_1, dark_green, deep_sky_blue_4a, deep_sky_blue_4b, deep_sky_blue_4c, dodger_blue_3, dodger_blue_2, green_4, spring_green_4, turquoise_4, deep_sky_blue_3a, deep_sky_blue_3b, dodger_blue_1, green_3a, spring_green_3a, dark_cyan, light_sea_green, deep_sky_blue_2, deep_sky_blue_1, green_3b, spring_green_3b, spring_green_2a, cyan_3, dark_turquoise, turquoise_2, green_1, spring_green_2b, spring_green_1, medium_spring_green, cyan_2, cyan_1, dark_red_1, deep_pink_4a, purple_4a, purple_4b, purple_3, blue_violet, orange_4a, grey_37, medium_purple_4, slate_blue_3a, slate_blue_3b, royal_blue_1, chartreuse_4, dark_sea_green_4a, pale_turquoise_4, steel_blue, steel_blue_3, cornflower_blue, chartreuse_3a, dark_sea_green_4b, cadet_blue_2, cadet_blue_1, sky_blue_3, steel_blue_1a, chartreuse_3b, pale_green_3a, sea_green_3, aquamarine_3, medium_turquoise, steel_blue_1b, chartreuse_2a, sea_green_2, sea_green_1a, sea_green_1b, aquamarine_1a, dark_slate_gray_2, dark_red_2, deep_pink_4b, dark_magenta_1, dark_magenta_2, dark_violet_1a, purple_1a, orange_4b, light_pink_4, plum_4, medium_purple_3a, medium_purple_3b, slate_blue_1, yellow_4a, wheat_4, grey_53, light_slate_grey, medium_purple, light_slate_blue, yellow_4b, dark_olive_green_3a, dark_green_sea, light_sky_blue_3a, light_sky_blue_3b, sky_blue_2, chartreuse_2b, dark_olive_green_3b, pale_green_3b, dark_sea_green_3a, dark_slate_gray_3, sky_blue_1, chartreuse_1, light_green_2, light_green_3, pale_green_1a, aquamarine_1b, dark_slate_gray_1, red_3a, deep_pink_4c, medium_violet_red, magenta_3a, dark_violet_1b, purple_1b, dark_orange_3a, indian_red_1a, hot_pink_3a, medium_orchid_3, medium_orchid, medium_purple_2a, dark_goldenrod, light_salmon_3a, rosy_brown, grey_63, medium_purple_2b, medium_purple_1, gold_3a, dark_khaki, navajo_white_3, grey_69, light_steel_blue_3, light_steel_blue, yellow_3a, dark_olive_green_3, dark_sea_green_3b, dark_sea_green_2, light_cyan_3, light_sky_blue_1, green_yellow, dark_olive_green_2, pale_green_1b, dark_sea_green_5b, dark_sea_green_5a, pale_turquoise_1, red_3b, deep_pink_3a, deep_pink_3b, magenta_3b, magenta_3c, magenta_2a, dark_orange_3b, indian_red_1b, hot_pink_3b, hot_pink_2, orchid, medium_orchid_1a, orange_3, light_salmon_3b, light_pink_3, pink_3, plum_3, violet, gold_3b, light_goldenrod_3, tan, misty_rose_3, thistle_3, plum_2, yellow_3b, khaki_3, light_goldenrod_2a, light_yellow_3, grey_84, light_steel_blue_1, yellow_2, dark_olive_green_1a, dark_olive_green_1b, dark_sea_green_1, honeydew_2, light_cyan_1, red_1, deep_pink_2, deep_pink_1a, deep_pink_1b, magenta_2b, magenta_1, orange_red_1, indian_red_1c, indian_red_1d, hot_pink_1a, hot_pink_1b, medium_orchid_1b, dark_orange, salmon_1, light_coral, pale_violet_red_1, orchid_2, orchid_1, orange_1, sandy_brown, light_salmon_1, light_pink_1, pink_1, plum_1, gold_1, light_goldenrod_2b, light_goldenrod_2c, navajo_white_1, misty_rose1, thistle_1, yellow_1, light_goldenrod_1, khaki_1, wheat_1, cornsilk_1, grey_100, grey_3, grey_7, grey_11, grey_15, grey_19, grey_23, grey_27, grey_30, grey_35, grey_39, grey_42, grey_46, grey_50, grey_54, grey_58, grey_62, grey_66, grey_70, grey_74, grey_78, grey_82, grey_85, grey_89, grey_93, default)
        :param on_color: Background color same as Foreground with "on_" as prefix
        :param attrs: List of attributes (bold, dim, underlined, blink, reverse, hidden, reset, res_bold, res_dim, res_underlined, res_blink, res_reverse, res_hidden)
        """
        self.write(colored(text, color, on_color, attrs))

    def writeln_colored(self, text, color=None, on_color=None, attrs=None):
        """
        Trigger a writeln on the xterm.js widget using the colored Python library

        :param text: Text to color
        :param color: Foreground color (black, red, green, yellow, blue, magenta, cyan, light_gray, dark_gray, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, grey_0, navy_blue, dark_blue, blue_3a, blue_3b, blue_1, dark_green, deep_sky_blue_4a, deep_sky_blue_4b, deep_sky_blue_4c, dodger_blue_3, dodger_blue_2, green_4, spring_green_4, turquoise_4, deep_sky_blue_3a, deep_sky_blue_3b, dodger_blue_1, green_3a, spring_green_3a, dark_cyan, light_sea_green, deep_sky_blue_2, deep_sky_blue_1, green_3b, spring_green_3b, spring_green_2a, cyan_3, dark_turquoise, turquoise_2, green_1, spring_green_2b, spring_green_1, medium_spring_green, cyan_2, cyan_1, dark_red_1, deep_pink_4a, purple_4a, purple_4b, purple_3, blue_violet, orange_4a, grey_37, medium_purple_4, slate_blue_3a, slate_blue_3b, royal_blue_1, chartreuse_4, dark_sea_green_4a, pale_turquoise_4, steel_blue, steel_blue_3, cornflower_blue, chartreuse_3a, dark_sea_green_4b, cadet_blue_2, cadet_blue_1, sky_blue_3, steel_blue_1a, chartreuse_3b, pale_green_3a, sea_green_3, aquamarine_3, medium_turquoise, steel_blue_1b, chartreuse_2a, sea_green_2, sea_green_1a, sea_green_1b, aquamarine_1a, dark_slate_gray_2, dark_red_2, deep_pink_4b, dark_magenta_1, dark_magenta_2, dark_violet_1a, purple_1a, orange_4b, light_pink_4, plum_4, medium_purple_3a, medium_purple_3b, slate_blue_1, yellow_4a, wheat_4, grey_53, light_slate_grey, medium_purple, light_slate_blue, yellow_4b, dark_olive_green_3a, dark_green_sea, light_sky_blue_3a, light_sky_blue_3b, sky_blue_2, chartreuse_2b, dark_olive_green_3b, pale_green_3b, dark_sea_green_3a, dark_slate_gray_3, sky_blue_1, chartreuse_1, light_green_2, light_green_3, pale_green_1a, aquamarine_1b, dark_slate_gray_1, red_3a, deep_pink_4c, medium_violet_red, magenta_3a, dark_violet_1b, purple_1b, dark_orange_3a, indian_red_1a, hot_pink_3a, medium_orchid_3, medium_orchid, medium_purple_2a, dark_goldenrod, light_salmon_3a, rosy_brown, grey_63, medium_purple_2b, medium_purple_1, gold_3a, dark_khaki, navajo_white_3, grey_69, light_steel_blue_3, light_steel_blue, yellow_3a, dark_olive_green_3, dark_sea_green_3b, dark_sea_green_2, light_cyan_3, light_sky_blue_1, green_yellow, dark_olive_green_2, pale_green_1b, dark_sea_green_5b, dark_sea_green_5a, pale_turquoise_1, red_3b, deep_pink_3a, deep_pink_3b, magenta_3b, magenta_3c, magenta_2a, dark_orange_3b, indian_red_1b, hot_pink_3b, hot_pink_2, orchid, medium_orchid_1a, orange_3, light_salmon_3b, light_pink_3, pink_3, plum_3, violet, gold_3b, light_goldenrod_3, tan, misty_rose_3, thistle_3, plum_2, yellow_3b, khaki_3, light_goldenrod_2a, light_yellow_3, grey_84, light_steel_blue_1, yellow_2, dark_olive_green_1a, dark_olive_green_1b, dark_sea_green_1, honeydew_2, light_cyan_1, red_1, deep_pink_2, deep_pink_1a, deep_pink_1b, magenta_2b, magenta_1, orange_red_1, indian_red_1c, indian_red_1d, hot_pink_1a, hot_pink_1b, medium_orchid_1b, dark_orange, salmon_1, light_coral, pale_violet_red_1, orchid_2, orchid_1, orange_1, sandy_brown, light_salmon_1, light_pink_1, pink_1, plum_1, gold_1, light_goldenrod_2b, light_goldenrod_2c, navajo_white_1, misty_rose1, thistle_1, yellow_1, light_goldenrod_1, khaki_1, wheat_1, cornsilk_1, grey_100, grey_3, grey_7, grey_11, grey_15, grey_19, grey_23, grey_27, grey_30, grey_35, grey_39, grey_42, grey_46, grey_50, grey_54, grey_58, grey_62, grey_66, grey_70, grey_74, grey_78, grey_82, grey_85, grey_89, grey_93, default)
        :param on_color: Background color same as Foreground with "on_" as prefix
        :param attrs: List of attributes (bold, dim, underlined, blink, reverse, hidden, reset, res_bold, res_dim, res_underlined, res_blink, res_reverse, res_hidden)
        """
        self.writeln(colored(text, color, on_color, attrs))

    def paste(self, data):
        """
        Trigger a paste on the xterm.js widget

        :param data: UTF-8 encoded string
        """
        self.server.js_call(self.__ref, "paste", data)

    def refresh(self, start, end):
        """
        Trigger a refresh on the xterm.js widget

        :param start: Start line
        :param end: End line
        """
        self.server.js_call(self.__ref, "refresh", start, end)

    def clear_texture_atlas(self):
        """Trigger a clear_texture_atlas on the xterm.js widget"""
        self.server.js_call(self.__ref, "clearTextureAtlas")

    def reset(self):
        """Trigger a reset on the xterm.js widget"""
        self.server.js_call(self.__ref, "reset")
