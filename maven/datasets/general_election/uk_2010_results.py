"""
Results data for the United Kingdom's 2010 General Election.

Sources:
    - http://www.electoralcommission.org.uk/__data/assets/excel_doc/0003/105726/GE2010-results-flatfile-website.xls
    - https://s3-eu-west-1.amazonaws.com/sixfifty/GE2010-results-flatfile-website.xls

Usage:
    > import maven
    > maven.get('general-election/UK/2010/results', data_directory='./data/')
"""
import os
import warnings
from pathlib import Path

import pandas as pd
import requests


class UK2010Results:
    """Handles results data for the United Kingdom's 2010 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2010/results")):
        self.directory = Path(directory)
        self.sources = [
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "GE2010-results-flatfile-website.xls",),
        ]

    def retrieve(self):
        """Retrieve results data for the United Kingdom's 2010 General Election."""
        target = self.directory / "raw"
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist
        for url, filename in self.sources:
            response = requests.get(url + filename)
            if response.status_code == 200:
                with open(target / filename, "wb") as file:
                    file.write(response.content)
                print(f"Successfully downloaded raw data into {target.resolve()}")
                return
            warnings.warn(f"Received status 404 when trying to retrieve {url}{filename}")
        raise RuntimeError("Unable to download UK 2010 General Election results data.")

    def process(self):
        """Process results data for the United Kingdom's 2010 General Election."""
        filename = self.sources[0][1]
        processed_results_filename = "general_election-uk-2010-results.csv"
        processed_results_full_filename = "general_election-uk-2010-results-full.csv"
        processed_results_location = self.directory / "processed" / processed_results_filename
        processed_results_full_location = self.directory / "processed" / processed_results_full_filename
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        ##########################
        # GENERAL ELECTION RESULTS
        ##########################
        print(f"Read and clean {filename}")

        # Import general election results
        results = pd.read_excel(self.directory / "raw" / filename, sheet_name="Party vote share")

        # Remove rows where Constituency Name is blank (one row only - the last row of the sheet)
        blank_rows = results["Constituency Name"].isnull()
        results = results[-blank_rows].copy()

        # Set NA vals to zero (NA => zero votes for that party within the constituency)
        for party_vote_result in results.columns[6:]:  # first 6 cols are not party votes
            results[party_vote_result] = results[party_vote_result].fillna(0)
        assert results.shape == (650, 144)

        # Save this for convenience
        results_full = results.copy()

        ############################
        # ADDITIONAL TRANSFORMATIONS
        ############################

        # Filter to metadata cols + parties of interest (from ~139 parties to ~11).
        parties_lookup = {
            "Con": "con",
            "Lab": "lab",
            "LD": "ld",
            "UKIP": "ukip",
            "Grn": "grn",
            # Northern Ireland
            "DUP": "dup",
            "SF": "sf",
            "SDLP": "sdlp",
            # Scotland
            "SNP": "snp",
            # Wales
            "PC": "pc",
            # Other
            "Other": "other",
        }
        other_parties = list(set(results.columns) - set(results.columns[:6]) - set(parties_lookup.keys()))

        results["Other"] = results.loc[:, other_parties].sum(axis=1)
        results = results.loc[:, list(results.columns[:6]) + list(parties_lookup.keys())]

        # Rename parties (if in parties_lookup, else ignore)
        # TODO: Cleaner with .rename()
        results.columns = [parties_lookup[x] if x in parties_lookup else x for x in results.columns]

        # Calculate constituency level vote share % (pc = percent)
        for party in parties_lookup.values():
            results[party + "_pc"] = results[party] / results["Votes"]

        # Create PANO -> geo lookup
        results["geo"] = results.Region.map(
            {
                "East Midlands": "England_not_london",
                "Eastern": "England_not_london",
                "London": "London",
                "North East": "England_not_london",
                "North West": "England_not_london",
                "Northern Ireland": "NI",
                "Scotland": "Scotland",
                "South East": "England_not_london",
                "South West": "England_not_london",
                "Wales": "Wales",
                "West Midlands": "England_not_london",
                "Yorkshire and the Humber": "England_not_london",
            }
        )
        assert results.loc[237.0, "geo"] == "London"

        # Who won?
        def winner(row):
            """Return winning party for given row of constituency outcomes."""
            # Need to remove Other as this represents multiple parties so (usually) not the actual FPTP winner.
            all_parties = set(results_full.columns[6:]) - set(["Other"])
            winning_party = row[all_parties].sort_values(ascending=False).index[0]
            if winning_party in parties_lookup.keys():
                winning_party = parties_lookup[winning_party]
            elif winning_party == "Speaker":
                winning_party = "other"
            return winning_party

        results["winner"] = results_full.apply(winner, axis=1)
        assert results.winner.value_counts()[0] == 306  # Check Conservatives won 306 seats in 2010

        # EXPORT
        print(f"Exporting dataset to {processed_results_location.resolve()}")
        results.to_csv(processed_results_location, index=False)
        print(f"Exporting dataset to {processed_results_full_location.resolve()}")
        results_full.to_csv(processed_results_full_location, index=False)
