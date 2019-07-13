"""
General Election polling data for the United Kingdom.

Sources:
    - SixFifty polling data: https://github.com/six50/pipeline/tree/master/data/polls/
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_london.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_scotland.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_wales.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_ni.csv

Usage:
    > import maven
    > maven.get('general-election/UK/polls', data_directory='./data/')
"""
import os
import warnings
from pathlib import Path

import requests


class UKPolls:
    """Handles General Election polling data for the United Kingdom."""

    def __init__(self, directory=Path('data/general-election/UK/polls')):
        self.directory = Path(directory)

    def retrieve(self):
        """Retrieve General Election polling data for the United Kingdom."""
        target_directory = self.directory / 'processed'
        os.makedirs(target_directory, exist_ok=True)  # create directory if it doesn't exist
        base_url = 'https://s3-eu-west-1.amazonaws.com/sixfifty/'
        files = [
            # (source_filename, target_filename)
            ('polls.csv', 'general_election-uk-polls.csv'),
            ('polls_london.csv', 'general_election-london-polls.csv'),
            ('polls_scotland.csv', 'general_election-scotland-polls.csv'),
            ('polls_wales.csv', 'general_election-wales-polls.csv'),
            ('polls_ni.csv', 'general_election-ni-polls.csv')
        ]
        for source_filename, target_filename in files:
            response = requests.get(base_url + source_filename)
            if response.status_code == 200:
                with open(target_directory / target_filename, 'wb') as f:
                    f.write(response.content)
                print(f'Successfully downloaded raw data into {target_directory.resolve()}')
            else:
                warnings.warn(f'Received status 404 when trying to retrieve {base_url}{source_filename}')

    def process(self):
        pass
