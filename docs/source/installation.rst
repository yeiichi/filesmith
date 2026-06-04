Installation
============

Filesmith requires Python 3.10 or newer.

Install from PyPI
-----------------

.. code-block:: bash

   pip install filesmith

Development install
-------------------

From a local checkout, install the package with its development dependencies:

.. code-block:: bash

   uv sync --extra dev

or with ``pip``:

.. code-block:: bash

   python -m pip install -e ".[dev]"

Dependencies
------------

Filesmith depends on ``smith-utils>=0.3.1``. The duplicate detection feature
uses ``smith_utils.crypto.get_file_digest`` to calculate SHA-256 file digests.
