
# mutmut_config.py

# This file is used to configure mutmut, a mutation testing tool for Python.
# It defines a function that determines whether to skip mutation for certain lines
def pre_mutation(context):
    line: str = context.current_source_line.strip()
    if line.startswith('log.') or line.startswith('@define') or line.startswith('@attr.s') \
        or line.strip().startswith('@abstractmethod') \
        or line.strip().startswith('@property'):
        context.skip = True

    if any([line.startswith(x) for x in {
        'TypeVar',
        'T = TypeVar'
    }]):
        context.skip = True
