from cookiecutter_python.utils import load

from ..dialog import InteractiveDialog


__all__ = ['InteractiveDialog']


# Import all classes subclassing InteractiveDialog
load(InteractiveDialog)
