.. _index:

Filesmith
=========

**Filesmith** is a collection of file manipulation and inspection utilities.
It provides small composable Python APIs plus command-line tools for finding,
copying, moving, selecting, and deduplicating files.

Key Features
------------

- **Find and transfer**: Locate files by glob pattern and copy or move them.
- **Capacity-based selection**: Pick files whose total size fits a byte budget.
- **Duplicate detection**: Find duplicate files by SHA-256 digest and write a downstream-friendly report.
- **Legacy regex copy**: Keep compatibility with the original pattern-based copy workflow.
- **Shared utility exports**: Re-export selected ``smith-utils`` APIs for text, numeric, date, and digest workflows.

Getting started
---------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   cli
   api/index
   development
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
