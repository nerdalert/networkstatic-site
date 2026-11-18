+++
title = "Using Docker Machine to Provision on Microsoft Azure"
date = "2015-04-30T07:40:25+00:00"
lastmod = "2015-06-13T01:49:24+00:00"
author = "Brent Salisbury"
wp_id = 7553
categories = ["In the Lab"]
tags = ["Azure", "Docker", "Docker-Machine", "Microsoft"]
description = ""
url = "/using-docker-machine-to-provision-on-microsoft-azure/"
image = "/wp-content/uploads/2015/04/Docker-Microsoft-Azure-Banner.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8419dd01e17d4bc3cdd512ef9c0e990bdea80cbb29effe8620dbe14fc0486372"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<H3> Using Docker Machine to Provision on Microsoft Azure </H3>

Microsoft has done a pretty amazing job with Azure over the years. It has been really cool seeing Microsoft <a href="http://azure.microsoft.com/blog/?s=docker" target="_blank">embrace</a> Docker and open source in general like they recently have. This post is a continuation of the <a href="http://normalizing-the-cloud-with-docker-machine" target="_blank">series</a> on docker machine provisioning to dev hypervisors, DC infra and cloud providers. If you are new to Azure or don't have an account, you can grab a free trial from <a href="http://azure.microsoft.com/en-us/pricing/free-trial/" target="_blank">Azure</a>. 


<hr>
Here is a quick diagram overviewing Docker Machine, more on docker and docker machine in the excellent docs at <a href="https://docs.docker.com/machine/" target="_blank">docs.docker.com</a> 

<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" class="aligncenter size-full wp-image-7574" /></a>

<H3>  Docker Machine Azure Setup </H3>

The following is covered in detail on the docker-machine docs <a href="https://docs.docker.com/machine/#microsoft-azure" target="_blank">page</a> 

<pre class="code-sample"><code>
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
openssl pkcs12 -export -out mycert.pfx -in mycert.pem -name "My Certificate"
openssl x509 -inform pem -in mycert.pem -outform der -out mycert.cer
</code></pre>

Those operations will leave you with three new files:

<pre class="code-sample"><code>
ls
mycert.pfx  mycert.pem  mycert.cer
</code></pre>

Next head to the Azure portal, go to the "Settings" at the bottom left of the page, followed by "Management Certificates" and upload mycert.cer.

 <em>Note</em>: The docker-machine example is structured to be run from the same directory as the credential files we just created (mycert.pfx  mycert.pem  mycert.cer).

 Next start the docker host machine in the Azure cloud with the following command. 
  
<pre class="code-sample"><code>
export AZURE_SUB_ID=<Azure Subscription ID>

docker-machine create -d azure \
 --azure-subscription-id="$AZURE_SUB_ID" \
 --azure-subscription-cert="mycert.pem" \
 machine-name12345
 
INFO[0000] Creating Azure machine...
# *Note* There will be a couple of minute pause while the machine is spinning up
# The client is currently not async ond will block until the Azure host returns ready.
INFO[0451] "machine-name12345" has been created and is now the active machine.
INFO[0451] To point your Docker client at it, run this in your shell: eval "$(docker-machine env machine-name12345)"

docker-machine create -d azure \
--azure-subscription-id="$AZURE_SUB_ID" \
--azure-subscription-cert="mycert.pem" \
machine-name

docker-machine ls
# NAME                ACTIVE   DRIVER       STATE      URL                                          SWARM
# dev                 *        virtualbox   Running    tcp://192.168.99.102:2376
# machine-name12345            azure        Starting   tcp://machine-name12345.cloudapp.net:2376
# aws-instance                 amazonec2    Running    tcp://52.5.11.81:2376

</code></pre>

Take a look at the host you created:

<pre class="code-sample"><code>
docker info
Password:
#Containers: 0
#Images: 0
#Storage Driver: aufs
# Root Dir: /var/lib/docker/aufs
# Backing Filesystem: extfs
# Dirs: 0
# Dirperm1 Supported: false
#Execution Driver: native-0.2
#Kernel Version: 3.13.0-36-generic
#Operating System: Ubuntu 14.04.1 LTS
#CPUs: 1
#Total Memory: 1.639 GiB
#Name: machine-name12345
#ID: ---------------------
#WARNING: No swap limit support
#Labels:
# provider=azure
</code></pre>

You can also get more information on the connection and cert locations using `docker-machine config <machine_name>`
<hr>
Next lets fire up a container and have a look around using docker exec to open a shell to the container running at the CSP, in this case Azure:

<pre class="code-sample"><code>
docker run -itd ubuntu /bin/bash
#Password:
#Unable to find image 'ubuntu:latest' locally
#latest: Pulling from ubuntu
#706766fe1019: Pull complete
#a62a42e77c9c: Pull complete
#2c014f14d3d9: Pull complete
#b7cf8f0d9e82: Already exists
#ubuntu:latest: The image you are pulling has been verified. Important: image verification is a tech preview feature and should not be relied on to provide security.
#Digest: sha256:80d996c3693d792505039a3612cf9221ae9704317ea11fda75c86ede672ee1b3
#Status: Downloaded newer image for ubuntu:latest
#0b1b39ed1f93e6e995d8ad01b9d1028f58f1a457ad2ff5a4a052dfb276e21ce0
#
docker ps -a
#CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
#0b1b39ed1f93        ubuntu:latest       "/bin/bash"         About a minute ago   Up About a minute                       loving_jones
</code></pre>
Exec into a shell on the new container and lets grab the public address of the instance:

<pre class="code-sample"><code>
# Get the container ID from docker ps -a and use it as an argument to docker exec to attach to the remote host console
docker exec -it 0b1b39ed1f93 bash
root@0b1b39ed1f93:/# apt-get install -y curl
root@0b1b39ed1f93:/# curl ifconfig.me
# 104.42.19.153 <-- Your public Azure IP addr
</code></pre>
Now you can delete the container with:

<pre class="code-sample"><code>
docker stop  0b1b39ed1f93 && docker rm 0b1b39ed1f93
# or to delete the most recent container:
docker ps -lq | xargs docker stop | xargs docker rm
 </code></pre>

Deleting machines is similar with `docker-machine rm <machine_name>`. All of the cloud providers I have added so far support deleting the machine except for one that I had to remove it from the provider's console. Azure and AWS do support stopping and starting also.
<hr>

Now you can freely switch between CSPs, your private on prem cloud or your local dev environment with a single line. Pretty awesome.

<em>Note</em> - When you switch between active hosts you also need to swap out your ENVs by simply running the eval command and passing the desired instance.

<pre class="code-sample"><code>
docker-machine active aws-instance
eval "$(docker-machine aws-instance)"
# Running the next line as you switch to verify your ENV variables
env | grep DOCKER
DOCKER_HOST=tcp://52.5.11.81:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/Users/brent/.docker/machine/machines/aws-instance
</code></pre>
Now I am back in an EC2 host we setup in the next tutorial. 

<pre class="code-sample"><code>

env | grep DOCKER
DOCKER_HOST=tcp://52.5.11.81:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/Users/brent/.docker/machine/machines/test-instance
[04:53:49] (='o'=) [azure]docker info
#Password:
#Containers: 0
#Images: 4
#Storage Driver: aufs
# Root Dir: /var/lib/docker/aufs
# Backing Filesystem: extfs
# Dirs: 4
# Dirperm1 Supported: false
#Execution Driver: native-0.2
#Kernel Version: 3.13.0-40-generic
#Operating System: Ubuntu 14.04.1 LTS
#CPUs: 1
#Total Memory: 992.4 MiB
#Name: test-instance
#ID: XXXX
#WARNING: No swap limit support
#Labels:
 provider=amazonec2
</code></pre>

I was super impressed by Docker/Azure integration, this was a breeze to setup. Once again, this is beta and there are still peices getting polished. 

Being able to context switch between providers <strong>without pain</strong>, feels like an important gate in the evolution of computing. The docker machine harness coupled with the dead simple UX for consuming virtually any cloud, public or private, opens the doors to some new patterns in cloud consumption that seemed far off not too long ago. 

 <H3> Troubleshooting </H3>


The MS <a href="http://azure.microsoft.com/en-us/documentation/articles/xplat-cli/">xplat-cli</a> client can be used if you have any issues getting attached to Azure with your account or to get another view at your resources. Credit to the Azure experience, I didn't need to use it once. 


<pre class="code-sample"><code>
This package will install the Microsoft Azure SDK into /usr/local/bin/azure/
To use the command line interface after installation, type `azure` in the Terminal.
To uninstall, type `azure-uninstall` in the Terminal.
</code></pre>

Make sure to use a very unique name for your docker machine in the azure cloud or else you will overlap in the default domain they advertise your hostname as the DNS prefix e.g. 'machine-name12345.cloudapp.net'. If you have overlap, you will notice an error like the one here:

<pre class="code-sample"><code>
docker-machine create -d azure \
  --azure-subscription-id="$AZURE_SUB_ID" \
  --azure-subscription-cert="mycert.pem" \
  machine-name
# ERRO[0000] Error creating machine: A hosted service with the specified name already exists.
# WARN[0000] You will want to check the provider to make sure the machine and associated resources were properly removed.
# FATA[0000] Error creating machine
</code></pre>

Thats about it. Super easy, a real testament to all involved. I also have handful of use cases, mostly around network metrics, validation and data collection that I will be using docker-machine as a base for if you want to follow along with me from home. 

If you are also starting to use docker-machine and get stuck on something, check out the open and closed issue on the project's github <a href="https://github.com/docker/machine/issues">issues</a> page. Anything I had questions on were already covered in issues and the folks working on the project are top notch and super friendly. 

<hr>

For more from Microsoft, there were some cool announcements of Azure features this week at MS Build.
<a href="http://azure.microsoft.com/blog/2015/04/29/iaas-just-got-easier-again/" target="_blank" rel="noopener noreferrer">Azure Docker Extensions Templates </a>

<hr>

<a href="{{< relurl "/docker-machine-provisioning-on-aws/" >}}" target="_blank" rel="noopener noreferrer">Next up is Docker Machine and AWS Usage</a>