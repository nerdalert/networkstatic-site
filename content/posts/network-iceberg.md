+++
title = "The Network Iceberg"
date = "2014-10-31T18:19:47+00:00"
lastmod = "2015-05-24T11:34:35+00:00"
author = "Brent Salisbury"
wp_id = 7411
categories = ["Speculative"]
tags = ["Containers", "Docker", "Go", "Socketplane"]
description = ""
url = "/network-iceberg/"
image = "/wp-content/uploads/2014/10/SocketPlane-Banner2.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "0a7d0d75b69793bb883efe8a479cb999495dab2861c196a21e04a6254c0a1f8c"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The Network Iceberg</h2>
The impact of compute virtualization on the data center network has been profound. There are more virtual ports then physical ports. That simple measurement overshadows any other disruption in networking. We arrived at this transformation as a result of significant adoption of OS virtualization.

The next revision of compute virtualization is the application. The last significant bastion of efficiency is to remove the OS from the equation and virtualize that application itself. At the helm of the compute disruption is <a href="https://www.docker.com/tryit/" target="_blank">Docker</a>. Depending on a providers oversubscription, a typical ratio of VM/CPU is in the range of 20-50 VMs per physical core. The consolidation and eventual removal of the guest OS will significantly affect the subscription ratio. The condensation of the application to CPU ratio and the demand that will be imposed on the network is pretty damn exciting. There is of course some debate around security, shared kernel etc, but we had the same conversations in the infancy of OS virtualization. Atomic and CoreOS are both cool projects if you haven't seen them before, take a look. The lightweight, purpose build OS are pretty awesome.
<h2>The Docker Impact on Networking Density </h2>
What this means for networking will be a hyper-dense networking environment, embedded deeply inside of the host operating system. Not only is the port virtual port density going to explode but also the traditional middle box services are being desegregated also.

If they haven't already, network Ops and architects need to evaluate the impact of the new soft edge. The 2-tier spine/leaf architecture was a response to a realignment of bandwidth and the resulting need for bisectional support (95/5; %95 of the traffic north/south leaving the data center and %5 remaining east/west). The 3rd tier is back (or never left) and it will require a deep fundamental understanding of networking in order to provide reliable scale. It will be reasonable to expect thousands of IP addresses hanging off each port (PAT has never fit many provider needs) in the top of rack. Uptime is sexy and also the number one measurement of most of ops value to an organization. All that cost savings means much less when we are riding high on two 9's.

There are inherent complexities to networks that aren't going anywhere, but fortunately, we do know how to compartmentalize that complexity. Breaking down the silo between the edge virtualization teams and the physical network ops is pretty important moving forward. This is much more significant then the underlay vs. overlay conversations and much more about getting the right architectures that allow for orchestrated provisioning coupled with operational visibility for troubleshooting. There is no one architecture that fits all needs, everything is a trade off but reliability is a non-negotiable core value. We have learned (often the hard way) in other projects that significant float in network state between numerous platforms are not easy consistency problems to solve.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/10/Iceberg-SocketPlane-Virt-Net.png" >}}" alt="SocketPlane.io Virtual Network"></figure>
<h2>SocketPlane</h2>
The early SDN model took us to a bizarre nascent land of complexity and fragility. The good news is that wasn't wasted effort but merely a refinement. It is now crystal clear pieces of networking both new and old will be composed to absorb the compute reconstruction that will place enormous demands on the network. My brilliant cohorts at our new venture <a href="http://socketplane.io/press/sdn-experts-unite-to-bring-devops-defined-networking-to-docker-users/" target="_blank">SocketPlane.io</a> <a href="https://twitter.com/botchagalupe" target="_blank">@botchagalupe</a>, <a href="https://twitter.com/MadhuVenugopal" target="_blank">@MadhuVenugopal</a>, <a href="https://twitter.com/dave_tucker" target="_blank">@dave_tucker</a> and I are excited to do our part in the community to develop a networking solution based on the practicals of the past and innovations of the present. Just as importantly, being laser focused on the ops/developer's needs. This is the most exciting part because we have been in the trenches much of our careers so there is no speculating at the problems we are solving. We know the problems and have the scars to prove it. So come join the community in the exciting transformation and leave your mark, its a fantastic time to stand and be counted. 

Take a look at one of our proposals <a href="https://github.com/docker/docker/issues/8951#issuecomment-62234817" target="_blank">#8951</a>, its intention was to get the community thinking about the need for basic building blocks of networks out of the box in Docker.  <a href="https://twitter.com/solomonstre" target="_blank">Solomon Hykes</a> and the rest of the Docker team are awesome and really get the open source community so we are excited to assist in scaling out Docker networking. Long story short, its building L3 switches with the ability to lay OVS services on top in every edge node. This is the only thing in our experience that we are comfortable in saying with confidence that users won't be sad pandas on fragile infra if we head down this path. No shortcuts especially when facing at least a 10x-20x  increase in density. provisioning will be measured in fractions of a second, the days of having plenty of time for a VM to boot and getting a port provisioned are gone. Workloads could be over and completed in the time it takes to boot a VM. To avoid race conditions we are disaggregating everything and letting our old trustys update peer nodes with state changes. Its a long <a href="https://github.com/docker/docker/issues/8951#issuecomment-62234817" target="_blank">thread</a> but lots of fun so take a read and leave your thoughts if interested in the subject. There is a survey if anyone is interested in giving their direct feedback about networking to all of the studs at Docker <a href="https://docs.google.com/forms/d/1EK6j5pEE14dHrxB2DAkwjiMg0KzDpMN__o-QkIX9OcQ/viewform?c=0&w=1" target="_blank">here.</a>

<h2>Community </h2>
Feel free to email/tweet etc. We live and breath collaboration. Community and open source isn't something we say we can "live with if we have to" or some strategic "first hit for free" nonsense. It is at the core of what we do and what we believe the future of infra will be. I have a series on Go programming as an alternative to Python for sysop/netops that I am excited to wrap up and post soon. <a href="http://www.golang-book.com" target="_blank">Go</a> is a really elegant, yet practical language that dominates PaaS, not to mention its a really fun language to use and we are having a blast with it. It blends the niceties of both low level and high level interfaces and suited for a wide range of experience and use cases. <a href="https://golang.org/doc/install" target="_blank">Go</a> has a nice transition from a high level Python like interface, OO struct compositions that can quickly progress towards lower level memory management concepts of pointers (dynamic zero latency GC), C-like speeds but a fraction of the C compile time for you test-driven hackers like me :) Catch you soon, thanks for stopping by and we'll see you upstream!


<h2><h2 class="legacy-heading">Updates</h2></h2

Take a look at Socketplane's very own John Willis aka <a href="https://twitter.com/botchagalupe/" target="_blank">@botchagalupe</a> demoing our tech preview:

[embed]https://www.youtube.com/watch?v=5uzUSk3NjD0[/embed]
