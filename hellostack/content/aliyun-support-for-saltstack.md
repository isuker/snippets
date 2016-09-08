Title: 把aliyun装进saltstack
Date: 2014-5-24 15:45
Category: Cloud
Tags: saltstack, python, cloud
Slug: aliyun-support-for-saltstack
Author: Ray Chen
Summary: 集成aliyun和salt-cloud


## salt-cloud

salt cloud 是一个轻量级的Cloud Orchestration工具，提供基于配置文件的云主机管理。利用它，我们可以在各个云服务提供商快速部署云主机。
好处主要有：

* 可以自动安装salt到云主机，进而维护整个云主机的配置管理和生命流程
* 支持的云主机很多，常见看到的都支持。
* 轻量级配置简单, YAML格式。


下面的例子可以很快的启动一台openstack实例。

VM profile 
```text
openstack_Fedora20:
    provider: openstack-config
    size: m1.small
    image: Fedora20
    ssh_key_name: myKey
    ssh_key_file: /home/ray/.ssh/id_rsa.pub
```

cloud provider file
```text
(vdev)[ray@fedora vdev]$ cat etc/salt/cloud.providers.d/openstack.conf 
openstack-config:
  # Configure the OpenStack driver
  #
  identity_url: http://192.168.1.111:5000
  #compute_name: nova
  protocol: ipv4

  compute_region: RegionOne

  # Configure Openstack authentication credentials
  #
  user: admin
  password: password
  # tenant is the project name
  tenant: demo

  provider: openstack

  # skip SSL certificate validation (default false)
  insecure: true

  networks:
      - fixed:
          - a1ccde5d-6817-4c98-862b-f90bd0e8c922
      - floating:
          - public

  ssh_interface: private_ips

```

更多的详细内容请参阅：
<http://docs.saltstack.com/topics/cloud/>


## aliyun

阿里云应该算是国内市场上用户量最大的云主机厂商。基本架构和REST API设计跟AWS类似。市场上模仿AWS的一大堆，却从未超过AWS。
这里能找到API文档： <http://help.aliyun.com/list/11113464.html?spm=5176.7224429.1997282881.55.J9XhVL>

我去申请了免费试用，只有5天的期限，跟亚马逊的一年免费使用比起来，呵呵呵。5天时间根本来不及体验更多的服务。
没有ssh key的概念，API也没有支持。root访问密码直接发送到手机。支持WEB访问主机终端，应该是VNC做的。

再说Aliyun ECS API，官方的SDK只有java， PHP 版本的。有python版本的demo。官方给出的第三方工具很少，基本是一些主机管理工具
和数据库管理工具，说明没有多少人在参与整个aliyun的生态建设。完全比不上taobao open API的规模。


## 集成

最近在看上面两个东西，所以很自然的想把aliyun集成到salt。salt的文档还行，照葫芦画瓢可以扩展salt cloud provider。大致的
步骤都是发送http rest请求，然后分析返回的数据，整理成json格式的，让salt cloud输出。

除了查询aliyun的基本信息，最重要的功能当然是创建一个主机实例出来，根据模板信息。openstack heat和AWS cloudformation都是一样的东西。

saltstack社区相当活跃，code review流程很快，而且几个core commiter人品很赞，很积极的帮你检查代码，给comment，
毫不吝啬给你代码点赞，鼓励你多给saltstack做贡献

提交的PR， 已经合并到上游，<https://github.com/saltstack/salt/pull/12888>

顺便贡献了我写的文档： [Get Started with Aliyun](http://docs.saltstack.com/en/latest/topics/cloud/aliyun.html)



