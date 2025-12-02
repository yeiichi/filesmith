.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to filesmith documentation
==================================

filesmith is a Python utility library for working with files.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Usage
=====

`filesmith` can be used as a command-line tool or as a Python library.

As a Library
------------

You can import the `copy_files` function from the `filesmith.core` module to use it in your Python scripts.

Here's an example of how to copy all `.txt` files from a source directory to a destination directory:

.. code-block:: python

   from filesmith.core import copy_files

   source_dir = "/path/to/source"
   destination_dir = "/path/to/destination"
   pattern = r".*\\.txt$"

   copy_files(source_dir, destination_dir, pattern)

As a Command-Line Tool
----------------------

You can also use `filesmith` from the command line.

**Copy all .txt files from `source` to `dest`:**

.. code-block:: bash

   filesmith /path/to/source /path/to/dest ".*\\.txt$"

**Perform a dry run to see which .jpg files would be copied:**

.. code-block:: bash

   filesmith /path/to/source /path/to/dest ".*\\.jpg$" --dry-run

**Copy .log files newer than a specific date:**

.. code-block:: bash

    filesmith /path/to/logs /path/to/backup ".*\\.log$" --newermt 2023-10-27T10:00:00

Python API
==========

In addition to the command-line interface, filesmith exposes a small Python API.

get_target_file
---------------

The :func:`filesmith.core.get_target_file` helper locates **exactly one** file
in a directory based on a substring and optional file extension filter.

Basic usage:

.. code-block:: python

   from filesmith import get_target_file

   # Find a single .xlsx file that contains "report" in its name
   path = get_target_file("/path/to/dir", "report", ".xlsx")
   print(path)

Behavior:

* Returns a :class:`pathlib.Path` object.
* Raises :class:`ValueError` if no files match the criteria.
* Raises :class:`ValueError` if more than one file matches.

This is useful when your workflow expects a single, uniquely-identified file
(such as a weekly export or a one-off report) and you want a simple guard
against "zero or many" matches.

Changelog (summary)
===================

Version 0.2.1
-------------

* Added :func:`filesmith.core.get_target_file` to locate a uniquely matched file.
* Improved :func:`filesmith.core.copy_files`:

  - Uses :mod:`logging` instead of :func:`print` for messages.
  - More robust handling of the ``--newermt`` option, accepting either a
    reference file path or an ISO-formatted date/datetime string.

