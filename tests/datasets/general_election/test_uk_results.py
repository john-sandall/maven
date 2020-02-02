"""
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest ./tests/datasets/test_uk_models

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest ./tests/datasets/test_uk_models
"""

from pathlib import Path

import pandas as pd

import maven


def check_uk_hoc_results_data(identifier, processed_filename):
    maven.get(identifier, data_directory="./data/")
    df = pd.read_csv(Path("./data") / identifier / "processed" / processed_filename)
    assert df.shape == (8450, 11)
    assert df.columns.tolist() == [
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


def test_uk_2010_results():
    check_uk_hoc_results_data(
        identifier="general-election/UK/2010/results", processed_filename="general_election-uk-2010-results.csv"
    )


def test_uk_2015_results():
    check_uk_hoc_results_data(
        identifier="general-election/UK/2015/results", processed_filename="general_election-uk-2015-results.csv"
    )


def test_uk_2017_results():
    check_uk_hoc_results_data(
        identifier="general-election/UK/2017/results", processed_filename="general_election-uk-2017-results.csv"
    )
