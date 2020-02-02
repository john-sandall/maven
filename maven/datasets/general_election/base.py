"""
Base classes.
"""
import os
from functools import partial
from pathlib import Path

import pandas as pd

from maven import utils


class Pipeline:
    """Generic class for retrieving & processing datasets with built-in caching & MD5 checking."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.sources = []  # tuples of (url, filename, checksum)
        self.retrieve_all = False
        self.target = (None, None)
        self.verbose_name = ""
        self.year = None
        self.verbose = False
        self.cache = True

    def retrieve(self):
        """Retrieve data from self.sources into self.directory / 'raw' and validate against checksum."""
        target_dir = self.directory / "raw"
        os.makedirs(target_dir, exist_ok=True)  # create directory if it doesn't exist
        for url, filename, md5_checksum in self.sources:
            if utils.is_url(url):
                processing_fn = partial(utils.fetch_url, url=url, filename=filename, target_dir=target_dir)
            else:
                processing_fn = partial(utils.get_and_copy, identifier=url, filename=filename, target_dir=target_dir)
            utils.retrieve_from_cache_if_exists(
                filename=filename,
                target_dir=target_dir,
                processing_fn=processing_fn,
                md5_checksum=md5_checksum,
                caching_enabled=self.cache,
                verbose=self.verbose,
            )
            if not self.retrieve_all:  # retrieve just the first dataset
                return
        if self.retrieve_all:  # all datasets retrieved
            return
        else:  # retrieving first dataset only but all fallbacks failed
            raise RuntimeError(f"Unable to download {self.verbose_name} data.")

    def process(self):
        pass


class UKResults(Pipeline):
    """Handles results data for UK General Elections."""

    @staticmethod
    def process_hoc_sheet(input_file, data_dir, sheet_name):
        # Import general election results
        print(f"Read and clean {input_file}")
        parties = ["Con", "LD", "Lab", "UKIP", "Grn", "SNP", "PC", "DUP", "SF", "SDLP", "UUP", "APNI", "Other"]
        results = pd.read_excel(
            data_dir / "raw" / input_file, sheet_name=sheet_name, skiprows=4, header=None, skipfooter=19
        )
        assert results.shape == (650, 49)

        # Specify columns (spread across multiple rows in Excel)
        cols = ["", "id", "Constituency", "County", "Country/Region", "Country", "Electorate", ""]
        for party in parties:
            cols += [f"{party}_Votes", f"{party}_Voteshare", ""]
        cols += ["Total votes", "Turnout"]
        results.columns = cols

        # Some basic data quality checks
        for party in parties:
            assert (results[f"{party}_Voteshare"] - results[f"{party}_Votes"] / results["Total votes"]).sum() == 0
        assert (
            results[[f"{party}_Votes" for party in parties]].fillna(0.0).sum(axis=1) == results["Total votes"]
        ).all()
        assert ((results["Total votes"] / results["Electorate"]) == results["Turnout"]).all()

        # Drop blank columns plus those that can be calculated
        cols_to_drop = [""] + [c for c in cols if "Voteshare" in c] + ["Total votes", "Turnout"]
        results = results.drop(columns=cols_to_drop)

        # Sanitise column names
        results.columns = [utils.sanitise(c) for c in results.columns]
        results = results.rename(columns={"id": "ons_id", "country/region": "region"})
        results.columns = [c.replace("_votes", "") for c in results.columns]

        # Reshape to long
        results_long = pd.melt(
            results,
            id_vars=["ons_id", "constituency", "county", "region", "country", "electorate"],
            var_name="party",
            value_name="votes",
        )
        assert results.shape == (650, 19)
        assert results_long.shape == (650 * len(parties), 19 - len(parties) + 2)

        # Sort by (ons_id, party)
        results_long["party"] = pd.Categorical(
            results_long.party, categories=pd.Series(parties).apply(sanitise), ordered=True
        )
        results_long = results_long.sort_values(["ons_id", "party"]).reset_index(drop=True)

        # Re-add total_votes & voteshare
        results_long["total_votes"] = results_long.ons_id.map(results_long.groupby("ons_id").votes.sum().astype(int))
        results_long["voteshare"] = results_long["votes"] / results_long["total_votes"]
        results_long["turnout"] = results_long["total_votes"] / results_long["electorate"]

        # Reorder cols for export
        results_long = results_long[
            [
                "ons_id",
                "constituency",
                "county",
                "region",
                "country",
                "electorate",
                "total_votes",
                "turnout",
                "party",
                "votes",
                "voteshare",
            ]
        ].copy()

        return results_long

    def process(self):
        """Process results data for a UK General Election."""
        filename = self.sources[0][1]
        processed_results_location = self.directory / "processed" / self.target[0]
        os.makedirs(self.directory / "processed", exist_ok=True)  # create directory if it doesn't exist

        def process_and_export():
            # Either caching disabled or file not yet processed; process regardless.
            results = self.process_hoc_sheet(input_file=filename, data_dir=self.directory, sheet_name=str(self.year))
            # Export
            print(f"Exporting dataset to {processed_results_location.resolve()}")
            results.to_csv(processed_results_location, index=False)

        utils.retrieve_from_cache_if_exists(
            filename=self.target[0],
            target_dir=(self.directory / "processed"),
            processing_fn=process_and_export,
            md5_checksum=self.target[1],
            caching_enabled=self.cache,
            verbose=self.verbose,
        )


class UKModel(Pipeline):
    """Generates model-ready data for UK General Elections."""

    pass
