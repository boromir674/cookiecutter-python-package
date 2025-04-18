import typing as t

import pytest


# GIVEN the Interface and Implementations modules are placed "correctly"
@pytest.fixture(scope='function')
def interface_and_implementations_lib():
    """

    filesystem
    # simple_interface.py
    #   ├── __init__.py
    #   ├── lib
    #   │   ├── __init__.py
    #   │   ├── implementation_1.py
    #   │   └── implementation_2.py

    """

    # GIVEN an "interface" from which we seek the concrete implementations
    INTERFACE_MODULE = """
from abc import ABC, abstractmethod
from software_patterns import SubclassRegistry


class SimpleInterface(ABC):
    @abstractmethod
    def method(self):
        raise NotImplementedError("Subclasses should implement this!")


class ImplementationsRegistry(SubclassRegistry[SimpleInterface]):
    pass


class Simple(metaclass=ImplementationsRegistry):
    pass

"""

    # GIVEN a "library" of 2 interface implementations (concrete classes)
    MODULE_1 = """
from ..simple_interface import Simple

__all__ = ["Implementation1"]

@Simple.register_as_subclass('implementation_1')
class Implementation1(Simple):
    def method(self):
        return "Implementation1"
"""

    MODULE_2 = """
from ..simple_interface import Simple

__all__ = ["Implementation2"]

@Simple.register_as_subclass('implementation_2')
class Implementation2(Simple):
    def method(self):
        return "Implementation2"
"""

    # create temp dir at tests/data
    import os
    import sys
    import tempfile
    from pathlib import Path

    # Create a temporary directory
    temp_dir: str = tempfile.mkdtemp()

    DISTRO_NAME = 'unit_test_python_package'
    DISTRO = Path(temp_dir) / DISTRO_NAME

    def modify_filesystem():
        # Create the directory structure
        os.makedirs(DISTRO, exist_ok=False)

        (DISTRO / "__init__.py").touch()

        (DISTRO / "simple_interface.py").write_text(INTERFACE_MODULE)

        os.makedirs(DISTRO / "lib", exist_ok=False)

        (DISTRO / "lib" / "__init__.py").touch()
        (DISTRO / "lib" / "implementation_1.py").write_text(MODULE_1)
        (DISTRO / "lib" / "implementation_2.py").write_text(MODULE_2)

    modify_filesystem()

    # Add the temp directory to sys.path
    sys.path.insert(0, temp_dir)

    yield DISTRO_NAME

    # Clean up the temporary directory
    # shutil.rmtree(temp_dir)
    # sys.path.remove(temp_dir)


@pytest.mark.parametrize(
    'load_arg',
    [
        'Simple',
        'SimpleInterface',
        'AnyRandomClass',
    ],
)
def test_calling_load_successfully_registers_implementations_in_factory(
    load_arg: str,
    interface_and_implementations_lib: str,
):
    from importlib import import_module
    from pathlib import Path

    # GIVEN the function that dynamically imports modules and modifies globals
    from cookiecutter_python.utils import load

    DISTRO_NAME: str = interface_and_implementations_lib

    # import the Facility (Registry Metaclass) Module
    simple_interface_module = import_module(
        '.'.join((Path(DISTRO_NAME) / "simple_interface").parts)
    )

    interface: t.Type
    if load_arg == 'AnyRandomClass':
        # if passed as an extra effect the load returns the 2 class.__name__ from the implementations
        interface = type('AnyRandomClass', (object,), {})
    else:
        from importlib import import_module
        from pathlib import Path

        interface = getattr(simple_interface_module, load_arg)

    # WHEN 'load' is called
    objects: t.List[t.Type] = load(
        interface, module='.'.join((Path(DISTRO_NAME) / "lib").parts)
    )
    # Sanity check (this is tested in the next test)
    assert objects if load_arg == 'Simple' else objects == []

    # THEN the Simple Factory is automatically loaded as intended
    impl1 = simple_interface_module.Simple.create('implementation_1')
    assert impl1.method() == "Implementation1"
    impl2 = simple_interface_module.Simple.create('implementation_2')
    assert impl2.method() == "Implementation2"


def test_calling_load_with_input_arg_Simple(
    interface_and_implementations_lib: str,
):
    from importlib import import_module
    from pathlib import Path

    # GIVEN the function that dynamically imports modules and modifies globals
    from cookiecutter_python.utils import load

    DISTRO_NAME: str = interface_and_implementations_lib

    simple_interface_module = import_module(
        '.'.join((Path(DISTRO_NAME) / "simple_interface").parts)
    )
    interface = simple_interface_module.Simple

    # WHEN 'load' is called
    objects = load(interface, module='.'.join((Path(DISTRO_NAME) / "lib").parts))

    # THEN the function returns a list of classes that implement the interface
    assert len(objects) == 2
    assert all(isinstance(obj, type) for obj in objects)

    # AND the classes are the expected ones
    assert objects[0].__name__ == "Implementation1"
    assert objects[1].__name__ == "Implementation2"
