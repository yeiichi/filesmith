# CHANGELOG

<!-- version list -->

## v0.5.0 (2026-06-04)

### Chores

- Correct pyproject.toml
  ([`2630f45`](https://github.com/yeiichi/filesmith/commit/2630f45b94b50c4b755c3660ff6ee9709b022b11))

- Correct pyproject.toml
  ([`32a612d`](https://github.com/yeiichi/filesmith/commit/32a612de7a32b7113722830c9b11da9d101dee93))

- Update pyproject.toml
  ([`de4a0c9`](https://github.com/yeiichi/filesmith/commit/de4a0c93555dcd050ef9be5e66e69ace535f9051))

- **make**: Add project make targets and help output
  ([`09f7403`](https://github.com/yeiichi/filesmith/commit/09f74038a5a17374da7550728c12d08168b5c946))

- **release**: Remove docs scaffolding and update packaging metadata
  ([`0542c3a`](https://github.com/yeiichi/filesmith/commit/0542c3ab7a833e5ff3515a9c9488c5550c9c47ac))

### Documentation

- Add sphinx documentation site
  ([`80f4771`](https://github.com/yeiichi/filesmith/commit/80f4771266b4877471f0c0c93b35360a93d52fdc))

### Features

- Add duplicate file detection
  ([`4355fbd`](https://github.com/yeiichi/filesmith/commit/4355fbde00dbfcb053ae3dd0720f96186873b024))


## v0.4.0 (2026-03-26)

### Chores

- Prepare 0.3.0 release (metadata, README, scripts)
  ([`fd7591f`](https://github.com/yeiichi/filesmith/commit/fd7591faf71d8da0b2f70f81c43370e22c36da9c))

### Features

- **cli**: Add umbrella command with nested find-move and knapsack subcommands
  ([`327348c`](https://github.com/yeiichi/filesmith/commit/327348c995d1f84478668f5977afc294a8ae659f))


## v0.3.0 (2025-12-10)

### Features

- Add filesmith-list, a file lister utility CLI (scripts/list_files.py)
  ([`cf83068`](https://github.com/yeiichi/filesmith/commit/cf8306893c003e9e7f449779cb555af2e3fd3bf3))

- **cli**: Add filesmith-find-move around FindMoveJob
  ([`dea784d`](https://github.com/yeiichi/filesmith/commit/dea784de0671ae427316d9e5fcb6a0684edd2e02))

- **cli**: Add filesmith-find-move command using FindMoveJob
  ([`a33aa4b`](https://github.com/yeiichi/filesmith/commit/a33aa4be423b7bb83c757fbba45e17eabdab33f4))

- **core**: Introduce finder/transfer/engine modules with unit tests
  ([`3388e4d`](https://github.com/yeiichi/filesmith/commit/3388e4d79eec26c5ab9fce168db05f27a4919123))

### Refactoring

- **core**: Delegate copy_files to transfer_files without changing public behavior
  ([`317e6e6`](https://github.com/yeiichi/filesmith/commit/317e6e6ef4ef30d06e232746263fde933abad6fe))


## v0.2.1 (2025-12-02)


## v0.2.0 (2025-12-02)

- Initial Release
