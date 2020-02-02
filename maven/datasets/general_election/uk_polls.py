"""
General Election polling data for the United Kingdom.

Usage:
    > import maven
    > maven.get('general-election/UK/polls', data_directory='./data/')

Sources:
    - SixFifty polling data: https://github.com/six50/pipeline/tree/master/data/polls/
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_london.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_scotland.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_wales.csv
        - https://s3-eu-west-1.amazonaws.com/sixfifty/polls_ni.csv
"""
from pathlib import Path

from maven.datasets.general_election.base import Pipeline


class UKPolls(Pipeline):
    """Handles General Election polling data for the United Kingdom."""

    def __init__(self, directory=Path("data/general-election/UK/polls")):
        super(UKPolls, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls.csv", "98f865803c782e1ffd0cdc4774707ae5"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_london.csv", "97eb4254039a6bca1a882a9afde2b067"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_scotland.csv", "096354c852a7c30e22a733eec133b9e3"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_wales.csv", "2134d55e5288bd5b12be2471f4aacab7"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_ni.csv", "ea871fad0ce51c03dda09ecec0377dc6"),
        ]
        self.retrieve_all = True
        self.verbose_name = "UKPolls"
