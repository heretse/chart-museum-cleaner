import click

from .api import list_all_charts
from .cleaner import get_name_and_versions_to_delete, delete_name_and_versions

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('--keep', default=2, help='Number of recent versions to keep and not delete', show_default=True)
def delete(keep):
    """
    Clean up chart versions and keep number of newer versions
    :param keep: number of versions to keep
    :return:
    """
    if keep < 1:
        click.echo("--keep should be greater than 1. Do you really want to remove all charts?")
        return

    response = list_all_charts()
    name_and_versions_to_delete = get_name_and_versions_to_delete(response, keep)
    delete_name_and_versions(name_and_versions_to_delete)


def main():
    cli()
