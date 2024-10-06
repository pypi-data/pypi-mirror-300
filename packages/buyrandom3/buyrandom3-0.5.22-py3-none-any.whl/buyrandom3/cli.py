"""Command-line interface."""
import click


@click.command()
@click.version_option()
def run() -> None:
    """buyrandom3."""
    pass


if __name__ == "__main__":
    run(prog_name="buyrandom3")  # pragma: no cover
