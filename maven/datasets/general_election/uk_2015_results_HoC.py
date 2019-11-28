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
        url = 'https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186/'
        filename = 'hocl-ge2015-results-summary.csv'
        target = self.directory / 'raw'
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist

        print(f'Downloading into {target.resolve()}')
        with open(target / filename, 'wb') as f:
            response = requests.get(url + filename)
            f.write(response.content)

        print('Cleaning up')
        os.remove(target / filename)
