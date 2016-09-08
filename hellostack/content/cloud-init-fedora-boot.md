Title: cloud init和fedora云镜像登陆问题
Date: 2014-5-31 21:12
Tags: cloud
Slug: cloud-init-fedora-boot
Author: Ray Chen
Summary: 解释为什么fedora云镜像可以ssh key登陆。为什么cloud init方案解决了这些问题。

## Cloud-Init

cloudinit最初是ubuntu用来给自己的cloud image制作的工具，主要是解决cloud实例的初始化问题。比如:

* 设置默认的语言环境
* 设置云实例的hostname
* 自动产生实例的ssh密钥
* 自动给登陆用户注入ssh key从而免密码登陆
* 初始化临时的mount点

基本来说，cloudinit可以在云实例启动的事情传入用户数据。最典型的例子，在AWS中，我们只能用过ssh key的方式
来登陆云主机。这个ssh key可以是用户import进来的。利用cloudinit服务。实例在启动过程，主动向AWS获取传入的
ssh key，写入到用户目录下。这样主实例启动之后，就可以用ssh key的方式免密码登陆。

后来这个工具逐步扩展其他的云实例，意味着除了ubuntu云镜像，大部分的cloud image会预安装cloud init服务。
openstack云平台为了兼容AWS，提供metadata service API，进而完成openstack云实例的初始化工作。


## Fedora Cloud Image

fedora社区提供了云镜像，方便EC2或者openstack。从这里可以下载：

<http://fedoraproject.org/en/get-fedora#clouds>

这个云镜像可以直接给openstack使用的。我们这里下载下来，主要是给local的kvm使用。问题在于默认
fedora云镜像屏蔽了root登陆，而且root和普通用户fedora的密码都没有设置。

cloudinit文档特别说明这种情况：  如何在非云环境中使用

<http://cloudinit.readthedocs.org/en/latest/topics/datasources.html#no-cloud>


## 操作步骤


根据文档说明，我们先产生`meta-data`和`user-data`
```text
[ray@fedora cloud-init]$ { echo instance-id: saltvm-f20; echo local-hostname: fedora20; } > meta-data
[ray@fedora cloud-init]$ cat meta-data 
instance-id: saltvm-f20
local-hostname: fedora20
[ray@fedora cloud-init]$ printf "#cloud-config\npassword: passw0rd\nchpasswd: { expire: False }\nssh_pwauth: True\n" > user-data
[ray@fedora cloud-init]$ cat user-data 
#cloud-config
password: password
chpasswd: { expire: False }
ssh_pwauth: True

```

第二步，生成一个辅助的iso传递data
```text
[ray@fedora cloud-init]$ genisoimage  -output seed.iso -volid cidata -joliet -rock user-data meta-data
I: -input-charset not specified, using utf-8 (detected in locale settings)
Total translation table size: 0
Total rockridge attributes bytes: 331
Total directory bytes: 0
Path table size(bytes): 10
Max brk space used 0
183 extents written (0 MB)
```

最后启动，输入前面设置的密码即可登陆。 这里fedora20.img就是云镜像
```text
qemu-kvm -m 1024 -net nic -net user -drive file=fedora20.img,if=virtio -drive file=seed.iso,if=virtio
```

以上是直接修改密码的方式。我们也可以传入用户的ssh key，下面的内容加入到`user-data`即可
```text
ssh_authorized_keys:
  - ssh-rsa ... foo@foo.com (insert ~/.ssh/id_rsa.pub here)
```

更多示例请参考:

<http://cloudinit.readthedocs.org/en/latest/topics/examples.html#configure-instances-ssh-keys>

## 参考资料

* <https://help.ubuntu.com/community/CloudInit>
* <https://www.technovelty.org/linux/running-cloud-images-locally.html>
