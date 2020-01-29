"""
Various helper functions.
"""

import hashlib
import shutil
import warnings
from urllib.parse import urlparse

import pandas as pd
import requests

import maven


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


def calculate_md5_checksum(filename):
    """
    Calculate the checksum of the file, exactly same as md5-sum linux util.
    Code from https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/downloader.py
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_url(url):
    """Source: https://stackoverflow.com/a/52455972"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_url(url, filename, target_dir):
    """Download filename from url into target_dir."""
    response = requests.get(url + filename)
    if response.status_code != 200:
        warnings.warn(f"Received status {response.status_code} when trying to retrieve {url}{filename}")
    # Save to file
    with open(target_dir / filename, "wb") as f:
        f.write(response.content)
    print(f"Successfully downloaded {filename} into {target_dir.resolve()}")
    return target_dir / filename


def get_and_copy(identifier, filename, target_dir):
    # """Run maven.get(identifier) and copy filename from identifier/processed/ data into target/."""
    # target_dir by default is data/general-election/UK/2015/model
    subdirectories_below = str(target_dir).count("/")
    go_up = "/".join([".." for _ in range(subdirectories_below)])
    data_directory = (target_dir / go_up).resolve()  # sensible guess?
    maven.get(identifier, data_directory=data_directory)
    source = data_directory / identifier / "processed"
    print(f"Copying {filename} from {source} -> {target_dir}.")
    shutil.copyfile(src=source / filename, dst=target_dir / filename)


def retrieve_from_cache_if_exists(
    filename, target_dir, processing_fn, md5_checksum=None, caching_enabled=True, verbose=False
):
    """Retrieve filename from target_dir if it exists, otherwise execute processing_fn.

    Raises a warning if the retrieved/processed file's checksum doesn't match the expected MD5.
    """
    if caching_enabled and (target_dir / filename).exists():
        # Check if it's already in target_dir.
        print(f"Cached file {filename} is already in {target_dir.resolve()}")
    else:
        # Either caching disabled or file not there yet.
        processing_fn()

    # File should now be there. Let's check checksums.
    downloaded_file_md5_checksum = calculate_md5_checksum(target_dir / filename)
    if verbose:
        print(f"Checksum for {filename}: {downloaded_file_md5_checksum}")
    if md5_checksum and downloaded_file_md5_checksum != md5_checksum:
        warnings.warn(f"MD5 checksum doesn't match for {filename}")
