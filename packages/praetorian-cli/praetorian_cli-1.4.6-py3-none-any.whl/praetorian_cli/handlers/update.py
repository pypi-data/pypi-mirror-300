import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler
from praetorian_cli.handlers.utils import AssetPriorities
from praetorian_cli.sdk.model.globals import Risk


@chariot.group()
@cli_handler
def update(ctx):
    """ Update an entity in Chariot """
    pass


@update.command('asset')
@click.argument('key', required=True)
@click.option('-p', '--priority', type=click.Choice(AssetPriorities.keys()), required=True,
              help='The priority of the asset')
@cli_handler
def asset(sdk, key, priority):
    """
    Update an asset

    KEY is the key of the asset
    """
    sdk.assets.update(key, AssetPriorities[priority])


@update.command('risk')
@click.argument('key', required=True)
@click.option('-s', '--status', type=click.Choice([s.value for s in Risk]), help=f'Status of the risk')
@click.option('-c', '--comment', default='', help='Comment for the risk')
@cli_handler
def risk(sdk, key, status, comment):
    """
    Update a risk

    KEY is the key of the risk
    """
    sdk.risks.update(key, status, comment)
