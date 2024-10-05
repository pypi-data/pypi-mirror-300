import contextlib
import functools
from pathlib import Path
from typing import Union, TYPE_CHECKING, Tuple, ContextManager, List, Optional

from pyhidra.converters import *  # pylint: disable=wildcard-import, unused-wildcard-import


if TYPE_CHECKING:
    from pyhidra.launcher import PyhidraLauncher
    from ghidra.base.project import GhidraProject
    from ghidra.program.flatapi import FlatProgramAPI
    from ghidra.program.model.lang import CompilerSpec, Language, LanguageService
    from ghidra.program.model.listing import Program


# stub for documentation and typing
# this is mostly to hide the function parameter
def debug_callback(suspend=False, **kwargs):
    """
    Decorator for enabling debugging of functions called from a thread started in Java.
    All parameters are forwarded to `pydevd.settrace`.
    It is recommended to remove this decorator from a function when it is no longer needed.

    :param suspend: The suspend parameter for `pydevd.settrace` (Defaults to False)
    :return: The decorated function
    """


# this is the actual implementation
def _debug_callback(fun=None, *, suspend=False, **pydevd_kwargs):
    if not fun:
        return functools.partial(_debug_callback, suspend=suspend, **pydevd_kwargs)

    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            import pydevd # type: ignore
            pydevd_kwargs["suspend"] = suspend
            pydevd.settrace(**pydevd_kwargs)
        except ImportError:
            # ignored, importing always fails if the pydevd debugger isn't attached
            pass
        return fun(*args, **kwargs)

    return wrapper


debug_callback = _debug_callback


def start(verbose=False) -> "PyhidraLauncher":
    """
    Starts the JVM and loads the Ghidra libraries.
    Full Ghidra initialization is deferred.

    :param verbose: Enable verbose output during JVM startup (Defaults to False)
    :return: The DeferredPhyidraLauncher used to start the JVM
    """
    from pyhidra.launcher import HeadlessPyhidraLauncher
    launcher = HeadlessPyhidraLauncher(verbose=verbose)
    launcher.start()
    return launcher


def started() -> bool:
    """
    Whether the PyhidraLauncher has already started.
    """
    from pyhidra.launcher import PyhidraLauncher
    return PyhidraLauncher.has_launched()


def _get_language(id: str) -> "Language":
    from ghidra.program.util import DefaultLanguageService
    from ghidra.program.model.lang import LanguageID, LanguageNotFoundException
    try:
        service: "LanguageService" = DefaultLanguageService.getLanguageService()
        return service.getLanguage(LanguageID(id))
    except LanguageNotFoundException:
        # suppress the java exception
        pass
    raise ValueError("Invalid Language ID: "+id)


def _get_compiler_spec(lang: "Language", id: str = None) -> "CompilerSpec":
    if id is None:
        return lang.getDefaultCompilerSpec()
    from ghidra.program.model.lang import CompilerSpecID, CompilerSpecNotFoundException
    try:
        return lang.getCompilerSpecByID(CompilerSpecID(id))
    except CompilerSpecNotFoundException:
        # suppress the java exception
        pass
    lang_id = lang.getLanguageID()
    raise ValueError(f"Invalid CompilerSpecID: {id} for Language: {lang_id.toString()}")


def _setup_project(
        binary_path: Union[str, Path],
        project_location: Union[str, Path] = None,
        project_name: str = None,
        language: str = None,
        compiler: str = None,
        loader: Union[str, JClass] = None
) -> Tuple["GhidraProject", "Program"]:
    from ghidra.base.project import GhidraProject
    from java.lang import ClassLoader
    from java.io import IOException
    if binary_path is not None:
        binary_path = Path(binary_path)
    if project_location:
        project_location = Path(project_location)
    else:
        project_location = binary_path.parent
    if not project_name:
        project_name = f"{binary_path.name}_ghidra"
    project_location /= project_name
    project_location.mkdir(exist_ok=True, parents=True)

    if isinstance(loader, str):
        from java.lang import ClassNotFoundException
        try:
            gcl = ClassLoader.getSystemClassLoader()
            loader = JClass(loader, gcl)
        except (TypeError, ClassNotFoundException) as e:
            raise ValueError from e

    if isinstance(loader, JClass):
        from ghidra.app.util.opinion import Loader
        if not Loader.class_.isAssignableFrom(loader):
            raise TypeError(f"{loader} does not implement ghidra.app.util.opinion.Loader")

    # Open/Create project
    program: "Program" = None
    try:
        project = GhidraProject.openProject(project_location, project_name, True)
        if binary_path is not None:
            if project.getRootFolder().getFile(binary_path.name):
                program = project.openProgram("/", binary_path.name, False)
    except IOException:
        project = GhidraProject.createProject(project_location, project_name, False)

    # NOTE: GhidraProject.importProgram behaves differently when a loader is provided
    # loaderClass may not be null so we must use the correct method override

    if binary_path is not None and program is None:
        if language is None:
            if loader is None:
                program = project.importProgram(binary_path)
            else:
                program = project.importProgram(binary_path, loader)
            if program is None:
                raise RuntimeError(f"Ghidra failed to import '{binary_path}'. Try providing a language manually.")
        else:
            lang = _get_language(language)
            comp = _get_compiler_spec(lang, compiler)
            if loader is None:
                program = project.importProgram(binary_path, lang, comp)
            else:
                program = project.importProgram(binary_path, loader, lang, comp)
            if program is None:
                message = f"Ghidra failed to import '{binary_path}'. "
                if compiler:
                    message += f"The provided language/compiler pair ({language} / {compiler}) may be invalid."
                else:
                    message += f"The provided language ({language}) may be invalid."
                raise ValueError(message)
        project.saveAs(program, "/", program.getName(), True)

    return project, program


def _setup_script(project: "GhidraProject", program: "Program"):
    from pyhidra.script import PyGhidraScript
    from ghidra.app.script import GhidraState
    from ghidra.program.util import ProgramLocation
    from ghidra.util.task import TaskMonitor

    from java.io import PrintWriter
    from java.lang import System

    if project is not None:
        project = project.getProject()

    location = None
    if program is not None:
        # create a GhidraState and setup a HeadlessScript with it
        mem = program.getMemory().getLoadedAndInitializedAddressSet()
        if not mem.isEmpty():
            location = ProgramLocation(program, mem.getMinAddress())
    state = GhidraState(None, project, program, location, None, None)
    script = PyGhidraScript()
    script.set(state, TaskMonitor.DUMMY, PrintWriter(System.out))
    return script


def _analyze_program(flat_api, program):
    from ghidra.program.util import GhidraProgramUtilities
    from ghidra.app.script import GhidraScriptUtil
    if GhidraProgramUtilities.shouldAskToAnalyze(program):
        GhidraScriptUtil.acquireBundleHostReference()
        try:
            flat_api.analyzeAll(program)
            if hasattr(GhidraProgramUtilities, "markProgramAnalyzed"):
                GhidraProgramUtilities.markProgramAnalyzed(program)
            else:
                GhidraProgramUtilities.setAnalyzedFlag(program, True)
        finally:
            GhidraScriptUtil.releaseBundleHostReference()


@contextlib.contextmanager
def open_program(
        binary_path: Union[str, Path],
        project_location: Union[str, Path] = None,
        project_name: str = None,
        analyze=True,
        language: str = None,
        compiler: str = None,
        loader: Union[str, JClass] = None
) -> ContextManager["FlatProgramAPI"]: # type: ignore
    """
    Opens given binary path in Ghidra and returns FlatProgramAPI object.

    :param binary_path: Path to binary file, may be None.
    :param project_location: Location of Ghidra project to open/create.
        (Defaults to same directory as binary file)
    :param project_name: Name of Ghidra project to open/create.
        (Defaults to name of binary file suffixed with "_ghidra")
    :param analyze: Whether to run analysis before returning.
    :param language: The LanguageID to use for the program.
        (Defaults to Ghidra's detected LanguageID)
    :param compiler: The CompilerSpecID to use for the program. Requires a provided language.
        (Defaults to the Language's default compiler)
    :param loader: The `ghidra.app.util.opinion.Loader` class to use when importing the program.
        This may be either a Java class or its path. (Defaults to None)
    :return: A Ghidra FlatProgramAPI object.
    :raises ValueError: If the provided language, compiler or loader is invalid.
    :raises TypeError: If the provided loader does not implement `ghidra.app.util.opinion.Loader`.
    """

    from pyhidra.launcher import PyhidraLauncher, HeadlessPyhidraLauncher

    if not PyhidraLauncher.has_launched():
        HeadlessPyhidraLauncher().start()

    from ghidra.app.script import GhidraScriptUtil
    from ghidra.program.flatapi import FlatProgramAPI

    project, program = _setup_project(
        binary_path,
        project_location,
        project_name,
        language,
        compiler,
        loader
    )
    GhidraScriptUtil.acquireBundleHostReference()

    try:
        flat_api = FlatProgramAPI(program)

        if analyze:
            _analyze_program(flat_api, program)

        yield flat_api
    finally:
        GhidraScriptUtil.releaseBundleHostReference()
        project.save(program)
        project.close()


@contextlib.contextmanager
def _flat_api(
        binary_path: Union[str, Path] = None,
        project_location: Union[str, Path] = None,
        project_name: str = None,
        verbose=False,
        analyze=True,
        language: str = None,
        compiler: str = None,
        loader: Union[str, JClass] = None,
        *,
        install_dir: Path = None
):
    """
    Runs a given script on a given binary path.

    :param binary_path: Path to binary file, may be None.
    :param script_path: Path to script to run.
    :param project_location: Location of Ghidra project to open/create.
        (Defaults to same directory as binary file)
    :param project_name: Name of Ghidra project to open/create.
        (Defaults to name of binary file suffixed with "_ghidra")
    :param script_args: Command line arguments to pass to script.
    :param verbose: Enable verbose output during Ghidra initialization.
    :param analyze: Whether to run analysis, if a binary_path is provided, before returning.
    :param language: The LanguageID to use for the program.
        (Defaults to Ghidra's detected LanguageID)
    :param compiler: The CompilerSpecID to use for the program. Requires a provided language.
        (Defaults to the Language's default compiler)
    :param loader: The `ghidra.app.util.opinion.Loader` class to use when importing the program.
        This may be either a Java class or its path. (Defaults to None)
    :param install_dir: The path to the Ghidra installation directory. This parameter is only
        used if Ghidra has not been started yet.
        (Defaults to the GHIDRA_INSTALL_DIR environment variable)
    :raises ValueError: If the provided language, compiler or loader is invalid.
    :raises TypeError: If the provided loader does not implement `ghidra.app.util.opinion.Loader`.
    """
    from pyhidra.launcher import PyhidraLauncher, HeadlessPyhidraLauncher

    if not PyhidraLauncher.has_launched():
        HeadlessPyhidraLauncher(verbose=verbose, install_dir=install_dir).start()

    project, program = None, None
    if binary_path or project_location:
        project, program = _setup_project(
            binary_path,
            project_location,
            project_name,
            language,
            compiler,
            loader
        )

    from ghidra.app.script import GhidraScriptUtil

    # always aquire a bundle reference to avoid a NPE when attempting to run any Java scripts
    GhidraScriptUtil.acquireBundleHostReference()
    try:
        script = _setup_script(project, program)
        if analyze and program is not None:
            _analyze_program(script, program)
        yield script
    finally:
        GhidraScriptUtil.releaseBundleHostReference()
        if project is not None:
            if program is not None:
                project.save(program)
            project.close()


# pylint: disable=too-many-arguments
def run_script(
    binary_path: Optional[Union[str, Path]],
    script_path: Union[str, Path],
    project_location: Union[str, Path] = None,
    project_name: str = None,
    script_args: List[str] = None,
    verbose=False,
    analyze=True,
    lang: str = None,
    compiler: str = None,
    loader: Union[str, JClass] = None,
    *,
    install_dir: Path = None
):
    """
    Runs a given script on a given binary path.

    :param binary_path: Path to binary file, may be None.
    :param script_path: Path to script to run.
    :param project_location: Location of Ghidra project to open/create.
        (Defaults to same directory as binary file if None)
    :param project_name: Name of Ghidra project to open/create.
        (Defaults to name of binary file suffixed with "_ghidra" if None)
    :param script_args: Command line arguments to pass to script.
    :param verbose: Enable verbose output during Ghidra initialization.
    :param analyze: Whether to run analysis, if a binary_path is provided, before running the script.
    :param lang: The LanguageID to use for the program.
        (Defaults to Ghidra's detected LanguageID)
    :param compiler: The CompilerSpecID to use for the program. Requires a provided language.
        (Defaults to the Language's default compiler)
    :param loader: The `ghidra.app.util.opinion.Loader` class to use when importing the program.
        This may be either a Java class or its path. (Defaults to None)
    :param install_dir: The path to the Ghidra installation directory. This parameter is only
        used if Ghidra has not been started yet.
        (Defaults to the GHIDRA_INSTALL_DIR environment variable)
    :raises ValueError: If the provided language, compiler or loader is invalid.
    :raises TypeError: If the provided loader does not implement `ghidra.app.util.opinion.Loader`.
    """
    script_path = str(script_path)
    args = binary_path, project_location, project_name, verbose, analyze, lang, compiler, loader
    with _flat_api(*args, install_dir=install_dir) as script:
        script.run(script_path, script_args)
