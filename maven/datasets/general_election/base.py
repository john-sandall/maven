"""
Base classes.
"""
import os
from functools import partial
from pathlib import Path

from maven import utils

CACHING_ENABLED = True
VERBOSE = True


class UKResults:
    """Handles results data for UK General Elections."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []
        self.target = (None, None)
        self.verbose_name = ""
        self.year = ""

    def retrieve(self):
        """Retrieve raw results data for a UK General Election."""
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
            return
        raise RuntimeError(f"Unable to download {self.verbose_name} data.")

    def process(self):
        """Process results data for a UK General Election."""
        filename = self.sources[0][1]
        processed_results_location = self.directory / "processed" / self.target[0]
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        def process_and_export():
            # Either caching disabled or file not yet processed; process regardless.
            results = utils.process_hoc_sheet(input_file=filename, data_dir=self.directory, sheet_name=self.year)
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
