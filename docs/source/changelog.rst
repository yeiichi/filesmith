Changelog
=========

0.6.1
-----

- Migrated package builds from setuptools to Hatchling.
- Added GitHub Actions CI for tests, package checks, and documentation builds.
- Added GitHub Actions PyPI publishing with Trusted Publishing/OIDC.
- Added ``v*`` tag push support for the publish workflow.

0.6.0
-----

- Added the Read the Docs documentation project link to package metadata.
- Refreshed the lockfile for release.
- Made ``find_files`` lazy.

0.5.0
-----

- Added duplicate file detection.
- Added the Sphinx documentation site.
- Added project ``make`` targets and help output.
- Updated packaging metadata.

0.4.0
-----

- Added unified ``filesmith`` command with ``find-move`` and ``knapsack`` subcommands.
- Added ``filesmith-legacy`` for the previous regex-based CLI.
- Expanded Python API in the ``filesmith`` package.
- Improved internal structure around finder, transfer, and engine modules.

0.2.0
-----

- Initial release.
