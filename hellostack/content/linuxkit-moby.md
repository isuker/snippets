Title: 容器生态系统.md
Date: 2017-6-21 21:30
Category: Docker
Tags: docker,hyper,linuxkit
Slug: linuxkit-moby-k8s
Author: Ray Chen
Summary: 容器生态系统渐成，大势所趋。


* 近期docker收回商标，开源项目docker改名为moby。这个无可厚非。docker期望复制redaht的成功模式，docker-moby的关系就对应着redhat linux-fedora。 Moby（https://github.com/moby/moby）包含很多容器化的后台组件（containerd, swramkit等）。docker希望借助moby搭积木的方式，让容器爱好者进行各种各样的组合。完全由开源社区驱动。

* docker公司推出linuxkit开源项目，剑指容器运行平台。容器诞生于linux平台，依赖LXC资源隔离。站稳linux后，docker进而想推广容器到win/mac平台。主要是依赖虚拟化软件，先创建linux vm，然后在vm里配置docker环境。比如说起初的docker for mac。参考[docker machine](https://docs.docker.com/machine/)项目。主要目的就是支持各大虚拟机provider，方便部署docker 运行时。但这仅仅是解决了简单部署，用户使用起来感觉docker依赖虚拟机。而这点恰恰跟市场上的主流期望相反：docker不是下一个银弹，用来代替虚拟机的吗？

孰不可忍的情况下，docker推出linuxkit，希望借此一统容器运行平台的控制平面。最大的改变（亮点）有两种：

1) everything service is container
立足于linux平台，精简linux kernel和服务启动流程。让docker containd变身id为1号的根进程。后续所有系统服务都采用容器方式运行。再后续的方向，无非裸机启动。容器已然演变成一个操作系统（任务会很艰巨，因为设备管理等常见os功能，这是另一项工程。）. 同时采用mocy的“积木”模块，可以让用户迅速启动一套复杂的容器系统。

2) docker can run on all platform
扩展至所有平台。三大主流linux/win/mac一网打尽。利用linuxkit打包linux kernel和initrd img，然后用平台虚拟化软件来启动这个docker os。这里容器和vm的界限已经很模糊，既是容器又是虚拟机。而linuxkit本身用go语言编程，运行在其他平台不是难事。
linuxkit初探案例：<http://feisky.xyz/2017/04/19/LinuxKit/>

这种思路跟目前市场已经存在的hypercontainer和vsphere。vic异曲同工。很难讲谁抄袭谁的思路。
假如linuxkit的原生运行容器方式大获成功，目前市场的各大容器os没有生存空间。docker基本平台一统天下，后面就到来发展生态圈的时刻。

* kubernetes作为容器管理平台，完美的诠释来google的技术实力和战略眼光。但毕竟是容器的管理平台，需要定义在哪里运行容器。开源之后，各大IAAS平台纷纷支持，推出相应的cloud provider，方便k8s进行控制平面。但google留了心眼，从一开始的插件设计，就考虑到支持不同的容器运行时。就是说docker那套运行时可以替换成第三方。这也从着侧面反应docker的亮点在于标准化的image。同时主导社区推出OCI基金会，标准化容器运行时，避免docker运行时一家独大。

```text
Established in June 2015 by Docker and other leaders in the container industry, the OCI currently contains two specifications: the Runtime Specification (runtime-spec) and the Image Specification (image-spec). The Runtime Specification outlines how to run a “filesystem bundle” that is unpacked on disk. At a high-level an OCI implementation would download an OCI Image then unpack that image into an OCI Runtime filesystem bundle. At this point the OCI Runtime Bundle would be run by an OCI Runtime.
```

* 容器运行时标准文档：<https://github.com/opencontainers/runtime-spec/blob/master/runtime.md>
各家厂商按照标准接口实现自己的runtime。 当然目前docker捐献的containerd是最主流支持。
比如hypercontainer采用hypervisor方式的运行时：<https://github.com/hyperhq/runv>

采用标准意味着你可以用docker的命令来运行hyercontainer的容器方式。下面的例子实际上在运行hypercontainer。

```shell
# in terminal #1 
$ docker-containerd --debug -l /var/run/docker/libcontainerd/docker-containerd.sock \ --runtime /path/to/runv --runtime-args --debug --runtime-args --driver=libvirt \ --runtime-args --kernel=/opt/hyperstart/build/kernel \ --runtime-args --initrd=/opt/hyperstart/build/hyper-initrd.img \ --start-timeout 2m 
# in terminal #2 
$ docker daemon -D -l debug --containerd=/var/run/docker/libcontainerd/docker-containerd.sock 
# in terminal #3 for trying it 
$ docker run busybox ls bin
```

* Linuxkit+Moby+Kubernetes组合形成容器基础架构的闭环开源系统。正如docker自己所说：“if the ecosystem succeeds, we succeed.” 技术改变世界，结尾彩蛋：<https://ruanyf.github.io/survivor/future/boundary.html>

