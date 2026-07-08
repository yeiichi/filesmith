Quickstart
==========

Find and copy files
-------------------

Use the unified CLI to find files and copy them into a destination directory:

.. code-block:: bash

   filesmith find-move ./src ./backup -p "*.py"

The same operation is available through the Python API:

.. code-block:: python

   from pathlib import Path
   from filesmith import find_files, transfer_files

   files = find_files(Path("./src"), glob_pattern="*.py", recursive=True)
   transfer_files(files, Path("./backup"), mode="copy", on_conflict="skip")

Find duplicate files
--------------------

Scan files up to a maximum directory depth and write a tab-separated report:

.. code-block:: bash

   filesmith duplicates ./archive --maxdepth 2 -o duplicate-report.txt

Programmatic duplicate detection returns structured groups:

.. code-block:: python

   from filesmith import find_duplicate_files, write_duplicate_report

   groups = find_duplicate_files("./archive", maxdepth=2)
   write_duplicate_report(
       groups,
       root="./archive",
       maxdepth=2,
       output_path="duplicate-report.txt",
   )

Select files by capacity
------------------------

Copy a subset of files without exceeding a total byte capacity:

.. code-block:: bash

   filesmith knapsack copy ./photos ./usb-drive 104857600 -p "*.jpg"

Use the solver directly for integer subset-sum problems:

.. code-block:: python

   from filesmith import run_knapsack

   best_sum, indices = run_knapsack([10, 20, 30, 40, 50], 65)
