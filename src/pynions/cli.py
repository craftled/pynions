import click
from dotenv import load_dotenv


@click.group()
def cli():
    """Pynions CLI - Simple AI automation framework"""
    load_dotenv()


@cli.command()
def version():
    """Show version"""
    from pynions import __version__

    click.echo(f"Pynions v{__version__}")


if __name__ == "__main__":
    cli()
