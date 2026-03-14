from pathlib import Path

serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {"__trame_xterm": serve_path}
scripts = ["__trame_xterm/trame-xterm.umd.js"]
styles = ["__trame_xterm/style.css"]
vue_use = ["trame_xterm"]
