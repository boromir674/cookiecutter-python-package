from os import path
import sys
from typing import Optional, Type, TypeVar
from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module

T = TypeVar('T')


def load(interface: Type[T], dire: Optional[str] = None) -> None:
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
        dire (str): directory containing the modules to inspect. Defaults to the
            same directory as the one where the module of the invoking code
            resides.
    """
    if not dire:  # set as dir the directory path where the invoking code is
        namespace = sys._getframe(1).f_globals  # caller's globals
        dire = path.dirname(path.realpath(namespace['__file__']))

    project_package_location = path.dirname(
        path.realpath(path.dirname(path.realpath(__file__))))
    # dot representation as in an import statement: ie software_release.utils
    _module: str = str(dire).replace(str(project_package_location), '')[1:].replace('/', '.')

    # iterate through the modules in the dire folder
    for (_, module_name, _) in iter_modules([dire]):

        module = import_module('{package}.{module}'.format(
            package=_module,
            module=module_name
        ))

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and issubclass(attribute, interface):
                # Add the class to this package's variables
                globals()[attribute_name] = attribute
