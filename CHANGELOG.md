# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased

### Added

- Support for Channel posts.

### Changed

- Should now reply in the thread or topic where the bot was invoked, rather than the
  global chat.


## 2.3.0 - 2023-03-05

### Changed

- Upgraded to Python 3.9.
- Updated dependencies.
- Move to `arm64` architecture.


## 2.2.1 - 2022-03-05

### Fixed

- Fixed a crash when a text query does not contain free text, only filters.


## 2.2.0 - 2021-12-30

### Added

- Single card results now also show an inline keyboard that allows you to change the shown
  result.


## 2.1.0 - 2021-09-12

### Added

- Fetch card price information by prepending a '$' or '€' sign to your query.


## 2.0.0 - 2021-09-12

### Changed

- Ported to Python because I need more zen in my life, and it's more mature in a
  Serverless context.


## 1.0.1 - 2020-02-05

### Fixed

- Fixed a bug where single-faced split cards (e.g. adventures) could not be found.


## 1.0.0 - 2020-02-04

### Added

- Initial tagged version.
