# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- `dockerfile`: support build without git history
  (by manually setting build argument `SETUPTOOLS_SCM_PRETEND_VERSION`)

### Removed
- compatibility with `python3.5`, `python3.6` & `python3.7`

## [0.1.1] - 2021-02-14
### Fixed
- loosen version constraint for `python-telegram-bot` to restore compatibility with python3.5
- fixed return type hints in class `_Persistence`
- added assertions fixing `mypy` errors
- tests: fixed compatibility with python3.5-3.7

## [0.1.0] - 2021-02-14
### Added
- telegram bot implementing single command `/photo`
  - sends a photo randomly selected from a [WikiMap](https://de.wikipedia.org/wiki/Benutzer:DB111/Tools#WikiMap) export
  - sends the wikimedia commons url and geolocation of the previously sent photo

[Unreleased]: https://github.com/fphammerle/location-guessing-game-telegram-bot/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/fphammerle/location-guessing-game-telegram-bot/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/fphammerle/location-guessing-game-telegram-bot/releases/tag/v0.1.0
