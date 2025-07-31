import click

from gitwhodid.blame import Blame


@click.command()
@click.argument("file", type=click.Path(exists=True))
def main(file: str):
    try:
        click.echo(Blame().run(file))
    except Exception as e:
        click.secho(e, fg="red", err=True)


if __name__ == "__main__":
    main()
