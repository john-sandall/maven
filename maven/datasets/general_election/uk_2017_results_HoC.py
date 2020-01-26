import os
from pathlib import Path

import numpy as np
import pandas as pd
import requests

import feather

csv_filename = "HoC-GE2017-constituency-results.csv"


class UK2017ResultsHoC:
    def __init__(self, directory=Path("data/general-election/UK/2017/hoc_results")):
        self.directory = Path(directory)

    def retrieve(self):
        # Config
        url = "http://researchbriefings.files.parliament.uk/documents/CBP-7979/"
        target = self.directory / "raw"
        os.makedirs(target, exist_ok=True)  # create directory if it doesn't exist

        # Download URL into local directory
        print("Downloading into {}".format(target.resolve()))
        with open(target / csv_filename, "wb") as f:
            response = requests.get(url + csv_filename)
            f.write(response.content)

    def process(self):

        processed_dir = self.directory / "processed"
        processed_results_filename = Path("general_election-uk-2017-results.csv")
        # GENERAL ELECTION RESULTS
        print(f"Read and clean RESULTS FOR {csv_filename}")

        # Import general election results
        results = pd.read_csv(self.directory / "raw" / csv_filename)
        assert results.shape == (650, 29)

        results = results.rename(
            columns={
                "ons_id": "Constituency ID",
                "constituency_name": "Constituency Name",
                "constituency_type": "Constituency Type",
                "county_name": "County",
                "region_name": "Region",
                "country_name": "Country",
                "ons_region_id": "Region ID",
                "electorate": "Electorate",
                "valid_votes": "Valid Votes",
                "first_party": "winner",
            }
        )
        results["Election Year"] = 2017
        results["Press Association ID Number"] = np.nan

        minor_parties = ["dup", "sf", "sdlp", "uup", "alliance"]
        major_parties = ["con", "lab", "ld", "ukip", "green", "snp", "pc"]

        # Add minor parties to "other", then drop
        results["other"] += results[minor_parties].sum(axis=1)
        results = results.drop(minor_parties, axis=1)

        # Calculate voteshare % for major parties
        for party in major_parties:
            results[party + "_pc"] = (results[party] / results["Valid Votes"]) * 100

        # Add 'geo' column to differentiate London from rest of England
        def map_geo(row):
            if row.Country == "England":
                if row.County == "London":
                    return "London"
                else:
                    return "England_not_london"
            elif row.Country == "Northern Ireland":
                return "NI"
            else:
                return row.Country

        results["geo"] = results.apply(map_geo, axis=1)

        results = results[
            [
                "Press Association ID Number",
                "Constituency ID",
                "Constituency Name",
                "Constituency Type",
                "County",
                "Region ID",
                "Region",
                "Country",
                "Election Year",
                "Electorate",
                "Valid Votes",
                "con",
                "lab",
                "ld",
                "ukip",
                # "grn",
                "snp",
                "pc",
                "other",
                "con_pc",
                "lab_pc",
                "ld_pc",
                "ukip_pc",
                # "grn_pc",
                "snp_pc",
                "pc_pc",
                # "other_pc",
                "winner",
                "geo",
            ]
        ]

        os.makedirs(processed_dir, exist_ok=True)  # create directory if it doesn't exist

        # Export as both CSV and Feather
        results.to_csv(processed_dir / processed_results_filename, index=False)
        feather.write_dataframe(results, str(processed_dir / "general_election-uk-2017-results.feather"))
