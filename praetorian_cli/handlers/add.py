import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler, status_options
from praetorian_cli.handlers.utils import Status


@chariot.group()
@cli_handler
def add(ctx):
    """Add a resource to Chariot"""
    pass


@add.command('seed')
@click.argument('seed', required=True)
@status_options(Status['seed'])
def assets(controller, seed, status, comment):
    """ Add a seed"""
    controller.add('seed', dict(dns=seed, status=status, comment=comment))


@add.command('file')
@click.argument('name')
@cli_handler
def upload(controller, name):
    """ Upload a file """
    controller.upload(name)


@add.command('definition')
@click.argument('path')
@click.option('-name', '--name', required=False, help='The risk name definition. Default: the filename used')
@cli_handler
def definition(controller, path, name):
    """ Upload a definition to use for a risk"""
    if name is None:
        name = path.split('/')[-1]
    controller.upload(path, f"definitions/{name}")


@add.command('webhook')
@cli_handler
def webhook(controller):
    """Add an authenticated URL for posting assets and risks"""
    response = controller.add_webhook()
    print(response)


@add.command('risk')
@click.argument('name', required=True)
@click.option('-key', '--key', required=True, help='Key of an existing asset')
@status_options(Status['risk'])
def risks(controller, name, key, status, comment):
    """ Add a risk"""
    controller.add('risk', dict(key=key, name=name, status=status, comment=comment))


@add.command('job')
@click.argument('capability', required=True)
@click.option('-key', '--key', required=True, help='Key of an existing asset')
@status_options(Status['job'])
def jobs(controller, capability, key, status, comment):
    """ Add a job"""
    controller.add('job', dict(key=key, name=capability, status=status, comment=comment))


@add.command('attribute')
@cli_handler
@click.argument('name', required=True)
@click.option('-key', '--key', required=True, help='Key of an existing asset')
@click.option('-class', '--class', 'clss', default="", help='Class of the attribute')
def attributes(controller, name, key, clss):
    """ Add an attribute"""
    params = {
        'key': key,
        'name': name,
        'class': clss
    }
    print(controller.add('asset/attribute', params))
