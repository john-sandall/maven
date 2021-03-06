"""
Various helper functions.
"""
import hashlib
import os
import shutil
import warnings
from functools import partial
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

import maven

#########
# GENERAL
#########


def sanitise(x, replace=None):
    if isinstance(x, str):
        out = x.lower().replace(" ", "_").replace("/", "_")
        if replace and out in replace:
            out = replace[out]
        return out
    elif isinstance(x, (list, pd.core.indexes.base.Index, pd.core.series.Series)):
        return [sanitise(element, replace=replace) for element in x]
    else:
        raise TypeError(f"Unexpected type encountered in sanitise: type(x) == '{type(x)}'")


def calculate_md5_checksum(filename):
    """
    Calculate the checksum of the file, exactly same as md5-sum linux util.
    Code from https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/downloader.py
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_url(url):
    """Source: https://stackoverflow.com/a/52455972"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_url(url, filename, target_dir, rename_file=False):
    """Download filename from url into target_dir."""
    if rename_file:
        url_to_retrieve = url
    else:
        url_to_retrieve = url + filename
    response = requests.get(url_to_retrieve)
    if response.status_code != 200:
        warnings.warn(
            f"Received status {response.status_code} when trying to retrieve {url}{filename}"
        )
    # Save to file
    with open(target_dir / filename, "wb") as f:
        f.write(response.content)
    print(f"Successfully downloaded {filename} into {target_dir.resolve()}")
    return target_dir / filename


def get_and_copy(identifier, filename, target_dir):
    """Run maven.get(identifier) and copy filename from identifier/processed/ data
       into target/ directory.
    """
    # target_dir by default is data/general-election/UK/2015/model
    subdirectories_below = str(target_dir).count("/")
    go_up = "/".join([".." for _ in range(subdirectories_below)])
    data_directory = (target_dir / go_up).resolve()  # sensible guess?
    maven.get(identifier, data_directory=data_directory)
    source = data_directory / identifier / "processed"
    print(f"Copying {filename} from {source} -> {target_dir}.")
    shutil.copyfile(src=source / filename, dst=target_dir / filename)


def retrieve_from_cache_if_exists(
    filename, target_dir, processing_fn, md5_checksum=None, caching_enabled=True, verbose=False
):
    """Retrieve filename from target_dir if it exists, otherwise execute processing_fn.

    Raises a warning if the retrieved/processed file's checksum doesn't match the expected MD5.
    """
    if caching_enabled and (target_dir / filename).exists():
        # Check if it's already in target_dir.
        print(f"Cached file {filename} is already in {target_dir.resolve()}")
    else:
        # Either caching disabled or file not there yet.
        processing_fn()

    # File should now be there. Let's check checksums.
    downloaded_file_md5_checksum = calculate_md5_checksum(target_dir / filename)
    if verbose:
        print(f"Checksum for {filename}: {downloaded_file_md5_checksum}")
    if md5_checksum and downloaded_file_md5_checksum != md5_checksum:
        warnings.warn(f"MD5 checksum doesn't match for {filename}")


##################
# PIPELINE CLASSES
##################


class Pipeline:
    """Generic class for retrieving & processing datasets with built-in caching & MD5 checking."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []  # tuples of (url, filename, checksum)
        self.rename_source = False
        self.retrieve_all = False
        self.target = (None, None)
        self.verbose_name = ""
        self.year = None
        self.verbose = False
        self.cache = True

    def retrieve(self):
        """
        Retrieve data from self.sources into self.directory / 'raw' and validate against checksum.
        """
        target_dir = self.directory / "raw"
        os.makedirs(target_dir, exist_ok=True)  # create directory if it doesn't exist
        for url, filename, md5_checksum in self.sources:
            if is_url(url):
                processing_fn = partial(
                    fetch_url,
                    url=url,
                    filename=filename,
                    target_dir=target_dir,
                    rename_file=self.rename_source,
                )
            else:
                processing_fn = partial(
                    get_and_copy, identifier=url, filename=filename, target_dir=target_dir
                )
            retrieve_from_cache_if_exists(
                filename=filename,
                target_dir=target_dir,
                processing_fn=processing_fn,
                md5_checksum=md5_checksum,
                caching_enabled=self.cache,
                verbose=self.verbose,
            )
            if not self.retrieve_all:  # retrieve just the first dataset
                return
        if self.retrieve_all:  # all datasets retrieved
            return
        else:  # retrieving first dataset only but all fallbacks failed
            raise RuntimeError(f"Unable to download {self.verbose_name} data.")

    def process(self):
        pass
