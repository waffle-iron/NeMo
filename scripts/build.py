import TN_build

#true north build
import get_defs
import click

@click.group()
def cli():
    pass
@click.command()
@click.argument('tn_header', type=click.File('r', encoding="utf-8"))
@click.argument('cwd', type=str)
def compileTN(tn_header,cwd):
    print("TN header " + str( tn_header))
    print("CWD " + str(cwd))
    get_defs.tnMain(tn_header.name,cwd)
    TN_build.compileTN(cwd)

@cli.command()
def hello():
    click.echo("Hello there")


cli.add_command(compileTN)


if __name__ == '__main__':
    cli()