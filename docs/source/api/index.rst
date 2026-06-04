API Reference
=============

The top-level ``filesmith`` package re-exports the most commonly used APIs.

.. autosummary::

   filesmith.find_files
   filesmith.transfer_files
   filesmith.FindMoveJob
   filesmith.copy_files
   filesmith.get_target_file
   filesmith.run_knapsack
   filesmith.copy_files_by_capacity
   filesmith.walk_files
   filesmith.find_duplicate_files
   filesmith.format_duplicate_report
   filesmith.write_duplicate_report
   filesmith.summarize_duplicate_groups
   filesmith.DuplicateFile
   filesmith.DuplicateGroup

Modules
-------

.. toctree::
   :maxdepth: 2

   filesmith
   finder
   transfer
   engine
   knapsack
   duplicates
   core
