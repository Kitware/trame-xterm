from pathlib import Path

from trame_xterm import __version__

serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {f"__trame_xterm_{__version__}": serve_path}
scripts = [f"__trame_xterm_{__version__}/trame-xterm.umd.js"]
styles = [f"__trame_xterm_{__version__}/style.css"]
vue_use = ["trame_xterm"]
