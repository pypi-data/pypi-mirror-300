from functools import wraps
from shutil import which

import click


def requires(command, help=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if which(command) is not None:
                return func(*args, **kwargs)
            if help:
                click.echo(help, err=True)
            else:
                click.echo(f'This function requires "{command}" to be installed.', err=True)
            exit(1)

        return wrapper

    return decorator
