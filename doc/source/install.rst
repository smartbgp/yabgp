Installation
============

Python >= 3.13 is required.

From source (using uv)
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ git clone https://github.com/smartbgp/yabgp
    $ cd yabgp
    $ uv sync
    $ uv run yabgpd -h

From pip
~~~~~~~~

.. code:: bash

    $ pip install yabgp
    $ yabgpd -h

Using Docker
~~~~~~~~~~~~

.. code:: bash

    $ docker run -it smartbgp/yabgp:latest --bgp-afi_safi=ipv4 \
        --bgp-local_as=65022 --bgp-remote_addr=10.75.44.219 --bgp-remote_as=65022
