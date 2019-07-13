"""
Results data for the United Kingdom's 2015 General Election.

Source: http://www.electoralcommission.org.uk/__data/assets/file/0004/191650/2015-UK-general-election-data-results-WEB.zip

Usage:
    > import maven
    > maven.get('general-election/UK/2015/results', data_directory='./data/')
"""
import os
import zipfile
from pathlib import Path

import pandas as pd
import requests


class UK2015Results:
    """Handles results data for the United Kingdom's 2015 General Election."""

    def __init__(self, directory=Path('data/general-election/UK/2015/results')):
        self.directory = Path(directory)

    def retrieve(self):
        """Retrieve results data for the United Kingdom's 2015 General Election."""
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
        processed_results_filename = 'general_election-uk-2015-results.csv'
        processed_results_full_filename = 'general_election-uk-2015-results-full.csv'
        processed_results_location = (self.directory / 'processed' / processed_results_filename)
        processed_results_full_location = (self.directory / 'processed' / processed_results_full_filename)
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
        print('Merging in constituency identifiers')

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
        column_order = ['Press Association ID Number', 'Constituency ID', 'Constituency Name', 'Constituency Type',
                        'County', 'Region ID', 'Region', 'Country', 'Election Year', 'Electorate',
                        'Valid Votes'] + list(results.columns[9:146])
        results = results[column_order].copy()


        ############################
        # ADDITIONAL TRANSFORMATIONS
        ############################
        # Some MPs are members of both the Labour Party and the Co-operative Party, which plays havoc with modelling.
        # We will therefore consider them all members of the Labour party.
        results['Lab'] = results['Lab'] + results['Lab Co-op']
        del results['Lab Co-op']

        # Save this for convenience
        results_full = results.copy()

        # Filter to metadata cols + parties of interest
        parties_lookup = {
            'C': 'con',
            'Lab': 'lab',
            'LD': 'ld',
            'UKIP': 'ukip',
            'Green': 'grn',
            'SNP': 'snp',
            'PC': 'pc',
            'Other': 'other'
        }
        other_parties = list(set(results.columns) - set(results.columns[:11]) - set(parties_lookup.keys()))
        results['Other'] = results.loc[:, other_parties].sum(axis=1)
        results = results.loc[:, list(results.columns[:11]) + list(parties_lookup.keys())]
        # Rename parties
        results.columns = [parties_lookup[x] if x in parties_lookup else x for x in results.columns]

        # Calculate constituency level vote share
        for party in parties_lookup.values():
            results[party + '_pc'] = results[party] / results['Valid Votes']

        # Create PANO -> geo lookup
        geo_lookup = {x[1][0]: x[1][1] for x in results[['Press Association ID Number', 'Country']].iterrows()}
        assert geo_lookup[14.0] == 'Northern Ireland'
        # Add London boroughs
        london_panos = results[results.County == 'London']['Press Association ID Number'].values
        for pano in london_panos:
            geo_lookup[pano] = 'London'
        assert geo_lookup[237.0] == 'London'
        # Rename other England
        for k in geo_lookup:
            if geo_lookup[k] == 'England':
                geo_lookup[k] = 'England_not_london'
            elif geo_lookup[k] == 'Northern Ireland':
                geo_lookup[k] = 'NI'
        results['geo'] = results['Press Association ID Number'].map(geo_lookup)

        # Calculate geo-level vote share
        # TODO: Do we use this?
        results_by_geo = results.loc[:, ['Valid Votes', 'geo'] + list(parties_lookup.values())].groupby('geo').sum()
        results_by_geo_voteshare = results_by_geo.div(results_by_geo['Valid Votes'], axis=0)
        del results_by_geo_voteshare['Valid Votes']

        # Who won?
        def winner(row):
            all_parties = set(results_full.columns[11:]) - set(['Other'])
            winning_party = row[all_parties].sort_values(ascending=False).index[0]
            if winning_party in parties_lookup.keys():
                winning_party = parties_lookup[winning_party]
            elif winning_party == 'Speaker':
                winning_party = 'other'
            return winning_party

        results['winner'] = results_full.apply(winner, axis=1)
        # Check Conservatives won 330 seats in 2015.
        assert results.groupby('winner').count()['Constituency Name'].sort_values(ascending=False)[0] == 330

        # EXPORT
        print(f'Exporting dataset to {processed_results_location.resolve()}')
        results.to_csv(processed_results_location, index=False)
        results_full.to_csv(processed_results_full_location, index=False)
