# Changelog

<!-- version list -->

## v2.0.2 (2026-09-07)

### Bug Fixes

- Add new can_extract_metadata permission
  ([`032820f`](https://github.com/rero/rero-invenio-files/commit/032820f0df1d2e51dfdb4821c6aa61812f175394))

- **files**: Raise ValueError on invalid filename
  ([`9656d03`](https://github.com/rero/rero-invenio-files/commit/9656d0351119e2ec054fc5721eb6778af9e64018))

### Build System

- **deps**: Run python-semantic-release through uvx
  ([`711a949`](https://github.com/rero/rero-invenio-files/commit/711a9496023cdb00512c6cd9cb6b7e8c5f6a07f1))

### Chores

- **deps**: Require python 3.14 and bump ci actions
  ([`2a112d4`](https://github.com/rero/rero-invenio-files/commit/2a112d49eaac6fcdaa007c6874a1981dd5ecd58c))

### Documentation

- Add claude code guide
  ([`5545948`](https://github.com/rero/rero-invenio-files/commit/5545948202a8bb5e79318b38e26274b890c1b328))

### Refactoring

- **files**: Use the pymupdf module name
  ([`87f3a0f`](https://github.com/rero/rero-invenio-files/commit/87f3a0f4b3b746c200a3209695e838c49c58fb95))


## v2.0.1 (2026-06-16)

### Code Style

- Replace verbose license headers with SPDX tags
  ([`7397b4a`](https://github.com/rero/rero-invenio-files/commit/7397b4ad7d4d44ddf0ed51dd6e244a54a565b37e))

### Continuous Integration

- Add semantic release workflow for automatic publication
  ([`5985719`](https://github.com/rero/rero-invenio-files/commit/5985719915c315298148021433af4cd34b5b03a0))

- Switch to github app permissions for release workflow
  ([`46bdb20`](https://github.com/rero/rero-invenio-files/commit/46bdb20b88abee4dff188a234dd48f10d142b580))

### Refactoring

- **files**: Replace ImageMagick with Pillow, optimize extraction
  ([`30a35de`](https://github.com/rero/rero-invenio-files/commit/30a35deb1d69a13fb4cc4c7f46b14bedce78d5a3))


## [v2.0.0](https://github.com/rero/rero-invenio-files/tree/v2.0.0) (2026-03-24)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.2.0...v2.0.0)

**Changes:**

- chore: remove unused Invenio default files and Sphinx infrastructure [#18](https://github.com/rero/rero-invenio-files/pull/18) (by @PascalRepond)
- BREAKING CHANGE: upgrade invenio-records-resources to v9 [#17](https://github.com/rero/rero-invenio-files/pull/17) (by @PascalRepond)

## [v1.2.0](https://github.com/rero/rero-invenio-files/tree/v1.2.0) (2025-09-02)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.1.3...v1.2.0)

**New features:**

- feat (pdf): improve PDFGenerator with better layout and image handling [#12](https://github.com/rero/rero-invenio-files/pull/12) (by @NathanPython2002)

## [v1.1.3](https://github.com/rero/rero-invenio-files/tree/v1.1.3) (2025-08-05)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.1.2...v1.1.3)

- chore: use uv_publish as a build system (by @PascalRepond)

## [v1.1.2](https://github.com/rero/rero-invenio-files/tree/v1.1.2) (2025-08-04)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.1.1...v1.1.2)

- chore: fix the wrong package publication on pypi for v1.1.1 (by @PascalRepond)

## [v1.1.1](https://github.com/rero/rero-invenio-files/tree/v1.1.1) (2025-07-31)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.1.0...v1.1.1)

**Changes:**

- feat(dev): add uv and ruff [#9](https://github.com/rero/rero-invenio-files/pull/9) (by @PascalRepond)
- chore(docs): fix readme badges [#7](https://github.com/rero/rero-invenio-files/pull/7) (by @PascalRepond)

## [v1.1.0](https://github.com/rero/rero-invenio-files/tree/v1.1.0) (2025-05-13)

[Full Changelog](https://github.com/rero/rero-invenio-files/compare/v1.0.0...v1.1.0)

**Enhancements:**

- invenio: new version [\#5](https://github.com/rero/rero-invenio-files/pull/5) (by @rerowep)
- actions: pipy publish package use poetry [\#2](https://github.com/rero/rero-invenio-files/pull/2) (by @jma)

## [v1.0.0](https://github.com/rero/rero-invenio-files/tree/v1.0.0) (2024-05-21)

- Initial commit
