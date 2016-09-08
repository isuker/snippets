Title: docker初探
Date: 2014-5-27 16:04
Category: Cloud
Tags: docker
Slug: first-look-docker
Author: Ray Chen
Summary: 初探docker，一个开源的应用容器引擎。

## 介绍
要理解docker, 必须看明白什么是容器。Docker的后端使用的是[LXC](https://linuxcontainers.org/). 后者是linux的系统虚拟化工具。容器不同于一般的虚拟化软件(KVM, XEN, Vmware)，它是基于linux cgroup二次开发的OS层面的虚拟化。LXC容器之间共享底层的OS，相对XEN/KVM/VMWARE等完全虚拟化一个硬件抽象的虚拟机。LXC的轻量特性就体现在资源隔离。容器内部只是一个文件系统级别的独立系统空间。

Docker基于LXC做了大量的工作，不仅仅只是个LXC的管理工具。最大的亮点是定义了一个完整的容器生命周期，包含创建/删除容器，管理容器，还有共享和分发容器。docker index是个在线的容器APP共享站点。一个APP，里面可能只装上了wordpress，或者配置好了LAMP环境。比如这个例子mysql docker app： [Mysql Docker](https://index.docker.io/u/panamax/panamax-docker-mysql/)

目前docker的三个组件：

* Docker container
* Docker images
* Docker registries

[docker和虚拟机的区别](http://docs.docker.io/introduction/understanding-docker/#docker-versus-virtual-machines)


## 安装
在Fedora平台，直接从yum仓库安装： `sudo yum install docker-io` 更多安装文档，请参考： <http://docs.docker.io/installation/>

安装docker之后，把docker服务启动。 `/etc/init.d/docker start`

接着，运行`docker info`  验证是否成功安装。
```text
[root@ncvm9087109 ~]# docker info
Containers: 10
Images: 41
Storage Driver: devicemapper
 Pool Name: docker-253:0-1332588-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 3635.9 Mb
 Data Space Total: 102400.0 Mb
 Metadata Space Used: 4.1 Mb
 Metadata Space Total: 2048.0 Mb
Execution Driver: lxc-0.9.0
Kernel Version: 2.6.32-431.el6.x86_64
[root@ncvm9087109 ~]# ps -ef | grep lxc
root      1518 32566  0 May26 pts/1    00:00:00 lxc-start -n d5ccfc971616c968e958f1d3bdfd3806b37f7159cf0a5d7cb1f6a7430f1e4d14 -f /var/lib/docker/containers/d5ccfc971616c968e958f1d3bdfd3806b37f7159cf0a5d7cb1f6a7430f1e4d14/config.lxc -- /.dockerinit -driver lxc -g 172.17.42.1 -i 172.17.0.2/16 -mtu 1500 -- /bin/bash
```


## Hello World

现在开始环境，从docker index下载一个base的fedora image： <https://index.docker.io/_/fedora/>. 这个fedora image只有100多MB，只包含了了最基本的运行环境。
```text
[ray@ncvm9087109 ~]$ sudo docker pull fedora
Pulling repository fedora
5cc9e91966f7: Download complete 
b7de3133ff98: Download complete 
511136ea3c5a: Download complete 
ef52fb1fe610: Download complete 
[root@ncvm9087109 devicemapper]# docker images fedora
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
fedora              rawhide             5cc9e91966f7        2 weeks ago         372.7 MB
fedora              20                  b7de3133ff98        4 weeks ago         372.7 MB
fedora              heisenbug           b7de3133ff98        4 weeks ago         372.7 MB
fedora              latest              b7de3133ff98        4 weeks ago         372.7 MB
```

运行下面的命令：
```text
[root@ncvm9087109 ~]# docker run fedora /bin/echo hello world
hello world
```


## SSH示例 

我们看一个复杂的例子，首先定义个[Dockerfile](http://docs.docker.io/reference/builder/)。 跟其他的配置工具(puppet/saltstack)类似，docker定义了一系统的关键字语法，让用户自动化创建image的步骤。看下面的文件。先下载ubuntu这个base image，接着添加软件源后同步系统到最新release。然后用apt安装了sshd server，同时修改了root的密码。最后告诉docker，这个容器需要暴露22端口，最后的命令用来启动sshd。
```text
# sshd
#
# VERSION               0.0.1
FROM     ubuntu
MAINTAINER Thatcher R. Peskens "thatcher@dotcloud.com"
# make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd  && chmod 755 /var/run/sshd
RUN echo 'root:screencast' |chpasswd
EXPOSE 22
CMD    /usr/sbin/sshd -D
```

注意`chmod 755 /var/run/sshd`不要忘记，不然会出现这个错误：可以用`docker logs <container>`检查错误。
```text
root@95de4d97ee3a:/var/run# /usr/sbin/sshd -D
/var/run/sshd must be owned by root and not group or world-writable.
```

dockerfile文件准备好之后，用`docker build`命令来build image
```text
root@ncvm9087109 devicemapper]# docker build --rm -t eg_sshd - < docker_sshd
Uploading context 2.048 kB
Uploading context 
Step 0 : FROM     ubuntu
 ---> 99ec81b80c55
Step 1 : MAINTAINER Thatcher R. Peskens "thatcher@dotcloud.com"
 ---> Running in d9e8a48ff85a
 ---> 5b880b2168aa
Removing intermediate container d9e8a48ff85a
Step 2 : RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
 ---> Running in 5611f57e25e6
 ---> da2fa697d676
Removing intermediate container 5611f57e25e6
Step 3 : RUN apt-get update
 ---> Running in b313afedb3ad
Ign http://archive.ubuntu.com precise InRelease
Get:1 http://archive.ubuntu.com precise Release.gpg [198 B]
Get:2 http://archive.ubuntu.com precise Release [49.6 kB]
Get:3 http://archive.ubuntu.com precise/main amd64 Packages [1273 kB]
Get:4 http://archive.ubuntu.com precise/universe amd64 Packages [4786 kB]
Fetched 6109 kB in 5s (1182 kB/s)
Reading package lists...
 ---> 0140b777b50b
Removing intermediate container b313afedb3ad
Step 4 : RUN apt-get install -y openssh-server
 ---> Running in e17e8919d7d1
Reading package lists...
Building dependency tree...
Reading state information...
The following extra packages will be installed:
  ca-certificates krb5-locales libedit2 libgssapi-krb5-2 libidn11 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libwrap0 libx11-6 libx11-data libxau6
  libxcb1 libxdmcp6 libxext6 libxmuu1 openssh-client openssl ssh-import-id
  tcpd wget xauth
Suggested packages:
  krb5-doc krb5-user ssh-askpass libpam-ssh keychain monkeysphere
  openssh-blacklist openssh-blacklist-extra rssh molly-guard ufw
The following NEW packages will be installed:
  ca-certificates krb5-locales libedit2 libgssapi-krb5-2 libidn11 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libwrap0 libx11-6 libx11-data libxau6
  libxcb1 libxdmcp6 libxext6 libxmuu1 openssh-client openssl ssh-import-id
  tcpd wget xauth
Suggested packages:
  krb5-doc krb5-user ssh-askpass libpam-ssh keychain monkeysphere
  openssh-blacklist openssh-blacklist-extra rssh molly-guard ufw
The following NEW packages will be installed:
  ca-certificates krb5-locales libedit2 libgssapi-krb5-2 libidn11 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libwrap0 libx11-6 libx11-data libxau6
  libxcb1 libxdmcp6 libxext6 libxmuu1 openssh-client openssh-server openssl
  ssh-import-id tcpd wget xauth
0 upgraded, 24 newly installed, 0 to remove and 0 not upgraded.
Need to get 4178 kB of archives.
After this operation, 12.9 MB of additional disk space will be used.
......
Setting up tcpd (7.6.q-21) ...
Setting up ssh-import-id (2.10-0ubuntu1) ...
Processing triggers for libc-bin (2.19-0ubuntu6) ...
Processing triggers for ureadahead (0.100.0-16) ...
 ---> 6e430d647352
Removing intermediate container e17e8919d7d1
Step 5 : RUN mkdir /var/run/sshd
 ---> Running in eee245ce4ee1
 ---> 468ba80bb857
Removing intermediate container eee245ce4ee1
Step 6 : RUN echo 'root:screencast' |chpasswd
 ---> Running in bd6f65acaf7a
 ---> 4a9fb44bd5df
Removing intermediate container bd6f65acaf7a
Step 7 : EXPOSE 22
 ---> Running in dfccfd6cd0de
 ---> f5b10cde65f7
Removing intermediate container dfccfd6cd0de
Step 8 : CMD    /usr/sbin/sshd -D
 ---> Running in ffc41d6e7204
 ---> 107b63fd863e
Removing intermediate container ffc41d6e7204
Successfully built 107b63fd863e
```

创建好image之后，可以启动这个image。
```text
[root@ncvm9087109 devicemapper]# docker run -d -P -name test_sshd eg_sshd
Warning: '-name' is deprecated, it will be replaced by '--name' soon. See usage.
f1b631682b58e2c72c1677703f96dcfe619afa3b61b9796abbd30010b0b28fd0
[root@ncvm9087109 devicemapper]# docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                   NAMES
f1b631682b58        eg_sshd:latest      /bin/sh -c '/usr/sbi   3 minutes ago       Up 3 minutes        0.0.0.0:49155->22/tcp   test_sshd      
```

ps可以看到刚才的container在运行，同时ssh的22 port映射到内部的49155， 也可以用`docker port`看出来。
```text
[root@ncvm9087109 devicemapper]# docker port test_sshd 22
0.0.0.0:49155
[root@ncvm9087109 devicemapper]# docker inspect test_sshd
[{
    "ID": "f1b631682b58e2c72c1677703f96dcfe619afa3b61b9796abbd30010b0b28fd0",
    "Created": "2014-05-27T06:50:11.800415844Z",
    "Path": "/bin/sh",
    "Args": [
        "-c",
        "/usr/sbin/sshd -D"
    ],
    "Config": {
        "Hostname": "f1b631682b58",
        "Domainname": "",
        "User": "",
        "Memory": 0,
        "MemorySwap": 0,
        "CpuShares": 0,
        "AttachStdin": false,
        "AttachStdout": false,
        "AttachStderr": false,
        "PortSpecs": null,
        "ExposedPorts": {
            "22/tcp": {}
        },
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": [
            "HOME=/",
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ],
        "Cmd": [
            "/bin/sh",
            "-c",
            "/usr/sbin/sshd -D"
        ],
        "Image": "eg_sshd",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "NetworkDisabled": false,
        "OnBuild": null
    },
    "State": {
        "Running": true,
        "Pid": 16375,
        "ExitCode": 0,
        "StartedAt": "2014-05-27T06:50:12.007032752Z",
        "FinishedAt": "0001-01-01T00:00:00Z"
    },
    "Image": "923a1ba95ae16047a0bf3a5430fc4cc858267fdca90b3c939cbcf6747ccfd595",
    "NetworkSettings": {
        "IPAddress": "172.17.0.2",
        "IPPrefixLen": 16,
        "Gateway": "172.17.42.1",
        "Bridge": "docker0",
        "PortMapping": null,
        "Ports": {
            "22/tcp": [
                {
                    "HostIp": "0.0.0.0",
                    "HostPort": "49155"
                }
            ]
        }
    },
    "ResolvConfPath": "/etc/resolv.conf",
    "HostnamePath": "/var/lib/docker/containers/f1b631682b58e2c72c1677703f96dcfe619afa3b61b9796abbd30010b0b28fd0/hostname",
    "HostsPath": "/var/lib/docker/containers/f1b631682b58e2c72c1677703f96dcfe619afa3b61b9796abbd30010b0b28fd0/hosts",
    "Name": "/test_sshd",
    "Driver": "devicemapper",
    "ExecDriver": "lxc-0.9.0",
    "MountLabel": "",
    "ProcessLabel": "",
    "Volumes": {},
    "VolumesRW": {},
    "HostConfig": {
        "Binds": null,
        "ContainerIDFile": "",
        "LxcConf": [],
        "Privileged": false,
        "PortBindings": {
            "22/tcp": [
                {
                    "HostIp": "0.0.0.0",
                    "HostPort": "49155"
                }
            ]
        },
        "Links": null,
        "PublishAllPorts": true,
        "Dns": null,
        "DnsSearch": null,
        "VolumesFrom": null,
        "NetworkMode": "bridge"
    }
}]
```

最后可以ssh连接到这个运行的容器。IP是docker在主机上daemon的ip，从ipconfig可以看出来：
```text
[root@ncvm9087109 devicemapper]# ip a
7: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN 
    link/ether fe:bc:7d:30:93:cb brd ff:ff:ff:ff:ff:ff
    inet 172.17.42.1/16 scope global docker0
    inet6 fe80::2c64:f0ff:feb8:d96e/64 scope link 
       valid_lft forever preferred_lft forever
[root@ncvm9087109 devicemapper]# ssh  root@172.17.42.1 -p 49155
The authenticity of host '[172.17.42.1]:49155 ([172.17.42.1]:49155)' can't be established.
RSA key fingerprint is d7:1c:11:ed:a2:03:76:54:7b:32:53:c6:b1:d3:ef:33.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[172.17.42.1]:49155' (RSA) to the list of known hosts.
root@172.17.42.1's password: 
Last login: Tue May 27 06:55:29 2014 from 172.17.42.1
root@f1b631682b58:~# netstat -anp
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      7/sshd          
tcp        0      0 172.17.0.2:22           172.17.42.1:49690       ESTABLISHED 32/0            
tcp6       0      0 :::22                   :::*                    LISTEN      7/sshd   
```


## 总结

docker提供了一个迅速部署linux容器的方案。一份docker image，可以放在装有docker的任何平台运行。特别应用于部署开发测试环境。占用系统主机资源少的同时，达到了资源隔离的效果（归功于cgroup）。
基于docker做了PAAS平台： https://github.com/deis/deis


## 参考

* <http://docs.docker.io/>
* <https://log.qingcloud.com/?p=129>
* <http://www.vpsee.com/2013/07/use-docker-and-lxc-to-build-a-desktop/>
* <https://www.docker.io/the_whole_story/>
