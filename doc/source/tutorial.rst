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
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_dir              = /home/bgpmon/data/bgp/
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_disk             = True
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] message.write_msg_max_size     = 500
    2015-05-15 13:13:36,586.586 10338 INFO yabgp.agent [-] ********************************************************************************

You can see that the default path to write BGP message is ``/home/bgpmon/data/bgp``, if you can't write to this path, please change the path in ``yabgp.ini`` file.

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

    [message]

    # how to process parsed BGP message?

    # Whether the BGP message is written to disk
    # write_disk = True

    # the BGP messages storage path
    # write_dir = /home/bgpmon/data/bgp/
    write_dir = your_own_path
    # The Max size of one BGP message file, the unit is MB
    # write_msg_max_size = 500

    [bgp]

    # BGP global configuration items

    # peer configuration file
    # config_file =

    # The interval to start each BGP peer
    # peer_start_interval = 10

    # The Global config for address family and sub address family
    # afi_safi = ['ipv4']

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
