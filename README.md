# Maven
> /meɪvən/ – a trusted expert who seeks to pass timely and relevant knowledge on to others.

Maven's goal is to reduce the time data scientists spend on data cleaning and preparation by providing easy access to open datasets in both raw and processed formats.

Maven was built to:

- **Improve availability and integrity of open data** by eliminating data issues, adding common identifiers, and reshaping data to become model-ready.
- **Source data in its rawest form** from the most authoritative data provider available with all transformations available as open source code to enhance integrity and trust.
- **Honour data licences wherever possible** whilst avoiding potential issues relating to re-distribution of data (especially open datasets where no clear licence is provided) by performing all data retrieval and processing on-device.


## Install
```
pip install maven
```


## Usage
```python
import maven
maven.get('general_election-gb-2015-results', data_directory='../data/')
```


## Datasets
Data dictionaries for all datasets are available by clicking on the dataset's name.

| Dataset | Description | Date | Source | Licence |
| -- | -- | -- | -- | -- |
| [**`general_election-gb-2015-results`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election#general_election-gb-2015-results) | UK 2015 General Election results | 7th May 2015 | [Electoral Commission](http://www.electoralcommission.org.uk/our-work/our-research/electoral-data) | [Open Government Licence v2.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/) |


## Licences
| Name | Description | Attribution Statement |
| -- | -- | -- |
| [Open Parliament Licence](http://www.parliament.uk/site-information/copyright/open-parliament-licence/) | Free to copy, publish, distribute, transmit, adapt and exploit commercially or non-commercially. See URL for full details. | Contains Parliamentary information licensed under the Open Parliament Licence v3.0. |
| [Open Government Licence](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/) | Free to copy, publish, distribute, transmit, adapt and exploit commercially and non-commercially. See URL for full details. | Contains public sector information licensed under the Open Government Licence v2.0. |


## Contributing
Maven was designed for your contributions!

1. Check for open issues or open a fresh issue to start a discussion around your idea or a bug.
2. Fork [the repository](https://github.com/john-sandall/maven) on GitHub to start making your changes to the master branch (or branch off of it).
3. For new datasets ensure the processed dataset is fully documented with a data dictionary. For new features and bugs, please write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) and bug the maintainer until it gets merged and published. 😄
