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
# import os
# import warnings
from pathlib import Path

from maven.datasets.general_election.base import ETL

# import requests


class UKPolls(ETL):
    """Handles General Election polling data for the United Kingdom."""

    def __init__(self, directory=Path("data/general-election/UK/polls")):
        super(UKPolls, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls.csv", None),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_london.csv", None),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_scotland.csv", None),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_wales.csv", None),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_ni.csv", None),
        ]
        self.retrieve_all_data = True
        self.verbose_name = "UKPolls"
