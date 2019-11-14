'''
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest
'''

import pytest

import maven


def test_nonexisting_identifier():
    with pytest.raises(KeyError):
        maven.get('this-identifier-will-never-exist')


def test_process_with_retrieve():
    # TODO: This is a useful test for now but we should actually handle this explicitly with a better error message.
    with pytest.raises(FileNotFoundError):
        maven.get('general-election/UK/2015/results', retrieve=False, process=True)
