import pytest
from pathlib import Path

import maven
import pandas as pd


def test_UK2017ResultsHoc():
    name = 'general-election/UK/2017/results_HoC'
    maven.get(name)
    output = Path(name) / Path('processed') / Path('general_election-uk-2017-results.csv')
    df = pd.read_csv(output)
    print(list(df.columns))


def test_UK2015ResultsHoc():
    name = 'general-election/UK/2015/results_HoC'
    maven.get(name)

    output = Path(name) / Path('processed') / Path('general_election-uk-2015-results.csv')
    df = pd.read_csv(output)
    print(list(df.columns))
