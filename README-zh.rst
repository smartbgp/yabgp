YABGP
=====

yabgp是什么？
~~~~~~~~~~~~~~

YABGP是另一种BGP协议的Python实现。它可以和各种路由器（包括Cisco/华为/Juniper的真实设备和一些模拟路由器比如GNS3）建立BGP连接，
接收解析BGP messages以供将来分析。

支持通过RESTful API发送BGP messages(route refresh/update)到其对等体。YABGP不能自主地发送任何BGP update messages，
它只是一个代理，一个控制器可以控制多个代理。

我们严格遵循RFCs文档的约定开发此项目。

此软件可应用于Linux/Unix，Mac OS和windows系统。

功能
~~~~~~~~

-  它可以通过IPv4地址以主动模式（作为TCP客户端）建立BGP会话连接。

-  支持TCP的MD5认证（只有IPv4并且不支持windows系统）

-  BGP capabilities支持：4字节的ASN，Route Refresh(Cisco Route Refresh)，添加发送/接收路径；

-  地址族支持：

   - IPv4/IPv6 Unicast
   
   - IPv4/IPv6 Labeled Unicast

   - IPv4 Flowspec(有限支持)

   - IPv4 SR Policy(draft-previdi-idr-segment-routing-te-policy-07)

   - IPv4/IPv6 MPLSVPN

   - EVPN (部分支持)
   
-  解析所有BGP messages为json格式并写入本地文件（可配置）；

-  支持通过基本的RESTFUL API获取对等体运行信息或者发送BGP messages。

快速开始
~~~~~~~~~~~

我们推荐在python的虚拟环境中运行``yabgp``，可以通过源码或者pip工具安装

源码安装：

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ git clone https://github.com/smartbgp/yabgp
    $ cd yabgp
    $ pip install -r requirements.txt
    $ cd bin
    $ python yabgpd -h

pip安装：

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ pip install yabgp
    $ which yabgpd
    /home/yabgp/yabgp-virl/bin/yabgpd
    $ yabgpd -h

例如：

.. code:: bash

    $ yabgpd --bgp-local_addr=1.1.1.1 --bgp-local_as=65001 --bgp-remote_addr=1.1.1.2 --bgp-remote_as=65001 --bgp-afi_safi=ipv4

文档
~~~~~~~~~~~~~

更多信息请参考 http://yabgp.readthedocs.org

相关项目
~~~~~~~~~~~~~~~~

路由监控能够向YABGP自动报警。https://github.com/nerdalize/routewatch

基于YABGP的一个BGP update生成器。https://github.com/trungdtbk/bgp-update-gen

支持
~~~~~~~

加入Slack，欢迎问题与建议，我们一起讨论。http://smartbgp.slack.com/

可以发送email到xiaoquwl@gmail.com，或者在GitHub上提issue。

贡献
~~~~~~~~~~

在这里创建GitHub Pull Request。https://github.com/smartbgp/yabgp/pulls

更多信息请阅读HACKING.rst文件。

感谢
~~~~~~

核心文件比如fsm，protocol我们从https://github.com/wikimedia/PyBal/blob/master/pybal/bgp.py 参考了一部分代码，

message解析，我们参照了这里的代码https://github.com/Exa-Networks/exabgp
