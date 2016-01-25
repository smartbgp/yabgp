RESTFUL API
===========

yabgp provides various endpoints that can be used to interact with the data and routers. Web API uses JSON format.


REST API has basic http auth, through usename and password. The usename and password configured in configuration file and they have default values.

.. code:: bash

   [rest]
   # Address to bind the API server to.
   # bind_host = 0.0.0.0

   # Port the bind the API server to.
   # bind_port = 8801

   # username and password for api server
   # username = admin
   # password = admin

.. toctree::
   :maxdepth: 2

   api/v1