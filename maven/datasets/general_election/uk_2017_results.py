"""
Results data for the United Kingdom's 2017 General Election.

Usage:
    >>> import maven
    >>> maven.get('general-election/UK/2017/results', data_directory='./data/')


Sources:
    - http://researchbriefings.files.parliament.uk/documents/CBP-8647/1918-2017election_results.csv

Other sources:
    - https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186
    - http://researchbriefings.files.parliament.uk/documents/CBP-7979/HoC-GE2017-constituency-results.csv
"""

import os
from pathlib import Path

from maven import utils
from maven.datasets.general_election.base import UKResults


class UK2017Results(UKResults):
    """Handles results data for the United Kingdom's 2017 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2017/results")):
        self.directory = Path(directory)
        self.sources = [
            (
                "http://researchbriefings.files.parliament.uk/documents/CBP-8647/",
                "1918-2017election_results_by_pcon.xlsx",
            ),
        ]
        self.verbose_name = "UK 2017 General Election results"

    def process(self):
        """Process results data for the United Kingdom's 2017 General Election."""
        filename = self.sources[0][1]
        processed_results_filename = "general_election-uk-2017-results.csv"
        processed_results_location = self.directory / "processed" / processed_results_filename
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        # Process
        results = utils.process_hoc_sheet(input_file=filename, data_dir=self.directory, sheet_name="2017")

        # Export
        print(f"Exporting dataset to {processed_results_location.resolve()}")
        results.to_csv(processed_results_location, index=False)
