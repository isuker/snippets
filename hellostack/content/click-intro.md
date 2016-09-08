Title: click介绍
Date: 2014-6-18 21:12
Tags: python
Slug: click-intro
Author: Ray Chen
Summary: python click library基本介绍和示例


## Click介绍

[Click](http://click.pocoo.org)是一个python库，用来写命令行接口的。默认python自带了[argparse](https://docs.python.org/2.7/library/argparse.html)和[optparse](https://docs.python.org/2.7/library/optparse.html#module-optparse)两个library来帮助用户很方便的写出用户友好的命令行接口。

[这里](http://click.pocoo.org/why/) 解释了为什么推荐大家用Click。主要亮点是可以类似搭积木组合那样，生成复杂的类似UNix命令行。而且自带了很多辅助参数类似，比如说[文件参数](http://click.pocoo.org/arguments/#file-arguments)， 还有彩色输出格式等等。

* is lazily composable without restrictions
* fully follows the Unix command line conventions
* supports loading values from environment variables out of the box
* supports for prompting of custom values
* is fully nestable and composable
* works the same in Python 2 and 3
* supports file handling out of the box
* comes with useful common helpers (getting terminal dimensions, ANSI colors, fetching direct keyboard input, screen clearing, finding config paths, launching apps and editors, etc.)

Click的作者[Armin Ronacher](http://lucumr.pocoo.org/)其实就是[Flask](http://flask.pocoo.org) Web开发框架的作者。所以Click的文档看起来跟[Flask](http://flask.pocoo.org/docs/)的在线文档格式一样。文档看起来漂亮得很。


## 实例

[click文档首页](http://click.pocoo.org/)写了一个例子。我根据文档说明很快也写出了包含子命令的接口程序。
代码就这样。创建了一个命令组，可以理解成Base，有一些子命令共同的参数。然后建立了子命令，每个子命令添加自己的参数。


```python
#!/usr/bin/python

import click


@click.group()
@click.option('--force', '-f', is_flag=True, help="Specify flavor name")
def flavor(force):
    click.echo("this is group cli")
    if force:
        click.echo("--force is set to %s" % force)


@flavor.command('flavor-list', help="list flavor object")
@click.option('--name', help="specify flavor name")
def flavor_list(name):
    if name:
        click.echo("only list %s flavor" % name)
    else:
        click.echo("list all flavor")


@flavor.command('flavor-create', help="create flavor object")
@click.argument('name')
@click.argument('cpu')
@click.argument('ram')
def flavor_create(name, cpu, ram):
    click.echo("flavor-create with param: %s %s %s" % (name, cpu, ram))


@flavor.command('flavor-delete', help="delete flavor object")
@click.argument('name')
def flavor_delete(name):
    click.echo("flavor-delete %s" % name)


if __name__ == "__main__":
    flavor()

```

这个例子的运行结果。


```text
[ray@fedora click]$ ./hello.py 
Usage: hello.py [OPTIONS] COMMAND [ARGS]...

Options:
  -f, --force  specify flavor name
  --help       Show this message and exit.

Commands:
  flavor-create  create flavor object
  flavor-delete  delete flavor object
  flavor-list    list flavor object
[ray@fedora click]$ ./hello.py ^C
[ray@fedora click]$ vim hello.py 
[ray@fedora click]$ ./hello.py 
Usage: hello.py [OPTIONS] COMMAND [ARGS]...

Options:
  -f, --force  Specify flavor name
  --help       Show this message and exit.

Commands:
  flavor-create  create flavor object
  flavor-delete  delete flavor object
  flavor-list    list flavor object
[ray@fedora click]$ ./hello.py flavor-create
this is group cli
Usage: hello.py flavor-create [OPTIONS] NAME CPU RAM

Error: Missing argument "name".
[ray@fedora click]$ ./hello.py flavor-create name 1 1024
this is group cli
flavor-create with param: name 1 1024
[ray@fedora click]$ ./hello.py flavor-delete
this is group cli
Usage: hello.py flavor-delete [OPTIONS] NAME

Error: Missing argument "name".
[ray@fedora click]$ ./hello.py flavor-delete myFlavor
this is group cli
flavor-delete myFlavor
[ray@fedora click]$ ./hello.py flavor-list
this is group cli
list all flavor
[ray@fedora click]$ ./hello.py flavor-list myFlavor
this is group cli
Usage: hello.py flavor-list [OPTIONS]

Error: Got unexpected extra argument (myFlavor)
[ray@fedora click]$ ./hello.py flavor-list --name myFlavor
this is group cli
only list myFlavor flavor
```

## 参考资料

* <https://pypi.python.org/pypi/click/2.1>
* <http://click.pocoo.org/>

