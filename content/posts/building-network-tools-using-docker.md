+++
title = "Building Network Tools using Docker"
date = "2015-06-01T10:22:09+00:00"
lastmod = "2016-03-29T07:37:04+00:00"
author = "Brent Salisbury"
wp_id = 7767
categories = ["In the Lab", "Programming"]
tags = ["DevOps", "Docker", "Programming"]
description = ""
url = "/building-network-tools-using-docker/"
image = "/wp-content/uploads/2015/06/docker-build-text.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "91c518282c2bf8554a40cf45652b6d99ef0409ce734efeed31f6385e1f117050"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>Building Network Tools using Docker</h3>

I am going to start pushing out an app every month that fixes some problem in networking. In this case I hacked it up over the past couple of weekends, but other times it will just be me using someones open source awesomeness and demoing it. 

First some thoughts on where we are in the wild world of networking to tee up the reason I am excited about delivering network tools via Docker. 

<h3>SDN Progression</h3>

If anyone thought decoupling the monolithic network software stack would create ubiquity in network architectures missed the mark. So here are some updates on what I am seeing and why its a great time for the network professionals to gain some high ground as the barrier to entry has never been lower.

We have the traditional controller/centralized folks plugging away. We have the decentralized camps. Not logically centralized, but one controller per node. In the traditional decentralized (one control daemon per node) there are two predominant trends. One is use traditional IGP/EGPs to distribute state and even integrate into the physical fabric and the existing network policies. The second, to be an independent layer that may be aware, but not tightly couple to the underlying fabric. Traditional protocols are ignored and network state is distributed via distributed data stores. All approaches have merit, I look for scale, performance and reliability when evaluating an architecture but different networks have different needs.

NFV, NFV, NFV. Know why you hear so much about NFV? It's because the telco market is $5+ trillion and service providers need to reinvent how they deliver services. The principles are still the same, move blackbox services to off the shelf compute. The scale is such that squeezing seemingly small efficiencies in cost, power, service revenue adds up to an enormous amount of savings or revenue. If you aren't looking at NFV and micro-services as one in the same I would probably love to debate you someday. The compute for those workloads need to be on demand and elastic to meet the realtime performance expected from the network. Not to mention, the performance you are starting to see from user space offloading is pretty ridiculous. How disruptive are off the shelf servers that can do 100Gb wire? A pair of servers in each rack for inline for use cases requiring cracking open payload is a fun scenario. The other side of the coin is services via user space processes. I am more optimistic on iptables and HAProxy then I had been in the past, mainly because I see the abstracting of the complexity happening via Docker and others that makes it transparent to the user. Same with v6. v6 adoption seems reasonable as we start to <a href="https://docs.docker.com/userguide/dockerlinks/" target="_blank">link</a> systems via names rather then addresses.

<h3>Network Tooling and Programmatic Management </h3>

What is less headline grabbing but what is a profound change is the need for programmatic management of the network. We will transition from reacting to the data to predicting from the data about the performance, health and overall user experience of your network. That is an organic path that will be defined by sharp network folks like you. To get it right, the people that know networks the best need to be at the table innovating on this front. A simple place to start is don't do manual changes anymore. Change controls should be scripted and signed off by network people, not paper pushers. Along with that, when a change goes in, or any anomaly, have tests running that you can have data from as many different angles as possible so you can triangulate in on the problem as quickly as possible.

We are continuing an exponential growth of endpoints with less tolerance then ever to any anomolies in the network. IoT will explode this even further. We are already at the point of massive monetary and life safety issues associated with network downtimes and we are on the verge of self-driving cars that rely on uninterupted access to IP networks. Networkers are guilty until proven innocent.

Open source software changed how systems are managed and will and is doing the same with networks. Why I am so optimistic on this front? It is because in order to run and share tools and software it has become so easy to get a stack of what was traditionally a week or so of bashing around on poorly documented scripts, it is now a matter of using someones build from Github and Docker Hub. We are slowly getting away from wheel reinvention infra when it comes to the basic elements as the stacks evolve. 

The ability to share open source and specifically apps, system configurations and deployments between members of the community is easy with Docker and other config tools for that matter I just find Docker to be the easiest. This includes the vendors developing products. Vendors can come up with excellent solutions but when it comes to enabling the customer to deploying it, the wheels often start to fall off. The configuration tools now enable you to take the exact intent of what you want the user experience to be and have the customer up and running in minutes. It wasnt too long ago I remember running around with a couple of buddies (lol if you're reading :p) at a conference with 6GB VM images to have the audience copy down to their laptops, and then trying to get interfaces, displays, terminals all setup in Virtuabox and VmFusion for the room to do a lab. It took almost the entire time to just get the audiences environents up and we barely got to the actual applications! But the application for networking was, `ping x.x.x.x`. As Network professionals, we can do more at the application layer then just pings.

<h3>Great Time to Start</h3>

More then anything, its a great time for networking professionals to take advantoage of the current momentum of seperating Application Virtualization from Hardware Virtualization. For example, projects like OpenStack can take a bunch of heat for being too hard to install, keep stable etc. I tend to argue that HW virtualization being tightly coupled to the applications as it is with the past decade of compute virtualization is inherantly the problem rather then laying it squarely on the shoulders of the orchsetration engine. Trying to do multiple layers is really hard to get right on each layer and if one isn't right it leads to fragile systems and complexity. My friend Matt Oswalt who is had a spot on post recently on why small and lightweight wins which is really laying out micro services for NetOps that you should read <a href="http://keepingitclassless.net/2015/07/big-flowering-thing/" target="_blank">here</a>. It is a chance for networking to close the gap as all infra verticals are re-examining how compute is consumed networking can evolve in lock step.

Guilty until proven innocent, the NetOps mantra. Open source is a huge win for network engineers. If you are like many, the whole server virtualization wave happened and you were buried in a comm closet trying to figure out why a UPS died, or one out of every 10 pings is dropping to someones server with nothing more then `show int | inc wtf`.

I think as networking to discover the value of Dockerizing their tools and starting to think of compute as processing workloads rather then some server that you get every now and then that is un-patched and ignored because you don't have the time for care and feeding.

If you are new to Docker or compute in general, get started with this <a href="https://www.docker.com/tryit/" target="_blank">tutorial</a>.

<h3>An Example of Throw Away Infra</h3>

Bottom line is you no longer have to be a developer to do DevOps. You don't have to work at scale to automate. It is much easier to reset your environment by destroying a container and starting a new one then it is to try and write software that will run forever and never meltdown. If you run processes knowing they will break if left up forever it makes life so much easier. Here is an example of this immutable concept.

Here is a container that will do something and then delete itself when the work is done. Next time more work comes through, you simply start another container. Why this is attractive is that I have a pristine environment every  time work needs to be done. 
<pre class="code-sample"><code> 
docker run -i --rm \
    --name=${PONY_RIDES} \
    --env=DB_IP=${DB_IP} \
    ${DOIN_WORK_IMAGE}'
</code></pre>

It is like having a new car every time I drive to the store and when I get home from the store I get to push the old car off a cliff before it breaks down on me (dramatic).

In this case its exact operations but with a different workload. There is not any variation in the functions being performed on the data because there was not any float between the 1st and 2nd `docker run` because we are using the common base container image each time.

<pre class="code-sample"><code> 
WORK=$(sudo docker run -d ubuntu /bin/sh -c "while true; do echo Driving to Walmart; sleep 3; done")
docker stop $WORK
docker rm $WORK
WORK=$(sudo docker run -d ubuntu /bin/sh -c "while true; do echo Driving to PetSmart; sleep 3; done")
</code></pre>


So check out this bandwidth monitoring app and even start building your own! No one knows the problems better then those of us from the trenches and the tools now a days enable you to build solutions in a fraction of the time then it used to. 


Here is a screenshot to give you a feel for what the app does:

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/06/Cloud-Bandwidth-smaller1.jpg" >}}" alt=""></figure>


<a href="{{< relurl "/wp-content/uploads/2015/06/Cloud-Bandwidth.jpg" >}}" target="_blank" rel="nobox">Link for a higher res screen cap</a>

So lets get hacking and sharing! If you have some kewl Dockerized apps I would love to give them a try.

<a href="https://github.com/nerdalert/cloud-bandwidth" target="_blank" rel="noopener noreferrer">Github: Cloud Bandwidth Performance Monitoring with Docker</a>



Thanks for stopping by!