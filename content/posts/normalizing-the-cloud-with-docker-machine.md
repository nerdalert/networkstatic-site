+++
title = "Normalizing the Cloud with Docker Machine"
date = "2015-04-30T07:43:32+00:00"
lastmod = "2015-07-21T06:42:07+00:00"
author = "Brent Salisbury"
wp_id = 7546
categories = ["In the Lab"]
tags = ["Cloud", "Docker", "Docker-Machine"]
description = ""
url = "/normalizing-the-cloud-with-docker-machine/"
image = "/wp-content/uploads/2015/04/docker-penguin-gopher-banner.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a153833a40698a869a861cba17fdc843901269846d1ba15bf8c6e78ff26c4b44"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> Normalizing the Cloud with Docker Machine </h3>


Docker machine creates a virtual machine running Docker located in an array of locations that I can then create containers and ship workloads to. The locations and types you can provision to range from the who is who of cloud computing, workstation resources and traditional on prem local resources sitting in the average enterprise DC.


<ul>
        <li>amazonec2</li>
        <li>azure</li>
	<li>digitalocean</li>
	<li>google</li>
	<li>openstack</li>
	<li>rackspace</li>
	<li>softlayer</li>
	<li>virtualbox</li>
	<li>vmwarefusion</li>
	<li>vmwarevcloudair</li>
	<li>vmwarevsphere</li>
	<li>*will list more as they grow</li>
</ul>


What I get from using Docker Machine is a is a cloud catalogue of virtually any provider type I would want (public and private), all in a single client sitting on my laptop. Even cooler is a puzzle piece that has long been missing, is what feels like a normalization of how I can use cloud resources without having to be a cloud ninja of all of the often disparate APIs.

Having a common interface like docker machine enables me to transcend any one provider and abstracts away virtually all remnants of the heterogenous public, private, sandbox implantation details that has been a time consuming constraint to many of us for years. I also see this as good for the CSP's, making it easier to consume their resources will mean a faster migrations to the cloud, easier testing between dev/prod and maybe even some rational hybrid strategies.

What this means to the consumer could be the content of an entire book but cloud buzz-word bingo is starting to shape up to be a reality. Workloads are truly portable between clouds with a much lower technical barrier to entry via a simple interface. Multi-cloud, hybrid-cloud, workload mobility (data issues aside :_), elasticity, cloud brokering, etc, all suddenly feel very real and with an interface that lends itself to the common enterprise ops and admins. Remove the disjointed complex nature of multi-cloud and you no longer have to be a superhero to start building infra across clouds.
<hr>
The mechanics are essentially, create a Docker host (VM running Docker) on any of the supported cloud or local provider types. Next register your credentials into your environmental variables and choose which provider you want to spin up resources on. Use 'docker run' just like you were on your local machine but instead it will spin up resources anywhere you want.

<hr />

The following diagram outlines the simple process:
wgt
<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img class="aligncenter size-full wp-image-7574" src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" /></a>

Enough chit chat, lets get hacking!
<h3> Install Docker Machine </h3>
Installation instructions are really good from Docker found <a href="https://docs.docker.com/machine/" target="_blank">here</a>.

In this example, I am using Mac OS X. The docker machine commands are the same across platforms. There is support for both Linux and Windows OS's also.

<pre class="code-sample"><code>
sudo wget --no-check-certificate -O /usr/local/bin/docker-machine https://github.com/docker/machine/releases/download/v0.3.0-rc1/docker-machine_darwin-amd64
sudo chmod +x /usr/local/bin/docker-machine
</code></pre>

See the <a href="https://github.com/docker/machine/releases" target="_blank">Docker Machine Releases page</a> on Github for the latest stable and RCs. I have some links in a an installer I use (and even update occasionally) sometimes to refresh the toolbox <a href="https://github.com/nerdalert/cloud-bandwidth/blob/master/scripts/docker-install-helper.sh" target="_blank">here</a>

<hr>

Take a look at the docker-machine options

<pre class="code-sample"><code>
docker-machine --help
#    NAME:
#    docker-machine - Create and manage machines running Docker.
#    
#    USAGE:
#    docker-machine [global options] command [command options] [arguments...]
#    
#    VERSION:
#    0.2.0 (HEAD)
#    
#    AUTHOR:
#    Docker Machine Contributors - https://github.com/docker/machine
#    
#    COMMANDS:
#    active Get or set the active machine
#    create Create a machine
#    config Print the connection config for machine
#    inspect Inspect information about a machine
#    ip Get the IP address of a machine
#    kill Kill a machine
#    ls List machines
#    regenerate-certs Regenerate TLS Certificates for a machine
#    restart Restart a machine
#    rm Remove a machine
#    env Display the commands to set up the environment for the Docker client
#    ssh Log into or run a command on a machine with SSH
#    start Start a machine
#    stop Stop a machine
#    upgrade Upgrade a machine to the latest version of Docker
#    url Get the URL of a machine
#    help, h Shows a list of commands or help for one command
#    
#    GLOBAL OPTIONS:
#    --debug, -D Enable debug mode
#    --storage-path "/Users/brent/.docker/machine" Configures storage path [$MACHINE_STORAGE_PATH]
#    --tls-ca-cert CA to verify remotes against [$MACHINE_TLS_CA_CERT]
#    --tls-ca-key Private key to generate certificates [$MACHINE_TLS_CA_KEY]
#    --tls-client-cert Client cert to use for TLS [$MACHINE_TLS_CLIENT_CERT]
#    --tls-client-key Private key used in client TLS auth [$MACHINE_TLS_CLIENT_KEY]
#    --help, -h show help
#    --version, -v print the version
</code></pre>

Install the Docker client if it isn't already. The following is for Darwin. Here are all of the <a href="https://docs.docker.com/installation/" target="_blank">platforms installs</a>.

<pre class="code-sample"><code>
curl https://get.docker.com/builds/Darwin/x86_64/docker-latest &gt; /usr/local/bin/docker
</code></pre>

- Verify the binary like so:

<pre class="code-sample"><code>
sudo docker-machine -v
machine version 0.2.0
</code></pre>
<h3> Start VirtualBox VM for Containers </h3>
Start a VM that will house your containers:

<pre class="code-sample"><code>
sudo docker-machine create --driver virtualbox dev
# INFO[0000] Creating SSH key...
# INFO[0000] Creating VirtualBox VM...
# INFO[0006] Starting VirtualBox VM...
# INFO[0006] Waiting for VM to start...
# INFO[0054] "dev" has been created and is now the active machine.
# INFO[0054] To point your Docker client at it, run this in your shell: eval "$(docker-machine env dev)"
</code></pre>

List the new machine:

<pre class="code-sample"><code>
sudo docker-machine ls
# NAME ACTIVE DRIVER STATE URL SWARM
# dev * virtualbox Running tcp://192.168.99.100:2376
</code></pre>
<h3> Setting Docker ENV Variables </h3>
To view the ENV variables you need to talk to the newly spun host, run the following. You likely need to prepend sudo to the statement.

<em>Note</em>: The 3 standard Docker ENV variables are what tells the docker client to run commands against a running Docker daemon. Two are for for the TLS crypto and cert and the third points to the docker host tcp/ip/port/api.

The following `docker env` command only prints the key/values of the ENVs. They still need to be exported in order to be passed in a $FOO variable fashion. New terminal windows/tabs the values need to be reinitiated into the new session.

<pre class="code-sample"><code>
docker-machine env dev
</code></pre>

In the docs the `eval` statement is listed w/o the `sudo` command prefix.

<pre class="code-sample"><code>
eval "$(docker-machine env dev)"
</code></pre>

- My environment requires that so the following is what I use.

<pre class="code-sample"><code>
eval "$(sudo docker-machine env dev)"
</code></pre>
- Either way what you are looking for are the variables in your shell like so:

<pre class="code-sample"><code>
env | grep DOCK
DOCKER_HOST=tcp://192.168.99.100:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/Users/brent/.docker/machine/machines/dev
</code></pre>
If those values are not in your environment, you will get some errors like so:

<pre class="code-sample"><code>
# "docker-machine" An error occurred trying to connect: Post https://192.168.59.103:2376/v1.18/containers/create: dial tcp 192.168.59.103:2376: i/o timeout
</code></pre>
<h3> Running Docker Containers in the new Machine </h3>
Lets start a container with a quick little test:

<pre class="code-sample"><code>
docker run busybox echo hello world
</code></pre>
output:

<pre class="code-sample"><code>
# Unable to find image 'busybox:latest' locally
# latest: Pulling from busy box
# cf2616975b4a: Pull complete
# 6ce2e90b0bc7: Pull complete
# 8c2e06607696: Already exists
# busybox:latest: The image you are pulling has been verified. # Important: image verification is a tech preview feature and should not be relied on to provide security.
# Digest: # sha256:38a203e1986cf79639cfb9b2e1d6e773de84002feea2d4eb006b52004ee8502d
# Status: Downloaded newer image for busybox:latest
# (Shell Output Next)
# hello world
</code></pre>

Or you can start a bash shell to poke around from a shell:

<pre class="code-sample"><code>
docker run -it ubuntu /bin/bash
</code></pre>
output:

<pre class="code-sample"><code>
root@99563aa8ffd6:/# ls
# bin boot dev etc home lib lib64 media mnt opt proc root run # sbin srv sys tmp usr var
root@99563aa8ffd6:/# ping 8.8.8.8
# PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=21.6 ms
</code></pre>

Or a web server to serve up pictures of kittahs:

<pre class="code-sample"><code>
docker run -d -p 8000:80 nginx
</code></pre>

Then test with:
<pre class="code-sample"><code>
curl $(docker-machine ip racker-test-instance):8000
</code></pre>

You can also inspect the new container from the base `docker` command with a few different approaches:

<pre class="code-sample"><code>
# Example #1
docker ps -a
# CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
# 2e23d01384ac iperf-v1:latest "/usr/bin/iperf -s" 10 minutes ago Up 10 minutes 5001/tcp, 0.0.0.0:32768;5201/tcp compassionate_goodall
# Append the container ID (CID) to the end of an inspect
docker inspect --format '{{ .NetworkSettings.IPAddress }}' 2e23d01384ac
# 172.17.0.1

# Example #2
# Add -q to automatically parse and return the last CID created.
docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -q)
# 172.17.0.1

# Example #3
# As of Docker v1.3 you can attach to a bash shell
docker exec -it 2e23d01384ac bash
# That drops you into a bash shell then use the 'ip' command to grab the addr
root@2e23d01384ac:/# ip add | grep global
inet 172.17.0.1/16 scope global eth0

# Example #4
# Add to bashrc/bash_profile to docker exec in passing the CID to dock-exec. E.g dock-exec $(docker ps -q) OR dock-exec 2e23d01384ac
dock-exec() { docker exec -i -t $@ bash ;}

# Example #5
# Always docker exec into the latest container
dock-exec() { docker exec -i -t $(docker ps -l -q) bash ;}
</code></pre>

If you run into any issues you can remove the docker host and recreate it with:

<pre class="code-sample"><code>
docker-machine -D ls
# ERRO[0000] error getting state for host dev: machine does not exist
# ERRO[0000] error getting URL for host dev: machine does not exist
# NAME ACTIVE DRIVER STATE URL SWARM
# dev * virtualbox Error
docker-machine create --driver virtualbox dev
</code></pre>

All of the machines you create by default are stored in `~/.docker/machine/` along with a couple of temp state files so its easy to backup the configuration of your machine harness since those are read at runtime every time you send a docker-machine command. You can of course opt for alternative storage paths for those. If you wanted to have copy or restore your machine list, you should be able to simply copy the `~/.docker/machine/` directory to another host and see the same remote machines.
<h3> Troubleshooting </h3>
The only issue, but not really issue, you may see is if you close your laptop or reboot your machine where docker-machine is running, the virtualbox image is probably not running. If you get a state of 'error' odds are the VM isn't running in VirtualBox (or any other machine for that matter).

<pre class="code-sample"><code>
docker-machine ps
# ERRO[0000] error getting state for host dev: machine does not exist
# ERRO[0000] error getting URL for host dev: machine does not exist
# NAME ACTIVE DRIVER STATE URL SWARM
# dev virtualbox Error
# machine-name12345 * azure Running tcp://machine-name12345.cloudapp.net:2376
# test-instance amazonec2 Running tcp://52.5.11.81:2376
</code></pre>

In most cases I just start the machine and VirtualBox plays nicely:

<pre class="code-sample"><code>
sudo docker-machine start dev
</code></pre>

If it doesn't, you can troubleshoot further with some debugging enabled (debug is your friend since this is beta `docker-machine -D [args]`). :

There is an issue I ran into with Virtualbox that returns true when starting a VM but it doesn't actually start even though it reports to Docker machine that it does

<pre class="code-sample"><code>
sudo /usr/bin/VBoxManage startvm dev --type headless
# Waiting for VM "dev" to power on...
# VM "dev" has been successfully started.
</code></pre>
In that case I just destroyed the old image and started a new one. This is the beauty of throw away infra!

<pre class="code-sample"><code>
# Attempt to start a broken or missing instance in VirtualBox
docker-machine -D start dev
# DEBU[0000] command=start machine=dev
# DEBU[0000] executing: /usr/bin/VBoxManage showvminfo dev --machinereadable
# DEBU[0000] STDOUT:
# DEBU[0000] STDERR: VBoxManage: error: Could not find a registered machine named 'dev'
# VBoxManage: error: Details: code VBOX_E_OBJECT_NOT_FOUND (0x80bb0001), component VirtualBox, interface IVirtualBox, callee nsISupports
# VBoxManage: error: Context: "FindMachine(Bstr(VMNameOrUuid).raw(), machine.asOutParam())" at line 2611 of file VBoxManageInfo.cpp
# ERRO[0000] machine does not exist

# List the machine using the VirtualBox API
/usr/bin/VBoxManage showvminfo dev --machinereadable
# VBoxManage: error: Could not find a registered machine named 'dev'
# VBoxManage: error: Details: code VBOX_E_OBJECT_NOT_FOUND (0x80bb0001), component VirtualBox, interface IVirtualBox, callee nsISupports
# VBoxManage: error: Context: "FindMachine(Bstr(VMNameOrUuid).raw(), machine.asOutParam())" at line 2611 of file VBoxManageInfo.cpp

# Delete the errored instance 'dev'
docker-machine rm dev
# INFO[0000] machine does not exist, assuming it has been removed already
# INFO[0000] The machine was successfully removed.

# Create a new virtualbox instance 'dev'
$ dm create --driver virtualbox dev
# INFO[0000] Creating VirtualBox VM...
# INFO[0000] Creating SSH key...
# INFO[0007] Starting VirtualBox VM...
# INFO[0008] Starting VM...
</code></pre>

A couple of Virtualbox debugging commands as follows:

<pre class="code-sample"><code>
/usr/bin/VBoxManage list runningvms
# "dev" {04f5844f-621c-44a5-9959-e85b67b92954}
/usr/bin/VBoxManage list vms
# "dev" {04f5844f-621c-44a5-9959-e85b67b92954}
</code></pre>

If your permissions get a little screwy w/ sudo you may run into this error:
<pre class="code-sample"><code>
# ERRO[0000] error loading host "dev": open /Users/brent/.docker/machine/machines/dev/config.json: permission denied
</code></pre>

That can be solved by dropping the `sudo` on the `docker-machine create`

If you run into an issue that resembles a name resolution issue with a message like so:
<pre class="code-sample"><code>
Building bind...
Step 0 : FROM ubuntu:latest
Pulling repository ubuntu
Service 'bind' failed to build: Get https://index.docker.io/v1/repositories/library/ubuntu/images: dial tcp: lookup index.docker.io on 172.20.10.1:53: read udp 172.20.10.1:53: i/o timeout
</code></pre>

Odds are the root is either a proxy issue or not able to resolve DNS names. If it is a DNS resolution issue, you can specify a DNS server in boot2docker by first SSH'ing to the underlying VM/Docker Host/Machine and popping in a DNS or two.
<pre class="code-sample"><code>
docker-machine ssh boot2docker 
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf
</code></pre>

<h3> OOM Killer and Docker v1.7 </h3>
If you have ever wondered how you can oversubscribe applications inside of an OS as well as you can in Linux when at runtime an application may try to lock up as much memory as possible even if it doesn't use it, it is because the kernel is a bit sneaky and is only allocating much of that memory when the app actually needs it. The downside of the over-commit memory model is when resources become starved, the kernel has to decide who to kill off with a -9 sig. In the current v1.7 master (still in development) I ran into an issues with the following error because I didn't have cgroup memory swap enabled.

So when I went to spin up a Docker container on a fresh build:

[highlight1 bgColor="#74D3F0" textColor="#ffffff"]Your kernel does not support oom kill disable[/highlight1]

<ol class="legacy-numbers">
<ol>
	<li>Fix croup memory by editing:
`/etc/default/grub`</li>
	<li>Replace: 
`GRUB_CMDLINE_LINUX=""`
With:
`GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"`</li>
<li>and `GRUB_CMDLINE_LINUX_DEFAULT="quiet"` with:</li>
<li> `GRUB_CMDLINE_LINUX_DEFAULT="cgroup_enable=memory swapaccount=1"`</li>

	<li>Update the loader `update-grub`</li>
<li>If you don't have the update-grub script (debian) you can do something like `exec grub-mkconfig -o /boot/grub/grub.cfg `</li>
	<li>reboot the host</li>
</ol>
</ol>

The Grub swap modification will also fix the error: `System error: no such directory for memory.swappiness. docker`

<h3> Build From Source </h3>

If you want to try out the latest dev build but don't feel like building it yourself, check out <a href="https://master.dockerproject.com" target="_blank">Docker Master Binaries</a>


A quick down and dirty to build a binary from source:
<pre class="code-sample"><code>
# First install Go.
apt-get build-essentials
git clone https://github.com/docker/docker.git
make binary
service docker stop
mv /usr/bin/docker /usr/bin/docker.bak
mv /home/brent/go/src/github.com/docker/bundles/1.7.0-dev/binary/docker-1.7.0-dev /usr/bin/docker
</code></pre>

See <a href="http://docs.docker.com/project/set-up-dev-env/" target="_blank" rel="noopener noreferrer">Setup and work in a Docker development container.</a>
<hr>

<h3> Installing Docker on Debian 8.0 Potential Errors</h3>

If you go to install docker.io on Jesse you may run into this. Adding the backport will provide a usable binary.

<pre class="code-sample"><code>
Package docker.io is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source
E: Package 'docker.io' has no installation candidate
</code></pre>

To fix this add the following sources to `vi /etc/apt/sources.list`
Add anywhere in sources.list:

<pre class="code-sample"><code>
deb http://ftp.us.debian.org/debian/ sid main
deb-src http://ftp.us.debian.org/debian/ sid main
</code></pre>

Now you will have an updated recent install of docker.io to install via apt-get.
<pre class="code-sample"><code>
apt-get update && apt-get install docker.io
docker -v
Docker version 1.6.1, build 97cd073
(='o'=)[root@deb8-150:docker$ ]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
</code></pre>


<h3> Next up </h3>
I was partly inspired by my buddies Brian and Aaron at <a href="http://thecloudcast.net" target="_blank">thecloudcast.net</a> recently talking about how hard staying on top of the rapidly changing world of compute over the past year or so. They mentioned they traditionally looking to blogs for the emerging innovations and mentioned <a href="http://blog.scottlowe.org" target="_blank">Scott Lowe's blog</a> which is one of the top on my reading list. These and other community focused peeps have perennially taken the time to share and pry information out of the valley to get info to those who don't have the time to stalk PRs, and attend all the cons. I couldn't agree more and kudos to the discussion. (I try to update the podcast links at the bottom of the page, email if I missed yours). For various reasons the current pace of disruption is accelerated and as a result its even more valuable to maintain relationships with friends and colleagues in the community to help one another out staying on top of relevant information that can give you or your company the competitive edge you are likely in some part, paid to do.

Now that you have the ability to provision anywhere you want, head over to <a href="https://hub.docker.com" target="_blank">Docker Hub</a> and take a look at all of the software and projects you can spin up in the time it takes to download the container image. The time it saves being able to use other peoples software builds fundamentally changed how I look at computing. What used to take days figuring out how to install and integrate a peice of software is now done in minutes because I can reuse others open source work and build on top of it.

In the next few posts we will take a look at using various cloud and on prem setups. The barriers to cloud consumption are too high today. There is also early docker swarm integration that will further blur the gaps between providers. The providers I am doing first, are ones that offer trial accounts so that anyone can follow along with me. Along the way and time permitting, showing some kewl ops and netops use cases from having compute and docker hub images already built waiting to be used.

I think we are starting to turn the corner on cloud computing by abstracting away primitive heterogenous APIs that can often lead to complexity and vendor lock-in. My opinion is having harnesses like docker machine that reduce complexity across all clouds, not just one-offs, has benefits to both users in cloud consumption and providers in increased volume and a new influx of customers.

For issues, PR and roadmap check out the project repo:
<a href="https://github.com/docker/machine" target="_blank">https://github.com/docker/machine</a>

Disclaimer, all of this are my own personal reactions and opinions of docker machine. I do my best to gear all of my posts so that a total novice can step in and follow along without too much hair pulling, yet not boring folks with detail overload. While I do work for Docker, I would be blogging about Docker anyways because you have either tried Docker or you haven't. If you have I don't need to convince even the most prickly of folk, still appreciate the fun of using Docker. If I never have to care about how an OS virtualizes hardware again, it won't be soon enough. 


[blockquote align="center" variation="orange" cite="Floppy Driver Exploits of HW Virtualization in 2015 " citeLink=" http://venom.crowdstrike.com" ]VENOM, CVE-2015-3456, is a security vulnerability in the virtual floppy drive code used by many computer virtualization platforms. This vulnerability may allow an attacker to escape from the confines of an affected virtual machine (VM) guest and potentially obtain code-execution access to the host. Absent mitigation, this VM escape could open access to the host system and all other VMs running on that host, potentially giving adversaries significant elevated access to the host’s local network and adjacent systems.[/blockquote]

Thanks for stopping by!

<a href="{{< relurl "/using-docker-machine-to-provision-on-microsoft-azure/" >}}" target="_blank" rel="noopener noreferrer">Next Up: Using Docker Machine to Provision on Microsoft Azure</a>