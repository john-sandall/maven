"""
Results data for the United Kingdom's 2010 General Election.

Usage:
    >>> import maven
    >>> maven.get('general-election/UK/2010/results', data_directory='./data/')


Sources:
    - http://researchbriefings.files.parliament.uk/documents/CBP-8647/1918-2017election_results.csv
        - From https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647

Deprecated sources:
    - http://www.electoralcommission.org.uk/__data/assets/excel_doc/0003/105726/GE2010-results-flatfile-website.xls
    - https://s3-eu-west-1.amazonaws.com/sixfifty/GE2010-results-flatfile-website.xls

Notes:
    - GE2010-results-flatfile-website.xls is currently the only known source with a full list of votes for ALL parties.
"""

from pathlib import Path

from maven.datasets.general_election.base import UKResults


class UK2010Results(UKResults):
    """Handles results data for the United Kingdom's 2010 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2010/results")):
        self.directory = Path(directory)
        self.sources = [
            # url, filename, checksum
            (
                "http://researchbriefings.files.parliament.uk/documents/CBP-8647/",
                "1918-2017election_results_by_pcon.xlsx",
                "a1e4628945574639b541b21bada2531c",
            ),
        ]
        self.target = ("general_election-uk-2010-results.csv", "954a0916f5ce791ca566484ce566088d")  # filename, checksum
        self.verbose_name = "UK 2010 General Election results"
        self.year = "2010"
