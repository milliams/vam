import pathlib
import shutil
import subprocess
import venv

import click

from environment import home, packages
from launcher import create_launcher_text, install_launcher
from package import package_dir, get_entry_points, get_distribution


def pip_command(package: str) -> pathlib.Path:
    return package_dir(package) / 'bin' / 'pip'


def call_pip(package: str, args):
    pip = pip_command(package)
    return subprocess.check_call([str(pip)] + args, stdout=subprocess.PIPE)


config = {
    'bindir': home() / '.local' / 'bin'
}


@click.group()
def vam():
    """Virtualenv Application Manager AKA 'pia'"""
    pass


@vam.command()
@click.argument('package')
@click.option('--upgrade/--no-upgrade', default=False)
def install(package: str, upgrade: bool):
    """Install a package"""
    click.echo('Installing {}'.format(package))

    if package_dir(package).exists() and not upgrade:
        click.echo('Application {} already installed, to upgrade use --upgrade'.format(package))
        exit(1)

    # Create venv
    venv_dir = package_dir(package)
    venv.create(str(venv_dir), clear=True, with_pip=True)

    # Ask pip to install the package
    call_pip(package, ['install', package])

    # Install entry-point launchers
    for entry_point_group, entry_point in get_entry_points(package):
        python_path = package_dir(package) / 'bin' / 'python'  # TODO ask setuptools for this info?
        launcher = create_launcher_text(
            package=package,
            version=entry_point.dist.version,
            entry_point=entry_point.name,
            entry_point_group=entry_point_group,
            python_path=str(python_path)
        )

        launcher_path = config['bindir'] / entry_point.name
        install_launcher(launcher_path, launcher)


@vam.command()
@click.argument('package')
def remove(package):
    """Remove a package"""

    for entry_point_group, entry_point in get_entry_points(package):
        launcher_path = config['bindir'] / entry_point.name
        launcher_path.unlink()

    d = package_dir(package)
    shutil.rmtree(str(d))


@vam.command('list')
@click.option('-v', '--verbose', count=True)
def _list(verbose):
    """List all installed packages"""
    for p in packages():
        package = p.name
        dist = get_distribution(package)
        click.echo('{}=={}'.format(package, dist.version))
        if verbose:
            for entry_point_group, entry_point in get_entry_points(package):
                click.echo('  {}'.format(entry_point_group))
                click.echo('    {}'.format(entry_point.name))
