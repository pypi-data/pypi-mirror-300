import functools
import importlib
import importlib.util
import inspect
import logging
import sys
import traceback
from collections.abc import ItemsView, KeysView
from importlib.machinery import ModuleSpec, SourceFileLoader
from pathlib import Path
from jpype import JClass, JImplementationFor
from typing import List


from .core import debug_callback

_NO_ATTRIBUTE = object()

_headless_interpreter = None


class _StaticMap(dict):
    # this is a special view of the PyGhidraScript for use with rlcompleter

    __slots__ = ('script',)

    def __init__(self, script: "PyGhidraScript"):
        super().__init__()
        self.script = script

    def __getitem__(self, key):
        res = self.get(key, _NO_ATTRIBUTE)
        if res is not _NO_ATTRIBUTE:
            if isinstance(res, property):
                # rlcompleter is attempting to use a property getter on the interpreter script
                # allow the property magic to take place
                # this is necessary for completions on currentAddress, currentProgram, etc.
                try:
                    return getattr(self.script, key)
                except AttributeError:
                    return res
            return res
        raise KeyError(key)

    def get(self, key, default=None):
        res = self.script.get_static(key)
        return res if res is not _NO_ATTRIBUTE else default

    def __iter__(self):
        yield from self.script

    def keys(self):
        return KeysView(self)

    def items(self):
        return ItemsView(self)


class _JavaProperty(property):

    def __init__(self, field):
        super().__init__()
        self._field = field

    def __get__(self, obj, cls):
        return self._field.fget(obj)

    def __set__(self, obj, value):
        self._field.fset(obj, value)


#pylint: disable=too-few-public-methods
@JImplementationFor("dc3.pyhidra.plugin.PythonFieldExposer")
class _PythonFieldExposer:

    #pylint: disable=no-member
    def __jclass_init__(self):
        exposer = JClass("dc3.pyhidra.plugin.PythonFieldExposer")
        if self.class_ == exposer:
            return
        try:
            for k, v in exposer.getProperties(self.class_).items():
                self._customize(k, _JavaProperty(v))
        # allowing any exception to escape here may cause the jvm to terminate
        # pylint: disable=bare-except
        except:
            logger = logging.getLogger(__name__)
            logger.error("Failed to add property customizations for %s", self, exc_info=1)


class _GhidraScriptModule:

    def __init__(self, spec: ModuleSpec):
        super().__setattr__("__dict__", spec.loader_state["script"])

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise AttributeError(f"readonly attribute {attr}")
        super().__setattr__(attr, value)


class _GhidraScriptLoader(SourceFileLoader):

    def __init__(self, script: "PyGhidraScript", spec: ModuleSpec):
        super().__init__(spec.name, spec.origin)
        spec.loader_state = {"script": script}

    def create_module(self, spec: ModuleSpec):
        return _GhidraScriptModule(spec)

    # this will make debugging "just work" if a debugger attaches to the process
    @debug_callback
    def exec_module(self, module):
        return super().exec_module(module)


def _build_script_print(stdout):
    @functools.wraps(print)
    def wrapper(*objects, sep=' ', end='\n', file=None, flush=False):
        # ensure we get the same behavior if the file is closed
        if file is None:
            file = stdout
            # since write will be used, it won't flush on a line ending
            # force it for stdout in a GhidraScript
            flush = flush or end == '\n'
        return print(*objects, sep=sep, end=end, file=file, flush=flush)
    return wrapper


def _has_runtime_metadata(script_path: str) -> bool:
    """
    Checks if this script has the @runtime PyGhidra metadata
    """
    # ScriptInfo doesn't provide a way to obtain all the raw metadata
    # so we have to get it ourselves
    in_block_comment = False
    with open(script_path) as fp:
        for line in fp:
            # this doesn't need to be perfect
            if line.startswith(('"""', "'''")):
                in_block_comment = not in_block_comment
            elif line.startswith('#'):
                if "@runtime PyGhidra" in line:
                    return True
            elif not in_block_comment:
                return False


# pylint: disable=missing-function-docstring
class PyGhidraScript(dict):
    """
    Python GhidraScript Wrapper
    """

    def __init__(self, jobj=None):
        super().__init__()
        if jobj is None:
            jobj = JClass("dc3.pyhidra.plugin.PyScriptProvider").PyhidraHeadlessScript()
        self._script = jobj

        global _headless_interpreter

        from ghidra.util import SystemUtilities

        if SystemUtilities.isInHeadlessMode() and _headless_interpreter is None:
            _headless_interpreter = jobj

        # ensure the builtin set takes precedence over GhidraScript.set
        super().__setitem__("set", set)

        super().__setitem__("__this__", self._script)

        # this is injected since Ghidra commit e66e72577ded1aeae53bcc3f361dfce1ecf6e24a
        super().__setitem__("this", self._script)

        # overwrite the builtin print so it will always work
        # the global redirection of stdout/stderr works on a best-effort basis
        printer = _build_script_print(self._script.writer)
        super().__setitem__("print", printer)

    def __missing__(self, k):
        attr = getattr(self._script, k, _NO_ATTRIBUTE)
        if attr is not _NO_ATTRIBUTE:
            return attr
        raise KeyError(k)

    def __getattr__(self, item):
        return getattr(self._script, item)

    def __setitem__(self, k, v):
        attr = inspect.getattr_static(self._script, k, _NO_ATTRIBUTE)
        if attr is not _NO_ATTRIBUTE and isinstance(attr, property):
            setattr(self._script, k, v)
        else:
            super().__setitem__(k, v)

    def __iter__(self):
        yield from super().__iter__()
        yield from dir(self._script)

    def get_static(self, key):
        res = self.get(key, _NO_ATTRIBUTE)
        if res is not _NO_ATTRIBUTE:
            return res
        return inspect.getattr_static(self._script, key, _NO_ATTRIBUTE)

    def get_static_view(self):
        return _StaticMap(self)

    def set(self, state, monitor, writer):
        """
        see GhidraScript.set
        """
        self._script.set(state, monitor, writer)

    def run(self, script_path: str = None, script_args: List[str] = None):
        """
        Run this GhidraScript

        :param script_path: The path of the python script
        :param script_args: The arguments for the python script
        """
        sf = self._script.getSourceFile()
        if sf is None and script_path is None:
            return
        if script_path is None:
            script_path = sf.getAbsolutePath()
            script_args = self._script.getScriptArgs()

        if script_args is None:
            script_args = []
        else:
            self._script.setScriptArgs(script_args)

        orig_argv = sys.argv
        script_root = str(Path(script_path).parent)

        if not _has_runtime_metadata(script_path):
            # emit a friendly yet annoying warning about the behavior
            # change coming in PyGhidra
            msg = "PyGhidra will not be Ghidra's default Python script runtime.\n" + \
                  "This script will be executed by Jython without the @runtime metadata.\n" + \
                  "To suppress this warning, add \"# @runtime PyGhidra\" " + \
                  "to the start of your script."
            self._script.printerr(msg)

        # honor the python safe_path flag introduced in 3.11
        safe_path = bool(getattr(sys.flags, "safe_path", 0))
        try:
            # Temporarily set command line arguments.
            sys.argv = [script_path] + list(script_args)

            if not safe_path:
                # add the directory containing the script to the start of the path
                # this provides the same import behavior as if the script was run normally
                sys.path.insert(0, script_root)

            spec = importlib.util.spec_from_file_location('__main__', script_path)
            spec.loader = _GhidraScriptLoader(self, spec)
            m = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(m)
            # pylint: disable=bare-except
            except:
                # filter the traceback so that it stops at the script
                exc_type, exc_value, exc_tb = sys.exc_info()
                i = 0
                tb = traceback.extract_tb(exc_tb)
                for fs in tb:
                    if fs.filename == script_path:
                        break
                    i += 1
                ss = traceback.StackSummary.from_list(tb[i:])
                e = traceback.TracebackException(exc_type, exc_value, exc_tb)
                e.stack = ss
                self._script.printerr(''.join(e.format()))
        finally:
            sys.argv = orig_argv

            if not safe_path:
                sys.path.remove(script_root)


def get_current_interpreter():
    """
    Gets the underlying GhidraScript for the focused Pyhidra InteractiveConsole.
    This will always return None unless it is being access from a function
    called from within the interactive console.

    :return: The GhidraScript for the active interactive console.
    """

    try:
        from ghidra.util import SystemUtilities
        from ghidra.framework.main import AppInfo

        global _headless_interpreter

        if SystemUtilities.isInHeadlessMode():
            if _headless_interpreter is None:
                # one hasn't been created yet so make one now
                PyScriptProvider = JClass("dc3.pyhidra.plugin.PyScriptProvider")
                _headless_interpreter = PyScriptProvider.PyhidraHeadlessScript()
            return _headless_interpreter

        project = AppInfo.getActiveProject()
        if project is None:
            return None

        ts = project.getToolServices()
        tool = None
        for t in ts.getRunningTools():
            if t.getActiveWindow().isFocused():
                tool = t
                break

        if tool is None:
            return None

        for plugin in tool.getManagedPlugins():
            if plugin.name == 'PyhidraPlugin':
                return plugin.script

    except ImportError:
        return None
