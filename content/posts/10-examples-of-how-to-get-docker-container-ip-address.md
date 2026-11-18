+++
title = "10 Examples of how to get Docker Container IP Address"
date = "2015-05-10T09:04:05+00:00"
lastmod = "2016-04-08T05:22:09+00:00"
author = "Brent Salisbury"
wp_id = 7626
categories = ["In the Lab"]
tags = ["Docker", "Docker Networking", "Ipvlan", "Libnetwork", "Macvlan"]
description = ""
url = "/10-examples-of-how-to-get-docker-container-ip-address/"
image = "/wp-content/uploads/2015/05/docker-turtles-banner-network-copy.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3b35a235c1dfe615d8cca96baf3e7802b74d6ce29e2b3ff70d753da5cc185d82"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>10 Examples of how to get Docker Container IP Address</h3>

One thing that is so much fun about the need virtualization paradigm we are heading towards is that in the age of "software defined", the flexibility of how to do things with infra are much more like programming then working with highly opinionated traditional infrastructure. Along that thread, here are 10 different ways to get a container or docker-machine address using the Docker/Docker-Machine CLI. This doesn't even go into the remote http API which is slick because the client commands below are actually making calls to the verioned API described <a href="https://docs.docker.com/reference/api/docker_remote_api/" target="_blank">here</a>.
<hr>
Much of the motivation to show so many different ways is to help folks see the flexibility that I still run into nearly daily which is hard not to excite a hacker. They can also be viewed in this <a href="https://gist.github.com/2126a6b80ad2e2137fe1" target="_blank">Gist</a>.

<pre class="code-sample"><code>
### Example #1 ###
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND               CREATED             STATUS                   PORTS                               NAMES
2e23d01384ac        iperf-v1:latest     "/usr/bin/iperf -s"   10 minutes ago      Up 10 minutes            5001/tcp, 0.0.0.0:32768->5201/tcp   compassionate_goodall
# Append the container ID (CID) to the end of an inspect
$ docker inspect --format '{{ .NetworkSettings.IPAddress }}' 2e23d01384ac
172.17.0.1
</code></pre>

<pre class="code-sample"><code>
### Example #2 ###
# Add -q to automatically parse and return the last CID created.
$ docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -q)
172.17.0.1
</code></pre>

<pre class="code-sample"><code>
### Example #3 ###
# As of Docker v1.3 you can attach to a bash shell
docker exec -it  2e23d01384ac  bash
# That drops you into a bash shell then use the 'ip' command to grab the addr
root@2e23d01384ac:/# ip add | grep global
    inet 172.17.0.1/16 scope global eth0
</code></pre>

<pre class="code-sample"><code>
### Example #4 ###
# Same as above but in a single line
$ docker exec -it  $(docker ps -q) bash
</code></pre>

<pre class="code-sample"><code>
### Example #5 ###
# Pop this into your ~/.bashrc (Linux) or ~/.bash_profile (Mac)
dockip() {
  docker inspect --format '{{ .NetworkSettings.IPAddress }}' "$@"
}
# Source it to re-read your bashrc/profile
source ~/.bash_profile
# Now run the function with the container ID you want to get the addr of:
$ dockip 2e23d01384ac
172.17.0.1
</code></pre>

<pre class="code-sample"><code>
### Example #6 ###
# Same as above but no argument needed and always return the latest container IP created.
dockip() {
  docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -q)
}
</code></pre>

<pre class="code-sample"><code>
### Example #7 ###
# Add to bashrc/bash_profile to docker exec in passing the CID to dock-exec. E.g dock-exec $(docker ps -q) OR dock-exec 2e23d01384ac
dock-exec() { docker exec -i -t $@ bash ;}
</code></pre>

<pre class="code-sample"><code>
### Example #8 ###
# Another little bash function you can pop into your bash profile
# Always docker exec into the latest container
dock-exec() { docker exec -i -t $(docker ps -l -q)  bash ;}
# The run ip addr
ip a
</code></pre>

<pre class="code-sample"><code>
### Example #9 ###
# Finally you can export the environmental variables from the running container
docker exec -i -t $(docker ps -l -q) env | grep ADDR
# Output --> CLOUDNETPERF_CARBON_1_PORT_2003_TCP_ADDR=172.17.0.229
</code></pre>

<pre class="code-sample"><code>
### Example #10 ###
# Or even run the ip address command as a parameter which fires off the ip address command and exits the exec
docker exec -i -t $(docker ps -l -q) ip a
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
#    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
#    inet 127.0.0.1/8 scope host lo
#       valid_lft forever preferred_lft forever
#    inet6 ::1/128 scope host
#       valid_lft forever preferred_lft forever
# 470: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
#    link/ether 02:42:ac:11:00:e9 brd ff:ff:ff:ff:ff:ff
#    inet 172.17.0.233/16 scope global eth0
#       valid_lft forever preferred_lft forever
#    inet6 fe80::42:acff:fe11:e9/64 scope link
#       valid_lft forever preferred_lft forever
</code></pre>

Bonus Example! :)
If you have a user defined network as opposed to the default network, simply grepping on `docker inspect` is a quick way to parse any field.

Lets say you created a Macvlan network to use the same network as the Docker host `eth0` interface. In this case `eth0` on the Linux host is the following:

<pre class="code-sample"><code>
$ ip a show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:13:e4:52 brd ff:ff:ff:ff:ff:ff
    inet 172.16.86.254/24 brd 172.16.86.255 scope global eth0
       valid_lft forever preferred_lft forever
</code></pre>

Create a network that will share the `eth0` interface:

<pre class="code-sample"><code>
$ docker network create -d macvlan \
     --subnet=192.168.1.0/24 \
     --gateway=192.168.1.1  \
     -o parent=eth1 mcv && \
     docker run --net=mcv -it --rm alpine /bin/sh
</code></pre>

Now grep details about the container:

<pre class="code-sample"><code>
# Get the IP of the most recently started container:
docker inspect  $(docker ps -q) | grep IPAddress
# Or get the gateway for the last container started:
docker inspect  $(docker ps -q) | grep Gateway
</code></pre>

You can just as easily look at the details of the network:

<pre class="code-sample"><code>
# Get the IP of the most recently started container:
docker inspect  $(docker ps -q) | grep IPAddress
# Or get the gateway for the last container started:
docker inspect  $(docker ps -q) | grep Gateway
</code></pre>

Lastly, take a look at the `docker network inspect` details to view the metadata of the network `mcv1` you created:

<pre class="code-sample"><code>
$ docker network inspect  mcv1  | grep -i ipv4
       "IPv4Address": "192.168.1.106/24",

# or look at the gateway of the network
$ docker network inspect  mcv1  | grep Gateway
       "Gateway": "192.168.1.1/24"
</code></pre>

Thats all for now. There are likely plenty of other ways but this should be enough to tackle most automation scenarios. I am wanting to keep most of the current blogging geared towards Docker novices for the next little bit until most in networking are up to speed and then we will go deep. Lots more to come! To my network hacking friends, I will be digging into some lower level Linux netlink and interfacing with that with Go funs next weekend so stay tuned!

<a href="https://github.com/docker/docker/blob/master/experimental/vlan-networks.md" target="_blank" rel="noopener noreferrer">New Ipvlan and Macvlan Drivers</a>

Thanks for stopping by!