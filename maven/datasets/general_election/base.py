"""
Base classes.
"""

import os
from pathlib import Path

from maven import utils


class UKResults:
    """Handles results data for UK General Elections."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []
        self.verbose_name = ""

    def retrieve(self):
        target_dir = self.directory / "raw"
        os.makedirs(target_dir, exist_ok=True)  # create directory if it doesn't exist
        for url, filename in self.sources:
            utils.download_file(url=url, filename=filename, target_dir=target_dir)
        raise RuntimeError(f"Unable to download {self.verbose_name} data.")
