"""
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest
"""

import maven
import pytest


def test_nonexisting_identifier():
    with pytest.raises(KeyError):
        maven.get("this-identifier-will-never-exist", data_directory="./data/")


def test_nothing_happens():
    """Setting retrieve=False and process=False should do nothing."""
    maven.get("general-election/UK/2010/results", retrieve=False, process=False)
