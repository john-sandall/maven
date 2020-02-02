"""
Results data for the United Kingdom's 2015 General Election.

Usage:
    >>> import maven
    >>> maven.get('general-election/UK/2015/results', data_directory='./data/')


Sources:
    - http://researchbriefings.files.parliament.uk/documents/CBP-8647/1918-2017election_results.csv
        - From https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647

Deprecated sources:
    - http://www.electoralcommission.org.uk/__data/assets/file/0004/191650/2015-UK-general-election-data-results-WEB.zip

Notes:
    - 2015-UK-general-election-data-results-WEB.zip has a lot more detailed data.
"""

from pathlib import Path

from maven.datasets.general_election.base import UKResults


class UK2015Results(UKResults):
    """Handles results data for the United Kingdom's 2015 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2015/results")):
        super(UK2015Results, self).__init__(directory=directory)
        self.directory = Path(directory)
        self.sources = [
            # url, filename, checksum
            (
                "http://researchbriefings.files.parliament.uk/documents/CBP-8647/",
                "1918-2017election_results_by_pcon.xlsx",
                "a1e4628945574639b541b21bada2531c",
            ),
        ]
        self.target = ("general_election-uk-2015-results.csv", "9a785cb19275e4dbc79da67eece6067f")  # filename, checksum
        self.verbose_name = "UK 2015 General Election results"
        self.year = "2015"
