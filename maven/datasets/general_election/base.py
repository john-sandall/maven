"""
Base classes.
"""
import os
from functools import partial
from pathlib import Path

from maven import utils

CACHING_ENABLED = True
VERBOSE = False


class ETL:
    """Generic class for retrieving & processing datasets with built-in caching & MD5 checking."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []  # tuples of (url, filename, checksum)
        self.retrieve_all_data = False
        self.target = (None, None)
        self.verbose_name = ""
        self.year = None

    def retrieve(self):
        """Retrieve data from self.sources into self.directory / 'raw' and validate against checksum."""
        target_dir = self.directory / "raw"
        os.makedirs(target_dir, exist_ok=True)  # create directory if it doesn't exist
        for url, filename, md5_checksum in self.sources:
            download_fn = partial(utils.fetch_url, url=url, filename=filename, target_dir=target_dir)
            utils.retrieve_from_cache_if_exists(
                filename=filename,
                target_dir=target_dir,
                processing_fn=download_fn,
                md5_checksum=md5_checksum,
                caching_enabled=CACHING_ENABLED,
                verbose=VERBOSE,
            )
            if not self.retrieve_all_data:  # retrieve just the first dataset
                return
        if self.retrieve_all_data:  # all datasets retrieved
            return
        else:  # retrieving first dataset only but all fallbacks failed
            raise RuntimeError(f"Unable to download {self.verbose_name} data.")

    def process(self):
        pass


class UKResults(ETL):
    """Handles results data for UK General Elections."""

    def process(self):
        """Process results data for a UK General Election."""
        filename = self.sources[0][1]
        processed_results_location = self.directory / "processed" / self.target[0]
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        def process_and_export():
            # Either caching disabled or file not yet processed; process regardless.
            results = utils.process_hoc_sheet(input_file=filename, data_dir=self.directory, sheet_name=str(self.year))
            # Export
            print(f"Exporting dataset to {processed_results_location.resolve()}")
            results.to_csv(processed_results_location, index=False)

        utils.retrieve_from_cache_if_exists(
            filename=self.target[0],
            target_dir=(self.directory / "processed"),
            processing_fn=process_and_export,
            md5_checksum=self.target[1],
            caching_enabled=CACHING_ENABLED,
            verbose=VERBOSE,
        )
