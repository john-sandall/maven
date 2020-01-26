"""
Base classes.
"""

import os
import warnings
from pathlib import Path

import requests


class UKResults:
    """Handles results data for UK General Elections."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []
        self.verbose_name = ""

    def retrieve(self):
        target = self.directory / "raw"
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist
        for url, filename in self.sources:
            response = requests.get(url + filename)
            if response.status_code == 200:
                with open(target / filename, "wb") as file:
                    file.write(response.content)
                print(f"Successfully downloaded raw data into {target.resolve()}")
                return
            else:
                warnings.warn(f"Received status 404 when trying to retrieve {url}{filename}")
        raise RuntimeError(f"Unable to download {self.verbose_name} data.")
