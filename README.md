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
maven.get('general-election/UK/2015/results', data_directory='./data/')
```


## Datasets
Data dictionaries for all datasets are available by clicking on the dataset's name.

| Dataset | Description | Date | Source | Licence |
| -- | -- | -- | -- | -- |
| [**`general-election/UK/2010/results`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election) | UK 2010 General Election results | 6th May 2010 | [House of Commons Library](https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647) | [Open Parliament Licence v3.0](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/) |
| [**`general-election/UK/2015/results`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election) | UK 2015 General Election results | 7th May 2015 | [House of Commons Library](https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647) | [Open Parliament Licence v3.0](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/) |
| [**`general-election/UK/2017/results`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election) | UK 2015 General Election results | 8th June 2017 | [House of Commons Library](https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647) | [Open Parliament Licence v3.0](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/) |
| [**`general-election/UK/2015/model`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election) | Model-ready datasets for forecasting the 2015 and 2017 UK General Elections | 2010, 2015 & 2017 data | [SixFifty](https://github.com/six50/) | Mixed |
| [**`general-election/UK/polls`**](https://github.com/john-sandall/maven/tree/master/maven/datasets/general_election) | UK General Election opinion polling | May 2005 - June 2017 | [SixFifty](https://github.com/six50/pipeline/tree/master/data/polls/) | Unknown |



## Running tests
To run tests against an installed version (either `pip install .` or `pip install maven`):
```
$ cd /path/to/repo
$ pytest
```

To run tests whilst in development:
```
$ cd /path/to/repo
$ python -m pytest
```


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
