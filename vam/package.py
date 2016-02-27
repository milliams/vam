import pathlib

import pkg_resources

from .environment import vam_dir


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
