import sys
from importlib import import_module
from inspect import isclass
from os import path
from pathlib import Path
from pkgutil import iter_modules
from typing import List, Optional, Type, TypeVar


SRC_DIR = Path(__file__).parent.parent.resolve()

T = TypeVar('T')


def load(interface: Type[T], module: Optional[str] = None) -> List[Type[T]]:
    """Dynamically import all class objects that implement the given interface.

    The classes (class objects) are discovered and imported in the namespace, by
    searching within each module found inside the input 'dire' (path) directory.

    Each class object is an attribute found in a module's namespace.
    We classify an attribute as a (correct) "class to import", if the following
    python boolean expression evaluates to True:

    isclass(attribute) and issubclass(attribute, interface)

    If 'dire' is not given then we consider the modules that are inside the same
    directory as the one where the module of the invoking code resides.

    Args:
        interface (Type[T]): the type (ie class) that the imported classes
            should 'inherit' (subclass) from
        module (str): module dotted-path containing the modules to inspect. Defaults to the
            same module (directory) as the one where the module of the invoking
            code resides.
    """
    lib_dir: str
    _module: str
    if module is None:  # set path as the dir where the invoking code is
        namespace = sys._getframe(1).f_globals  # caller's globals
        # Set as Lib the directory where the invoker module is located at runtime
        lib_dir = path.dirname(path.realpath(namespace['__file__']))
        relative_path = Path(lib_dir).relative_to(SRC_DIR)

        _module = str(relative_path).replace('\\', '/').replace('/', '.')  # pragma: no mutate
    else:
        # Import input module
        # module_object = import_module(module.replace('/', '.'))
        module_object = import_module(module)

        # Set as Lib the directory where the INPUT module is located at runtime
        lib_dir = str(Path(str(module_object.__file__)).parent)
        # if top-level init is at '/site-packages/some_python_package/__init__.py'
        # then distro_path is '/site-packages/some_python_package'

        _module = module

    if not Path(lib_dir).exists():
        raise FileNotFoundError

    objects = []

    # iterate through the modules inside the LIB directory
    for _, module_name, _ in iter_modules([lib_dir]):
        module_object = import_module(
            '{package}.{module}'.format(package=_module, module=module_name)
        )

        for attribute_name in dir(module_object):
            attribute = getattr(module_object, attribute_name)

            if (
                attribute != interface
                and isclass(attribute)
                and issubclass(attribute, interface)
            ):
                objects.append(attribute)
    return objects
