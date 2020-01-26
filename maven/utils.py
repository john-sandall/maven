"""
Various helper functions.
"""

import pandas as pd


def sanitise(x):
    return x.lower().replace(" ", "_")


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
    assert (results[[f"{party}_Votes" for party in parties]].fillna(0.0).sum(axis=1) == results["Total votes"]).all()
    assert ((results["Total votes"] / results["Electorate"]) == results["Turnout"]).all()

    # Drop blank columns plus those that can be calculated
    cols_to_drop = [""] + [c for c in cols if "Voteshare" in c] + ["Total votes", "Turnout"]
    results = results.drop(columns=cols_to_drop)

    # Sanitise column names
    results.columns = [sanitise(c) for c in results.columns]
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
