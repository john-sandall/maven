"""
Model-ready dataset for the United Kingdom's 2015 General Election.

Usage:
    > import maven
    > maven.get('general-election/UK/2015/model', data_directory='./data/')
"""
import os
from pathlib import Path

import pandas as pd

from maven import utils
from maven.datasets.general_election.base import Pipeline


class UK2015Model(Pipeline):
    """Generates model-ready data for the United Kingdom's 2015 General Election."""

    def __init__(self, directory=Path("data/general-election/UK/2015/model")):
        super(UK2015Model, self).__init__(directory=directory)  # inherit base __init__ but override default directory
        self.sources = [
            # tuples of (url, filename, checksum)
            (
                "general-election/UK/2010/results",
                "general_election-uk-2010-results.csv",
                "954a0916f5ce791ca566484ce566088d",
            ),
            (
                "general-election/UK/2015/results",
                "general_election-uk-2015-results.csv",
                "9a785cb19275e4dbc79da67eece6067f",
            ),
            ("general-election/UK/polls", "general_election-uk-polls.csv", "98f865803c782e1ffd0cdc4774707ae5"),
            ("general-election/UK/polls", "general_election-london-polls.csv", "97eb4254039a6bca1a882a9afde2b067"),
            ("general-election/UK/polls", "general_election-scotland-polls.csv", "096354c852a7c30e22a733eec133b9e3"),
            ("general-election/UK/polls", "general_election-wales-polls.csv", "2134d55e5288bd5b12be2471f4aacab7"),
            ("general-election/UK/polls", "general_election-ni-polls.csv", "ea871fad0ce51c03dda09ecec0377dc6"),
        ]
        self.retrieve_all = True
        self.verbose_name = "UK2015Model"
        self.year = 2015

    def process(self):
        """Process results data from the United Kingdom's 2010 and 2015 General Elections
           into a single model-ready dataset for predicting the 2015 General Election."""
        processed_directory = self.directory / "processed"
        os.makedirs(processed_directory, exist_ok=True)  # create directory if it doesn't exist

        #############
        # IMPORT DATA
        #############
        train = 2010
        test = 2015
        pred = 2017
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
        }
        winner_fixes = {
            2010: [
                # https://en.wikipedia.org/wiki/Fermanagh_and_South_Tyrone_(UK_Parliament_constituency)
                ("N06000007", "sf"),  # SF = 21,304, Independent Unionist (with DUP support) = 21,300, Independent = 188
            ]
        }

        # Import general election results
        results = {}
        results[train] = pd.read_csv(self.directory / "raw" / f"general_election-uk-{train}-results.csv")
        results[test] = pd.read_csv(self.directory / "raw" / f"general_election-uk-{test}-results.csv")
        # Add geos
        results[train]["geo"] = results[train].region.map(geo_lookup)
        results[test]["geo"] = results[test].region.map(geo_lookup)
        # ge_2010 = pd.read_csv(self.directory / "raw" / "general_election-uk-2010-results.csv")
        # ge_2015 = pd.read_csv(self.directory / "raw" / "general_election-uk-2015-results.csv")
        polls = {}
        for geo in geos:
            polls[geo] = pd.read_csv(
                self.directory / "raw" / f"general_election-{geo}-polls.csv", parse_dates=["to"]
            ).sort_values("to")

        # Check constituencies are mergeable
        assert (results[train].sort_values("ons_id").ons_id == results[test].sort_values("ons_id").ons_id).all()

        #########
        # POLLING
        #########

        election_dates = {d.year: d for d in [pd.to_datetime(x) for x in ["2010-05-06", "2015-05-07", "2017-06-08"]]}
        for year in [test, pred]:
            election_day = election_dates[year]
            one_week_before = election_day - pd.Timedelta(days=7)
            one_month_before = election_day - pd.Timedelta(days=30)

            # TODO: Remove if not needed
            # # Look at pollsters active in final month before each election
            # pollsters = polls["uk"][
            #     (polls["uk"].to >= one_month_before) & (polls["uk"].to < election_day)
            # ].company.unique()

            # Use single last poll from each pollster in final week of polling then average out
            final_polls = {}
            for geo in geos:
                final_polls[geo] = (
                    polls[geo][(polls[geo].to >= one_week_before) & (polls[geo].to < election_day)]
                    .groupby("company")
                    .tail(1)
                )

            # Calculate regional polling
            if year == 2015:
                parties = ["con", "lab", "ld", "ukip", "grn"]
                # Create new polls dictionary by geo containing simple average across all pollsters
                national_polling = final_polls["uk"].mean().loc[parties]
                # We don't yet have regional polling in 2015 for Scotland, Wales, NI, London - add as other.
                national_polling["other"] = 1 - national_polling.sum()
                poll_of_polls = {"uk": national_polling}

                # Export
                polls_csv_list = []
                for geo in poll_of_polls:
                    polls_csv_list.append(
                        pd.DataFrame(
                            {"geo": geo, "party": poll_of_polls[geo].index, "voteshare": poll_of_polls[geo]}
                        ).reset_index(drop=True)
                    )
                polls_csv = pd.concat(polls_csv_list, axis=0)
                polls_csv.to_csv(processed_directory / f"final_polls_{year}.csv", index=False)
            elif year == 2017:
                parties = {
                    "uk": ["con", "lab", "ld", "ukip", "grn", "snp"],
                    "scotland": ["con", "lab", "ld", "ukip", "grn", "snp"],
                    "wales": ["con", "lab", "ld", "ukip", "grn", "pc"],
                    "ni": ["con", "ukip", "grn"],
                    "london": ["con", "lab", "ld", "ukip", "grn"],
                    "england_not_london": ["con", "lab", "ld", "ukip", "grn"],
                }
                all_parties = set([x for y in parties.values() for x in y])
                poll_of_polls = {}
                for geo in geos:
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
                for geo in geos + ["england_not_london"]:
                    poll_of_polls[geo]["other"] = 1 - poll_of_polls[geo].sum()

                # Export
                polls_csv_list = []
                for geo in poll_of_polls:
                    polls_csv_list.append(
                        pd.DataFrame(
                            {"geo": geo, "party": poll_of_polls[geo].index, "voteshare": poll_of_polls[geo]}
                        ).reset_index(drop=True)
                    )
                polls_csv = pd.concat(polls_csv_list, axis=0)
                polls_csv.to_csv(processed_directory / f"final_polls_{year}.csv", index=False)

            # If year is 2015, last_election is 2010
            last_election = train if year == test else test
            # Use res for code readability and write back into results[last_election] at the end
            res = results[last_election].copy()

            # Merge into previous election's results to calculate swing
            res = (
                res.merge(
                    right=polls_csv.query('geo == "uk"')[["party", "voteshare"]].rename(
                        columns={"voteshare": "national_polls"}
                    ),
                    on="party",
                    how="outer",
                )
                .sort_values(["ons_id", "party"])
                .reset_index(drop=True)
            )
            # If we have geo-polls, add those too
            if list(poll_of_polls.keys()) != ["uk"]:
                res = (
                    res.merge(
                        right=polls_csv.query('geo != "uk"')[["geo", "party", "voteshare"]].rename(
                            columns={"voteshare": "geo_polls"}
                        ),
                        on=["geo", "party"],
                        how="outer",
                    )
                    .sort_values(["ons_id", "party"])
                    .reset_index(drop=True)
                )

            #############################
            # Calculate uplifts ("swing")
            #############################

            # Calculate national voteshare
            national_voteshare_by_party = res.groupby("party").votes.sum() / res.votes.sum()
            res["national_voteshare"] = res.party.map(national_voteshare_by_party)

            # Calculate swing between last election results and latest poll-of-polls
            res["national_swing"] = (res.national_polls / res.national_voteshare) - 1

            # Forecast is previous result multiplied by swing uplift
            res["national_swing_forecast"] = res.voteshare * (1 + res.national_swing)

            # Predict the winner in each constituency using national_swing_forecast
            # Note: these are pointless for NI as polls/swings are all aggregated under "other" but results
            # are given per major party.
            national_swing_winners = utils.calculate_winners(res, "national_swing_forecast")
            res["national_swing_winner"] = res.ons_id.map(national_swing_winners)

            # Add the winner for the results
            winners = utils.calculate_winners(res, "voteshare")
            res["winner"] = res.ons_id.map(winners)

            # Apply fixes
            if last_election in winner_fixes:
                for ons_id, actual_winner in winner_fixes[last_election]:
                    res.loc[res.ons_id == ons_id, "winner"] = actual_winner

            # Check this matches the results on record
            seat_count = res[["ons_id", "winner"]].drop_duplicates().groupby("winner").size()
            assert dict(seat_count) == results_seat_count[last_election]

            ########################################################
            # Calculate Geo-Level Voteshare + Swing inc. all parties
            ########################################################

            if "geo_polls" in res.columns:
                # Calculate geo-level voteshare
                votes_by_geo = res.groupby("geo").votes.sum().reset_index()
                votes_by_geo_by_party = (
                    res.groupby(["geo", "party"])
                    .votes.sum()
                    .reset_index()
                    .merge(votes_by_geo, on="geo", how="left", suffixes=("", "_geo"))
                )
                votes_by_geo_by_party["geo_voteshare"] = votes_by_geo_by_party.votes / votes_by_geo_by_party.votes_geo
                res = res.merge(
                    votes_by_geo_by_party[["geo", "party", "geo_voteshare"]], on=["geo", "party"], how="left"
                )

                # Calculate geo-swing between last election results and latest geo-polls
                res["geo_swing"] = (res.geo_polls / res.geo_voteshare) - 1

                # Forecast is previous result multiplied by swing uplift
                res["geo_swing_forecast"] = res.voteshare * (1 + res.national_swing)

                # Predict the winner in each constituency using geo_swing_forecast
                geo_swing_winners = utils.calculate_winners(res, "geo_swing_forecast")
                res["geo_swing_winner"] = res.ons_id.map(geo_swing_winners)

            # Put res back into results[last_election]
            results[last_election] = res.copy()

        ###########################
        # Create ML-ready dataframe
        ###########################

        # Use "last" and "now" in order to re-use this code for either train->test or test->pred.
        last = train
        now = test
        df = (
            results[now][
                [
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
                ]
            ]
            .rename(
                columns={
                    "total_votes": "total_votes_now",
                    "turnout": "turnout_now",
                    "votes": "votes_now",
                    "voteshare": "voteshare_now",
                }
            )
            .merge(
                results[last][
                    [
                        "ons_id",
                        "party",
                        "votes",
                        "voteshare",
                        "national_polls",
                        "national_voteshare",
                        "national_swing",
                        "national_swing_forecast",
                        "national_swing_winner",
                    ]
                ].rename(
                    columns={
                        "votes": "votes_last",
                        "voteshare": "voteshare_last",
                        "national_polls": "national_polls_now",
                        "national_voteshare": "national_voteshare_last",
                    }
                )
            )
        )

        ### GOT TO HERE - double check the polls and swing forecasts in last vs now, national_swing_winner pertains to which year?! ###

        # polls_now
        df["polls_now"] = df.party.map(polls["UK"])

        # swing_now
        swing_now = pd.melt(
            ge_2010[["Press Association Reference"] + [p + "_swing" for p in parties]],
            id_vars=["Press Association Reference"],
            value_vars=[p + "_swing" for p in parties],
            var_name="party",
            value_name="swing_now",
        )
        swing_now["party"] = swing_now.party.apply(lambda x: x.replace("_swing", ""))

        df = pd.merge(left=df, right=swing_now, how="left", on=["Press Association Reference", "party"],)

        # swing_forecast_pc
        swing_forecast_pc = pd.melt(
            ge_2010[["Press Association Reference"] + [p + "_forecast" for p in parties]],
            id_vars=["Press Association Reference"],
            value_vars=[p + "_forecast" for p in parties],
            var_name="party",
            value_name="swing_forecast_pc",
        )
        swing_forecast_pc["party"] = swing_forecast_pc.party.apply(lambda x: x.replace("_forecast", ""))

        df = pd.merge(left=df, right=swing_forecast_pc, how="left", on=["Press Association Reference", "party"],)

        # swing_forecast_win
        swing_forecast_win = ge_2010[["Press Association Reference", "win_15"]]
        swing_forecast_win.columns = ["Press Association Reference", "swing_forecast_win"]
        df = pd.merge(left=df, right=swing_forecast_win, on=["Press Association Reference"])

        # actual_win_now
        actual_win_now = ge_2010[["Press Association Reference", "act_15"]]
        actual_win_now.columns = ["Press Association Reference", "actual_win_now"]
        df = pd.merge(left=df, right=actual_win_now, on=["Press Association Reference"])

        # actual_pc_now
        actual_pc_now = pd.melt(
            ge_2010[["Press Association Reference"] + [p + "_actual" for p in parties]],
            id_vars=["Press Association Reference"],
            value_vars=[p + "_actual" for p in parties],
            var_name="party",
            value_name="actual_pc_now",
        )
        actual_pc_now["party"] = actual_pc_now.party.apply(lambda x: x.replace("_actual", ""))

        df = pd.merge(left=df, right=actual_pc_now, how="left", on=["Press Association Reference", "party"],)

        # dummy party
        df = pd.concat([df, pd.get_dummies(df.party)], axis=1)

        # dummy region
        df = pd.concat([df, pd.get_dummies(df.Region, prefix="Region")], axis=1)

        # won_here_last
        df["won_here_last"] = (df["party"] == df["win_last"]).astype("int")

        # turnout
        df["turnout"] = df.Votes / df.Electorate

        # parties = ["con", "lab", "ld", "ukip", "grn"]
        # act_15_lookup = {k: v for i, (k, v) in ge_2015[["Press Association ID Number", "winner"]].iterrows()}
        # ge_2010["act_15"] = ge_2010["Press Association Reference"].map(act_15_lookup)
        # pc_15_lookup = {
        #     p: {k: v for i, (k, v) in ge_2015[["Press Association ID Number", p + "_pc"]].iterrows()} for p in parties
        # }
        # for p in parties:
        #     ge_2010[p + "_actual"] = ge_2010["Press Association Reference"].map(pc_15_lookup[p])

        # df = ge_2010[["Press Association Reference", "Constituency Name", "Region", "Electorate", "Votes",] + parties]
        # df = pd.melt(
        #     df,
        #     id_vars=["Press Association Reference", "Constituency Name", "Region", "Electorate", "Votes",],
        #     value_vars=parties,
        #     var_name="party",
        #     value_name="votes_last",
        # )

        # # pc_last
        # pc_last = pd.melt(
        #     ge_2010[["Press Association Reference"] + [p + "_pc" for p in parties]],
        #     id_vars=["Press Association Reference"],
        #     value_vars=[p + "_pc" for p in parties],
        #     var_name="party",
        #     value_name="pc_last",
        # )
        # pc_last["party"] = pc_last.party.apply(lambda x: x.replace("_pc", ""))
        # df = pd.merge(left=df, right=pc_last, how="left", on=["Press Association Reference", "party"],)

        # # win_last
        # win_last = ge_2010[["Press Association Reference", "winner"]]
        # win_last.columns = ["Press Association Reference", "win_last"]
        # df = pd.merge(left=df, right=win_last, on=["Press Association Reference"])

        # # polls_now
        # df["polls_now"] = df.party.map(polls["UK"])

        # # swing_now
        # swing_now = pd.melt(
        #     ge_2010[["Press Association Reference"] + [p + "_swing" for p in parties]],
        #     id_vars=["Press Association Reference"],
        #     value_vars=[p + "_swing" for p in parties],
        #     var_name="party",
        #     value_name="swing_now",
        # )
        # swing_now["party"] = swing_now.party.apply(lambda x: x.replace("_swing", ""))

        # df = pd.merge(left=df, right=swing_now, how="left", on=["Press Association Reference", "party"],)

        # # swing_forecast_pc
        # swing_forecast_pc = pd.melt(
        #     ge_2010[["Press Association Reference"] + [p + "_forecast" for p in parties]],
        #     id_vars=["Press Association Reference"],
        #     value_vars=[p + "_forecast" for p in parties],
        #     var_name="party",
        #     value_name="swing_forecast_pc",
        # )
        # swing_forecast_pc["party"] = swing_forecast_pc.party.apply(lambda x: x.replace("_forecast", ""))

        # df = pd.merge(left=df, right=swing_forecast_pc, how="left", on=["Press Association Reference", "party"],)

        # # swing_forecast_win
        # swing_forecast_win = ge_2010[["Press Association Reference", "win_15"]]
        # swing_forecast_win.columns = ["Press Association Reference", "swing_forecast_win"]
        # df = pd.merge(left=df, right=swing_forecast_win, on=["Press Association Reference"])

        # # actual_win_now
        # actual_win_now = ge_2010[["Press Association Reference", "act_15"]]
        # actual_win_now.columns = ["Press Association Reference", "actual_win_now"]
        # df = pd.merge(left=df, right=actual_win_now, on=["Press Association Reference"])

        # # actual_pc_now
        # actual_pc_now = pd.melt(
        #     ge_2010[["Press Association Reference"] + [p + "_actual" for p in parties]],
        #     id_vars=["Press Association Reference"],
        #     value_vars=[p + "_actual" for p in parties],
        #     var_name="party",
        #     value_name="actual_pc_now",
        # )
        # actual_pc_now["party"] = actual_pc_now.party.apply(lambda x: x.replace("_actual", ""))

        # df = pd.merge(left=df, right=actual_pc_now, how="left", on=["Press Association Reference", "party"],)

        # # dummy party
        # df = pd.concat([df, pd.get_dummies(df.party)], axis=1)

        # # dummy region
        # df = pd.concat([df, pd.get_dummies(df.Region, prefix="Region")], axis=1)

        # # won_here_last
        # df["won_here_last"] = (df["party"] == df["win_last"]).astype("int")

        # # turnout
        # df["turnout"] = df.Votes / df.Electorate

        ########################################
        # Export final 2010 -> 2015 training set
        ########################################
        print(f"Exporting 2010->2015 model dataset to {processed_directory.resolve()}")
        df.to_csv(processed_directory / "general_election-uk-2015-model.csv", index=False)

        ######################
        # REPEAT FOR 2015-2017
        ######################
        # Recreate this training dataset using same column names for 2015 -> 2017 for a GE2017 forecast
        # TODO: Needs refactoring!
        # Add SNP and Plaid Cymru
        parties += ["snp", "pc"]
        df15 = ge_2015[
            ["Press Association ID Number", "Constituency Name", "Region", "geo", "Electorate", "Valid Votes",]
            + parties
        ]
        df15.columns = [
            "Press Association ID Number",
            "Constituency Name",
            "Region",
            "geo",
            "Electorate",
            "Votes",
        ] + parties
        df15 = pd.melt(
            df15,
            id_vars=["Press Association ID Number", "Constituency Name", "Region", "geo", "Electorate", "Votes",],
            value_vars=parties,
            var_name="party",
            value_name="votes_last",
        )

        # pc_last
        pc_last = pd.melt(
            ge_2015[["Press Association ID Number"] + [p + "_pc" for p in parties]],
            id_vars=["Press Association ID Number"],
            value_vars=[p + "_pc" for p in parties],
            var_name="party",
            value_name="pc_last",
        )
        pc_last["party"] = pc_last.party.apply(lambda x: x.replace("_pc", ""))

        df15 = pd.merge(left=df15, right=pc_last, how="left", on=["Press Association ID Number", "party"],)

        # win_last
        win_last = ge_2015[["Press Association ID Number", "winner"]]
        win_last.columns = ["Press Association ID Number", "win_last"]
        df15 = pd.merge(left=df15, right=win_last, on=["Press Association ID Number"])

        # polls_now <- USE REGIONAL POLLING! (Possibly a very bad idea, the regional UNS performed worse than national!)
        df15["polls_now"] = df15.apply(lambda row: polls_17[row.geo][row.party], axis=1)

        # swing_now
        swing_now = pd.melt(
            ge_2015[["Press Association ID Number"] + [p + "_swing" for p in parties]],
            id_vars=["Press Association ID Number"],
            value_vars=[p + "_swing" for p in parties],
            var_name="party",
            value_name="swing_now",
        )
        swing_now["party"] = swing_now.party.apply(lambda x: x.replace("_swing", ""))

        df15 = pd.merge(left=df15, right=swing_now, how="left", on=["Press Association ID Number", "party"],)

        # swing_forecast_pc
        swing_forecast_pc = pd.melt(
            ge_2015[["Press Association ID Number"] + [p + "_2017_forecast" for p in parties]],
            id_vars=["Press Association ID Number"],
            value_vars=[p + "_2017_forecast" for p in parties],
            var_name="party",
            value_name="swing_forecast_pc",
        )
        swing_forecast_pc["party"] = swing_forecast_pc.party.apply(lambda x: x.replace("_2017_forecast", ""))

        df15 = pd.merge(left=df15, right=swing_forecast_pc, how="left", on=["Press Association ID Number", "party"],)

        # swing_forecast_win
        swing_forecast_win = ge_2015[["Press Association ID Number", "win_17"]]
        swing_forecast_win.columns = ["Press Association ID Number", "swing_forecast_win"]
        df15 = pd.merge(left=df15, right=swing_forecast_win, on=["Press Association ID Number"])

        # dummy party
        df15 = pd.concat([df15, pd.get_dummies(df15.party)], axis=1)

        # dummy region
        df15 = pd.concat([df15, pd.get_dummies(df15.Region, prefix="Region")], axis=1)

        # won_here_last
        df15["won_here_last"] = (df15["party"] == df15["win_last"]).astype("int")

        # turnout
        df15["turnout"] = df.Votes / df.Electorate

        ##########################################
        # Export final 2015 -> 2017 prediction set
        ##########################################
        print(f"Exporting 2015->2017 model dataset to {processed_directory.resolve()}")
        df15.to_csv(processed_directory / "general_election-uk-2017-model.csv", index=False)
