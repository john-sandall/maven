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


def check_uk_model_output(identifier, train_file, pred_file):
    maven.get(identifier, data_directory="./data/")
    df_train = pd.read_csv(Path("./data") / identifier / "processed" / train_file)
    df_pred = pd.read_csv(Path("./data") / identifier / "processed" / pred_file)
    assert df_train.shape == (8450, 23)
    assert df_pred.shape == (8450, 24)
    assert df_train.columns.tolist() == [
        "ons_id",
        "constituency",
        "county",
        "region",
        "geo",
        "country",
        "electorate",
        "total_votes_last",
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
        "total_votes_now",
        "turnout_now",
        "votes_now",
        "voteshare_now",
        "winner_now",
    ]
    assert df_pred.columns.tolist() == [
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
        "geo_polls_now",
        "geo_voteshare_last",
        "geo_swing",
        "geo_swing_forecast",
        "geo_swing_winner",
    ]


def test_uk_2015_model():
    check_uk_model_output(
        identifier="general-election/UK/2015/model",
        train_file="general_election-uk-2015-model.csv",
        pred_file="general_election-uk-2017-model.csv",
    )
