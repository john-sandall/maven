"""
Running tests in development:
    $ cd /path/to/repo
    $ python -m pytest ./tests/datasets/coronavirus/test_csse.py

Running tests against installed version (either `pip install .` or `pip install maven`):
    $ cd /path/to/repo
    $ pytest ./tests/datasets/coronavirus/test_csse.py
"""

from pathlib import Path

import pandas as pd

import maven


def test_csse():
    identifier = "coronavirus/CSSE"
    maven.get(identifier, data_directory="./data/")
    # CSSE_country.csv
    processed_filename = "CSSE_country.csv"
    df = pd.read_csv(Path("./data") / identifier / "processed" / processed_filename)
    assert df.columns.tolist() == ["date", "country_region", "confirmed", "deaths", "recovered"]
    # CSSE_country_province.csv
    processed_filename = "CSSE_country_province.csv"
    df = pd.read_csv(Path("./data") / identifier / "processed" / processed_filename)
    assert df.columns.tolist() == [
        "date",
        "country_region",
        "province_state",
        "lat",
        "lon",
        "confirmed",
        "deaths",
        "recovered",
    ]
