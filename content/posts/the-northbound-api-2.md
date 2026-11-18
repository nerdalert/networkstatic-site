+++
title = "The Northbound API- A Big Little Problem"
date = "2012-06-10T03:27:11+00:00"
lastmod = "2012-11-28T04:52:29+00:00"
author = "Brent Salisbury"
wp_id = 967
categories = ["Speculative"]
tags = ["Northbound API", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/the-northbound-api-2/"
aliases = ["/2012/06/the-northbound-api-2/"]
image = "/wp-content/uploads/2012/06/misaligned-bridge-api.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a7a91e795c6a28c775f0b7306bb72422d71b463b16bf3b2f7ddc209f0cc07e50"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

The Northbound API- A Big Little Problem : What is a Northbound API (Application Programming Interface) in SDN? The Northbound API is available on a SDN controller that allows for applications to interact with the controller. The controller in turn, interacts with the network hardware through the OpenFlow protocol to manipulate the flow tables and send instructions to the underlying network substrate. I am going to call that the Southbound API. The controller appears to be the glue at the center of the SDN paradigm. While crucial in the incubation period we are in, I think in the long run it will be just another resource pool we scale up and out, similar to what we have in the x86 compute construct. The following are three fundamentals if I were to rank what I need from an OpenFlow controller.
<h2 style="text-align: left;"><span style="text-align: left;">SDN Components</span></h2>
<ol class="legacy-numbers">
<ol>
	<li>Push a data path to the network hardware substrate based on match + action + count rules into a switch's flow tables via OpenFlow protocol.</li>
	<li>Expose a "Southbound API" for networking devices to integrate into the ecosystem.</li>
	<li>Expose a "Northbound API" for applications to attach to the ecosystem.</li>
</ol></ol>
<div><a href="{{< relurl "/wp-content/uploads/2012/06/SDN-API1.jpg" >}}"><img class="size-full wp-image-944 aligncenter" title="SDN openflow API northbound southbound" src="{{< relurl "/wp-content/uploads/2012/06/SDN-API1.jpg" >}}" alt="SDN openflow API northbound southbound proper abstraction" width="366" height="390" /></a></div>
<strong>Figure 2.</strong> The API degrees

<hr />

<h2>SDN Disruption Timing is Important</h2>
The API’s today for the two most active OpenFlow controller projects judging from the cobwebs on some of the sites are NOX/POX and Floodlight. No surprise that NOX is from the Nacira camp and Floodlight is from the BigSwitch camp, the two startups that have evolved out of Stanford and SDN. Both have incredibly talented people.  Of the two controllers, the Floodlight API is my head and shoulders above preferred of the two. The FloodLight JSON/REST API provides an easily readable HTTP GET,POST, DELETE style actions. I think that a fairly abstracted API is important if traditional engineers are to be comfortable with what is going on under the hood in provisioning and troubleshooting. Especially, if they are in networking because they are not fans of endless hours of grinding out crappy code, in my case. As far as the NOX API, Google around and see if you can find it..

Art Fewell in an <a href="http://goo.gl/Kvou6" target="_blank">interview</a> asked Martin Casado about this last year at the fall ONS. Martin is one of the parents of OpenFlow, the creator of OpenvSwtich and in my opinion from my interactions with him is one of the biggest believers in the community aspect that is so lacking in R&amp;E. It is not only his intellect but probably more importantly his ego profile that has him on the frontlines of so many groundbreaking projects (sorry being a network fan boy).
<blockquote>
<p class="textbox">"My personal opinion is that we need to stay very, very focused on one layer right now. I’d be very interested in seeing OpenFlow coming out, having general support in hardware, having multivendor support, having a good ecosystem on products that use it. Even though this comes up all the time, I think we should all focus on one piece of the puzzle. That said, clearly, you do want kind of a higher way of interacting with the network. But it’s not clear to me that this is a northbound API, it’s not clear to me that this is something that sits on top of a network operating system; it’s not clear to me how this will look. This is so totally embryonic. I view OpenFlow almost as a BIOS. It’s kind of a nice independent way of talking to the hardware, and that’s it. And I think if we just get this accomplished, we’ve done a great thing, and then the rest will follow." -Martin Casado</p>
</blockquote>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/06/SDN-Abstraction.jpg" >}}"><img class="size-full wp-image-946 aligncenter" title="SDN-Abstraction" src="{{< relurl "/wp-content/uploads/2012/06/SDN-Abstraction.jpg" >}}" alt="" width="459" height="317" /></a></p>

<blockquote> <strong>Figure 3.</strong> It is starting to look a little more like proven benefits from abstracted architectures.</blockquote>

<hr />

<h4>My 2 Pennies Worth</h4>
The sooner we get some coherent coalescence around the Northbound API the sooner the magical apps and the multi-billion dollar industry can begin. If the community cannot come up with something well defined, open and flexible without being overly complex. I am not optimistic that the research and education community is capable of doing so with how fragmented R&amp;E feels at times. I don't expect Cisco and Juniper to collaborate together to produce a vision together just as I don't expect to siloed institutions to do that either. The individual or institutional glory will always trump giving away ideas collaboratively unfortunately. I expect a vendor to fill that void rather quickly.

This coming week we have Cisco Live US (<a href="{{< relurl "/2012/06/cisco-networkers-live-clus-or-whatever-we-call-it-now-sdn-predictions/" >}}" target="_blank">my predictions add yours!</a>) and Interop Japan, in which I expect to hear aggressive announcements around SDN. That said I have told all vendors I do not want to know anything NDA regarding SDN. Telling me something being planned that may give hope to our broken networking OAM and then telling me I can’t discuss it with anyone but them pisses me off most the time. It’s more fun to guess at how this gets bungled or embraced by the big shops. I am excited to see the big players in the industry to get involved. They will not sit on the Northbound API for long because that is the crown jewels. Hopefully it will get the community what they need or consolidate on something like the RESTful/JSON API already defined from some. , stable API roadmaps to begin developing the truly revolutionary layer of SDN which is the applications.

<hr />