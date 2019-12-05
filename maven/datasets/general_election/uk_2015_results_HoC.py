"""
Results data for the United Kingdom's 2015 General Election.

Source: https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186

Usage:
    > import maven
    > maven.get('general-election/UK/2015/hoc_results', data_directory='./data/')
"""
import os
import zipfile
from pathlib import Path

import pandas as pd
import requests


class UK2015ResultsHoC:
    """Handles results data from the HoC source for the United Kingdom's 2015 General Election."""

    def __init__(self, directory=Path('data/general-election/UK/2015/hoc_results')):
        self.directory = Path(directory)

    def retrieve(self):
        """Retrieve results data for the United Kingdom's 2015 General Election."""
        url =  "http://researchbriefings.files.parliament.uk/documents/CBP-7186"
        filename = "hocl-ge2015-results-summary.csv"
        # filename = 'hocl-ge2015-results-summary.csv'
        target = self.directory / 'raw'
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist

        print(f'Downloading into {target.resolve()}')
        with open(target / filename, 'wb') as f:
            response = requests.get(url + "/" + filename)
            assert response.status_code == 200
            f.write(response.content)

    def process(self):
        processed_results_filename = 'general_election-uk-2015-results.csv'
        processed_results_full_filename = 'general_election-uk-2015-results-full.csv'
        processed_results_location = self.directory / 'processed' / processed_results_filename
        processed_results_full_location = self.directory / 'processed' / processed_results_full_filename

        results = pd.read_csv(self.directory / 'raw' / "hocl-ge2015-results-summary.csv")

        minor_parties = ['dup', 'sf', 'sdlp', 'uup', 'alliance']
        major_parties = ['con', 'lab', 'ld', 'ukip', 'green', 'snp', 'pc']

        results = results.rename({
            'ons_id': 'Constituency ID', 
            'constituency_name': 'Constituency Name',
            'constituency_type': 'Constituency Type', 
            'county_name': 'County', 
            'region_name': 'Region',
            'country_name': 'Country',
            'electorate': 'Electorate',
            'valid_votes': 'Valid Votes',
            'first_party': 'Winner'
        }, axis=1)

        # Add minor parties to "other", then drop 
        results['other'] += results[minor_parties].sum(axis=1)
        results = results.drop(minor_parties, axis=1)

        # Calculate voteshare % for major parties
        for party in major_parties:
            results[party + "_pc"] = (results[party] / results["Valid Votes"]) * 100

        # Add 'geo' column to differentiate London from rest of England
        def map_geo(row):
            if row.Country == 'England':
                if row.County == 'London':
                    return 'London'
                else:
                    return 'England_not_london'
            elif row.Country == "Northern Ireland":
                return "NI"
            else:
                return row.Country

        results['geo'] = results.apply(map_geo, axis=1)


        os.makedirs(self.directory / 'processed', exist_ok=True)  # create directory if it doesn't exist

        assert results.groupby('Winner').count()['Constituency Name'].sort_values(ascending=False)[0] == 330
        results.to_csv(processed_results_location, index=False)
