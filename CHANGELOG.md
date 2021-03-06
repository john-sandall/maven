# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

## [0.1.0] - 2020-02-03
### Changed
- Model-ready datasets can now be "prediction-only" (i.e. for use pre-election when we don't know results).
- Model-ready datasets include UKIP and BXP as part of "Other" until a better solution can be found.
- Various changes to enable a better regional UNS forecast:
    - better handling of NI parties;
    - regional poll-of-polls goes back a month to incorporate large sample regional polling and not just sub-samples;
    - MRP sample sizes are disregarded for weighted poll-of-polls;
    - missing sample sizes (such as for polls derived from PollBase) are imputed using mean sample size within the same region;
### Added
- Merged SixFifty UK polling data (detailed inc. sample sizes) up to June 2017 with Mark Pack's PollBase which has less columns but all polls up to Dec 2019.
- Incorporated regional polling & regional sub-samples for December 2019 from SixFifty. 
- `general-election/UK/2019/model`: added model-ready dataset including UNS and regional UNS forecasts for the 2019 UK General Election.

## [0.0.12] - 2020-02-03
### Changed
- `general-election/UK/2015/model`: model-ready dataset for just the 2015 UK General Election.
### Added
- `general-election/UK/2017/model`: model-ready dataset for the 2017 UK General Election.

## [0.0.11] - 2020-02-02
### Added
- Updated & refactored polling pipeline code.
- Updated & refactored pipeline for building model-ready datasets for 2015/2017 UK general elections.

## [0.0.10] - 2020-01-26
### Added
- Raw datasets are now cached on download, and processed datasets cached after processing, and always checked against MD5 for integrity.
- Tests now exist for utils.py

## [0.0.9] - 2020-01-26
### Added
- UK 2017 General Election dataset (**`general-election/UK/2017/results`**).
- Some tests (that really need caching!).
### Changed
- Now using data from the [House of Commons Library](https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647).
- The basic processed election results are now "long form" with less but more standardised information.
- The full election results are (for now) no longer provided.
- Lots of refactoring with some new base classes & utils making it faster to add new datasets.

## [0.0.8] - 2019-11-14
### Fixes
- Electoral Commission [no longer hosts 2010 GE results](https://github.com/john-sandall/maven/pull/15) so use our fallback until a new primary can be found.
- Fixed URL to EC's 2015 GE results.

## [0.0.7] - 2019-11-14
### Added
- Tests added to setup.py.
### Changed
- Switched to using [pip-tools](https://github.com/jazzband/pip-tools) instead of Pipenv for generating requirements.txt & locking dependencies.

## [0.0.6] - 2019-07-13
### Added
- `general-election/UK/2015/model`: model-ready datasets for the 2015/2017 UK General Elections.
- Regional polling datasets.

## [0.0.5] - 2019-07-13
### Added
- Basic tests for `get.py`
- Additional processing for the GE2015 results pipeline to generate a more useful dataset for common election modelling tasks.
- Added `general-election/UK/2010/results` dataset.
### Changed
- API design for dataset identifiers to use dash/slash instead of underscore/dash and capitalised country codes to make it clearer these will be ISO 3166 Alpha-2 codes, e.g. `general_election-gb-2015-results` -> `general-election/GB/2015/results`.
- Changed GB to UK everywhere as these results are full UK results including Northern Ireland.

## [0.0.4] - 2019-07-07
### Fixes
- Fixed relative imports and switch to using a class for each dataset.

## [0.0.3] - 2019-07-07
### Added
- Improved README.

## [0.0.2] - 2019-07-07
### Added
- UK 2015 General Election dataset (**`general_election-gb-2015-results`**).
- Proper README plus data dictionary.
- MANIFEST.in plus additional packaging info and this changelog.

## [0.0.1] - 2019-07-07
### Added
- Barebones functionality, Python package requirements (setup.py, Pipfile, .gitignore, LICENSE)


[Unreleased]: https://github.com/john-sandall/maven/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/john-sandall/maven/compare/v0.0.12...v0.1.0
[0.0.12]: https://github.com/john-sandall/maven/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/john-sandall/maven/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/john-sandall/maven/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/john-sandall/maven/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/john-sandall/maven/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/john-sandall/maven/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/john-sandall/maven/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/john-sandall/maven/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/john-sandall/maven/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/john-sandall/maven/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/john-sandall/maven/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/john-sandall/maven/releases/tag/v0.0.1
