+++
title = "Docker Command One Liners"
date = "2015-02-24T04:35:54+00:00"
lastmod = "2015-05-11T00:40:18+00:00"
author = "Brent Salisbury"
wp_id = 7519
categories = ["In the Lab", "Programming"]
tags = ["Docker", "Tutorials"]
description = ""
url = "/docker-one-liners/"
image = "/wp-content/uploads/2015/02/docker-logo.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "187d68b7419b5e21702e56e3710951d2adef33f58caa6468a6394fa87816c3a1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<H3>Docker Command One Liners</H3>

I love the code snippets, it's how I learn any syntax by rolling up the sleeves, hacking and breaking while taking notes along the way. It's probably not the most efficient but the muscle memory is how I learn. Here is a list of one liners from my notes in no particular order (even though I tried to in a couple of places :).

This post is for people fairly new to Docker or looking to build out their command notes list. The Docker API is as nice of a CLI as there has ever been. It is very intuitive and exemplifies the practicality of Golang. The list also drives home the ease of use that is at the heart of why Docker is adopting so rapidly. I see it almost daily now, the lightbulb comes on when they use Docker for the first time and spin up what usually takes a long multi-Gig download, patching, compiling sw etc and is condensed into a 50-80MB download and a fraction of a second to start. 

Whether a network professional, sys admin, devops, sw eng, product manager, etc once they use Docker, they often come to the same conclusion, how apps are delivered will look radically different over the next couple of years. It is truly infrastructure as code that lowers the ability to install software and incrementally pattern systems with as much granularity as you desire that can be replicated that consistently time after time. For those providing software to customers or to production, there has never been a simpler way to deliver your intent to the user or service with the exact experience you want them to have without the exposed complexity that was becoming far too pervasive in today's infra. 
<H3>If you are new to Docker</H3>

If you are new to Docker, check out the Docs and pick the OS you're running:

<a href="https://docs.docker.com/installation/" target="_blank" rel="noopener noreferrer">Install Docker Instructions</a>

What excites many (including myself) is that traditional technological barriers and "how we have always done things" are being overcome by open source composable building blocks. While everyone has some degree of opinion on "best practice" new patterns are emerging daily that challenge what was either not technically feasible or had a complexity factor that made it impractical.
<H3>Dockerfile and Containers is Code as Infrastructure</H3>

Before the list, there may be one command here folks might not be familiar with. To clear up the magic, xargs is a handy command that in the examples below takes the results as a string from a docker command that breaks on whitespace and then uses the stored string as a parameter.
  
<pre class="code-sample"><code> # xargs example
$ docker ps -lq | xargs echo "Heeey Buuuuddy its a container ID  --> "
Heeey Buuuuddy its a container ID  -->  9f5c57b6148d
</code></pre>

I also drop them into my ~/.bash_profile (Mac) or ~/.bashrc for aliasing for that extra fraction of efficiency :) 

Apologies for any duplicates, I will proof it better later in the week. There will be typos and errors but thats ok, if new to Docker it will all be fun and learning with a syntax debug or two :)

<pre class="code-sample"><code> # Run a container  with a random name
docker run -i -t debian /bin/bash
</code></pre> 

<pre class="code-sample"><code> # run a container  with a specified name  and a bash shell that stays up as long as the bash process is running. This is most familiar to folks who manage VMs today
docker run -i -t --name mittens debian /bin/bash
</code></pre> 

<pre class="code-sample"><code>
# next run a container and instead of running a bash shell, running a single application. The container will exit once it has completed.
docker run -i -t --name mittens debian echo 'I am elastic compute'
Password:
Output -> I am elastic compute

# view the echo container just run, it is now exited since the workload was done. Run it again with `docker start mittens`
docker ps -l
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                      PORTS               NAMES
e46facaf4935        debian:latest       "echo 'I am elastic    44 seconds ago      Exited (0) 42 seconds ago                       mittens
</code></pre> 

<pre class="code-sample"><code> # start a stopped container by ID or name
docker start <container_id or name>
docker start mittens
</code></pre> 


<pre class="code-sample"><code> # stop a container by ID or name
docker stop <container_id or name>
docker stop mittens
</code></pre> 

<pre class="code-sample"><code> # start a stopped container by ID or name
docker start <container_id or name>
docker start mittens
</code></pre> 

<pre class="code-sample"><code> # attach to a running container.
docker attach <container_id or name>
docker attach mittens
</code></pre> 

<pre class="code-sample"><code> # get json formatted detailed information about a container
docker inspect <container_id or name>
docker inspect mittens
# parse using grep for interesting fields like so to get a container IP address:
docker inspect mittens | grep IPAddress
</code></pre>

<pre class="code-sample"><code>
# To cleanup all of those untagged images (Those labeled with <none>)

docker images -a
# REPOSITORY                          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
# <none>                              <none>              4008b117428e        17 hours ago        210.2 MB
# <none>                              <none>              53eb80109e88        17 hours ago        210.2 MB
# <none>                              <none>              f48d7a9838a0        17 hours ago        210.2 MB

# If a container is using it or there is a conflict it will abort the current image delta and move on to the next.
docker rmi $(docker images -a | grep "^<none>" | awk '{print $3}')
</code></pre>

<pre class="code-sample"><code> # to remove a container    
docker rm  <container_id or name>
</code></pre>

<pre class="code-sample"><code> # to remove all containers, even stopped ones.   
docker rm $(docker ps -aq)
</code></pre>

<pre class="code-sample"><code> # to stop all containers.   
docker stop $(docker ps -q)
</code></pre>

<pre class="code-sample"><code> # view the last container to be started
docker ps -l
</code></pre>

<pre class="code-sample"><code> # get the container ID column only
docker ps -l -q
</code></pre>

<pre class="code-sample"><code> # stop the last container created
docker stop $(docker ps -l -q) 
</code></pre>

<pre class="code-sample"><code> #stop and delete the last container created
docker ps -l -q | xargs docker stop | xargs docker rm
</code></pre>

<pre class="code-sample"><code> # delete the container name
docker rm <container_id or name>
</code></pre> 

<pre class="code-sample"><code> # Remove all containers    
docker rm $(docker ps -a -q)
</code></pre> 

<pre class="code-sample"><code> # remove all containers
docker rm $(docker ps -a -q)
#... or ...
docker ps -a -q | xargs docker rm
</code></pre> 

<pre class="code-sample"><code> # another way to stop and delete the last container created
docker ps -l -q | awk '{ print $1 }' | xargs docker stop | awk '{ print $1 }' | xargs docker rm
</code></pre> 

<pre class="code-sample"><code> # When you 'docker run' an image and it fails at runtime, it will appear as Exited for example:"Exited (0) 8 days ago"
 # exiited containers are  refered to as "dangling" images.
 # delete all exited/dangling images
docker rmi $(docker images -q --filter "dangling=true")
</code></pre> 

<pre class="code-sample"><code> # same as above but for containers, remove all Exited/failed containers.
docker rm $(docker ps -q -a  --filter "dangling=true")
</code></pre> 

<pre class="code-sample"><code> #  Install an image from docker reg   
docker pull <image_id>
</code></pre> 

<pre class="code-sample"><code> # all images installed on the host
docker images
</code></pre> 

<pre class="code-sample"><code> # build an image by running in the same directory as a Dockerfile. This is often referred to as 'build time' while 'docker run' is referred to as... you guessed it! 'run time!'
docker build  whatever_I_want_to_name .
</code></pre> 

<pre class="code-sample"><code>  # All of the following assume a Dockerfile has "Expose 80" meaning bind a port to 80 for a service
docker run  -i -t -p 80 --name container_name  image_name
docker port $(docker ps -l -q) # returns the port bindings,  or simply `docker port <ID or container name>
80/tcp -> 0.0.0.0:49153

 # bind a specific port to the container and host OS.
docker run  -i -t -p 81:80 --name container_name  image_name
80/tcp -> 0.0.0.0:81

# bind a random port to the container and host OS for the "Expose" binding in Dockerfile.
docker run  -i -t  -P --name container_name  image_name
docker port $(docker ps -l -q)
80/tcp -> 0.0.0.0:49158
</code></pre> 

<pre class="code-sample"><code> # remove a single image    
docker rmi <image_id>
</code></pre> 

<pre class="code-sample"><code> # return all containers on the host    
docker ps
</code></pre> 

<pre class="code-sample"><code> # stop all running containers (Note: simply replace "grep Up" with whatever column value you want to match on.
docker ps -a | grep Up | awk '{ print $1 }' | xargs docker stop
</code></pre> 

<pre class="code-sample"><code> # delete all containers    
docker rm $(docker ps -a -q)
</code></pre> 

<pre class="code-sample"><code> # delete all containers    
docker rm $(docker ps -a -q)
</code></pre> 

<pre class="code-sample"><code> # image operations are nearly identical to container operations.
docker images | grep some_image_name | awk '{ print $3 }' | xargs docker rmi
 # or ...
docker rmi $(docker images | grep some_image_name | awk '{ print $3 }')
 # Or change the awk operation to the image "tag" column and parse an OS name for example
docker rmi $(docker images | grep centos | awk '{ print $2 }')
</code></pre> 


<pre class="code-sample"><code>
# stop and remove all running containers. similar approach due to the consistent API to containers as prior with images. (status=='Up')
docker ps -a | grep Up | awk '{ print $6 }' | xargs docker stop
</code></pre> 

<pre class="code-sample"><code> # upgrade to the latest  Mac boot2docker Docker image
boot2docker upgrade
</code></pre>

<pre class="code-sample"><code> # list the container ip for Mac boot2docker 
boot2docker status
</code></pre>

<pre class="code-sample"><code> #stop and delete running containers
docker ps -l -q | awk '{ print $1 }' | xargs docker stop | awk '{ print $1 }' | xargs docker rm
</code></pre> 

<pre class="code-sample"><code> #Attach to a bash shell in the last started container
dockexecl() { docker exec -i -t $(docker ps -l -q) bash ;}
</code></pre> 

<pre class="code-sample"><code> #Attach to a bash shell in the specified container ID passed to $ dockexecl <cid>
dockexec() { docker exec -i -t $@ bash ;}
</code></pre> 

<pre class="code-sample"><code> #Get the IP address of all running  containers
docker inspect --format "{{ .NetworkSettings.IPAddress }}" $(docker ps -q)
</code></pre> 

<pre class="code-sample"><code> #Get the IP address of the last started container
docker inspect --format "{{ .NetworkSettings.IPAddress }}" $(docker ps -ql)
</code></pre> 

<pre class="code-sample"><code> #stop and delete a container by name
docker stop <image_name> && docker rm flow_img
</code></pre> 

<pre class="code-sample"><code>
# Delete all containers matching whatever you pass as a parameter
delcon() { docker rm $(docker ps  -a | grep $@ | awk '{print $1}') ;}
# This doesn't delete running containers. You can add '-f' to stop and remove the container 
# An Example is deleting any image matching 'ubuntu:latest': 
delcon ubuntu:latest 
# Or delete any container matching a process 
delcon "/bin/bash"
</code></pre>

<pre class="code-sample"><code> # list the container ip for Mac boot2docker 
boot2docker ip
</code></pre>

<pre class="code-sample"><code> # occasionally you will see the following REST errors which means your boot2docker (or docker for that matter) was probably not started in initialization of a host or you dev machine etc. You can restart or start depending on the status.
FATA[0000] An error occurred trying to connect: Get https://192.168.59.103:2376/v1.17/containers/json?all=1&limit=1: dial tcp 192.168.59.103:2376: host is down
boot2docker restart (or) boot2docker start
</code></pre>
<H3>Docker Machine CLI  Command One Liners</H3>

If you haven't tried out <a href="{{< relurl "/normalizing-the-cloud-with-docker-machine/" >}}" target="_blank">Docker Machine</a> yet you should give it a whirl, its pretty damn cool.

Here are my aliases for it from my `~/.bash_profile`

<pre class="code-sample"><code> 
# Docker Machine
alias dmachine='cd ~/Downloads/dmachine'
alias dm='sudo docker-machine '
alias dml='docker-machine ls '
alias devstar='docker-machine start dev'
alias denv='env | grep  DOCKER'
alias dkenv='eval "$(sudo docker-machine env dev)"'
alias dmc='docker-machine create '
alias dmip='docker-machine ip '
alias dmub='docker run -d -p ubuntu /bin/bash'
alias dmstar='docker-machine start '
alias dmstop='docker-machine stop '
alias mstar='docker-machine start '
alias mstop='docker-machine stop '
# Start/Stop the last container created
alias mstar1='docker-machine start $(docker-machine ls | tail -1 | awk "{print $1}")'
alias mstop1='docker-machine stop $(docker-machine ls | tail -1 | awk "{print $1}")'
alias dmk='docker-machine kill'
# Inspect the last container created
alias dmin='docker-machine inspect $(docker-machine ls | tail -1 | awk "{print $1}")'
# Remove the last container created
alias dmrm='docker-machine rm $(docker-machine ls | tail -1 | awk "{print $1}")'
</code></pre>

You can download all of the Docker CLI one liners above from <a href="https://github.com/nerdalert/dotfiles/blob/master/docker_cli_one_liners.sh" target="_blank">github here</a>.
<hr>
I will keep adding as new features come in and what not. I have no doubt there are tons of duplicates but I have just run out of time so will clean them up another day. Will also get to more advanced topics soon but for my friends new to Docker, basics first. Beauty is, u can master the APIs in no time because they aren't insane and super easy to consume. 

Next time you want to share an app with someone, try sending a file that will download <100MB with the ability to configure the app exactly how you want it rather then a file that will pull down full blown operating systems without native means to deploy the App how you intended not guessing the hundreds/thousands of potential variable states in the target host environment. Rather then trying to keep the state of your systems from gradually eating themselves over time, it is worth giving some thought to a less mutable infrastructure that you simply recreate rather then repair. 

In the meantime, keep the coffee coming and the containers running!