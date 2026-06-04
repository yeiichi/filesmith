Command Line Interface
======================

Filesmith exposes a unified command:

.. code-block:: bash

   filesmith <command> [arguments] [options]

It also exposes compatibility entry points for individual tools:
``filesmith-find-move``, ``filesmith-knapsack``, ``filesmith-duplicates``, and
``filesmith-legacy``.

``find-move``
-------------

Find files and copy or move them.

.. code-block:: bash

   filesmith find-move <src> <dst> [-p PATTERN] [-m {copy,move}] [-n] [-R]

Arguments and options:

- ``src``: source directory to search.
- ``dst``: destination directory.
- ``-p, --pattern``: glob pattern, default ``*``.
- ``-m, --mode``: ``copy`` or ``move``, default ``copy``.
- ``-n, --dry-run``: print planned operations without changing files.
- ``-R, --no-recursive``: search only files directly in ``src``.

``knapsack copy``
-----------------

Copy a subset of matching files without exceeding a byte capacity.

.. code-block:: bash

   filesmith knapsack copy <src_dir> <dest_dir> <capacity> [-p PATTERN] [-n] [-R]

``knapsack solve``
------------------

Solve a subset-sum problem for integer items.

.. code-block:: bash

   filesmith knapsack solve <capacity> <items...>

``duplicates``
--------------

Find duplicate files by walking a root directory to an instructed depth and
comparing SHA-256 file digests.

.. code-block:: bash

   filesmith duplicates <root> --maxdepth <depth> [-p PATTERN] [-o REPORT]

Arguments and options:

- ``root``: root directory to scan.
- ``--maxdepth``: maximum directory depth. Use ``0`` for files directly in ``root``.
- ``-p, --pattern``: glob pattern, default ``*``.
- ``-o, --output``: text report path, default ``filesmith-duplicates.txt``.

Duplicate report format
~~~~~~~~~~~~~~~~~~~~~~~

The report is line-oriented and tab-separated so downstream tasks can parse it
without reverse-engineering console prose.

.. code-block:: text

   # filesmith duplicate report v1
   root	./archive
   maxdepth	2
   duplicate_groups	1
   duplicate_files	2
   wasted_bytes	1024
   group	1	sha256	...	size	1024	count	2
   file	1	1024	./archive/a.bin
   file	1	1024	./archive/copy/a.bin

``filesmith-legacy``
--------------------

The original regex-based copy command remains available:

.. code-block:: bash

   filesmith-legacy copy <origin> <destination> <pattern> [--newermt REF] [-n] [-q]
