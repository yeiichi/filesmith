Development
===========

Set up the project
------------------

.. code-block:: bash

   uv sync --extra dev

Run tests
---------

.. code-block:: bash

   uv run pytest -q

Run focused tests
-----------------

.. code-block:: bash

   uv run pytest tests/test_duplicates.py tests/test_cli.py -q

Build documentation
-------------------

Install the documentation extra, then build the HTML docs:

.. code-block:: bash

   uv sync --extra docs
   make -C docs html

Release notes
-------------

The project is configured for Python Semantic Release in ``pyproject.toml`` and
allows version ``0.x`` releases.
