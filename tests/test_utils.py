"""
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest
"""
import os
from functools import partial
from pathlib import Path

import requests

import pytest
from maven import utils


class MockResponse:
    """requests.get() returns an object of class Response. Let's mock that and add:
        - status_code attribute
        - content attribute
    """

    status_code = 200
    content = b"some content"


def test_sanitise():
    assert utils.sanitise("Vote Count") == "vote_count"


def test_calculate_md5_checksum(tmpdir):
    filepath = tmpdir / "file.txt"
    with open(filepath, "w") as f:
        f.write("some content")
    assert utils.calculate_md5_checksum(filename=filepath) == "9893532233caff98cd083a116b013c0b"


def test_fetch_url(monkeypatch, tmpdir):
    """Ref: https://docs.pytest.org/en/latest/monkeypatch.html"""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)  # replace requests.get() with our mock_get()
    utils.fetch_url(url="https://fakeurl", filename="fakefile.txt", target_dir=Path(tmpdir))
    with open(tmpdir / "fakefile.txt", "rb") as f:
        assert f.read() == b"some content"


def test_retrieve_from_cache_if_exists(tmpdir):
    def _create_file(target_dir):
        """Puts file.txt in the target_dir"""
        with open(target_dir / "file.txt", "w") as f:
            f.write("some content")

    # Put it there for now.
    _create_file(target_dir=tmpdir)

    # Test basic usage
    utils.retrieve_from_cache_if_exists(
        filename="file.txt",
        target_dir=Path(tmpdir),
        processing_fn=None,
        md5_checksum=None,
        caching_enabled=True,
        verbose=False,
    )
    # Test incorrect MD5
    with pytest.warns(UserWarning):
        utils.retrieve_from_cache_if_exists(
            filename="file.txt",
            target_dir=Path(tmpdir),
            processing_fn=None,
            md5_checksum="badchecksum",
            caching_enabled=True,
            verbose=True,
        )
    # Remove file & put it there via processing_fn
    os.remove(tmpdir / "file.txt")
    utils.retrieve_from_cache_if_exists(
        filename="file.txt",
        target_dir=Path(tmpdir),
        processing_fn=partial(_create_file, target_dir=tmpdir),
        md5_checksum=None,
        caching_enabled=True,
        verbose=True,
    )
