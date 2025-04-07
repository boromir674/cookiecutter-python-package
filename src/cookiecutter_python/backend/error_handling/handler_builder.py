import typing as t

import click
from software_patterns import SubclassRegistry


class HandlerBuilderRegistry(SubclassRegistry[t.Callable]):
    pass


class HandlerBuilder(metaclass=HandlerBuilderRegistry):
    pass


@HandlerBuilder.register_as_subclass('non-critical')
class NonCriticalHandlerBuilder:
    def __call__(self, error):
        click.echo(error)


@HandlerBuilder.register_as_subclass('critical')
class CriticalHandlerBuilder:
    def __call__(self, error):
        click.echo('{}'.format(str(error)))
        click.echo('Error message: {}'.format(str(error)))

        # Message that program is exiting due to error
        click.echo('Exiting due to error')
