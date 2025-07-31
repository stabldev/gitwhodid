import click

from gitwhodid import __version__
from gitwhodid.blame import Blame
from gitwhodid.utils import print_result


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option(__version__)
def main(file: str):
    try:
        result = Blame().run(file)
        print_result(result)
    except Exception as e:
        click.secho(e, fg="red", err=True)


if __name__ == "__main__":
    main()
