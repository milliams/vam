import stat
import string

template = """#!${python_path}
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
    t = string.Template(template)
    return t.safe_substitute(kwargs)


def install_launcher(path, text):
    with open(str(path), 'w+') as f:
        f.write(text)
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
