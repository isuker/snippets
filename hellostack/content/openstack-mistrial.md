Title: Openstack Mistral 工作流组件介绍
Date: 2014-5-12 23:59
Category: Openstack
Tags: openstack, python
Slug: openstack-mistral-intro
Author: Ray Chen
Summary: Mistral是mirantis公司为openstack开发的工作流组件，提供WorkFlow as a service。 典型的用户用例包括云平台的任务计划服务（Cloud Cron），任务调度（Task Scheduling）， 复杂的运行时间长的业务流程服务。目前项目还在开始阶段。对应的是AWS的SWS（Simple WorkFlow Service）。


##Mistral是什么
Mistral是mirantis公司为openstack开发的工作流组件，提供WorkFlow as a service。 典型的用户用例包括云平台的任务计划服务（Cloud Cron），任务调度（Task Scheduling）， 复杂的运行时间长的业务流程服务。目前项目还在开始阶段。对应的是AWS的SWS（Simple WorkFlow Service）。

项目wiki: <https://wiki.openstack.org/wiki/Mistral>
项目Code: <https://github.com/stackforge/mistral>


##基本术语

Workbook: 工作本，用户的工作流接口，可以理解成一篇任务文档用来录入用户的工作流程，步骤，需要完成的任务。每个任务的执行顺序，依赖关系，以及每个任务完成之后产生的事件。站在用户的角度，这篇文档完整的记录了某项任务的流程，让执行者能够清楚怎么完成。站在开发人员的角度，为了方便编程。定义了一种新的语言DSL（下面会有介绍），用来描述整个工作流。

Task: 即工作流的具体步骤。可以是Action的集合。

Action: Mistral的最小单位。特指一个具体的工作，比如说发送一个HTTP请求，或者运行某条命令。

Flow：工作流。 指的是Mistral系统中如何执行task，解析task的依赖关系等等，从而让task顺利结束，并返回状态。

WorkFlow Execution: 工作流执行纪录。就是指某次具体的Flow，每次执行task产成的WorkFlow Execution会永久保存在数据库中，方便后续查询，或者重新执行Flow。


##DSL 介绍

这是Mistral自定义的工作流定义语言。在业界，工作流程管理 已经存在某些语言，可参考:

* <http://en.wikipedia.org/wiki/Business_Process_Execution_Language>
* <http://en.wikipedia.org/wiki/YAWL>

Mistral 使用YAML 来定义工作流 wiki: <https://wiki.openstack.org/wiki/Mistral/DSL>


##实战

从Github下载最新的代码，安装好运行环境。同时启动API和executor服务
```shell
tox -evenv -- python mistral/cmd/launch.py --server executor --config-file etc/mistral.conf
tox -evenv -- python mistral/cmd/launch.py --server api --config-file etc/mistral.conf
```
然后运行“scripts/upload_workbook_and_run.py” 脚本，可以清楚看到整个流程。
```shell
[ray@fedora mistral]$ python scripts/upload_workbook_and_run.py 
Created workbook: Workbook [description='My test workbook', name='my_workbook', tags='[u'test']']

Uploaded workbook:
"
Services:
   MyRest:
     type: REST_API
     parameters:
         baseUrl: http://localhost:8989/v1/
     actions:
         my-action:
           parameters:
               url: workbooks
               method: GET

Workflow:
   tasks:
     my_task:
         action: MyRest:my-action

#   events:
#     my_event:
#        type: periodic
#        tasks: my_task
#        parameters:
#            cron-pattern: "* * * * *"
"

execution: Execution [state='RUNNING', task='my_task', id='b5cf7e00-ef5d-46d7-b505-2d23809d29d0', context='None', workbook_name='my_workbook']
execution: Execution [state='RUNNING', task='my_task', id='b5cf7e00-ef5d-46d7-b505-2d23809d29d0', context='None', workbook_name='my_workbook']
execution: Execution [state='SUCCESS', task='my_task', id='b5cf7e00-ef5d-46d7-b505-2d23809d29d0', context='None', workbook_name='my_workbook']
```

我们可以装上[Misttral client](https://github.com/stackforge/python-mistralclient)来看看到底发生了什么。首先看看系统中存在哪些workbook，已经刚刚运行的my-wokbook

```shell
[ray@fedora mistral]$ mistral workbook-list
Starting new HTTP connection (1): localhost
+---------------+------------------+------+
| Name          | Description      | Tags |
+---------------+------------------+------+
| echo_workbook | My test workbook | test |
| my_workbook   | My test workbook | test |
+---------------+------------------+------+
[ray@fedora mistral]$ mistral workbook-get-definition my_workbook
Starting new HTTP connection (1): localhost
Services:
   MyRest:
     type: REST_API
     parameters:
         baseUrl: http://localhost:8989/v1/
     actions:
         my-action:
           parameters:
               url: workbooks
               method: GET

Workflow:
   tasks:
     my_task:
         action: MyRest:my-action

#   events:
#     my_event:
#        type: periodic
#        tasks: my_task
#        parameters:
#            cron-pattern: "* * * * *"
```

这个workbook，首先定义了一个服务（在系统中注册个新的服务，服务一般都包含定义好的action，这样用户就可以在task flow中指定运行这个action），这个服务类型是REST，然后参数有哪些等等。然后定义了一个工作流，其中的任务列表（tasks）第一个是my_task （taks名字），这个task做了一件事情，就是运行一次MyRest服务中的my_action动作。

在看看另外一个workbook， 就简单定义个一个ECHO type的服务。这个服务仅在内部测试使用，就直接返回ECHO值。

```shell
[ray@fedora mistral]$ mistral workbook-get-definition echo_workbook
Starting new HTTP connection (1): localhost
Services:
  MyEcho:
    type: ECHO
    actions:
        EchoWords:        
          parameters:
            word:
                optional: False
                

Workflow:
    tasks:
        logPassTask:
            action: MyEcho:EchoWords
            parameters:
               word: "log pass" 
        MyEchoTask:
            action: MyEcho:EchoWords
            parameters:
               word: "hello, world" 
            on-success: logPassTask
```

具体的运行log：

```shell
[ray@fedora mistral]$ mistral execution-get echo_workbook bcf47b8c-6d44-4732-b32d-ebef92662f38
Starting new HTTP connection (1): localhost
+----------+--------------------------------------+
| Field    | Value                                |
+----------+--------------------------------------+
| ID       | bcf47b8c-6d44-4732-b32d-ebef92662f38 |
| Workbook | echo_workbook                        |
| Target   | MyEchoTask                           |
| State    | SUCCESS                              |
+----------+--------------------------------------+
[ray@fedora mistral]$ mistral task-list echo_workbook bcf47b8c-6d44-4732-b32d-ebef92662f38
Starting new HTTP connection (1): localhost
+--------------------------------------+---------------+--------------------------------------+-------------+-------------+---------+--------+
| ID                                   | Workbook      | Execution                            | Name        | Description | State   | Tags   |
+--------------------------------------+---------------+--------------------------------------+-------------+-------------+---------+--------+
| e5cb4a7a-b6c6-46ec-b62b-aa385bd3f8c2 | echo_workbook | bcf47b8c-6d44-4732-b32d-ebef92662f38 | MyEchoTask  | <none>      | SUCCESS | <none> |
| 1c99cc02-e1b0-44c2-b961-8589164bb851 | echo_workbook | bcf47b8c-6d44-4732-b32d-ebef92662f38 | logPassTask | <none>      | SUCCESS | <none> |
+--------------------------------------+---------------+--------------------------------------+-------------+-------------+---------+--------+
```

##最近进展

上面的实战例子可能没让大家意识到mistral跟openstack的关系，然后相信这个workbook 会让大家明白。

<https://wiki.openstack.org/wiki/Mistral/DSL#Full_YAML_example>

关于VM的工作流，创建NOVA VM。 Mistral开发组正在实现这种类型的workbook，即集成openstack服务。这样用户就不需要用openstack CLI or API来操作，可以直接编写workbook（*简单编写文档，而不是写code*），让mistral帮你做完整个工作流程。

另外关于Mistral和taskflow的集成：

Mistral在实现的过程中，需要开发大量的工作流代码。这跟openstack项目库中TaskFlow 目的有些类似。为了避免重复劳动，两边的开发者已经在讨论，在Mistral代码中，后端的工作流代码尽量采用taskflow作为后端。

这里有最近的讨论记录 <https://github.com/enykeev/mistral/pull/1>

全文完。 转载请保留出处。


