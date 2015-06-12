RESTFUL API
===========

yabgp provides various endpoints that can be used to interact with the data and routers. Web API uses JSON format.

Version 1
~~~~~~~~~

REST API has basic http auth, through usename and password. The usename and password configured in configuration file and they have default values.

.. code:: bash

   (yabgp)bgpmon@demo:~$ curl -i -X GET http://127.0.0.1:8801/v1/peers
   HTTP/1.1 401 UNAUTHORIZED
   Date: Fri, 12 Jun 2015 09:33:55 GMT
   Content-Length: 19
   Content-Type: text/html; charset=utf-8
   WWW-Authenticate: Basic realm="Authentication Required"
   Server: TwistedWeb/15.0.0

   Unauthorized Access(yabgp)bgpmon@demo:~$ curl -u admin:admin -i -X GET http://127.0.0.1:8801/v1/peers
   HTTP/1.1 200 OK
   Date: Fri, 12 Jun 2015 09:34:03 GMT
   Content-Length: 222
   Content-Type: application/json
   Server: TwistedWeb/15.0.0

   {
     "peers": [
       {
         "fsm": "ESTABLISHED",
         "local_addr": "10.75.44.11",
         "local_as": 23650,
         "remote_addr": "10.124.1.245",
         "remote_as": 23650,
         "uptime": 55.64501404762268
       }
     ]
   }(yabgp)bgpmon@demo:~$

.. autoflask:: yabgp.api.app:app
   :undoc-static: