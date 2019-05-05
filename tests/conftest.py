import os
import subprocess
import venv

from pathlib import Path
from typing import List

import pytest

from . import isolated_filesystem


@pytest.fixture
def virtualenv():
    def run_python(
        cmd: List[str], *args, **kwargs
    ) -> subprocess.CompletedProcess:
        interpreter = Path(path) / 'bin' / 'python'
        cmd.insert(0, str(interpreter))
        return subprocess.run(cmd, *args, **kwargs)

    with isolated_filesystem() as path:
        use_symlinks = os.name != 'nt'
        venv.create(path, symlinks=use_symlinks, with_pip=True)
        yield run_python
