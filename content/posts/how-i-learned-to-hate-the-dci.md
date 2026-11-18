+++
title = "How I Learned to Hate the DCI"
date = "2012-04-09T00:57:46+00:00"
lastmod = "2012-11-22T07:48:11+00:00"
author = "Brent Salisbury"
wp_id = 287
categories = ["Speculative"]
tags = ["Data Centers"]
description = ""
url = "/how-i-learned-to-hate-the-dci/"
image = "/wp-content/uploads/2012/04/internet.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b3483a2a3540926f22ec3df1115237472ec94ed2e9101197b0ecef345a137f27"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

How I Learned to Hate the DCI: Layer 2 data center interconnects (DCI) is still alive and well. I blame VMware with vMotion and now every other Hypervisor vendor on the planet. Live workload migration is certainly vital to most operations. The further up the stack that happens the more flexibility you have with choosing more layers beneath you to reach for in the toolkit.

The problem needing to be solved is how to move a live data workloads that a client is communicating with directly from one hypervisor (physical peice of gear) without losing TCP state and maintaining service delivery. You are essentially replicating memory and draining the session from one VM to another. To do this you have to keep the IP address the same for the client. The bandaid is overlay and tunneling mechanisms that are being spun up daily now to facilitate the extension of the broadcast domain from one location to another, without to have end to end Layer2 connectivity. Basically going against every sane networking principle we have implemented for the past 10 years.

Two huge problems over distance:
<ol>
	<li>5ms latency threshold.</li>
	<li>Storage needs to be replicated between both sites.</li>
</ol>
The two figures at the bottom, depict the networking gear managing the tunneling and the hypervisors managing the tunnel. I think today I prefer the networking components handling that piece for a few stability factors such as unicast flooding etc, but that will flip fairly quickly in my opinion to distribute the load for massive scale.

IP routing scales, example below the Internet.
<p style="text-align: center;"><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/internet.jpg"><img class="size-medium wp-image-288 aligncenter" title="Internet" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/internet.jpg?w=300" alt="" width="300" height="293" /></a></p>
<strong><em>Figure 1.</em></strong> The Internet scales. Obviously debatable but it beats bridging.

We have basically two options if one wants to move live workloads between data centers. Disclaimer: trying to interconnect data centers beyond being in the same city for realtime replication is fairly risky since you begin fighting time and space with  latency as you keep adding fiber miles to your DCI.

Leave the DCI on the networking hardware to nail up tunnels. MPLS pseudowires/VPLS/TP win in my mind every time. Guess why that doesn't work for many people? The Nexus 7000 does not support VPLS. So do you add yet another layer or succumb to the OTV pre-standard of TRILL.
<p style="text-align: left;"><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/tor-tunnnel.jpg"><img class="size-full wp-image-290 aligncenter" title="TOR-tunnnel" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/tor-tunnnel.jpg" alt="" width="294" height="365" /></a><strong><em>Figure 2.</em></strong> Network gear building the DCI.</p>
The second option is more interesting, not necessarily better, but for a hyper scale provider the potential is critical as we head towards open standard, XML based API cloud aaS movements like Openstack/Cloudstack. As those continue to grow the networking piece will be pushed for more flexibility in automation and provisioning.

The goals of reducing or demolishing operational staffing over the next decade or two (no-ops), will require programatic flexibility through API's to hand the entire operational process over to an orchestration component. Today's networking provisioning and automation isn't quit there beyond scripting from orchestration solutions and SNMP type configurations that have never really gone anywhere. Abstract it with the rest of the stack into software on the Hypervisor softswitch and scale out and up on the same framework. Workloads and data sets are what make it tricky in my opinion, especially outside of the cloud and content provider space like a typical enterprise where you deliver every app possible at a smaller scale, thus needing a very flexible compute platform.
<p style="text-align: left;"><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/hyperv-tunnel.jpg"><img class="size-full wp-image-292 aligncenter" title="Hyperv-tunnel" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/hyperv-tunnel.jpg" alt="" width="284" height="353" /></a><em><strong>Figure 3</strong>.</em> Hypervisors tunneling everything as a DCI.</p>
I still say the further up the stack you go the more options you have in most cases. Global server load balancing (GSLB) offers scale and performance. Google's DNS play has been interesting to watch shape. today in my opinion to global scale.