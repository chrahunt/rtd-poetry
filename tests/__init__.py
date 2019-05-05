import os
import tempfile

from contextlib import contextmanager
from pathlib import Path
from typing import ContextManager, Union


@contextmanager
def chdir(path: Union[Path, str]) -> ContextManager:
    current_path = Path.cwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(str(current_path))


@contextmanager
def isolated_filesystem() -> ContextManager[Path]:
    with tempfile.TemporaryDirectory() as d:
        with chdir(d):
            yield Path(d)
