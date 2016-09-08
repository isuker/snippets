Title: yum-axelget插件更新
Date: 2014-5-13 00:12
Category: Python
Tags: yum, python
Slug: yum-axelget-update
Author: Ray Chen
Summary: yum-axelget更新到Fedora20并且已经在官方库. 实现的基本原理就是：在Yum Code下载之前，用axel把所有需要的RPM/DRPM提前下载好。之前的版本有问题，主要是因为presto（Delta RPM）现在直接merge到Yum Core Code。

周末花了一天时间，把 yum-axelget更新到Fedora20. 实现的基本原理就是：在Yum Code下载之前，用axel把所有需要的RPM/DRPM提前下载好。之前的版本有问题，主要是因为presto（Delta RPM）现在直接merge到Yum Core Code。

远期计划支持多种下载工具，让用户自己选择

项目地址：<https://github.com/crook/yum-axelget/>

目前yum-axelget已经在Fedora官方库，可以直接`yum install yum-axelget` 安装


截图：
```text
(vdev)[ray@fedora yum-axelget]$ sudo yum install ddd
Loaded plugins: axelget, fastestmirror, priorities
No metadata available for fedora
No metadata available for rpmfusion-free
No metadata available for rpmfusion-free-updates
No metadata available for rpmfusion-nonfree
No metadata available for rpmfusion-nonfree-updates
No metadata available for updates
Loading mirror speeds from cached hostfile
 * fedora: mirrors.hustunique.com
 * rpmfusion-free: mirror.bjtu.edu.cn
 * rpmfusion-free-updates: mirror.switch.ch
 * rpmfusion-nonfree: mirror.bjtu.edu.cn
 * rpmfusion-nonfree-updates: mirror.bjtu.edu.cn
 * updates: mirrors.hustunique.com
Resolving Dependencies
--> Running transaction check
---> Package ddd.x86_64 0:3.3.12-16.fc20 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==============================================================================================================================================
 Package                Arch                              Version                                    Repository                          Size
==============================================================================================================================================
Installing:
 ddd                    x86_64                            3.3.12-16.fc20                             updates                            1.5 M

Transaction Summary
=============================================================================================================================================
Install  1 Package

Total download size: 1.5 M
Installed size: 4.5 M
Is this ok [y/d/N]: y
Downloading packages:
ddd-3.3.12-16.fc20.x86_64.rpm                                                                                             | 1.5 MB  00:00:05     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : ddd-3.3.12-16.fc20.x86_64                                                                                                 1/1 
  Verifying  : ddd-3.3.12-16.fc20.x86_64                                                                                                 1/1 

Installed:
  ddd.x86_64 0:3.3.12-16.fc20                                                                                                                         

Complete!
```

跟没有axelget插件的安装界面完全一样。但是这里的ddd rpm实质是axel安装的。 可用`yum -d 3 install ddd`看实际的效果。

全文完。

