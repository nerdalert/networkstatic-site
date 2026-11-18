+++
title = "Running Docker Machine on Digital Ocean"
date = "2015-05-11T00:23:42+00:00"
lastmod = "2015-05-24T21:37:59+00:00"
author = "Brent Salisbury"
wp_id = 7646
categories = ["In the Lab"]
tags = ["Digital Ocean", "Docker", "Docker-Machine"]
description = ""
url = "/running-docker-machine-on-digital-ocean/"
image = "/wp-content/uploads/2015/05/Docker-large_h-dark.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b37ee00f284d6fa9cf5537309bde856d0466049ea2b0770efbf2c9d617a58b78"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> Running Docker Machine on Digital Ocean </h3>

Continuing the series on <a href="{{< relurl "/normalizing-the-cloud-with-docker-machine/" >}}" target="_blank">cloud provider examples using Docker machine</a>, up next is Digital Ocean. 
<hr>
As with the other posts here is a diagram of how I view Docker Machine usage.

<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" class="aligncenter size-full wp-image-7574" /></a>


For those who don't have an account already, you can sign get $10 credit with the following link. When you sign up it requires a credit card that won't be charged unless you run out of your credit. At $0.007 /hour for the small image you have tons of test time ~60 days with a single instance if you left it running the whole time.

<a href="https://www.digitalocean.com/?refcode=103fdf2177d8">Sign up for a free Digital Ocean account with $10 credit</a>


Once you have signed up you simply need to grab your security token from your digital ocean management page. In order to o create a personal access token under "Apps & API" in the Digital Ocean Control Panel and pass that to docker-machine create with the `--digitalocean-access-token option`.

<h3> Setup a Docker Machine on Digital Ocean </h3>


By default the smallest VM from Digitalocean is spun up (which I thought was quite considerate I might add to not sneak in a mainframe and rack up a bill).

<pre class="code-sample"><code>
# $ 5 /mo
# $0.007 /hour
# 512 MB / 1 CPU
# 20 GB SSD Disk
# 1000 GB Transfer
</code></pre>


<pre class="code-sample"><code>
export DIGITAL_OCEAN_TOKEN=<token from Apps & API menu on Digitalocean site>

docker-machine create \
  --driver digitalocean \
  --digitalocean-access-token=$DIGITAL_OCEAN_TOKEN \
  test-machine
# Creating SSH key...
# Creating Digital Ocean droplet...
# To see how to connect Docker to this machine, run: docker-machine env test-machine

</code></pre>

As the instructions say, lets `eval` the new digitalocean host:

<pre class="code-sample"><code>
eval "$(docker-machine env test-machine)"
</code></pre>

While Digital Ocean has been the only cloud I have used so far that requires only one parameter (crypto key), it also has APIs options that enable the granularity that production workloads often require.

Here is a simple example of an additional flag requesting a container with 1GB of memory rather then the 512MB default.

<pre class="code-sample"><code>
docker-machine create \
  --driver digitalocean \
  --digitalocean-access-token=$DIGITAL_OCEAN_TOKEN \
  --digitalocean-size "1gb" 
    test-machine-1gb
</code></pre>

I can't help but emphasize how much I appreciate a good set of default values initialized by the CSP. The first go around with a provider is typically getting up and running, not high levels of customization. Digital Ocean nailed it with one required parameter.

As we think about docker infra as code, it only makes sense to see that through with our APIs, Dockerfiles and scripts composing the micro architectures by practicing sound software development principles such as constructors, inheritance, DRY, KISS and so on.

<h3> Run a Docker Container on the New Machine </h3>

Fire up an nginx instance. We will pass the `-d` or `--detach` telling the instance to run in the background and release the CLI. `-p 80:80` simply says expose the web service of the nginx process on port 80 to the world. That could be mapped to any deisred port such as `-p 80:8080` meaning the service would be publicly accessable via port `8080`.


<pre class="code-sample"><code>
docker run -d -p 80:80  nginx
</code></pre>

Next verify the service you started. First by getting the IP address of the VM you started with `docker-machine create`.

<pre class="code-sample"><code>
docker-machine ip test-machine
</code></pre>

Next curl the public port you started the service on using the IP address you just retreived:

<pre class="code-sample"><code>
curl 45.55.146.243:8000

# You can also nest the 'docker-machine ip' command in the curl requested
curl $(docker-machine ip test-machine):80
</code></pre>

Now if you want to troubleshoot that instance, simply use `docker exec` to attach to the host remotely by spawning a bash shell within the instance.

<pre class="code-sample"><code>
# The long way to attach is to first get the container ID (CID) of the host you just spun
docker ps
# which returns
# CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
# 6f6415f773b0        nginx:latest        "nginx -g 'daemon of   4 minutes ago       Up 4 minutes        80/tcp, 443/tcp     high_bardeen

# Now pass that CID along with the command you want to run.
docker exec -i -t 6f6415f773b0 bash
# root@6f6415f773b0:/# ls
# bin  boot  dev	etc  home  lib	lib64  media  mnt  opt	proc  root  run  sbin  srv  sys  tmp  usr  var

# Or pass any other command you want to the underlying Ubuntu virtualized OS
# When you hit control ^c it will exit the current command you passed
docker exec -i -t 6f6415f773b0 top
#    top - 07:32:17 up 43 min,  0 users,  load average: 0.06, 0.03, 0.05
#    Tasks:   3 total,   1 running,   2 sleeping,   0 stopped,   0 zombie
#    %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
#    KiB Mem:    501800 total,   429972 used,    71828 free,    19972 buffers
#    KiB Swap:        0 total,        0 used,        0 free.   319692 cached Mem
#    
#      PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
#        1 root      20   0   31484   2764   2020 S  0.0  0.6   0:00.04 nginx
#        5 nginx     20   0   31868   1680    460 S  0.0  0.3   0:00.00 nginx
#       14 root      20   0   21904   1328   1008 R  0.0  0.3   0:00.04 top
 
</code></pre>

Or start an Ubuntu image and execute a bash shell at runtime.

<pre class="code-sample"><code>
docker run -i -t ubuntu /bin/bash
# Unable to find image 'ubuntu:latest' locally
# latest: Pulling from ubuntu
# e9e06b06e14c: Pull complete
# a82efea989f9: Pull complete
# 37bea4ee0c81: Pull complete
# 07f8e8c5e660: Already exists
# ubuntu:latest: The image you are pulling has been verified. Important: image verification is a tech preview feature and should not be relied on to provide security.
# Digest: sha256:8126991394342c2775a9ba4a843869112da8156037451fc424454db43c25d8b0
# Status: Downloaded newer image for ubuntu:latest
</code></pre>

Note: There are tons of condensed ways to get the CID and run the desired command all in one line. For example:

<pre class="code-sample"><code>
# a single command like so
docker exec -i -t $(docker ps -l -q)  cat /proc/cpuinfo  | grep cores
#Output -->  cpu cores	: 1

# Or you can add aliases to your bash profile 
dexl() { docker exec -i -t $(docker ps -l -q)  bash ;}
</code></pre>
Follow this link for some more <a href="{{< relurl "/docker-one-liners/" >}}" target="_blank">Docker one-liners</a>.

Lastly you can stop with:
<pre class="code-sample"><code>
docker-machine stop test-machine
</code></pre>
And delete the machine with:

<pre class="code-sample"><code>
docker-machine rm test-machine
# Successfully removed test-machine
</code></pre>
Thats it! I was SUPER impressed with Digital Ocean. It was super easy, very fast (de)provisioning and supported all of the docker-machine API calls flawlessly. I was also testing out the Docker Machine 0.3.0-dev build that will be released shortly and it also worked perfectly so kudos all the way around.

This is just scratching the surface of whats possible, take a look at the Docker docs found <a href="https://docs.docker.com/machine/" target="_blank">here</a>
<hr> 

Thanks for stopping by!