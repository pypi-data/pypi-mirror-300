import os
from os import PathLike
from typing import Dict, List

import typer

from sw_ut_report.__init__ import __version__
from sw_ut_report.parse_txt_file import format_txt_file
from sw_ut_report.parse_xml_file import format_xml_to_dict
from sw_ut_report.template_manager import get_local_template

cli = typer.Typer()


def input_folder_option() -> typer.Option:
    return typer.Option(
        ...,
        "--input-folder",
        help="Path to the folder containing the txt and xml files",
    )


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
    input_folder: str = input_folder_option(),
):
    if ctx.invoked_subcommand is None:
        generate_report(input_folder)


@cli.command()
def generate_report(
    input_folder: str = input_folder_option(),
):
    typer.echo("test reports generation started")

    all_reports = []

    try:
        file_list = os.listdir(input_folder)
    except FileNotFoundError:
        typer.echo(f"Path '{input_folder}' does not exist.")
        raise typer.Exit(code=1)
    except PermissionError:
        typer.echo(f"Permission denied for the folder '{input_folder}'.")
        raise typer.Exit(code=1)

    for filename in file_list:
        input_file = os.path.join(input_folder, filename)
        _, file_extension = os.path.splitext(filename)

        match file_extension.lower():
            case ".txt":
                scenarios = format_txt_file(read_file_content(input_file))
                for scenario in scenarios:
                    scenario["filename"] = filename
                all_reports.append(
                    {"type": "txt", "filename": filename, "content": scenarios}
                )

            case ".xml":
                suites_data = format_xml_to_dict(input_file)
                suites_data["filename"] = filename
                all_reports.append(
                    {"type": "xml", "filename": filename, "content": suites_data}
                )

            case _:
                if os.path.isdir(input_file):
                    typer.echo(f"Skipping folder: {filename}")
                    continue
                else:
                    print(f"Skipping unsupported file format: {filename}")
                    continue

    generate_single_markdown(all_reports)
    typer.echo("Markdown report generated.")


def read_file_content(input_file: PathLike) -> str:
    with open(input_file, "r", encoding="utf-8") as f:
        return f.read()


def generate_single_markdown(all_reports: List[Dict]) -> None:
    template = get_local_template("combined_test_report.j2")
    markdown_content = template.render(reports=all_reports)

    with open("sw_ut_report.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
