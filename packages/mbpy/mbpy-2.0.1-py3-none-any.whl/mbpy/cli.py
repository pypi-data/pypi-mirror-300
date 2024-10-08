import atexit
import inspect
import logging
import logging.handlers
import subprocess
import sys
import tempfile
import traceback
from asyncio.subprocess import PIPE
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Thread
from time import time
from typing import Generic, Iterator, Literal, TypeVar, Union

import rich_click as click
import tomlkit
from mrender.md import Markdown
from rich.console import Console
from rich.traceback import Traceback

from mbpy.commands import run_command
from mbpy.create import create_project
from mbpy.mpip import (
    ADDITONAL_KEYS,
    INFO_KEYS,
    base_name,
    find_and_sort,
    find_toml_file,
    get_package_info,
    modify_pyproject_toml,
    modify_requirements,
    name_and_version,
)
from mbpy.publish import append_notion_table_row

console = Console()

@click.group("mbpy")
@click.pass_context
@click.option(
    "-v",
    "--hatch-env",
    default=None,
    help="Specify the Hatch environment to use",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug logging",
)
def cli(ctx: click.Context, hatch_env, debug) -> None:
    if sys.flags.debug or debug:
        logging.basicConfig(level=logging.DEBUG, force=True)
    if ctx.invoked_subcommand is None:
        console.print("No subcommand specified. Showing dependencies:")
        show_command(hatch_env)


@cli.command("install", no_args_is_help=True)
@click.argument("packages", nargs=-1)
@click.option(
    "-r",
    "--requirements",
    type=click.Path(exists=True),
    help="Install packages from the given requirements file",
)
@click.option("-U", "--upgrade", is_flag=True, help="Upgrade the package(s)")
@click.option(
    "-e",
    "--editable",
    is_flag=True,
    help="Install a package in editable mode",
)
@click.option("--hatch-env", default=None, help="Specify the Hatch environment to use")
@click.option(
    "-g",
    "--dependency-group",
    default="dependencies",
    help="Specify the dependency group to use",
)
@click.option("-d", "--debug", is_flag=True, help="Enable debug logging")
def install_command(
    packages,
    requirements,
    upgrade,
    editable,
    hatch_env,
    dependency_group,
    *,
    debug=False,
) -> None:
    """Install packages and update requirements.txt and pyproject.toml accordingly.

    Args:
        packages (tuple): Packages to install.
        requirements (str, optional): Requirements file to install packages from. Defaults to None.
        upgrade (bool, optional): Upgrade the package(s). Defaults to False.
        editable (bool, optional): Install a package in editable mode. Defaults to False.
        hatch_env (str, optional): The Hatch environment to use. Defaults to "default".
        dependency_group (str, optional): The dependency group to use. Defaults to "dependencies".
        debug (bool, optional): Enable debug logging. Defaults to False.
    """
    if sys.flags.debug or debug:
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.info("Debug logging enabled.")
    try:
        installed_packages = []
        if requirements:
            requirements_file = requirements
            package_install_cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
            if upgrade:
                package_install_cmd.append("-U")
            for line in run_command(package_install_cmd):
                click.echo(line)
            # Get installed packages from requirements file
            with Path(requirements_file).open() as req_file:
                installed_packages = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]
        
        if packages:
            for package in packages:
                package_install_cmd = [sys.executable, "-m", "pip", "install"]
                if editable:
                    package_install_cmd.append("-e")
                if upgrade:
                    package_install_cmd.append("-U")
                package_install_cmd.append(package)

                for line in run_command(package_install_cmd):
                    click.echo(line, nl=False)
                installed_packages.append(package)

        for package in installed_packages:
            package_name, package_version = name_and_version(package, upgrade=upgrade)
            logging.debug(f"installing {package_name} {package_version}")
            modify_pyproject_toml(
                package_name,
                package_version,
                action="install",
                hatch_env=hatch_env,
                dependency_group=dependency_group,
            )
            logging.info(f"Successfully installed {package_name} to {find_toml_file()} {'for ' + hatch_env if hatch_env else ''}")


        if not requirements and not packages:
            click.secho("No packages specified for installation.")

    except FileNotFoundError as e:
        click.secho("Error: Installation failed.", err=True)
    finally:
        logging.info("")


@cli.command("uninstall", no_args_is_help=True)
@click.argument("packages", nargs=-1)
@click.option("--hatch-env", default=None, help="Specify the Hatch environment to use")
@click.option(
    "-g",
    "--dependency-group",
    default="dependencies",
    help="Specify the dependency group to use",
)
@click.option("-d", "--debug", is_flag=True, help="Enable debug logging")
def uninstall_command(packages, hatch_env, dependency_group, debug) -> None:
    """Uninstall packages and update requirements.txt and pyproject.toml accordingly.

    Args:
        packages (tuple): Packages to uninstall.
        hatch_env (str, optional): The Hatch environment to use. Defaults to "default".
        dependency_group (str, optional): The dependency group to use. Defaults to "dependencies".
        debug (bool, optional): Enable debug logging. Defaults to False.
    """
    if sys.flags.debug or debug:
        logging.basicConfig(level=logging.DEBUG, force=True)
    for package in packages:
        package_name = base_name(package)

        try:
            modify_requirements(package_name, action="uninstall")
            modify_pyproject_toml(
                package_name,
                action="uninstall",
                hatch_env=hatch_env,
                dependency_group=dependency_group,
                pyproject_path=find_toml_file(),
            )
            print_success = None
            console.print(f"Uninstalling {package_name}...")
            for line in run_command([sys.executable, "-m", "pip", "uninstall", "-y", package_name]):
                click.echo(line, nl=False)
                print_success = partial(click.echo, f"Successfully uninstalled {package_name}")
            print_success() if print_success else None
        except subprocess.CalledProcessError as e:
            click.echo(f"Error: Failed to uninstall {package_name}.", err=True)
            click.echo(f"Reason: {e}", err=True)
            sys.exit(e.returncode)
        except Exception as e:
            click.echo(
                f"Unexpected error occurred while trying to uninstall {package_name}: {e}",
                err=True,
            )
            console.print(Traceback.from_exception(e.__class__, e, e.__traceback__))



@cli.command("show", no_args_is_help=False)
@click.argument("package", default=" ")
@click.option("--hatch-env", default=None, help="Specify the Hatch environment to use")
def show_command(package=None, hatch_env="") -> None:
    """Show the dependencies from the pyproject.toml file.

    Args:
        package (str, optional): The package to show information about. Defaults to None.
        hatch_env (str, optional): The Hatch environment to use. Defaults to "default".
    """
    if package.strip():
        try:
            run_command([sys.executable, "-m", "pip", "show", package], show=True).readlines(show=True)
        except Exception:
            traceback.print_exc()
    toml_path = find_toml_file()
    try:
        with Path(toml_path).open() as f:
            content = f.read()
            pyproject = tomlkit.parse(content)

        # Determine if we are using Hatch or defaulting to project dependencies
        if "tool" in pyproject and "hatch" in pyproject["tool"] and hatch_env is not None:
            dependencies = (
                pyproject.get("tool", {}).get("hatch", {}).get("envs", {}).get(hatch_env, {}).get("dependencies", [])
            )
        else:
            dependencies = pyproject.get("project", {}).get("dependencies", [])

        if dependencies:
            from rich.table import Table
            from rich.panel import Panel
            table = Table(title=Panel("Dependencies", style="bold"))
            table.add_column("Package", style="cyan")
            for dep in dependencies:
                table.add_row(dep)
            console.print(table)
        else:
            click.echo("No dependencies found.")
    except FileNotFoundError:
        click.echo("Error: pyproject.toml file not found.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")



SEARCH_DOC = """Find a package on PyPI and optionally sort the results.\n

    Args:\n
        package (str): The package to search for.
        limit (int, optional): Limit the number of results. Defaults to 5.
        sort (str, optional): Sort key to use. Defaults to "downloads".
        include (str, optional): Include pre-release versions. Defaults to None.
        release (str, optional): Release type to use. Defaults to None.
        full list of options:
    """  # noqa: D205


@cli.command("search", no_args_is_help=True)
@click.argument("package", type=str, nargs=-1)
@click.option("--limit", default=10, help="Limit the number of results")
@click.option("--sort", default="downloads", help="Sort key to use")
@click.option("--include", multiple=True,type=click.Choice(["all"]+INFO_KEYS+ADDITONAL_KEYS), default=None, help="Include additional information")
@click.option("--release", default=None, help="Release version to use")
@click.option("-d", "--debug", is_flag=True, help="Enable debug logging")
def search_command(package, limit, sort, include, release, debug) -> None:
    """Find a package on PyPI and optionally sort the results.
    
    Args:
        package (str): The package to search for.s
        limit (int, optional): Limit the number of results. Defaults to 5.
        sort (str, optional): Sort key to use. Defaults to "downloads".
        include (str, optional): Include pre-release versions. Defaults to None.
        release (str, optional): Release type to use. Defaults to None.
        debug (bool, optional): Enable debug logging. Defaults to False.
    """
    if not isinstance(package, str):
        package = " ".join(package)
    if debug:
        logging.basicConfig(level=logging.DEBUG, force=True)
    try:
        packages = find_and_sort(package, limit, sort, include=include, release=release)
        md = Markdown(packages)
        md.stream()
    except Exception:
        traceback.print_exc()


@cli.command("info", no_args_is_help=True)
@click.argument("package")
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
def info_command(package, verbose) -> None:
    """Get information about a package from PyPI.

    Args:
        package (str): The package to get information about.
        verbose (bool, optional): Show detailed output. Defaults to False.
    """
    try:
        package_info = get_package_info(package, verbose)
        md = Markdown(package_info)
        md.stream()
    except Exception:
        traceback.print_exc()


@cli.command("create", no_args_is_help=True)
@click.argument("project_name")
@click.argument("author")
@click.option("--description", default="", help="Project description")
@click.option("--deps", default=None, help="Dependencies separated by commas")
@click.option("--python", default="3.12", help="Python version to use")
@click.option("--no-cli", is_flag=True, help="Do not add a CLI")
@click.option("--doc-type", type=click.Choice(["sphinx", "mkdocs"]), default="sphinx", help="Documentation type to use")
def create_command(project_name, author, description, deps, python="3.12", no_cli=False, doc_type="sphinx") -> None:
    """Create a new Python project. Optionally add dependencies and a CLI."""
    python_version = python
    try:
        if deps:
            deps = deps.split(",")
        create_project(project_name=project_name, author=author, description=description, python_version=python_version,
                          dependencies=deps, add_cli=not no_cli, doc_type=doc_type)
        click.secho(f"Project {project_name} created successfully with {doc_type} documentation.", fg="green")
    except Exception:
        traceback.print_exc()

@cli.command("publish", no_args_is_help=True)
@click.argument("package")
@click.option("--token", default=None, help="Notion API token")
@click.option("--table", default=None, help="Notion table URL")
def publish_command(package, token, table) -> None:
    """Publish a package to a Notion table."""
    try:
        append_notion_table_row(package, token, table)
    except Exception:
        traceback.print_exc()


@cli.command("run", no_args_is_help=True)
@click.argument("command", nargs=-1)
def run_cli_command(command) -> None:
    """Run a command."""
    from mbpy.commands import run
    try:
        run(command,show=True)
    except Exception:
        traceback.print_exc()

def main():
    cli()
if __name__ == "__main__":
    main()
