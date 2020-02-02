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
            results_long.party, categories=pd.Series(parties).apply(utils.sanitise), ordered=True
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

    # geos sit between region and country (e.g. "england_not_london") and map to things we can extract from polls
    geos = ["uk", "scotland", "wales", "ni", "london"]
    geo_lookup = {
        "Northern Ireland": "ni",
        "Scotland": "scotland",
        "Wales": "wales",
        "London": "london",
        "South East": "england_not_london",
        "West Midlands": "england_not_london",
        "North West": "england_not_london",
        "East Midlands": "england_not_london",
        "Yorkshire and The Humber": "england_not_london",
        "Eastern": "england_not_london",
        "South West": "england_not_london",
        "North East": "england_not_london",
    }

    results_seat_count = {
        2010: {
            "con": 306,
            "lab": 258,
            "ld": 57,
            "dup": 8,
            "snp": 6,
            "sf": 5,
            "pc": 3,
            "sdlp": 3,
            "grn": 1,
            "apni": 1,
            "other": 2,  # {'speaker': 'John Bercow', 'independent': 'Sylvia Hermon'}
        },
        2015: {
            "con": 330,
            "lab": 232,
            "snp": 56,
            "ld": 8,
            "dup": 8,
            "sf": 4,
            "pc": 3,
            "sdlp": 3,
            "uup": 2,
            "ukip": 1,
            "grn": 1,
            "other": 2,  # {'speaker': 'John Bercow', 'independent': 'Sylvia Hermon'}
        },
        2017: {
            "con": 317,
            "lab": 262,
            "snp": 35,
            "ld": 12,
            "dup": 10,
            "sf": 7,
            "pc": 4,
            "grn": 1,
            "other": 2,  # {'speaker': 'John Bercow', 'independent': 'Sylvia Hermon'}
        },
    }

    winner_fixes = {
        2010: [
            # https://en.wikipedia.org/wiki/Fermanagh_and_South_Tyrone_(UK_Parliament_constituency)
            ("N06000007", "sf"),  # SF = 21,304, Independent Unionist (with DUP support) = 21,300, Independent = 188
        ]
    }

    # Define these to make them available as expected attributes.
    last_date = None
    now_date = None
    last = None
    now = None

    def load_results_data(self):
        """Load UK General Election results for consecutive elections with one row / party / constituency and add:
             - `geo`: geo this constituency is in (e.g. `scotland`, `england_not_london`)
             - `winner`: winner per constituency (derived from data, with corrections to match reported results)
             - `won_here`: did this party win this seat?

        Args:
            last (int): Year of prior election (used to provide historical trend information).
            now (int):  Year of election to be modelled.

        Returns: dict containing key-value pairs of (year, pd.DataFrame) of results.
        """
        # Define these for code readability
        last = self.last
        now = self.now

        # Import general election results
        results = {}
        results[last] = pd.read_csv(self.directory / "raw" / f"general_election-uk-{last}-results.csv")
        results[now] = pd.read_csv(self.directory / "raw" / f"general_election-uk-{now}-results.csv")
        # Add geos
        results[last]["geo"] = results[last].region.map(self.geo_lookup)
        results[now]["geo"] = results[now].region.map(self.geo_lookup)

        # Check constituencies are mergeable
        assert (results[last].sort_values("ons_id").ons_id == results[now].sort_values("ons_id").ons_id).all()

        # Add the winner for the results
        for year in [last, now]:
            res = results[year].copy()
            winners = self.calculate_winners(res, "voteshare")
            res["winner"] = res.ons_id.map(winners)

            # Apply fixes
            if year in self.winner_fixes:
                for ons_id, actual_winner in self.winner_fixes[year]:
                    res.loc[res.ons_id == ons_id, "winner"] = actual_winner

            # Check this matches the results on record
            seat_count = res[["ons_id", "winner"]].drop_duplicates().groupby("winner").size()
            assert dict(seat_count) == self.results_seat_count[year]

            # Add boolean per row for if this party won this seat
            res["won_here"] = res.party == res.winner
            results[year] = res.copy()

        return results

    def load_polling_data(self):
        """Load polling data for UK General Elections."""
        polls = {}
        for geo in self.geos:
            polls[geo] = pd.read_csv(
                self.directory / "raw" / f"general_election-{geo}-polls.csv", parse_dates=["to"]
            ).sort_values("to")

        return polls

    @staticmethod
    def calculate_poll_of_polls(polls, from_date, to_date):
        return polls[(polls.to >= from_date) & (polls.to < to_date)].groupby("company").tail(1)

    def get_regional_and_national_poll_of_polls(self, polls):
        """Takes straight average across each pollster's final poll in last week prior to election day.
            Repeat for regions, if regional polling is available.
        """
        election_day = self.now_date
        one_week_before = election_day - pd.Timedelta(days=7)

        # Use single last poll from each pollster in final week of polling then average out
        final_polls = {}
        for geo in self.geos:
            final_polls[geo] = self.calculate_poll_of_polls(
                polls=polls[geo], from_date=one_week_before, to_date=election_day
            )

        # Calculate regional polling
        regional_polling_missing = any(final_polls[geo].empty for geo in self.geos)

        # Regional polling is missing, just calculate UK-level polling only.
        if regional_polling_missing:
            parties = ["con", "lab", "ld", "ukip", "grn"]
            # Create new polls dictionary by geo containing simple average across all pollsters
            national_polling = final_polls["uk"].mean().loc[parties]
            # We don't yet have regional polling in 2015 for Scotland, Wales, NI, London - add as other.
            national_polling["other"] = 1 - national_polling.sum()
            poll_of_polls = {"uk": national_polling}
            # Turn into dataframe
            polls_df_list = []
            for geo in poll_of_polls:
                polls_df_list.append(
                    pd.DataFrame(
                        {"geo": geo, "party": poll_of_polls[geo].index, "voteshare": poll_of_polls[geo]}
                    ).reset_index(drop=True)
                )
            polls_df = pd.concat(polls_df_list, axis=0)

        # We have polling for all regions.
        else:
            parties = {
                "uk": ["con", "lab", "ld", "ukip", "grn", "snp"],
                "scotland": ["con", "lab", "ld", "ukip", "grn", "snp"],
                "wales": ["con", "lab", "ld", "ukip", "grn", "pc"],
                "ni": ["con", "ukip", "grn"],
                "london": ["con", "lab", "ld", "ukip", "grn"],
                "england_not_london": ["con", "lab", "ld", "ukip", "grn"],
            }
            all_parties = set(x for y in parties.values() for x in y)
            poll_of_polls = {}
            for geo in self.geos:
                sample_size_weights = final_polls[geo].sample_size / final_polls[geo].sample_size.sum()
                weighted_poll_of_polls = (
                    final_polls[geo][parties[geo]]
                    .multiply(sample_size_weights, axis=0)
                    .sum()
                    .reindex(all_parties, fill_value=0.0)
                )
                poll_of_polls[geo] = weighted_poll_of_polls

            # Estimate polling for England excluding London
            # survation_wts from http://survation.com/wp-content/uploads/2017/06/Final-MoS-Post-BBC-Event-Poll-020617SWCH-1c0d4h9.pdf
            survation_wts = pd.Series({"scotland": 85, "england": 881, "wales": 67, "ni": 16})
            survation_wts["uk"] = survation_wts.sum()
            survation_wts["london"] = 137
            survation_wts["england_not_london"] = survation_wts.england - survation_wts.london

            england_not_london = poll_of_polls["uk"] * survation_wts["uk"]
            for geo in ["scotland", "wales", "ni", "london"]:
                england_not_london = england_not_london.sub(poll_of_polls[geo] * survation_wts[geo], fill_value=0.0)
            england_not_london /= survation_wts["england_not_london"]
            england_not_london.loc[["pc", "snp"]] = 0.0
            poll_of_polls["england_not_london"] = england_not_london

            # Fix PC (Plaid Cymru) for UK
            poll_of_polls["uk"]["pc"] = poll_of_polls["wales"]["pc"] * survation_wts["wales"] / survation_wts["uk"]

            # Add Other
            for geo in self.geos + ["england_not_london"]:
                poll_of_polls[geo]["other"] = 1 - poll_of_polls[geo].sum()

            # Export
            polls_df_list = []
            for geo in poll_of_polls:
                polls_df_list.append(
                    pd.DataFrame(
                        {"geo": geo, "party": poll_of_polls[geo].index, "voteshare": poll_of_polls[geo]}
                    ).reset_index(drop=True)
                )
            polls_df = pd.concat(polls_df_list, axis=0)

        return polls_df

    @staticmethod
    def combine_results_and_polls(results, polls):
        """Merge national polling, and geo-level polling if available, into results dataframe."""
        # Merge into previous election's results to calculate swing
        results = (
            results.merge(
                right=polls.query('geo == "uk"')[["party", "voteshare"]].rename(
                    columns={"voteshare": "national_polls"}
                ),
                on="party",
                how="outer",
            )
            .sort_values(["ons_id", "party"])
            .reset_index(drop=True)
        )
        # If we have geo-polls, add those too
        if set(polls.geo.unique()) != {"uk"}:
            results = (
                results.merge(
                    right=polls.query('geo != "uk"')[["geo", "party", "voteshare"]].rename(
                        columns={"voteshare": "geo_polls"}
                    ),
                    on=["geo", "party"],
                    how="outer",
                )
                .sort_values(["ons_id", "party"])
                .reset_index(drop=True)
            )

        return results

    @staticmethod
    def calculate_winners(df, voteshare_col):
        """Assumes df has `ons_id` and `party` columns."""
        return (
            df.sort_values(voteshare_col, ascending=False)
            .groupby("ons_id")
            .head(1)[["ons_id", "party"]]
            .set_index("ons_id")
            .party
        )

    def calculate_national_swing(self, results):
        """Uses previous election results plus current polling to calculate:
               - `national_voteshare`: per party
               - `national_swing`: from previous voteshare to current polling
               - `national_swing_forecast`: forecasted voteshare per party per seat
               - `national_swing_winner`: per seat

        Returns: updated results dataframe with new columns.
        """
        # Calculate national voteshare
        national_voteshare_by_party = results.groupby("party").votes.sum() / results.votes.sum()
        results["national_voteshare"] = results.party.map(national_voteshare_by_party)

        # Calculate swing between last election results and latest poll-of-polls
        results["national_swing"] = (results.national_polls / results.national_voteshare) - 1

        # Forecast is previous result multiplied by swing uplift
        results["national_swing_forecast"] = results.voteshare * (1 + results.national_swing)

        # Predict the winner in each constituency using national_swing_forecast
        # Note: these are pointless for NI as polls/swings are all aggregated under "other" but results
        # are given per major party.
        national_swing_winners = self.calculate_winners(results, "national_swing_forecast")
        results["national_swing_winner"] = results.ons_id.map(national_swing_winners)

        return results

    def calculate_geo_swing(self, results):
        """Calculate geo-Level voteshare + swing inc. all parties. Adds:
               - `geo_voteshare`: geo-level voteshare (per party).
               - `geo_swing`: swing from previous geo_voteshare to current geo-polling.
               - `geo_swing_forecast`: geo-swing based forecast per party per seat.
               - `geo_swing_winner`: per seat.

        Returns: updated results dataframe with new columns.
        """

        # Calculate geo-level voteshare
        votes_by_geo = results.groupby("geo").votes.sum().reset_index()
        votes_by_geo_by_party = (
            results.groupby(["geo", "party"])
            .votes.sum()
            .reset_index()
            .merge(votes_by_geo, on="geo", how="left", suffixes=("", "_geo"))
        )
        votes_by_geo_by_party["geo_voteshare"] = votes_by_geo_by_party.votes / votes_by_geo_by_party.votes_geo
        results = results.merge(
            votes_by_geo_by_party[["geo", "party", "geo_voteshare"]], on=["geo", "party"], how="left"
        )

        # Calculate geo-swing between last election results and latest geo-polls
        results["geo_swing"] = (results.geo_polls / results.geo_voteshare) - 1

        # Forecast is previous result multiplied by swing uplift
        results["geo_swing_forecast"] = results.voteshare * (1 + results.geo_swing)

        # Predict the winner in each constituency using geo_swing_forecast
        geo_swing_winners = self.calculate_winners(results, "geo_swing_forecast")
        results["geo_swing_winner"] = results.ons_id.map(geo_swing_winners)

        return results

    def export_model_ready_dataframe(self, results_dict):
        """Create ML-ready dataframe and export."""
        df_cols_now = [
            "ons_id",
            "constituency",
            "county",
            "region",
            "geo",
            "country",
            "electorate",
            "total_votes",
            "turnout",
            "party",
            "votes",
            "voteshare",
            "winner",
        ]
        df_cols_last = [
            "ons_id",
            "party",
            "total_votes",
            "turnout",
            "votes",
            "voteshare",
            "national_polls",
            "national_voteshare",
            "national_swing",
            "national_swing_forecast",
            "national_swing_winner",
            "winner",
            "won_here",
        ]
        df_cols_final_geo = []
        if "geo_polls" in results_dict[self.last].columns:
            df_cols_last += ["geo_polls", "geo_voteshare", "geo_swing", "geo_swing_forecast", "geo_swing_winner"]
            df_cols_final_geo += [
                "geo_polls_now",
                "geo_voteshare_last",
                "geo_swing",
                "geo_swing_forecast",
                "geo_swing_winner",
            ]
        df_cols_final = (
            [
                # Constant per constituency
                "ons_id",
                "constituency",
                "county",
                "region",
                "geo",
                "country",
                "electorate",
                "total_votes_last",
                "turnout_last",
                # Constant per party (per constituency)
                "party",
                "votes_last",
                "voteshare_last",
                "winner_last",
                "won_here_last",
                "national_voteshare_last",
                "national_polls_now",
                "national_swing",
                "national_swing_forecast",
                "national_swing_winner",
            ]
            + df_cols_final_geo
            + [
                # Target
                "total_votes_now",
                "turnout_now",
                "votes_now",
                "voteshare_now",
                "winner_now",
            ]
        )
        df = (
            results_dict[self.now][df_cols_now]
            .rename(
                columns={
                    "total_votes": "total_votes_now",
                    "turnout": "turnout_now",
                    "votes": "votes_now",
                    "voteshare": "voteshare_now",
                    "winner": "winner_now",
                }
            )
            .merge(
                # Note: even though polling represents "now", they're in results[last] to calculate swings.
                results_dict[self.last][df_cols_last].rename(
                    columns={
                        "total_votes": "total_votes_last",
                        "turnout": "turnout_now_last",
                        "votes": "votes_last",
                        "voteshare": "voteshare_last",
                        "national_polls": "national_polls_now",
                        "geo_polls": "geo_polls_now",
                        "national_voteshare": "national_voteshare_last",
                        "geo_voteshare": "geo_voteshare_last",
                        "winner": "winner_last",
                        "won_here": "won_here_last",
                    }
                ),
                on=["ons_id", "party"],
                how="inner",
                validate="1:1",
            )
            .filter(df_cols_final)
        )

        return df

    def process(self):
        """Process results data from consecutive UK General Elections (e.g. 2010 and 2015) into a single model-ready
           dataset ready for predicting the later (e.g. 2015) election."""
        processed_directory = self.directory / "processed"
        os.makedirs(processed_directory, exist_ok=True)  # create directory if it doesn't exist

        # Import general election results & polling data
        results_dict = self.load_results_data()
        polls_full = self.load_polling_data()

        # Calculate poll of polls
        polls = self.get_regional_and_national_poll_of_polls(polls=polls_full)

        # Merge polls into previous election results dataframe
        results_dict[self.last] = self.combine_results_and_polls(results=results_dict[self.last], polls=polls)

        # Add into previous election results: national voteshare, national swing (vs current polling),
        # national swing forecast (per party per seat) and national swing forecast winner (per seat).
        results_dict[self.last] = self.calculate_national_swing(results_dict[self.last])

        # If we have geo-polling for previous election, also calculate a geo-level swing forecast.
        if "geo_polls" in results_dict[self.last].columns:
            results_dict[self.last] = self.calculate_geo_swing(results_dict[self.last])

        # Create ML-ready dataframe and export
        model_df = self.export_model_ready_dataframe(results_dict=results_dict)

        print(f"Exporting {self.last}->{self.now} model dataset to {processed_directory.resolve()}")
        model_df.to_csv(processed_directory / f"general_election-uk-{self.now}-model.csv", index=False)

        # Think this is what we use if predicting and don't have results? Therefore will need to check for 2019 modelling df.
        # df_cols_last = [
        #     "ons_id",
        #     "constituency",
        #     "county",
        #     "region",
        #     "geo",
        #     "country",
        #     "electorate",
        #     "total_votes",
        #     "turnout",
        #     "party",
        #     "votes",
        #     "voteshare",
        #     "winner",
        #     "won_here",
        #     "national_polls",
        #     "national_voteshare",
        #     "national_swing",
        #     "national_swing_forecast",
        #     "national_swing_winner",
        # ]
        # df_cols_final_geo = []
        # if "geo_polls" in results[last].columns:
        #     df_cols_last += ["geo_polls", "geo_voteshare", "geo_swing", "geo_swing_forecast", "geo_swing_winner"]
        #     df_cols_final_geo += [
        #         "geo_polls_now",
        #         "geo_voteshare_last",
        #         "geo_swing",
        #         "geo_swing_forecast",
        #         "geo_swing_winner",
        #     ]
        # df_cols_final = [
        #     # Constant per constituency
        #     "ons_id",
        #     "constituency",
        #     "county",
        #     "region",
        #     "geo",
        #     "country",
        #     "electorate",
        #     "total_votes_last",
        #     "turnout_last",
        #     # Constant per party (per constituency)
        #     "party",
        #     "votes_last",
        #     "voteshare_last",
        #     "winner_last",
        #     "won_here_last",
        #     "national_voteshare_last",
        #     "national_polls_now",
        #     "national_swing",
        #     "national_swing_forecast",
        #     "national_swing_winner",
        # ] + df_cols_final_geo
        # df = (
        #     results[last][df_cols_last]
        #     .rename(
        #         columns={
        #             "total_votes": "total_votes_last",
        #             "turnout": "turnout_last",
        #             "votes": "votes_last",
        #             "voteshare": "voteshare_last",
        #             "national_polls": "national_polls_now",
        #             "geo_polls": "geo_polls_now",
        #             "national_voteshare": "national_voteshare_last",
        #             "geo_voteshare": "geo_voteshare_last",
        #             "winner": "winner_last",
        #             "won_here": "won_here_last",
        #         }
        #     )
        #     .filter(df_cols_final)
        # )
        # print(f"Exporting {last}->{now} model dataset to {processed_directory.resolve()}")
        # df.to_csv(processed_directory / f"general_election-uk-{now}-model.csv", index=False)
