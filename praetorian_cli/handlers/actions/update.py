import click

from praetorian_cli.handlers.products import chariot
from praetorian_cli.sdk.constants import Status
from praetorian_cli.handlers.utils.cli_decorators import cli_handler, status_options


@chariot.group()
@cli_handler
def update(ctx):
    """Update a resource in Chariot"""
    pass


def create_update_command(item_type, item_key_name, status_choices):
    @update.command(item_type, help=f"Update {item_type}")
    @click.argument(item_key_name, required=True)
    @status_options(status_choices)
    @click.pass_context
    def command(controller, item_type, item_key, status, comment):
        controller.update(item_type, dict(key=item_key, status=status, comment=comment))


create_update_command('asset', 'asset-key', Status['asset'])
create_update_command('risk', 'risk-key', Status['risk'])
create_update_command('job', 'job-key', Status['job'])
