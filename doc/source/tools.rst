Tools
======

Here are some tools can be used for yabgp.

Route Injector
~~~~~~~~~~~~~~~

Tools location: https://github.com/smartbgp/yabgp/blob/master/tools/route_injector

This tool can be used to send bgp update messages to yabgp process. For example, you start a yabgp process:

.. code-block:: bash

    $ python yabgp/bin/yabgpd --bgp-local_as=100 --bgp-local_addr=127.0.0.1 \
                              --bgp-remote_addr=2.2.2.2 --bgp-remote_as=100

If you have some BGP messages come from some other yabgp process, like:

.. code-block:: bash

    $ pwd
    /home/yabgp/data/bgp/1.1.1.1/msg
    $ ls
    1450668274.82.msg 1450668593.59.msg

We want to send all the BGP message received from peer ``1.1.1.1`` to ``2.2.2.2``. We can use route injector like this:

.. code-block:: bash

    $ python route_injector --rest-host=127.0.0.1 --rest-port=8801  \
                            --message-json=/home/yabgp/data/bgp/1.1.1.1/msg/1450668274.82.msg \
                            --peerip=2.2.2.2
    Percent: [########################################          ] 81.05%

Then, route-injector will read bgp message file and try to send all bgp messages to peer ``2.2.2.2`` through REST API. When finised:

.. code-block:: bash

    Percent: [##################################################] 100.00%
    Total messages:   128444.
    Success send out: 15109
    Failed send out:  113335

Postman Collection
~~~~~~~~~~~~~~~~~~

Located in ``/yabgp/tools/Yabgp.json.postman_collection``. You can import this collection into POSTMAN(http://www.getpostman.com/)
and there are some REST API request examples.