"""
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest ./tests/datasets/general_election/test_uk_models.py

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest ./tests/datasets/general_election/test_uk_models.py
"""

from pathlib import Path

import pandas as pd

import maven


def check_uk_model_output(identifier, output_file):
    maven.get(identifier, data_directory="./data/")
    df = pd.read_csv(Path("./data") / identifier / "processed" / output_file)
    geo_columns = []
    target_columns = []
    if "geo_polls_now" in df.columns:
        geo_columns += [
            "geo_polls_now",
            "geo_voteshare_last",
            "geo_swing",
            "geo_swing_forecast",
            "geo_swing_winner",
        ]
    if "total_votes_now" in df.columns:
        target_columns += ["total_votes_now", "turnout_now", "votes_now", "voteshare_now", "winner_now"]
    column_list = (
        [
            "ons_id",
            "constituency",
            "county",
            "region",
            "geo",
            "country",
            "electorate",
            "total_votes_last",
            "turnout_last",
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
        + geo_columns
        + target_columns
    )
    assert df.shape == (7800, len(column_list))
    assert df.columns.tolist() == column_list


def test_uk_2015_model():
    check_uk_model_output(identifier="general-election/UK/2015/model", output_file="general_election-uk-2015-model.csv")


def test_uk_2017_model():
    check_uk_model_output(identifier="general-election/UK/2017/model", output_file="general_election-uk-2017-model.csv")


def test_uk_2019_model():
    check_uk_model_output(identifier="general-election/UK/2019/model", output_file="general_election-uk-2019-model.csv")
