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
    - PollBase: https://www.markpack.org.uk/opinion-polls/
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd

from maven import utils
from maven.datasets.general_election.base import Pipeline


class UKPolls(Pipeline):
    """Handles General Election polling data for the United Kingdom.

    Mark Pack's PollBase : https://www.markpack.org.uk/opinion-polls/
    """

    def __init__(self, directory=Path("data/general-election/UK/polls")):
        super(UKPolls, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            (
                "https://3859gp38qzh51h504x6gvv0o-wpengine.netdna-ssl.com/files/2020/01/",
                "PollBase-Q4-2019.xlsx",
                "81e9dd972f17d0b4f572e7da6c4c497f",
            ),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls.csv", "8c32b623346c8c0faa603bc76c4d7fd1"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_london.csv", "cd28ebb7233b808796535fc0b572304e"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_scotland.csv", "6c2ba92e2325de0e22a208fb0b3e95fc"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_wales.csv", "6857df3c18df525d5e59a6bf1170b10c"),
            ("https://s3-eu-west-1.amazonaws.com/sixfifty/", "polls_ni.csv", "46bbe5e9dc29d4b3042837fe4c16ca07"),
        ]
        self.retrieve_all = True
        self.target = ("general_election-uk-polls.csv", "cbc3c19a376b4ab632f122008f593799")  # filename, checksum
        self.verbose_name = "UKPolls"

    def process(self):
        """Process UK polling data."""
        filename = self.sources[0][1]
        processed_results_location = self.directory / "processed" / self.target[0]
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        def process_and_export():
            # Read in PollBase
            df = pd.read_excel(self.directory / "raw" / filename, sheet_name="17-19", usecols="A:C,G:H,I,K,M,O,Q,S,U,Y")

            # Clean it up
            df.columns = utils.sanitise(
                df.columns,
                replace={
                    "polling": "company",
                    "publisher": "client",
                    "unnamed:_24": "method",
                    "green": "grn",
                    "tig/cuk": "chuk",
                },
            )
            df["year"] = df.year.replace({"?": 2019}).ffill().astype(int)
            df["month"] = df.month.ffill()
            df = df[df["fieldwork"].notnull()].copy()
            df["day_from"] = df.fieldwork.apply(
                lambda x: str(x).split("-")[0].replace("?", "") if "-" in str(x) else str(x).replace("?", "")
            )
            df["day_to"] = df.fieldwork.apply(
                lambda x: str(x).split("-")[1].replace("?", "") if "-" in str(x) else str(x).replace("?", "")
            )
            df["from"] = pd.to_datetime(df.apply(lambda row: f"{row.year}-{row.month}-{row.day_from}", axis=1))
            df["to"] = pd.to_datetime(df.apply(lambda row: f"{row.year}-{row.month}-{row.day_to}", axis=1))

            # Fix month & year in df['to'] where e.g. fieldwork is "30-3 Jan"
            month_shifted = (
                df.year.astype(str)
                + "-"
                + ((df.to.dt.month + 1) % 12).astype(str).replace("0", "12")
                + "-"
                + df.day_to.astype(str)
            )
            year_needs_shifting = month_shifted.apply(lambda x: str(x).split("-")[1]) == "1"
            month_shifted.loc[year_needs_shifting] = (
                ((df.loc[year_needs_shifting, "year"]).astype(int) + 1).astype(str).replace("0", "12")
                + "-"
                + ((df.to.dt.month + 1) % 12).astype(str)
                + "-"
                + df.day_to.astype(str)
            )
            df.loc[df["from"] > df["to"], "to"] = month_shifted.loc[df["from"] > df["to"]]
            df["to"] = pd.to_datetime(df.to)

            # Divide numbers by 100
            for party in ["con", "lab", "ld", "ukip", "grn", "chuk", "bxp"]:
                df[party] = df[party].replace(" ", np.nan).astype(float) / 100

            # Prepare for merge with SixFifty data
            df["sample_size"] = np.nan
            df["snp"] = np.nan
            df["pdf"] = np.nan
            columns = [
                "company",
                "client",
                "method",
                "from",
                "to",
                "sample_size",
                "con",
                "lab",
                "ld",
                "ukip",
                "grn",
                "chuk",
                "bxp",
                "snp",
                "pdf",
            ]
            df = df[columns].copy().sort_values("to")

            # Read in SixFifty polling data (2005 -> June 2017)
            df_sixfifty = pd.read_csv(self.directory / "raw" / "polls.csv", parse_dates=["from", "to"])
            df_sixfifty["chuk"] = np.nan
            df_sixfifty["bxp"] = np.nan
            df_sixfifty = df_sixfifty[columns].copy().sort_values("to")

            # Merge
            df_sixfifty = df_sixfifty[df_sixfifty.to < df.to.min()].copy()
            assert df_sixfifty.to.max() < df.to.min()
            df_polls = pd.concat([df_sixfifty, df], axis=0)

            # Export
            print(f"Exporting dataset to {processed_results_location.resolve()}")
            df_polls.to_csv(processed_results_location, index=False)

        utils.retrieve_from_cache_if_exists(
            filename=self.target[0],
            target_dir=(self.directory / "processed"),
            processing_fn=process_and_export,
            md5_checksum=self.target[1],
            caching_enabled=self.cache,
            verbose=self.verbose,
        )
