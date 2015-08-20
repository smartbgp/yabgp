Installation
============

We recommend run ``yabgp`` through python virtual-env from source
code or pip install

From source code
~~~~~~~~~~~~~~~~

Use yabgp from source code:

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ git clone https://github.com/smartbgp/yabgp
    $ cd yabgp
    $ pip install -r requirements.txt
    $ cd bin
    $ python yabgpd -h

From pip
~~~~~~~~

Use pip install

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ pip install yabgp
    $ which yabgpd
    /home/yabgp/yabgp-virl/bin/yabgpd
    $ yabgpd -h

.. note::

    For ``virtualenv``, you can install it from pip. And make sure you have installed ``python-dev`` based on
    your operation system, for example Ubuntu, you can install it from ``apt-get install python-dev``.
    otherwise, you may get error when install requirement from requirements.txt