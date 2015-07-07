RESTFUL API
===========

yabgp provides various endpoints that can be used to interact with the data and routers. Web API uses JSON format.

Version 1
~~~~~~~~~

REST API has basic http auth, through usename and password. The usename and password configured in configuration file and they have default values.

.. autoflask:: yabgp.api.app:app
   :undoc-static: