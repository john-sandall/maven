"""
Main data getting functionality. Maps data identifiers to data pipeline classes.

Example usage:
    > import maven
    > maven.get('general-election/GB/2015/results', data_directory='./data/')
"""

from pathlib import Path

from .datasets import general_election


def get(name, data_directory=Path('.'), retrieve=True, process=True):
    """Core data getter function.

    Args:
        name (str): Name of dataset to retrieve/process.
        data_directory (str or pathlib.PosixPath): Path to directory where datasets will be saved (either as string
                                                   a pathlib Path).
        retrieve (bool): Toggle dataset retrieval.
        process (bool): Toggle dataset processing.

    Returns: Nothing (datasets are placed into current working directory).
    """
    mapper = {
        'general-election/GB/2015/results': general_election.GB2015Results,
        }
    if name not in mapper:
        raise KeyError(f'"{name}" not found in datasets.')

    if isinstance(data_directory, str):
        data_directory = Path(data_directory)
    pipeline = mapper[name](directory=(data_directory / name))

    if retrieve:
        pipeline.retrieve()
    if process:
        pipeline.process()
