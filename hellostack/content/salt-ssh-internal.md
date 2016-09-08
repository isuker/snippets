Title: salt-ssh实现原理
Date: 2014-6-10 22:37
Tags: python,saltstack
Slug: salt-ssh-internal
Author: Ray Chen
Summary: salt-ssh最终还是在远程机器上本地执行salt-call

## salt-ssh
salt-ssh出现的理由是这么个逻辑。一般salt需要安装和启动minion，这样master才能控制minion。
对于远程执行命令，最常见的方法是用ssh，因为直接启动远程的sshd服务即可。那么有没有一种方式
可以集成两者的优点，同时免安装minion又同时可以使用saltstack的功能特点。salt-ssh的出现
回答了这个问题。

salt-ssh基本上是零配置。你想控制哪个host，直接把host的ip和用户密码或者keys告诉salt。剩下的
就直接执行:

* `salt-ssh <ssh target> -r <raw cmd>` 这个可以直接在远程机器运行命令
* `salt-ssh <ssh target> state.highstate` 这个可以同步整个salt状态
* 更多的salt执行的模块命令

默认的配置文件位于`/etc/salt/roster`, 添加ssh机器即可，例如：

```text
web1:
  host: 192.168.42.1 # The IP addr or DNS hostname
  user: fred         # Remote executions will be executed as user fred
  passwd: foobarbaz  # The password to use for login, if omitted, keys are used
  sudo: True         # Whether to sudo to root, not enabled by default
web2:
  host: 192.168.42.2
```

更多文档在这里:

* <http://docs.saltstack.com/en/latest/topics/ssh/>
* <http://docs.saltstack.com/topics/ssh/roster.html>


## 原理

salt-ssh主要的代码路径位于`<TOP>/salt/client/ssh`目录

```text
(vdev)[ray@fedora salt]$ tree salt/client/ssh/
salt/client/ssh/
|-- __init__.py
|-- shell.py        # 利用ssh协议，安装部署key和shim脚本
|-- ssh_py_shim.py  # shim脚本，在minion端实际运行。
|-- state.py        # saltstack State的ssh方式现实
`-- wrapper         # 此目录提供更多的salt支持
    |-- config.py
    |-- grains.py
    |-- __init__.py
    |-- pillar.py
    |-- state.py
```

salt-ssh是不需要启动minion的，那么如何控制远程机器的呢？
我们可以打开debug信息看看具体流程，`salt-ssh '*' test.ping`

1. 从roster配置文件中找到所有的minion和ssh登陆信息。生成类似
`ssh host command`的命令行准备执行. 因为执行的命令很复杂，最好
是用ssh执行一个脚本文件，那样自定义效果最好。这里其实就是`ssh_py_shim.py`

2. salt-ssh会打包一份精简的包含大部分salt核心模块并压缩成salt-thin.tgz，
并发送给minion的`/tmp/.salt/`路径（默认路径，可以配置修改）。同时缓存一份
在`/var/cache/salt/master/thin/`以备后需之用。

3. 为了让salt-ssh很顺利在远程机器执行`ssh_py_shim.py`，初始化过程中包含
一个小型的shell代码。 shell的主要内容可以在`SSH_SH_SHIM`变量中看到。
前期主要是探索python版本环境，进入到main函数后，实际上还是用python执行
`ssh_py_shim.py`并传入参数。


```text
main()
{
    local py_cmd
    local py_cmd_path
    for py_cmd in $PYTHON_CMDS; do
        if "$py_cmd" -c 'import sys; sys.exit(not sys.hexversion >= 0x02060000);' >/dev/null 2>&1; then
            local py_cmd_path
            py_cmd_path=`"$py_cmd" -c 'import sys; print sys.executable;'`
            exec $SUDO "$py_cmd_path" -c 'exec """{{SSH_SHIM_PY_CODE}}
""".decode("base64")' -- \-\-config \{id\:\ ssh\-saltvm\,\ root_dir\:\ \/tmp\/\.salt\/running_data\} \-\-delimeter _edbc7885e4f9aac9b83b35999b68d015148caf467b78fa39c05f669c0ff89878 \-\-saltdir \/tmp\/\.salt \-\-checksum bb9df33affeafa50849c1a906c04ac09e4b5f22a \-\-hashfunc sha1 \-\-version 2014\.1\.0\-6968\-ga1d939d \-\- test\.ping
            exit 0
        else
            continue
        fi
    done

    echo "ERROR: Unable to locate appropriate python command" >&2
    exit $EX_PYTHON_OLD
}
```

4. `ssh_py_shim.py`脚本是可以单独运行。看看help文档，就大致知道上面main
函数传入参数的意思。

```text
(vdev)[ray@fedora ssh]$ python ssh_py_shim.py -- --help
Usage: ssh_py_shim.py -- [SHIM_OPTIONS] -- [SALT_OPTIONS]

Options:
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        YAML configuration for salt thin
  -d DELIMETER, --delimeter=DELIMETER
                        Delimeter string (viz. magic string) to indicate
                        beginning of salt output
  -s SALTDIR, --saltdir=SALTDIR
                        Directory where salt thin is or will be installed.
  --sum=CHECKSUM, --checksum=CHECKSUM
                        Salt thin checksum
  --hashfunc=HASHFUNC   Hash function for computing checksum
  -v VERSION, --version=VERSION
                        Salt thin version to be deployed/verified
```

5. 看看另外的例子`salt-ssh -l debug 'ssh-saltvm2' state.highstate test=True`。
很明显，salt-ssh的原理就在此。依然是在远程环境中运行salt-call命令，只不过这时的
工作路径是`/tmp/.salt`。结果返回给master端。两边的通信依赖ssh/scp协议。

```text
SALT_ARGV: ['/usr/bin/python2.7', '/tmp/.salt/salt-call', '--local', '--out', 'json', '-l', 'quiet', '-c', '/tmp/.salt', '--', 'state.pkg /tmp/.salt/salt_state.tgz test=True pkg_sum=dd39c5804385befc3ac8d87aa5b40f56 hash_type=md5']
```

## 总结

salt-ssh的原理, 依然是在远程环境中运行salt-call命令，此时远程机器已经被部署了
salt运行环境。这样salt的很多特性和模块功能可以在本地调用。运行的结果用过ssh协议
返回给master。

这里附上我修改的一个salt-ssh bug。

<https://github.com/saltstack/salt/pull/13292>

