Tutorial
========

Basic Usage
~~~~~~~~~~~

We can use ``yabgpd`` help.

.. code:: bash

    $ yabgpd -h

The simple way to start a yabgp agent is (There are four mandatory parameters):

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 \
             --bgp-remote_addr=10.124.1.245 --bgp-remote_as=23650

Configuration
~~~~~~~~~~~~~

The configuration sample can be found at https://github.com/smartbgp/yabgp/blob/master/etc/yabgp/yabgp.ini.sample

Advanced Usage
~~~~~~~~~~~~~~

If you change the default setting (like change the ``write_dir``), please start the ``yabgp`` use the configuration file:

.. code:: bash

    $ cp etc/yabgp/yabgp.ini.sample etc/yabgp/yabgp.ini
    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 \
             --bgp-remote_as=23650 --bgp-md5=cisco --config-file=../etc/yabgp/yabgp.ini

Running Mode
~~~~~~~~~~~~

By default, the yabgp will be running as standalone mode, and it will write all BGP messages in local disk where as ``write_dir`` point out.
If you run yabgp with ``--nostandalone``,  you must configure mongodb and rabbitmq, then you can control which kind of bgp message will be
sent to rabbitmq queue for further process.

Logging and Debug
~~~~~~~~~~~~~~~~~

The default setting is loggint to console, if you want to write log files and no console output, please use:

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 \
             --bgp-remote_as=23650 --bgp-md5=cisco --nouse-stderr --log-file=test.log

If you want to change the log level to debug, use `--verbose` option.

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 \
             --bgp-remote_as=23650 --bgp-md5=cisco --verbose
