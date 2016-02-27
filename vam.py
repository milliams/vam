import os
import pathlib
import shutil
import subprocess
import venv

import click
import pkg_resources

from launcher import create_launcher_text, install_launcher


def home() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser('~'))


def vam_dir() -> pathlib.Path:
    return home() / '.vam'


def package_dir(package: str) -> pathlib.Path:
    return vam_dir() / package


def get_distribution(package: str) -> pkg_resources.Distribution:
    lib = package_dir(package) / 'lib'
    package_dists = []
    for py_version in lib.iterdir():  # Iterate over 'python3.4' etc.
        if not py_version.is_dir():
            continue
        site_packages = py_version / 'site-packages'
        dists = [d for d in pkg_resources.find_distributions(str(site_packages))]
        package_dists += [d for d in dists if d.project_name == package]

    if not package_dists:
        raise Exception('Distribution not found in {}'.format(lib))

    return package_dists[0]


def get_entry_points(package: str):
    dist = get_distribution(package)
    entry_map = pkg_resources.get_entry_map(dist)
    for entry_point_group, entry_points in entry_map.items():
        for entry_point in entry_points.values():
            yield entry_point_group, entry_point


def packages():
    return [x for x in vam_dir().iterdir() if x.is_dir()]


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
@click.option('--bindir', default=config['bindir'], type=pathlib.Path)
def install(package: str, bindir: pathlib.Path):
    """Install a package"""
    click.echo('Installing {}'.format(package))

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

        launcher_path = bindir / entry_point.name
        install_launcher(launcher_path, launcher)


@vam.command()
@click.argument('package')
def remove(package):
    """Remove a package"""
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
