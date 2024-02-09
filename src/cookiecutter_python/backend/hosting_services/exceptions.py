__all__ = ['ContextVariableDoesNotExist']


class ContextVariableDoesNotExist(Exception):
    """Raised when a Context Variable does not exist, in a dict-like object."""

    pass
