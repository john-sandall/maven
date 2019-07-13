# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


<!-- ## [Unreleased] -->

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


[Unreleased]: https://github.com/john-sandall/maven/compare/v0.0.5...HEAD
[0.0.5]: https://github.com/john-sandall/maven/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/john-sandall/maven/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/john-sandall/maven/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/john-sandall/maven/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/john-sandall/maven/releases/tag/v0.0.1
