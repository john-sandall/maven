"""
Results data for the United Kingdom's 2017 General Election.

Usage:
    >>> import maven
    >>> maven.get('general-election/UK/2017/results', data_directory='./data/')


Sources:
    - http://researchbriefings.files.parliament.uk/documents/CBP-8647/1918-2017election_results.csv
        - From https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647

Other sources:
    - https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186
    - http://researchbriefings.files.parliament.uk/documents/CBP-7979/HoC-GE2017-constituency-results.csv
"""

from pathlib import Path
import os
import pandas as pd
from functools import partial

from maven import utils

CACHING_ENABLED = True
VERBOSE = False


class UK2019Results():
    """Handles results data for the United Kingdom's 2017 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2019/results")):
        self.directory = Path(directory)
        self.sources = [
            # url, filename, checksum
            (
                "http://researchbriefings.files.parliament.uk/documents/CBP-8749/",
                "HoC-GE2019-results-by-constituency.csv",
                "6f299c3e79287627746e50ad295f863b",
            ),
        ]
        self.target = ("general_election-uk-2019-results.csv", "c7e1fde647e55f9d4567cb81e62c782a")  # filename, checksum
        self.verbose_name = "UK 2019 General Election results"
        self.year = "2019"

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

            # WRONG: this datasource is not an excel file
            # results = utils.process_hoc_sheet(input_file=filename, data_dir=self.directory, sheet_name=self.year)

            # RIGHT: 
            df = pd.read_csv(self.directory / "raw" / filename)

            parties = [
                'con', 
                'lab', 
                'ld', 
                'brexit', 
                'green', 
                'snp', 
                'pc', 
                'dup',
                'sf', 
                'sdlp', 
                'uup', 
                'alliance', 
                'other'
            ]

            df['total_votes'] = df.valid_votes + df.invalid_votes
            df['turnout'] = df.total_votes / df.electorate

            melted = pd.melt(df, id_vars=[
                    'ons_id',
                    'constituency_name',
                    'county_name',
                    'region_name',
                    'country_name',
                    'electorate',
                    'total_votes',
                    'turnout'
                ], value_vars=parties, var_name='party', value_name='votes').sort_values(by='constituency_name')

            melted['voteshare'] = melted.votes / melted.total_votes

            melted = melted.rename({
                'constituency_name': 'constituency',
                'county_name': 'county',
                'region_name': 'region',
                'country_name': 'country'
            }, axis=1)
            melted.constituency = melted.constituency.map(lambda s: s.upper())

            results = melted

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
