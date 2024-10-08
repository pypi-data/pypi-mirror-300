import click
from erikrowens_de_toolkit.vm import *

@click.group()
def cli():
    pass

cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)


if __name__ == '__main__':
    cli()
