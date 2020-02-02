"""
Model-ready dataset for the United Kingdom's 2015 General Election.

Usage:
    > import maven
    > maven.get('general-election/UK/2017/model', data_directory='./data/')
"""
import os
from pathlib import Path

import pandas as pd

from maven.datasets.general_election.base import UKModel


class UK2017Model(UKModel):
    """Generates model-ready data for the United Kingdom's 2017 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2017/model")):
        super(UK2017Model, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            (
                "general-election/UK/2015/results",
                "general_election-uk-2015-results.csv",
                "9a785cb19275e4dbc79da67eece6067f",
            ),
            (
                "general-election/UK/2017/results",
                "general_election-uk-2017-results.csv",
                "c7e1fde647e55f9d4567cb81e62c782a",
            ),
            ("general-election/UK/polls", "general_election-uk-polls.csv", "98f865803c782e1ffd0cdc4774707ae5"),
            ("general-election/UK/polls", "general_election-london-polls.csv", "97eb4254039a6bca1a882a9afde2b067"),
            ("general-election/UK/polls", "general_election-scotland-polls.csv", "096354c852a7c30e22a733eec133b9e3"),
            ("general-election/UK/polls", "general_election-wales-polls.csv", "2134d55e5288bd5b12be2471f4aacab7"),
            ("general-election/UK/polls", "general_election-ni-polls.csv", "ea871fad0ce51c03dda09ecec0377dc6"),
        ]
        self.retrieve_all = True
        self.verbose_name = "UK2017Model"
        self.year = 2017
        self.last_date = pd.to_datetime("2015-05-07")
        self.now_date = pd.to_datetime("2017-06-08")
        self.last = self.last_date.year
        self.now = self.now_date.year
