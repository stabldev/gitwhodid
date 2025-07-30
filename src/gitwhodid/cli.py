import click

@click.command()
@click.argument("file", type=click.Path(exists=True))
def main(file: str):
    click.echo(f"Who did {file}?")

if __name__ == "__main__":
    main()
