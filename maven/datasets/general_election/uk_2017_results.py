"""
Results data for the United Kingdom's 2017 General Election.

Usage:
    >>> import maven
    >>> maven.get('general-election/UK/2017/results', data_directory='./data/')


Sources:
    - http://researchbriefings.files.parliament.uk/documents/CBP-8647/1918-2017election_results.csv
        - From https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647

Other sources:
    - https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186
    - http://researchbriefings.files.parliament.uk/documents/CBP-7979/HoC-GE2017-constituency-results.csv
"""

from pathlib import Path

from maven.datasets.general_election.base import UKResults


class UK2017Results(UKResults):
    """Handles results data for the United Kingdom's 2017 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2017/results")):
        super(UK2017Results, self).__init__(directory=directory)
        self.directory = Path(directory)
        self.sources = [
            # url, filename, checksum
            (
                "http://researchbriefings.files.parliament.uk/documents/CBP-8647/",
                "1918-2017election_results_by_pcon.xlsx",
                "a1e4628945574639b541b21bada2531c",
            ),
        ]
        self.target = ("general_election-uk-2017-results.csv", "c7e1fde647e55f9d4567cb81e62c782a")  # filename, checksum
        self.verbose_name = "UK 2017 General Election results"
        self.year = "2017"
