import os
import subprocess

from pathlib import Path

from . import chdir


def test_does_not_install_dev_requirements_normally(virtualenv):
    result = virtualenv(['-m', 'pip', 'install', '--upgrade', 'pip'])
    assert result.returncode == 0

    env = os.environ.copy()
    env.pop('READTHEDOCS', None)
    with chdir(Path(__file__).parent / '..'):
        result = virtualenv(['-m', 'pip', 'install', '.'], env=env)
    assert result.returncode == 0

    result = virtualenv(['-m', 'pip', 'freeze'], stdout=subprocess.PIPE)
    assert result.returncode == 0
    output = result.stdout.decode('utf-8')
    assert 'rtd-poetry' in output
    assert 'pytest' not in output


def test_installs_dev_requirements_if_rtd_env_is_set(virtualenv):
    result = virtualenv(['-m', 'pip', 'install', '--upgrade', 'pip'])
    assert result.returncode == 0

    env = os.environ.copy()
    env['READTHEDOCS'] = 'True'
    with chdir(Path(__file__).parent / '..'):
        result = virtualenv(['-m', 'pip', 'install', '.'], env=env)
    assert result.returncode == 0

    result = virtualenv(['-m', 'pip', 'freeze'], stdout=subprocess.PIPE)
    assert result.returncode == 0
    output = result.stdout.decode('utf-8')
    assert 'rtd-poetry' in output
    assert 'pytest' in output
