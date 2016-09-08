Title: openstack默认关闭文件注入功能
Date: 2014-7-03 23:32
Tags: python,openstack
Slug: openstack-disable-file-injection
Author: Ray Chen
Summary: openstack 从H版本默认不再支持文件注入，推荐使用ConfigDrive或metadata服务。


openstack 从H版本默认不再支持文件注入，推荐使用ConfigDrive或metadata服务。如果要继续使用，
需要配置inject_key=true，inject_partition，inject_password=true

1. inject_partition = -1 表示只注入文件
2. inject_partition = -2 表示disable此功能
3. inject_partition = $number 表示分区号码


## Config Drive

Config Drive的目的是，当nova实例启动后，可以mount一个元数据的文件系统，方便交换数据。

例如这样的命令行：
```text
nova boot --config-drive=true --file test_file=/home/ray/.ssh/known_hosts --meta name=Ray --flavor 1 --key-name mykey --block-device-mapping vda=4f1f0e06-4bdf-4af3-b301-dd24d8395e5b --security_group default myOSWithKey2
```

想对应的log。 用到`genisoimage`命令生成一个新的iso

```text
2000 2014-07-03 22:39:16.244 INFO nova.virt.libvirt.driver [req-4d01bb41-3689-4143-a4c4-961fc86b3dd8 admin demo] [instance: af475750-2c58-48c8-9c2d-bd     13d2d0fb7f] Creating config drive at /opt/stack/data/nova/instances/af475750-2c58-48c8-9c2d-bd13d2d0fb7f/disk.config
2001 2014-07-03 22:39:16.245 DEBUG nova.openstack.common.processutils [req-4d01bb41-3689-4143-a4c4-961fc86b3dd8 admin demo] Running cmd (subprocess):      genisoimage -o /opt/stack/data/nova/instances/af475750-2c58-48c8-9c2d-bd13d2d0fb7f/disk.config -ldots -allow-lowercase -allow-multidot -l -publis     her OpenStack Nova 2014.2 -quiet -J -r -V config-2 /tmp/cd_gen_oKkFq3 execute /opt/stack/nova/nova/openstack/common/processutils.py:160
2002 2014-07-03 22:39:16.311 DEBUG nova.openstack.common.processutils [req-4d01bb41-3689-4143-a4c4-961fc86b3dd8 admin demo] Result was 0 execute /opt/     stack/nova/nova/openstack/common/processutils.py:194
......
2004 2014-07-03 22:39:16.623 DEBUG nova.openstack.common.processutils [req-4d01bb41-3689-4143-a4c4-961fc86b3dd8 admin demo] Running cmd (subprocess):      env LC_ALL=C LANG=C qemu-img info /opt/stack/data/nova/instances/af475750-2c58-48c8-9c2d-bd13d2d0fb7f/disk.config execute /opt/stack/nova/nova/op     enstack/common/processutils.py:160
```

等实例启动之后，登陆进去,可以mount这个config drive。 默认的disk label 是`config-2`
```text
$ sudo mkdir -p /mnt/config
$ sudo mount /dev/disk/by-label/config-2 /mnt/config
mount: mounting /dev/disk/by-label/config-2 on /mnt/config failed: No such file or directory
$ sudo blkid -t LABEL="config-2" -odevice
/dev/sr0
$ sudo mount /dev/sr0 /mnt/config
$ cd /mnt/config
$ ls -l
total 4
dr-xr-xr-x    4 root     root          2048 Jul  3 10:20 ec2
dr-xr-xr-x    7 root     root          2048 Jul  3 10:20 openstack
$ cat latest/meta_data.json 
{"files": [{"path": "test_file", "content_path": "/content/0000"}], "admin_pass": "uogP9pqkr9Tz", "random_seed": "wGxbuZ2CVfQpKvF5IoHLDss2YwQEBudGGSxhLXz0JWtF+FEBKnVPbudfNPJIINwPSrUPxsHbX1YUg+pnUv9Lqxc6YWjxsIDoxfh4Ybh/LVUjTIcr+AletrPF5/3DKvwjquqHN218LmEPx/l4H6eryf2S2GPE2CUJHjnEjIFL0cqb2EcCTFSVEw9Eve1RELVPpPMmIpPowumEz+ML0IvnLXpgyhUA4WsDIUCEXScPsnE7GuuLEJAN2D0NpggXZzMj2/kM6dr6ox07w7UMaLBzTwzrvqRgg6W+4oARk40IXp2j8KGRaoFAh6gO4eO2PzmrRSGDqXTTwpa5vBBXgy4qMHOWldaOdaA0p9+JrwqEbsPEceMPrUGEkqS/kiEqa2hUCp9uwTzeRkp19FSJ19FqqoSav6n5wDnsgnFB7JJ5pR037YM56riNOcmS8Xjh5Gg72rqz43I8mADqVCau84IqgIEVBqPWnE0CRYpinJhmslXdfg/GY13B7rtXtZKazt2W14zlHuHMa9R612C6hCYXams0bOWYIlGso81ae01TVH5p6f/4fm0Kq8GTz6YVeDl+mjYdp+6p75GXa0QdsvzbjNjAb/2hNmhpZ7tx26E3QMjJrNDC4DBNA81U5IoZxG8Ppwj8SiC2qtTpNDlKb7OuiQmpmGTBRAjdJ+/KVLPsmb0=", "uuid": "84c73cad-d8ec-4dad-aa75-a89b0ef11266", "availability_zone": "nova", "hostname": "myoswithkey2.novalocal", "launch_index": 0, "meta": {"name": "Ray"}, "public_keys": {"mykey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3pipuritq3xYAy2dpGULD9jw+6IKJwe1UI/tuy5hsbgjOLjUU1xMjF00BsmRMnXu/W8G+l58yNsncwXc1TS8eq3brm9692cZmweJv23BcWRfVtVhqmsRsyA6FZf/fOGKJ/OlYt1/7pWZEiftQiLB2jusRBeGn0kWb9oD/q1O2Ii9eTI2Wzrtd3dSzGLP8PMqb0qwEfdYr7PJYO9LjcDqptk0yNTodsPpPyuuySwsdXu/qcV3+2aJBR32wB0z8GQ2vP1MeHpttsaze5462s36XtnYWaDmFTZl5GmlWg7izYNQovzplzWOmruF6S/v/S3sIK4PKcYwdwE6LnKgF2uYz ray@fedora20\n"}, "name": "myOSWithKey2"}$ 
```

更多官方文档介绍：

* <http://docs.openstack.org/grizzly/openstack-compute/admin/content/config-drive.html>
* <http://docs.openstack.org/grizzly/openstack-compute/admin/content/instance-data.html>


## Metadata Service

openstack元数据服务，用来给虚拟机实例传递数据。 服务端口地址是写死的： http://169.254.169.254 

为什么是这个地址，[再这里有介绍](http://www.pubyun.com/blog/openstack/%E4%BB%80%E4%B9%88%E6%98%AFopenstack%E7%9A%84-metadata/)

官方文档有详细介绍用法。
<http://docs.openstack.org/grizzly/openstack-compute/admin/content/metadata-service.html>


## 参考资料

* <https://blueprints.launchpad.net/nova/+spec/disable-file-injection-by-default>
* <https://review.openstack.org/#/c/70239/>
* <https://bugzilla.redhat.com/show_bug.cgi?id=1056381>
* <https://bugs.launchpad.net/nova/+bug/1221985>

