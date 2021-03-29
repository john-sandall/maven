"""
Model-ready dataset for the United Kingdom's 2019 General Election.

Usage:
    > import maven
    > maven.get('general-election/UK/2019/model', data_directory='./data/')
"""
from pathlib import Path

import pandas as pd

from maven.datasets.general_election.base import UKModel


class UK2019Model(UKModel):
    """Generates model-ready data for the United Kingdom's 2019 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2019/model")):
        super(UK2019Model, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            (
                "general-election/UK/2017/results",
                "general_election-uk-2017-results.csv",
                "c7e1fde647e55f9d4567cb81e62c782a",
            ),
            ("general-election/UK/polls", "general_election-uk-polls.csv", "cbc3c19a376b4ab632f122008f593799"),
            ("general-election/UK/polls", "general_election-london-polls.csv", "cd28ebb7233b808796535fc0b572304e"),
            ("general-election/UK/polls", "general_election-scotland-polls.csv", "6c2ba92e2325de0e22a208fb0b3e95fc"),
            ("general-election/UK/polls", "general_election-wales-polls.csv", "6857df3c18df525d5e59a6bf1170b10c"),
            ("general-election/UK/polls", "general_election-ni-polls.csv", "46bbe5e9dc29d4b3042837fe4c16ca07"),
        ]
        self.retrieve_all = True
        self.verbose_name = "UK2019Model"
        self.year = 2019
        self.last_date = pd.to_datetime("2017-06-08")
        self.now_date = pd.to_datetime("2019-12-12")
        self.last = self.last_date.year
        self.now = self.now_date.year
