import json

import click
from software_patterns import SubclassRegistry


class HandlerBuilder(metaclass=SubclassRegistry):
    pass


@HandlerBuilder.register_as_subclass('non-critical')
class NonCriticalHandlerBuilder:
    def __call__(self, error):
        click.echo(error)


@HandlerBuilder.register_as_subclass('critical')
class CriticalHandlerBuilder:
    def __call__(self, error):
        click.echo('{}'.format(error.message))
        click.echo('Error message: {}'.format(error.error.message))

        context_str = json.dumps(error.context, indent=4, sort_keys=True)
        click.echo('Context: {}'.format(context_str))
