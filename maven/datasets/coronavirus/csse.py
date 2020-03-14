"""
Coronavirus CSSE data from https://github.com/CSSEGISandData/COVID-19/

Usage:
    >>> import maven
    >>> maven.get('coronavirus/CSSE', data_directory='./data/')


Sources:
    - https://github.com/CSSEGISandData/COVID-19/
"""
import os
from pathlib import Path

import pandas as pd

from maven import utils


class CSSE(utils.Pipeline):
    """Handle CSSE data from https://github.com/CSSEGISandData/COVID-19/"""

    def __init__(self, directory=Path("data/coronavirus/CSSE")):
        # inherit base __init__ but override default directory
        super(CSSE, self).__init__(directory=directory)
        # Source & targets
        base_url = (
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
            "csse_covid_19_data/csse_covid_19_time_series/"
        )
        self.sources = [
            # url, filename, checksum
            (base_url, "time_series_19-covid-Confirmed.csv", None,),
            (base_url, "time_series_19-covid-Deaths.csv", None,),
            (base_url, "time_series_19-covid-Recovered.csv", None,),
        ]
        self.targets = [
            # filename, checksum(
            ("CSSE_country_province.csv", None),
            ("CSSE_country.csv", None),
        ]
        # Config
        self.rename_source = False
        self.retrieve_all = True
        self.cache = True
        self.verbose_name = "CSSE"

    def process(self):
        """Process CSSE data."""
        target_dir = self.directory / "processed"
        os.makedirs(target_dir, exist_ok=True)  # create directory if it doesn't exist

        def process_and_export():
            """Either caching disabled or file not yet processed; process regardless."""
            data = {}
            for metric in ["Confirmed", "Deaths", "Recovered"]:
                df = pd.read_csv(self.directory / "raw" / f"time_series_19-covid-{metric}.csv")
                # Pivot all to long
                id_vars = ["Province/State", "Country/Region", "Lat", "Long"]
                value_vars = list(set(df.columns) - set(id_vars))
                df = df.melt(
                    id_vars=id_vars, value_vars=value_vars, var_name="date", value_name=metric
                )
                df["date"] = pd.to_datetime(df.date, format="%m/%d/%y")
                data[metric] = df.copy()

            # Merge together
            df_country_province = pd.merge(
                data["Confirmed"],
                data["Deaths"],
                how="outer",
                on=["Province/State", "Country/Region", "Lat", "Long", "date"],
            ).merge(
                data["Recovered"],
                how="outer",
                on=["Province/State", "Country/Region", "Lat", "Long", "date"],
            )

            # Clean
            df_country_province.columns = utils.sanitise(
                df_country_province.columns, replace={"long": "lon"}
            )
            df_country_province = df_country_province[
                [
                    "date",
                    "country_region",
                    "province_state",
                    "lat",
                    "lon",
                    "confirmed",
                    "deaths",
                    "recovered",
                ]
            ].sort_values(["date", "country_region", "province_state"])

            # Country-level data
            df_country = (
                df_country_province.groupby(["date", "country_region"])[
                    ["confirmed", "deaths", "recovered"]
                ]
                .sum()
                .reset_index()
            )

            # Export
            print(f"Exporting dataset to {target_dir.resolve()}")
            df_country_province.to_csv(target_dir / "CSSE_country_province.csv", index=False)
            df_country.to_csv(target_dir / "CSSE_country.csv", index=False)

        for filename, checksum in self.targets:
            utils.retrieve_from_cache_if_exists(
                filename=filename,
                target_dir=target_dir,
                processing_fn=process_and_export,
                md5_checksum=checksum,
                caching_enabled=self.cache,
                verbose=self.verbose,
            )
