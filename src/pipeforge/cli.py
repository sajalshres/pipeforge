# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

import click

from pipeforge import __about__
from pipeforge.errors import PipeForgeError
from pipeforge.transpiler import PipelineTranspiler


@click.group(invoke_without_command=True, help="Transpile CI/CD pipeline specs between providers.")
@click.option("--version", is_flag=True, help="Show the PipeForge version and exit.")
@click.pass_context
def app(ctx: click.Context, version: bool) -> None:
    if version:
        click.echo(__about__.__version__)
        ctx.exit(0)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(0)


transpiler = PipelineTranspiler()


@app.command(help="Transpile a CI pipeline definition to a new target.")
@click.argument(
    "input",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    help="Optional path to write the generated pipeline. Prints to stdout when omitted.",
)
@click.option("-s", "--source", default="bamboo", show_default=True, help="Source CI format.")
@click.option("-t", "--target", default="bitbucket", show_default=True, help="Target CI format.")
@click.option("--name", help="Override the pipeline name inside the rendered file.")
def convert(input: Path, output: Path | None, source: str, target: str, name: str | None) -> None:
    try:
        rendered = transpiler.convert_path(input, source=source, target=target, name=name)
    except PipeForgeError as exc:
        click.secho(f"Error: {exc}", fg="red", err=True)
        raise click.Abort()

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        click.echo(f"Wrote {target} pipeline to {output}")
    else:
        click.echo(rendered)


@app.command("list")
def list_formats() -> None:
    """Show supported source and target formats."""
    click.echo("Sources:")
    for slug in transpiler.available_sources():
        click.echo(f"  - {slug}")
    click.echo("\nTargets:")
    for slug in transpiler.available_targets():
        click.echo(f"  - {slug}")
