Title: openldap配置
Date: 2014-8-11 10:12
Category: Linux
Tags: ldap
Slug: openldap-config
Author: Ray Chen
Summary: OpenLDAP表示轻量级目录访问协议。

## 目录服务

目录是一个专门的数据库，专门用于搜索和浏览，另外也支持基本的查询和更新功能。目录往往包含描述性的，基于属性的信息和支持先进的过滤功能。目录的更新通常是简单的全部或者全无的变更，如果变更被允许的话。目录一般都调整为快速反应大批量查找或者搜索操作。


## OPENLDAP

LDAP表示轻型目录访问协议。它定义了一个简单协议，用来访问目录服务。什么样的信息可以存储在目录中？LDAP的信息模型是基于条目的。一个条目是一些属性的集合。有一个全球唯一的识别名(DN)，每个条目的有个类型和一个或多个值。每个条目下面属性和值就是明显的key-value模式。

例如：

```text
dn: ou=People,dc=example,dc=com
objectClass: organizationalUnit
ou: People
dn: ou=Groups,dc=example,dc=com
objectClass: organizationalUnit
ou: Groups
dn: cn=miners,ou=Groups,dc=example,dc=com
objectClass: posixGroup
cn: miners
gidNumber: 5000
dn: uid=john,ou=People,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: john
sn: Doe
givenName: John
cn: John Doe
displayName: John Doe
uidNumber: 10000
gidNumber: 5000
userPassword: johnldap
gecos: John Doe
loginShell: /bin/bash
homeDirectory: /home/john
```

LDAP目录树的组织，被排列爱一个分层的树形结构。这个结果反映了地域或者组织界限。下面的图片是两种不同的组织命名。

<http://www.openldap.org/doc/admin24/intro_tree.png>

<http://www.openldap.org/doc/admin24/intro_dctree.png>


## LDAP如何工作

LDAP采用客户－服务器模式. 包含在一个或多个LDAP服务器中的数据组成了目录信息树(DIT). 客户端连接到服务器然后问一个问题. 服务器返回一个应答和/或一个指针告诉客户端去哪里获得更多的信息 (通常是另一台 LDAP 服务器). 客户端连接哪台LDAP服务器不重要, 目录的视图看起来都一样; 一个提交到某台LDAP服务器的名字在另一台LDAP服务器上也将指向相同的条目. 这是全球目录服务的一个重要功能.


## 配置

LDAP安装好之后，2.3版本之前必须要配置sldapd文件。但在2.3版本之后，完全允许LDAP利用LDIF数据库文件来管理LDAP。LDAP配置引擎允许所有的slapd配置选项在运行中改变，一把不需要重启sldapd使其生效。例如之前，我们想修改ldap的logging level，一般直接到slapd.conf文件直接修改。现在支持这样，先定义一个LDIF文件logging.ldif

```text
dn: cn=config
changetype: modify
add: olcLogLevel
olcLogLevel: stats
```

然后执行这个改变: `sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f logging.ldif`

换句话说，新版的LDAP建议用户使用LDIF和ldap命令集合来管理LDAP。但是旧风格的dlapd.conf依旧是支持的，为了保持向前兼容。特别要注意的是，新风格采用了slapd后端数据库来存储配置，务必不能两个风格混用。

旧风格的slapd.conf配置在centos上

<http://www.centoscn.com/image-text/config/2013/0819/1367.html>

新风格的IDIF配置在ubuntu

<https://help.ubuntu.com/12.04/serverguide/openldap-server.html#openldap-server-logging>

另外，我们需要注意到，LDIF方式只是slapd的某一种数据库方式，因为它把信息保存在text文件当中。slapd本身支持很多数据库后端，常见的就是Berkeley DB backends，配置文件中看到的hdb即是。


## 调试

我们可以开启sldapd debug mode，方便看到更多的错误日志。运行`slapd -d 1`即可。更多的调试级别：

```text
级别|关键字|描述
---|--------|---
0||不调试
1|(0x1 trace)|跟踪函数调用
2|(0x2 packets)|调试包的处理
4|(0x4 args)|重度跟踪调试
8|(0x8 conns)|连接管理
16|(0x10 BER)|打印发送和接收的包
32|(0x20 filter)|搜索过滤器的处理
64|(0x40 config)|配置处理
128|(0x80 ACL)|访问控制列表处理
256|(0x100 stats)|连接/操作/结果的统计日志
512|(0x200 stats2)|发送的条目的统计日志
1024|(0x400 shell)|打印和shell后端的通信
2048|(0x800 parse)|打印条目解析调试
16384|(0x4000 sync)|syncrepl消费者处理
32768|(0x8000 none)|只显示那些不受日志级别设置影响的消息
```


## 参考

1. <http://wiki.jabbercn.org/OpenLDAP2.4%E7%AE%A1%E7%90%86%E5%91%98%E6%8C%87%E5%8D%97#.E4.BB.80.E4.B9.88.E6.98.AF.E7.9B.AE.E5.BD.95.E6.9C.8D.E5.8A.A1.3F>
2. <http://www.openldap.org/doc/admin24/>
