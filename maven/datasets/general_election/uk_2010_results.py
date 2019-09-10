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
            (
                "http://www.electoralcommission.org.uk/__data/assets/excel_doc/0003/105726/",
                "GE2010-results-flatfile-website.xls",
            ),
            (
                "https://s3-eu-west-1.amazonaws.com/sixfifty/",
                "GE2010-results-flatfile-website.xls",
            ),
        ]
        self.raw_data_dir = self.directory / "raw"

        # create variables for storing the procesed results
        self.processed_results_filename = "general_election-uk-2010-results.csv"
        self.processed_results_full_filename = (
            "general_election-uk-2010-results-full.csv"
        )
        self.processed_results_location = (
            self.directory / "processed" / self.processed_results_filename
        )
        self.processed_results_full_location = (
            self.directory / "processed" / self.processed_results_full_filename
        )

        # will ensure that these dimensions are met
        self.expected_row_dim = 650
        self.expected_col_dim = 144

        # 6 here is tehe column which contains vote counts, and this column
        # (col 6, indexing from 0) is the total for each vote.
        self.first_col_with_party_vote_info = 6

        # Filter to metadata cols + parties of interest. The original data has
        # ~139 parties, we want to filter this down for future analysis.
        self.parties_lookup = {
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

        self.uk_regions_to_NI_scotland_london_and_not_london = {
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

    def retrieve(self):
        """Retrieve results data for the United Kingdom's 2010 General Election."""
        os.makedirs(
            self.raw_data_dir, exist_ok=True
        )  # create directory if it doesn't exist
        for url, filename in self.sources:
            response = requests.get(url + filename)
            if response.status_code == 200:
                with open(self.raw_data_dir / filename, "wb") as f:
                    f.write(response.content)
                print(
                    f"Successfully downloaded raw data into {self.raw_data_dir.resolve()}"
                )
                return
            warnings.warn(
                "Received status 404 when trying to retrieve {}{}".format(url, filename)
            )
        raise RuntimeError("Unable to download UK 2010 General Election results data.")

    def process(self):
        """Process results data for the United Kingdom's 2010 General Election."""
        os.makedirs(
            self.directory / "processed", exist_ok=True
        )  # create directory if it doesn't exist

        #######################################################################


        ##########################
        # GENERAL ELECTION RESULTS
        ##########################
        print(f"Read and clean {self.sources[0][1]}")

        # Import general election results from the correct sheet, there are two
        # sheets, the other being 'Party Abbreviations'
        results = pd.read_excel(
            self.directory / "raw" / self.sources[0][1], sheet_name="Party vote share"
        )

        # Remove rows where Constituency Name is blank - in the spreadsheet
        # this is only one row, the last row of the sheet
        blank_rows = results["Constituency Name"].isnull()
        results = results[-blank_rows].copy()

        # NA represents zero votes for that party within that consituency, so
        # set them to zero.
        results.to_csv("d2.csv")
        for party_vote_result in results.columns[self.first_col_with_party_vote_info :]:
            results[party_vote_result] = results[party_vote_result].fillna(0)

        # missing rows/columns will impact further analysis
        assert results.shape == (self.expected_row_dim, self.expected_col_dim), (
            f"Dimensions of data are incorrect, expect {self.expected_row_dim} rows"
            f"and {self.expected_col_dim} columns. "
            f"data has {results.shape[0]} rows, {results.shape[1]} cols"
        )

        # Save this for convenience
        results_full = results.copy()
        results_full.to_csv("./test-full-results.csv")

        ############################
        # ADDITIONAL TRANSFORMATIONS
        ############################

        other_parties = list(
            set(results.columns)
            - set(results.columns[: self.first_col_with_party_vote_info])
            - set(self.parties_lookup.keys())
        )

        results["Other"] = results.loc[:, other_parties].sum(axis=1)
        results = results.loc[
            :, list(results.columns[:6]) + list(self.parties_lookup.keys())
        ]

        # Rename parties using the defined values in parties_lookup, ignore
        # columns relating to Press Association Reference, Constituency Name,
        # Region, Election Year, and Electorate.
        #
        results.columns = [
            self.parties_lookup[x] if x in self.parties_lookup else x
            for x in results.columns
        ]

        # Calculate constituency level vote share proportion (pc=proportion count)
        for party in self.parties_lookup.values():
            results[party + "_pc"] = results[party] / results["Votes"]

        # Create PANO -> geo lookup
        # Store regions in England as either London or not-London, rather than
        # having East/West Midlands and such.
        results["geo"] = results.Region.map(
            self.uk_regions_to_NI_scotland_london_and_not_london
        )

        assert results.loc[237.0, "geo"] == "London"

        # Who won?
        def winner(row):
            """
            given a row representing outome for a consituency sort and return
            the winning party 
            """
            winning_party = (
                row[self.first_col_with_party_vote_info :]
                .sort_values(ascending=False)
                .index[0]
            )
            if winning_party in self.parties_lookup.keys():
                winning_party = self.parties_lookup[winning_party]
            elif winning_party == "Speaker":
                winning_party = "other"
            return winning_party.lower()

        results_full.to_csv("dfull.csv")
        results["winner"] = results_full.apply(winner, axis=1)
        results.to_csv("d1.csv")
        # Check Conservative won 306 seats in 2010.
        assert (
            results.winner.value_counts()[0] == 306
        ), "Conservative should have won 306 seats in 2010, data shows otherwise"

        # EXPORT
        print(f"Exporting dataset to {self.processed_results_location.resolve()}")
        results.to_csv(self.processed_results_location, index=False)
        print(f"Exporting dataset to {self.processed_results_full_location.resolve()}")
        results_full.to_csv(self.processed_results_full_location, index=False)

