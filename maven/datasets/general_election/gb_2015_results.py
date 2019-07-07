"""
Results data for the United Kingdom's 2015 General Election.

Source: http://www.electoralcommission.org.uk/__data/assets/file/0004/191650/2015-UK-general-election-data-results-WEB.zip

Usage:
    python -m data.european_parliament.2014.scripts.retrieve_electoral_commission
"""
import os
import zipfile
from pathlib import Path

import pandas as pd
import requests


class GB2015Results:
    """Handles results data for the United Kingdom's 2010 General Election."""

    def __init__(self, directory=Path('.')):
        self.directory = directory

    def retrieve(self):
        """Retrieve results data for the United Kingdom's 2010 General Election."""
        url = 'http://www.electoralcommission.org.uk/__data/assets/file/0004/191650/'
        filename = '2015-UK-general-election-data-results-WEB.zip'
        target = self.directory / 'raw'
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist

        print(f'Downloading into {target.resolve()}')
        with open(target / filename, 'wb') as f:
            response = requests.get(url + filename)
            f.write(response.content)

        print(f'Extracting into {target.resolve()}')
        with zipfile.ZipFile(target / filename, 'r') as f:
            f.extractall(target)

        print('Cleaning up')
        os.remove(target / filename)

    def process(self):
        """Process results data for the United Kingdom's 2015 General Election."""
        processed_filename = 'general_election-gb-2015-results.csv'
        processed_dataset_location = (self.directory / 'processed' / processed_filename)
        os.makedirs(self.directory / 'processed', exist_ok=True)  # create directory if it doesn't exist

        # TODO: Refactor these sections into functions to make it easier to read.

        ##########################
        # GENERAL ELECTION RESULTS
        ##########################
        print('Read and clean RESULTS FOR ANALYSIS.csv')

        # Import general election results
        results = pd.read_csv(self.directory / 'raw' / 'RESULTS FOR ANALYSIS.csv')

        # Remove 'Unnamed: 9' columnd
        del results['Unnamed: 9']

        # Fix bad column name (' Total number of valid votes counted ' to 'Valid Votes')
        results.columns = list(results.columns[:8]) + ['Valid Votes'] + list(results.columns[9:])

        # Remove rows where Constituency Name is blank
        blank_rows = results['Constituency Name'].isnull()
        results = results[-blank_rows].copy()

        # Remove commas & coerce Electorate and Total number of valid votes counted
        for col in ['Electorate', 'Valid Votes']:
            results[col] = results[col].apply(lambda x: float(x.replace(",", "")))

        # Set NA vals to zero
        for col in results.columns[9:]:
            results[col] = results[col].fillna(0)

        # Checks
        assert results.shape == (650, 146)

        ###################
        # CONSTITUENCY DATA
        ###################
        print('Read and clean CONSTITUENCY.csv')

        # Import constituency data
        constituency = pd.read_csv(self.directory / 'raw' / 'CONSTITUENCY.csv', encoding='latin1')

        # Remove rows where Constituency Name is blank
        blank_rows = constituency['Constituency Name'].isnull()
        constituency = constituency[-blank_rows].copy()

        # Remove 'Unnamed: 6' columnd
        del constituency['Unnamed: 6']

        # Checks
        assert constituency.shape == (650, 10)

        #######
        # MERGE
        #######
        print(f'Merging and exporting dataset to {processed_dataset_location.resolve()}')

        # Pre-merge checks
        match_col = 'Constituency ID'
        assert len(set(constituency[match_col]).intersection(set(results[match_col]))) == 650
        assert len(set(constituency[match_col]).difference(set(results[match_col]))) == 0
        assert len(set(results[match_col]).difference(set(constituency[match_col]))) == 0

        # Merge on Constituency ID
        results = pd.merge(
            left=results,
            right=constituency[['Constituency ID', 'Region ID', 'County']],
            how='left',
            on='Constituency ID'
        )

        # EXPORT
        column_order = ['Press Association ID Number', 'Constituency ID', 'Constituency Name', 'Constituency Type',
                        'County', 'Region ID', 'Region', 'Country', 'Election Year', 'Electorate',
                        'Valid Votes'] + list(results.columns[9:146])
        results = results[column_order]
        results.to_csv(processed_dataset_location, index=False)
