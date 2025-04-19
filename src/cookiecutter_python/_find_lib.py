import sys
import typing as t
from importlib import import_module
from os import path
from pathlib import Path


SRC_DIR = Path(__file__).parent.parent.resolve()

__all__ = ['find_lib']

T = t.TypeVar('T')


def find_lib(module: t.Optional[str] = None) -> t.Tuple[str, str]:
    lib_dir: str
    if module is None:  # set path as the dir where the invoking code is
        namespace = sys._getframe(2).f_globals  # caller's globals
        # Set as Lib the directory where the invoker module is located at runtime
        lib_dir = path.dirname(path.realpath(namespace['__file__']))
        dotted_lib_path: str = '.'.join(
            Path(lib_dir).relative_to(SRC_DIR).parts
        )  # pragma: no mutate
        return lib_dir, dotted_lib_path

    # Import input module
    # module_object = import_module(module.replace('/', '.'))
    module_object = import_module(module)  # TODO: read __file__ without importing

    # Set as Lib the directory where the INPUT module is located at runtime
    # if top-level init is at '/site-packages/some_python_package/__init__.py'
    # then distro_path is '/site-packages/some_python_package'
    lib_dir = str(Path(str(module_object.__file__)).parent)
    return lib_dir, module
