import importlib
import sys
from functools import wraps
from inspect import signature
from io import StringIO

import click


def handle_api_error(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.secho(e.args[0], fg='red')

    return handler


def cli_handler(func):
    func = click.pass_obj(func)
    func = handle_api_error(func)
    return func


def list_options(filter_name):
    def decorator(func):
        func = cli_handler(func)
        func = click.option('-filter', '--filter', default="", help=f"Filter by {filter_name}")(func)
        func = click.option('-details', '--details', is_flag=True, default=False, help="Show detailed information")(
            func)
        return func

    return decorator


def status_options(status_choices):
    def decorator(func):
        func = cli_handler(func)
        func = click.option('-status', '--status', type=click.Choice([s.value for s in status_choices]), required=False,
                            help="Status of the object")(func)
        func = click.option('-comment', '--comment', default="", help="Add a comment")(func)
        return func

    return decorator


def page_options(func):
    func = click.option('-offset', '--offset', default='', help='List results from an offset')(func)
    func = click.option('-page', '--page', type=click.Choice(('no', 'interactive', 'all')), default='no',
                        help="Pagination mode. 'all' pages up to 100 pages. Default: 'no'")(func)

    return func


def scripts(f):
    @click.option('--script', help="Specify a script to process the output")
    @wraps(f)
    def decorated_function(*args, script=None, **kwargs):
        if script is None:
            return f(*args, **kwargs)

        if 'page' in kwargs and kwargs['page'] == 'interactive':
            print("Scripts can only be used with 'no' or 'all' pagination mode.")
            exit(1)

        old_stdout = sys.stdout
        sys.stdout = my_stdout = StringIO()

        try:
            result = f(*args, **kwargs)
            output = my_stdout.getvalue().rstrip()
        finally:
            sys.stdout = old_stdout

        if script:
            process_with_script(script, output, kwargs)
        else:
            click.echo(output)

        return result

    return decorated_function


def process_with_script(script_name, output, cli_kwargs):
    try:
        script_module = importlib.import_module(f'.scripts.{script_name}', 'praetorian_cli')
        if hasattr(script_module, 'process') and len(signature(script_module.__dict__['process']).parameters) == 4:
            ctx = click.get_current_context()
            controller = ctx.obj
            if ctx.parent.command.name == 'cli':
                cmd = dict(product=ctx.command.name, action=None, type=None)
            if ctx.parent.parent.command.name == 'cli':
                cmd = dict(product=ctx.parent.command.name, action=ctx.command.name, type=None)
            else:
                cmd = dict(product=ctx.parent.parent.command.name, action=ctx.parent.command.name,
                           type=ctx.command.name)

            script_module.process(controller, cmd, cli_kwargs, output)
        else:
            click.echo(f"The script {script_name} does not have a 'process' function that takes 4 arguments.")
    except ImportError as e:
        click.echo(f'Error importing script {script_name}: {e}')
