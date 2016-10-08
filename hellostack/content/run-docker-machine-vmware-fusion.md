Title:Run Docker on VMware Fusion
Date: 2016-10-08 16:49
Category: Docker
Tags: docker
Slug: run-docker-machine-vmware-fusion
Author: Ray Chen
Summary: Mac OS上安装部署docker以及troubleshooting

## What's docker-machine

Docker Machine is a tool that lets you install Docker Engine on virtual hosts, and manage the hosts with docker-machine commands. You can use Machine to create Docker hosts on your local Mac or Windows box, on your company network, in your data center, or on cloud providers like AWS or Digital Ocean.

Using docker-machine commands, you can start, inspect, stop, and restart a managed host, upgrade the Docker client and daemon, and configure a Docker client to talk to your host.


## Create docker machine

Create the default docker machine with 'vmwarefusion' driver:
```bash
docker-machine create --driver=vmwarefusion default
ranc-m01:~ ranc$ docker-machine create -d vmwarefusion default
Creating CA: /Users/ranc/.docker/machine/certs/ca.pem
Creating client certificate: /Users/ranc/.docker/machine/certs/cert.pem
Running pre-create checks...
(default) Image cache directory does not exist, creating it at /Users/ranc/.docker/machine/cache...
(default) No default Boot2Docker ISO found locally, downloading the latest release...
(default) Latest release for github.com/boot2docker/boot2docker is v1.12.1
(default) Downloading /Users/ranc/.docker/machine/cache/boot2docker.iso from https://github.com/boot2docker/boot2docker/releases/download/v1.12.1/boot2docker.iso...
(default) 0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
Creating machine...
(default) Copying /Users/ranc/.docker/machine/cache/boot2docker.iso to /Users/ranc/.docker/machine/machines/default/boot2docker.iso...
(default) Creating SSH key...
(default) Creating VM...
(default) Creating disk '/Users/ranc/.docker/machine/machines/default/default.vmdk'
(default) Virtual disk creation successful.
(default) Starting default...
(default) Waiting for VM to come online...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with boot2docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: docker-machine env default
ranc-m01:~ ranc$ docker-machine ls
NAME      ACTIVE   DRIVER         STATE     URL                       SWARM   DOCKER    ERRORS
default   -        vmwarefusion   Running   tcp://172.16.8.135:2376           v1.12.1
ranc-m01:~ ranc$ docker-machine env default
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://172.16.8.135:2376"
export DOCKER_CERT_PATH="/Users/ranc/.docker/machine/machines/default"
export DOCKER_MACHINE_NAME="default"
# Run this command to configure your shell:
# eval $(docker-machine env default)
ranc-m01:~ ranc$ eval $(docker-machine env default)
ranc-m01:~ ranc$ docker-machine ssh default
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/
 _                 _   ____     _            _
| |__   ___   ___ | |_|___ \ __| | ___   ___| | _____ _ __
| '_ \ / _ \ / _ \| __| __) / _` |/ _ \ / __| |/ / _ \ '__|
| |_) | (_) | (_) | |_ / __/ (_| | (_) | (__|   <  __/ |
|_.__/ \___/ \___/ \__|_____\__,_|\___/ \___|_|\_\___|_|
Boot2Docker version 1.12.1, build HEAD : ef7d0b4 - Thu Aug 18 21:18:06 UTC 2016
Docker version 1.12.1, build 23cf638
```


## Run without proxy

Add the '--no-proxy' part to tell docker not to use proxy

```bash
ranc-m01:~ ranc$ docker-machine env --no-proxy
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://172.16.8.135:2376"
export DOCKER_CERT_PATH="/Users/ranc/.docker/machine/machines/default"
export DOCKER_MACHINE_NAME="default"
export NO_PROXY="172.16.8.135"
# Run this command to configure your shell:
# eval $(docker-machine env --no-proxy)
```


## Run with proxy

Mostly we need proxy to pull down the docker images.

1. Use ssh to log in to the virtual machine (e.g., default).

```bash
 $ docker-machine ssh default
 docker@default:~$ sudo vi /var/lib/boot2docker/profile
```
2. Add a NO_PROXY setting to the end of the file similar to the example below.

```bash
 # replace with your office's proxy environment
 export "HTTP_PROXY=http://PROXY:PORT"
 export "HTTPS_PROXY=http://PROXY:PORT"
 # you can add more no_proxy with your environment.
 export "NO_PROXY=192.168.99.*,*.local,169.254/16,*.example.com,192.168.59.*"
```
3. Restart Docker. After you modify the profile on your VM, restart Docker and log out of the machine.

```bash
docker@default:~$ sudo /etc/init.d/docker restart
 docker@default:~$ exit
```


## Port Forward in VMware Fusion

Update the 'incomingtcp' secion in Vmware Fusion Nat conf file
```bash
sudo vi /Library/Preferences/VMware\ Fusion/vmnet8/nat.conf
 55 [incomingtcp]
 56
 57 # Use these with care - anyone can enter into your VM through these...
 58 # The format and example are as follows:
 59 #<external port number> = <VM's IP address>:<VM's port number>
 60 #8080 = 172.16.3.128:80
```

## Reference

1. <https://docs.docker.com/toolbox/faqs/troubleshoot/>
2. <https://github.com/docker/toolbox/issues/102>
3. <https://github.com/docker/machine/issues/1351>
4. <https://github.com/docker/machine/issues/3099>
5. <https://docs.docker.com/machine/drivers/vm-fusion/>

