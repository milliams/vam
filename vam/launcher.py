import stat
import string

launcher_template = """#!${python_path}
# VAM-LAUNCHER-SCRIPT: '${package}==${version}','${entry_point_group}','${entry_point}'
__requires__ = '${package}==${version}'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('${package}==${version}', '${entry_point_group}', '${entry_point}')()
    )
"""


def create_launcher_text(**kwargs):
    return string.Template(launcher_template).safe_substitute(kwargs)


def install_launcher(path, text):
    with open(str(path), 'w+') as launcher_file:
        launcher_file.write(text)
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
