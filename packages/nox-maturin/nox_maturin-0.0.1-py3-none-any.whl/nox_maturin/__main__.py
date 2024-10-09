"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """nox-maturin."""


if __name__ == "__main__":
    main(prog_name="nox-maturin")  # pragma: no cover
