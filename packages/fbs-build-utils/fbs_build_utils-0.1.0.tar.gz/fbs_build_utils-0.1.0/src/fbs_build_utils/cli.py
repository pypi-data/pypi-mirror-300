import os

import click

from fbs_build_utils.main import get_settings, get_target_dir, update_version
from fbs_build_utils.os_cmd import execute_command
from fbs_build_utils.rename_installer import name_installer, package_portable
from fbs_build_utils.generate_icons import generate_icons
from qt_build_utils.convert_ui import convert_ui_glob

ICON_PATH = "src/main/icons/icon.png"

# setup_path()


@click.group()
def cli():
    pass


def generate_files():
    update_version()
    generate_icons(ICON_PATH)
    settings = get_settings()
    for ui_dir in settings["ui_paths"]:
        convert_ui_glob(ui_dir, inplace=True)


@cli.command()
def generate():
    generate_files()


@cli.command()
@click.option("--debug", is_flag=True)
def build(debug):
    # Run the generate command
    generate_files()

    # Create EXE
    if debug:
        execute_command("fbs freeze --debug")
    else:
        execute_command("fbs freeze")

    execute_command("fbs installer")

    info = get_settings()
    name = f"{info['app_name']}_{info['version']}"
    name_installer(f"{name}_installer_win64")
    name_installer("latest", remove_source=True)
    package_portable(f"{name}_portable")


@cli.command()
def run():
    # Run the app
    info = get_settings()
    portable_path = os.path.join(get_target_dir(), info["app_name"])
    execute_command(f"{portable_path}/pyside_template.exe")


@cli.command()
def run_python():
    execute_command("fbs run")


@cli.command()
def run_installer():
    # Run the installer
    execute_command(os.path.join(get_target_dir(), "latest.exe"))


if __name__ == "__main__":
    cli()
