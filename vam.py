#! /usr/bin/env python3

import venv
import sys
import subprocess
import os
import pathlib

name = sys.argv[1]

home = pathlib.Path(os.path.expanduser('~'))

venv_dir = home / '.vam' / name

venv.create(str(venv_dir), clear=True, with_pip=True)

pip_command = venv_dir / 'bin' / 'pip'

subprocess.check_call([str(pip_command), 'install', name], stdout=subprocess.PIPE)

