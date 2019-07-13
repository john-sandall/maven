"""
General Election polling data for the United Kingdom.

Sources:
    - https://s3-eu-west-1.amazonaws.com/sixfifty/polls.csv
        - Read more: https://github.com/six50/pipeline/tree/master/data/polls/

Usage:
    > import maven
    > maven.get('general-election/UK/polls', data_directory='./data/')
"""
import os
from pathlib import Path

import requests


class UKPolls:
    """Handles General Election polling data for the United Kingdom."""

    def __init__(self, directory=Path('general-election/UK/polls')):
        self.directory = Path(directory)

    def retrieve(self):
        """Retrieve General Election polling data for the United Kingdom."""
        target = self.directory / 'processed'
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist
        url = 'https://s3-eu-west-1.amazonaws.com/sixfifty/'
        filename = 'polls.csv'
        response = requests.get(url + filename)
        if response.status_code == 200:
            with open(target / filename, 'wb') as f:
                f.write(response.content)
            print(f'Successfully downloaded raw data into {target.resolve()}')
            return
        raise RuntimeError(f'Received status 404 when trying to retrieve {url}{filename}')

    def process(self):
        pass
