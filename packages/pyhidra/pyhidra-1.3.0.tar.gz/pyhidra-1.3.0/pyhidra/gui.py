import argparse
import io
import os
from pathlib import Path
import platform
import sys
import traceback
from typing import NoReturn
import warnings

import pyhidra


class _GuiOutput(io.StringIO):

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title

    def close(self):
        import tkinter.messagebox
        tkinter.messagebox.showinfo(self.title, self.getvalue())
        super().close()


class _GuiArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, *_):
        sys.exit(status)

    def print_usage(self, file=None):
        if file is None:
            file = _GuiOutput("Usage")
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = _GuiOutput("Help")
        self._print_message(self.format_help(), file)


def _gui_mac() -> NoReturn:
    args = _parse_args()
    install_dir = args.install_dir
    path = Path(sys.base_exec_prefix) / "Resources/Python.app/Contents/MacOS/Python"
    if path.exists():
        # the python launcher app will correctly start the venv if sys.executable is in a venv
        argv = [sys.executable, "-m", "pyhidra", "-g"]
        if install_dir is not None:
            argv += ["--install-dir", str(install_dir)]
        actions = ((os.POSIX_SPAWN_CLOSE, 0), (os.POSIX_SPAWN_CLOSE, 1), (os.POSIX_SPAWN_CLOSE, 2))
        os.posix_spawn(str(path), argv, os.environ, file_actions=actions)
    else:
        print("could not find the Python.app path, launch failed")
    sys.exit(0)


def _parse_args():
    parser = _GuiArgumentParser(prog="pyhidraw")
    parser.add_argument(
        "--install-dir",
        type=Path,
        default=None,
        dest="install_dir",
        metavar="",
        help="Path to Ghidra installation. "\
            "(defaults to the GHIDRA_INSTALL_DIR environment variable)"
    )
    return parser.parse_args()


def _gui_default(install_dir: Path):
    pid = os.fork()
    if pid != 0:
        # original process can exit
        return

    fd = os.open(os.devnull, os.O_RDWR)
    # redirect stdin, stdout and stderr to /dev/null so the jvm can't use the terminal
    # this also prevents errors from attempting to write to a closed sys.stdout #21
    os.dup2(fd, sys.stdin.fileno(), inheritable=False)
    os.dup2(fd, sys.stdout.fileno(), inheritable=False)
    os.dup2(fd, sys.stderr.fileno(), inheritable=False)

    # run the application
    gui(install_dir)


def _gui():
    # this is the entry from the gui script
    # there may or may not be an attached terminal
    # depending on the current operating system

    if platform.system() == "Darwin":
        _gui_mac()

    # This check handles the edge case of having a corrupt Python installation
    # where tkinter can't be imported. Since there may not be an attached
    # terminal, the problem still needs to be reported somehow.
    try:
        import tkinter.messagebox as _
    except ImportError as e:
        if platform.system() == "Windows":
            # there is no console/terminal to report the error
            import ctypes
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, str(e), "Import Error", 0)
            sys.exit(1)
        # report this before detaching from the console or no
        # errors will be reported if they occur
        raise

    try:
        args = _parse_args()
        install_dir = args.install_dir
    except Exception as e:
        import tkinter.messagebox
        msg = "".join(traceback.format_exception(type(e), value=e, tb=e.__traceback__))
        tkinter.messagebox.showerror(type(e), msg)
        sys.exit(1)

    if platform.system() == 'Windows':
        # gui_script works like it is supposed to on windows
        gui(install_dir)
    else:
        _gui_default(install_dir)


def gui(install_dir: Path = None):
    """
    Starts the Ghidra GUI

    :param install_dir: The path to the Ghidra installation directory.
        (Defaults to the GHIDRA_INSTALL_DIR environment variable)
    """
    pyhidra.GuiPyhidraLauncher(install_dir=install_dir).start()


def get_current_interpreter():
    warnings.warn(
        "get_current_interpreter has been moved. Please use pyhidra.get_current_interpreter",
        DeprecationWarning
    )
    return pyhidra.get_current_interpreter()

