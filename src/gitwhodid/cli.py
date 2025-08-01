"""
gitwhodid.cli
Command-line interface for gitwhodid.
"""

import click

from gitwhodid import __version__
from gitwhodid.blame import Blame
from gitwhodid.utils import print_result


# pylint: disable=no-value-for-parameter
@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option(__version__)
def main(file: str):
    """Runs git blame on the given file and prints the en-riched result.

    This function calls `run(file)` method of `Blame` class and prints the structured output
    using rich library with en-riched format.

    Args:
        file (str): Path to the file to analyze.
    """
    try:
        result = Blame().run(file)
        print_result(result)
    except RuntimeError as e:
        click.secho(e, fg="red", err=True)


if __name__ == "__main__":
    main()
