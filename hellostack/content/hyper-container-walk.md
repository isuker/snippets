Title: 超容器：虚拟机 or 容器
Date: 2016-9-13 21:49
Category: Docker
Tags: docker
Slug: hyper-container-walk
Author: Ray Chen
Summary: 容器和虚拟机谁是未来？哪个更好？答案也许是集两者优点之超容器。

## 什么是超容器

容器大有取代虚拟机之势，但最大的缺点就是安全问题。要想从根本上解决安全问题，就是要做资源隔离，特别是共享的底层操作系统要做到逻辑上的隔离。然而这恰恰是docker容器引以为傲的特性之一：共享一个内核。

其实容器和虚拟机的应用场景大有不同。docker容器解决的问题就是部署，运维和分布软件的方式。VM在数据中心中依然占有统治地位，而且生态系统已经运行了很多年。docker容器出现之后，针对虚拟机的诟病是各大非标准化的iamge，而且体积巨大（上GB）。 hypervisor之间互不兼容。

可不可以既保证虚拟机的安全，又可以享用容器的轻便和方便部署。在我们平常的容器部署中，基本上是在虚拟机上运行容器。例如在AWS EC2上面搭建k8s集群。这种方式的缺点是资源浪费, 包含虚拟机的运行开销。比如申请了一台4GB的EC2.你在上面只跑了一个docker运行http服务。或者优化空间是在一台虚拟机上面多运行些容器。

另外一个优化方向是，申请虚拟机资源的时候，尽量申请小资源的EC2。 云服务提供商尽可能提供小的资源单位。例如virtustream的uVM <http://www.virtustream.com/software/micro-vms>

以上就是超容器这个概念出现的原因。 这里我看到一个新的方案 <http://www.hypercontainer.io/>： 

    * HyperContainer = Hypervisor + Guest Kernel + Data (image) *

容器利用虚拟机的硬件隔离提高安全系数，结合定制化的微内核，在hypervior直接运行Image（兼容docker image）。 容器启动运行之后，即是虚拟机又是容器。即可以继续使用虚拟机的生态工具，又可以提供容器运行环境。简单来说，就说用hypervisor带代替容器需要的运行时和命令空间。



## 架构

Hyper包含四个组件：

* HyperKernel:  定制化的linux kernel，可以直接被hypervior运行。可以理解成一个微型的container os

* HyperDamon: 运行在主机上的后台agent。主要是提供REST API

* CLI:  hyper的前端入口。通过REST跟Damon通信，调度后端具体哪个host来部署container

* HyperStart: 基本就是initramfs 和 init服务

![](http://thenewstack.io/wp-content/uploads/2015/07/image011.png)

容器基础工作弄好之后，hyper基本就是一个docker的翻版。基本命令行跟docker一行，然后hyper可以直接运行docker hub上面的iamge。 为了更有效的管理hyper容器, 开发了支持k8s运行时的<https://github.com/hyperhq/hypernetes>. 就是一个Caas，同时支持多租户。这个容器云已经开放，用户可以注册使用，按秒为单位计费。初始赠送20美元。有兴趣的可以去看看。



## 容器标准化

为了避免docker一家独大后的垄断行为（Docker的强推SWARM就好比微软捆绑IE销售，在容器编排器的百家争鸣下，google的k8s明显是开源社区的一致选择）， 开源社区推出标准化组织OCI<https://www.opencontainers.org/>, 在其[github主页](https://github.com/opencontainers/runtime-spec)的自我介绍是： The Open Container Initiative develops specifications for standards on Operating System process and application containers.

hypercontainer有自己的实现： <https://blog.hyper.sh/a_step_towards_the_open_container_initiative.html>



## 类似项目

* Interl的clearContainer: https://clearlinux.org/features/clear-containers
* Vmware的VIC: https://github.com/vmware/vic [传统容器主机和VIC模式的比较](https://github.com/vmware/vic/blob/master/doc/design/arch/vic-container-abstraction.md)


## 资料

* <http://thenewstack.io/hyper-a-hypervisor-agnostic-docker-engine/>
* <https://blog.hyper.sh/hyper-and-the-art-of-containerization.html>
* <http://wangxu.me/zhihu/2016/05/20/how-about-hyper/index.html>
* <https://m.douban.com/note/581584151/?bid=u39uR-VeuJs>
* <http://blog.kubernetes.io/2016/05/hypernetes-security-and-multi-tenancy-in-kubernetes.html>
