+++
title = "Running Docker Machine on Rackspace Public Cloud"
date = "2015-05-01T04:43:45+00:00"
lastmod = "2015-05-24T21:28:29+00:00"
author = "Brent Salisbury"
wp_id = 7615
categories = ["In the Lab"]
tags = ["Docker", "Docker-Machine", "Rackspace"]
description = ""
url = "/running-docker-machine-on-rackspace-public-cloud/"
image = "/wp-content/uploads/2015/05/docker_logo_banner.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "1453ad9a4281a30fd47828dced329b41dae97b9b19eb66259dd0fbd64ed820cb"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> Running Docker Machine on Rackspace Public Cloud</h3>

Next up I am giving Docker Machine on Rackspace public cloud a whirl. If you don't have an account and want to check it out take a look at their <a href="https://developer.rackspace.com/signup/">developer+</a> credit. 

Here is a gif diagram (I'm addicted to making gifs atm, sometimes not even cats doing cute fluffy cat stuff like here) overviewing Docker Machine. To get installed and much more on docker and docker machine check out the excellent docs at <a href="https://docs.docker.com/machine/" target="_blank">docs.docker.com</a> 

<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" class="aligncenter size-full wp-image-7574" /></a>

<h3>Create a Docker Machine </h3>

First head over to your Rackspace console and grab your UID, and your API key. If you are knowledgable about OpenStack, the CLI options should look pretty familiar (thats pretty cool btw). You can also you ENVs for some of the values listed in the docker-machine docs one overriding the other.

<pre class="code-sample"><code>
Options:
   --rackspace-api-key 													Rackspace API key [$OS_API_KEY]
   --rackspace-docker-install "true"											Set if docker have to be installed on the machine
   --rackspace-endpoint-type "publicURL"										Rackspace endpoint type (adminURL, internalURL or the default publicURL) [$OS_ENDPOINT_TYPE]
   --rackspace-flavor-id "general1-1"											Rackspace flavor ID. Default: General Purpose 1GB [$OS_FLAVOR_ID]
   --rackspace-image-id 												Rackspace image ID. Default: Ubuntu 14.04 LTS (Trusty Tahr) (PVHVM)
   --rackspace-region 													Rackspace region name [$OS_REGION_NAME]
   --rackspace-ssh-port "22"												SSH port for the newly booted machine. Set to 22 by default
   --rackspace-ssh-user "root"												SSH user for the newly booted machine. Set to root by default
   --rackspace-username 												Rackspace account username [$OS_USERNAME]
</code></pre>

Rackspace VM flavors are listed <a href="http://docs.rackspace.com/servers/api/v2/cs-devguide/content/server_flavors.html" target="_blank">here</a>
<hr>
Next lets spin up the instance using an image flavor-id of '2' which is the smallest 512MB machine. I specified the region ID that was listed in the <a href="https://mycloud.rackspace.com/" target="_blank">Rackspace Console</a>.

<pre class="code-sample"><code>
docker-machine create \
  --driver rackspace \
  --rackspace-username <$USERNAME> \
  --rackspace-api-key <$SUPER_SECRET_KEY> \
  --rackspace-flavor-id 2 \
   --rackspace-region IAD \
  racker-test-instance
</code></pre>

And voila, we have an instance that is now our active instance in docker-machine:

<pre class="code-sample"><code>
$ dml
NAME                   ACTIVE   DRIVER       STATE     URL                                         SWARM
dev                             virtualbox   Running   tcp://192.168.99.100:2376
machine-name12345               azure        Running   tcp://machine-name12345.cloudapp.net:2376
racker-test-instance   *        rackspace    Running   tcp://162.209.126.37:2376
test-instance                   amazonec2    Running   tcp://52.5.11.81:2376
</code></pre>

<h3> Run some Docker Containers on Rackspace </h3>

Now load the environmental variables for the Rackspace instance:

<pre class="code-sample"><code>
eval "$(docker-machine env racker-test-instance)"
</code></pre>

You can then verify with `env | grep DOCK`
<pre class="code-sample"><code>
$ eval "$(docker-machine env racker-test-instance)"
$ env | grep DOCK
DOCKER_HOST=tcp://162.209.126.37:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/Users/brent/.docker/machine/machines/racker-test-instance
</code></pre>

Now start spin up some containers:

<pre class="code-sample"><code>
$ docker run busybox echo hello world
Password:
Unable to find image 'busybox:latest' locally
latest: Pulling from busybox
cf2616975b4a: Pull complete
...
Status: Downloaded newer image for busybox:latest
hello world

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS                      PORTS               NAMES
31cb98825df0        busybox:latest      "echo hello world"   14 seconds ago      Exited (0) 14 seconds ago                       sleepy_sammet
</code></pre>

or fire up a webserver mapping port 80 to port 8000:

<pre class="code-sample"><code>
docker run -d -p 8000:80 nginx
</code></pre>

Now grab the IP and open a socket to the server for funs:

<pre class="code-sample"><code>
$ docker-machine ip racker-test-instance
$ curl <ip>:8000
</code></pre>

or even more clever from the docker machine docs this:

<pre class="code-sample"><code>
$ curl $(docker-machine ip racker-test-instance):8000
<title>Welcome to nginx!</title>
</code></pre>

I was impressed how easy it was to consume resources from Rackspace Pub Cloud using machine. Thanks to my pal <a href="https://twitter.com/andyhky" target="_blank">@andyhky</a> from Rackspace getting a test account for me. If you dont already read his <a href="https://virtualandy.wordpress.com" target="_blank">blog</a>, check it out for some netops meets devops funz. Rackspace has a nice detailed blog entry that I didn't see until I finished this so that leaves lots of resources in case anyone gets blocked. Check it <a href="https://developer.rackspace.com/blog/using-docker-machine-to-deploy-your-docker-containers-on-rackspace/" target="_blank">here</a>.

<hr>

<a href="{{< relurl "/running-docker-machine-on-digital-ocean/" >}}" target="_blank" rel="noopener noreferrer">Next up is Docker Machine on Digital Ocean Pub Cloud</a>
<hr>
Thanks for stopping by!