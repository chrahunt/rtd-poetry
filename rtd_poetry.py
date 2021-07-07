import os

from functools import wraps
from pathlib import Path

from poetry.masonry.api import *
from poetry.factory import Factory


__version__ = '0.1.1'


@wraps(prepare_metadata_for_build_wheel)
def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    name = prepare_metadata_for_build_wheel.__wrapped__(
        metadata_directory, config_settings
    )

    if os.environ.get('READTHEDOCS') != 'True':
        return name

    poetry = Factory().create_poetry(Path("."))

    metadata = Path(metadata_directory) / name / 'METADATA'

    text = metadata.read_text(encoding='utf-8')

    try:
        # Start of long description.
        index = text.index('\n\n')
    except ValueError:
        # End of text, minus trailing newline.
        index = len(text) - 1

    dev_requires = '\n'.join(
        f'Requires-Dist: {d.to_pep_508()}'
        for d in poetry.package.dev_requires
    )

    new_text = f'{text[:index]}\n{dev_requires}{text[index:]}'

    metadata.write_text(new_text, encoding='utf-8')

    Path('/tmp/foo.txt').write_text(new_text, encoding='utf-8')
    return name
