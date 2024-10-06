import os

import click
from .setup import setup_path
from .cmds import pyside_uic_run, pyside_designer_run
from typing import List


def pyside_uic(input, output):
    print(f"Converting {input} to {output}")
    pyside_uic_run(f"{input} -o {output}")


# icon filename to use
def convert_ui(ui_file: str, inplace: bool, target: str | None):
    if inplace:
        pyside_uic(ui_file, ui_file.replace(".ui", ".py"))
    else:
        assert target is not None, "Target directory must be specified when not converting in place"
        assert os.path.exists(target), f"Target directory {target} does not exist"
        pyside_uic(ui_file, os.path.join(target, os.path.basename(ui_file).replace(".ui", ".py")))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("sources", type=click.Path(exists=True), required=True, nargs=-1)
@click.option("--inplace", "-i", is_flag=True, help="Convert the files in place")
@click.option("--target", "-t", help="Target directory for the converted files")
def convert(sources: List[str], inplace: bool, target: str | None):
    setup_path()

    for source in sources:
        convert_ui(source, inplace, target)


# edit command
@cli.command()
@click.argument("sources", type=click.Path(exists=True), required=True, nargs=-1)
def edit(sources: str):
    setup_path()
    pyside_designer_run(" ".join(sources))


if __name__ == "__main__":
    cli()
