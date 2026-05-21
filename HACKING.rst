Hacking Guide
=============


Code style
----------

Step 1: Read http://www.python.org/dev/peps/pep-0008/

Step 2: Read http://www.python.org/dev/peps/pep-0008/ again

Step 3: Read on


Running Tests
-------------

Using uv + pytest (recommended):

.. code:: bash

  $ cd yabgp
  $ uv sync --group test --group dev
  $ uv run pytest yabgp/tests/unit/ -v

Running Lint / Type Check
-------------------------

.. code:: bash

  $ cd yabgp
  $ uv run ruff check yabgp/ --exclude yabgp/tests
  $ uv run pyright


Building Docs
-------------

.. code:: bash

  $ cd yabgp
  $ uv sync --group docs
  $ uv run sphinx-build -b html doc/source doc/build
