import typing as t
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from ._find_lib import find_lib


T = t.TypeVar('T')


def load(interface: t.Type[T], module: t.Optional[str] = None) -> t.List[t.Type[T]]:
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
    dotted_lib_path: str  #
    lib_dir, dotted_lib_path = find_lib(module=module)

    if not Path(lib_dir).exists():
        raise FileNotFoundError

    objects = []

    # iterate through the modules inside the LIB directory
    for _, module_name, _ in iter_modules([lib_dir]):
        # if module has a register_as_subclass decorator then the below import
        # will cause the class to be registered in the Facility/Factory Registry
        module_object = import_module(
            '{package}.{module}'.format(package=dotted_lib_path, module=module_name)
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
