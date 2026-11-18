+++
title = "Why the NOS will decouple"
date = "2012-04-02T03:43:30+00:00"
lastmod = "2012-09-09T00:16:10+00:00"
author = "Brent Salisbury"
wp_id = 224
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/why-the-nos-will-decouple/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "dba8325e61b8612f0639520ff86de0b33150358bf75ca60b5d98648f28cc30a7"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

Over the next couple of years some of us expect the networking industry to have some fairly significant changes.

There are really two options:
<ul>
	<li>A distributed approach we have today or a controller based centralized model. We  have today just that, autonomous devices building adjacencies to one another, exchanging what it hopes are the best healthy paths to send next hop traffic to. I am not holding my breath that Netconf is suddenly going to revolutionize operational scale of distributed networks under a single organization.</li>
</ul>
<div></div>
<ul>
	<li>There are three components in our networking switches/routers today, management, data (Layer2 forwarding) and control (Layer3 routing) planes. Centralizing or at least abstracting distributed networks into a single management and possibly control plane to our network. We have some examples of that today that show significant ROI of decoupling the network operating system from the network edge device. Wireless controllers have allowed wireless to scale operationally without having to double the networking staff to support 2x 3x growth in most enterprises annually. QFabric is another example of an exploding chassis across a data center. Software defined networks (SDN) means just that, abstracting operations, administration and management one layer up the stack.</li>
</ul>
I expect us to see a start from vendors to explore decoupling the network operating system from the hardware beyond just data center software switches like a Nexus 1000v. Decoupling the NOS and at least the management plane to start with will allow for innovation beyond just what a handful of networking vendors deem as good software solutions. Decoupling the NOS will allow for our researchers and new startups to develop software above the net.

If we can do this with everything else in the data center why not on the network also? I get a little aggravated when we come up with as many reasons possible to at the end of the day avoid change and innovation when the x86 market has set the roadmap of what I believe we will see over the next decade in the networking industry. The road to innovation is paved with the likes of those unwilling to take risk, Sun, Kodak, Nortel etc. Doing the right thing for the consumer and customer tends to work in my experience.

Let's give the people that do software great have a shot at the industry. The Quantum plugin to Openstack has a lot of potential on this front in the data center where provisioning does not have the luxury of waiting around for two week change tickets like service providers have. We are probably a ways out from regular enterprise and carrier models that isn't special sauce vendor locks.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/decouple-nos.jpg"><img class="alignleft size-full wp-image-225" title="Decouple-NOS" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/decouple-nos.jpg" alt="" width="450" height="261" /></a>