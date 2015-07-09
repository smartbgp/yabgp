Tutorial
========

Basic Usage
~~~~~~~~~~~

We can use ``yabgpd`` help.

.. code:: bash

    $ yabgpd -h
    usage: yabgpd [-h] [--bgp-local_addr BGP_LOCAL_ADDR]
                  [--bgp-local_as BGP_LOCAL_AS] [--bgp-md5 BGP_MD5]
                  [--bgp-remote_addr BGP_REMOTE_ADDR]
                  [--bgp-remote_as BGP_REMOTE_AS] [--config-dir DIR]
                  [--config-file PATH] [--log-config-file LOG_CONFIG_FILE]
                  [--log-dir LOG_DIR] [--log-file LOG_FILE]
                  [--log-file-mode LOG_FILE_MODE] [--nouse-stderr] [--use-stderr]
                  [--verbose] [--version] [--noverbose]

    optional arguments:
      -h, --help            show this help message and exit
      --config-dir DIR      Path to a config directory to pull *.conf files from.
                            This file set is sorted, so as to provide a
                            predictable parse order if individual options are
                            over-ridden. The set is parsed after the file(s)
                            specified via previous --config-file, arguments hence
                            over-ridden options in the directory take precedence.
      --config-file PATH    Path to a config file to use. Multiple config files
                            can be specified, with values in later files taking
                            precedence. The default files used are: None.
      --log-config-file LOG_CONFIG_FILE
                            Path to a logging config file to use
      --log-dir LOG_DIR     log file directory
      --log-file LOG_FILE   log file name
      --log-file-mode LOG_FILE_MODE
                            default log file permission
      --nouse-stderr        The inverse of --use-stderr
      --use-stderr          log to standard error
      --verbose             show debug output
      --version             show program's version number and exit
      --noverbose           The inverse of --verbose

    rest options:
      --rest-bind_port REST_BIND_PORT
                            Port the bind the API server to
      --rest-password REST_PASSWORD
                            Password for api server
      --rest-username REST_USERNAME
                            Username for api server
      --rest-bind_host REST_BIND_HOST
                            Address to bind the API server to

    bgp options:
      --bgp-local_addr BGP_LOCAL_ADDR
                            The local address of the BGP
      --bgp-local_as BGP_LOCAL_AS
                            The Local BGP AS number
      --bgp-md5 BGP_MD5     The MD5 string use to auth
      --bgp-remote_addr BGP_REMOTE_ADDR
                            The remote address of the peer
      --bgp-remote_as BGP_REMOTE_AS
                            The remote BGP peer AS number

The simple way to start a yabgp agent is:

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 --bgp-remote_as=23650 --bgp-md5=cisco

The log output sample:

.. code:: bash

    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] Log (Re)opened.
    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] Configuration:
    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] ********************************************************************************
    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] Configuration options gathered from:
    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] command line args: ['--bgp-local_addr=10.75.44.11', '--bgp-local_as=23650', '--bgp-remote_addr=10.124.1.245', '--bgp-remote_as=23650', '--bgp-md5=cisco']
    2015-05-15 13:13:36,583.583 10338 INFO yabgp.agent [-] config files: []
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] ================================================================================
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] config_dir                     = None
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] config_file                    = []
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] log_config_file                = None
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] log_dir                        = None
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] log_file                       = None
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] log_file_mode                  = 0644
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] use_stderr                     = True
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] verbose                        = False
    2015-05-15 13:13:36,584.584 10338 INFO yabgp.agent [-] bgp.afi_safi                   = ['ipv4']
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.config_file                = None
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.local_addr                 = 10.75.44.11
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.local_as                   = 23650
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.md5                        = cisco
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.peer_start_interval        = 10
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.remote_addr                = 10.124.1.245
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.remote_as                  = 23650
    2015-05-15 13:13:36,585.585 10338 INFO yabgp.agent [-] bgp.running_config             = {}
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_dir              = /home/yabgp/data/bgp/
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_disk             = True
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_msg_max_size     = 500
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] ********************************************************************************

You can see that the default path to write BGP message is ``/home/yabgp/data/bgp``, if you can't write to this path, please change the path in ``yabgp.ini`` file.

Configuration
~~~~~~~~~~~~~

The configuration sample is:

.. code:: bash

    [DEFAULT]

    # log file name and location
    # log-file =

    # show debug output
    # verbose = False

    # log to standard error
    # use-stderr = True

    # log file directory
    # log-dir

    # log configuration file
    # log-config-file =

    # run mode
    # standalone = True

    [message]

    # how to process parsed BGP message?

    # Whether the BGP message is written to disk
    # write_disk = True

    # the BGP messages storage path
    # write_dir = /home/yabgp/data/bgp/

    # The Max size of one BGP message file, the unit is MB
    # write_msg_max_size = 500

    # Whether write keepalive message to disk
    # write_keepalive = True

    [bgp]

    # BGP global configuration items

    # peer configuration file
    # config_file =

    # The interval to start each BGP peer
    # peer_start_interval = 10

    # The Global config for address family and sub address family
    # if you want to support more than one address family, you can set afi_safi = ipv4, ipv6, ....
    # afi_safi = ipv4

    # ===================== items for peer configuration ================================
    # the following parameters will be ignored if conf_file is configured
    # and this configuration only support one bgp peer, if you need start more peers in
    # one yabgp process, please use conf_file to configure them.

    # remote as number
    # remote_as =

    # remote ip address
    # remote_addr =

    # local as number
    # local_as =

    # local ip address
    # local_addr =

    # The MD5 string
    # md5 =

    # ======================= BGP capacity =============================

    # support 4 bytes AS
    # four_bytes_as = True

    # support route refresh
    # route_refresh = True

    # support cisco route refresh
    # cisco_route_refresh = True

    # BGP add path feature.This field indicates whether the sender is (a) able to receive
    # multiple paths from its peer (value 1), (b) able to send
    # multiple paths to its peer (value 2), or (c) both (value 3) for
    # the <AFI, SAFI>.
    # add_path = 1

    # suport graceful restart or not
    # graceful_restart = True

    # support cisco multi session or not
    # cisco_multi_session = True

    # support enhanced route refresh or not
    # enhanced_route_refresh = True

    [rest]
    # Address to bind the API server to.
    # bind_host = 0.0.0.0

    # Port the bind the API server to.
    # bind_port = 8801

    # username and password for api server
    # username = admin
    # password = admin

    [rabbit_mq]

    # The RabbitMQ broker address where a single node is used. (string value)
    # rabbit_host = localhost

    # The RabbitMQ broker port where a single node is used. (integer value)
    # rabbit_port = 5672

    # Connect over SSL for RabbitMQ. (boolean value)
    # rabbit_use_ssl = false

    # The RabbitMQ userid. (string value)
    # rabbit_userid = guest

    # The RabbitMQ password. (string value)
    # rabbit_password = guest

    [database]

    # database configuration

    # connection url
    # eg: mongodb://10.75.44.10:27017,10.75.44.11:27017,10.75.44.12:27017
    # connection = mongodb://127.0.0.1:27017'

    # database name
    # dbname = yabgp

    # if use replica set
    # use_replica = True

    # replica set name
    # replica_name = rs1

    # Read preference if use replica set
    # PRIMARY = 0  Queries are sent to the primary of the replica set.
    # PRIMARY_PREFERRED = 1 Queries are sent to the primary if available, otherwise a secondary.
    # SECONDARY = 2 Queries are distributed among secondaries. An error is raised if no secondaries are available.
    # SECONDARY_PREFERRED = 3  Queries are distributed among secondaries, or the primary if no secondary is available.
    # NEAREST = 4 Queries are distributed among all members.
    # read_preference = 3

    # write concern (integer or string)If this is a replica set, write operations will block until
    # they have been replicated to the specified number or tagged set of servers. w= always includes
    # the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two
    # secondaries). Setting w=0 disables write acknowledgement and all other write concern options.
    # write_concern = -1

    # write concern timeout (integer) Used in conjunction with w. Specify a value in milliseconds to
    # control how long to wait for write propagation to complete. If replication does not complete
    # in the given timeframe, a timeout exception is raised.
    # write_concern_timeout = 5000

If you change the default setting (like change the ``write_dir``), please start the ``yabgp`` use the configuration file:

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 --bgp-remote_as=23650 --bgp-md5=cisco --config-file=yabgp.ini.sample

Logging and Debug
~~~~~~~~~~~~~~~~~

The default setting is loggint to console, if you want to write log files and no console output, please use:

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 --bgp-remote_as=23650 --bgp-md5=cisco --nouse-stderr --log-file=test.log

If you want to change the log level to debug, use `--verbose` option.

.. code:: bash

    $ yabgpd --bgp-local_addr=10.75.44.11 --bgp-local_as=23650 --bgp-remote_addr=10.124.1.245 --bgp-remote_as=23650 --bgp-md5=cisco --verbose
