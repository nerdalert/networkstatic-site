+++
title = "Ethernet Switch Fabric Cards"
date = "2012-06-01T06:23:34+00:00"
lastmod = "2012-09-27T02:49:19+00:00"
author = "Brent Salisbury"
wp_id = 789
categories = ["Study Time"]
tags = ["ethernet"]
description = ""
url = "/ethernet-switch-fabric-cards/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "13ef5fc307ca67212d696ee1126358a1b14326602f8ac771ee69b91494482e2f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

I was working with a buddy today about ethernet switch fabric cards in the nexus 7000 and not doing a very good job at explaining it, so I figured I would draw some pictures. The conversation was around how adding more fabric cards increases the bandwidth. I think some, myself included growing up on Catalyst 6500's got accustomed to a single stage architecture which in the case of the ASR 9000 and similarly the  Sup 7200 and newer, have the switch fabric living on the route processor (RP), routing engine (RE juniper) or supervisor (sup Cat 6500). Chip, ASIC, fabric hardware developers are tackling the same problems in silicon design that we as network engineers/architects tackle  in macro engineering network design. Its all modularity the building blocks of scale and abstraction.

I was comparing the Nexus 7000 to the ASR 9000. The ASR is single stage The Nexus 7000 is a typical three stage Clos fabric (figure 2) meaning it interconnects three separate crossbar (figure 1) fabrics together.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/crossbar.jpg"><img class="alignleft size-full wp-image-790" title="crossbar" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/crossbar.jpg" alt="" width="206" height="198" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em><strong>Figure 1.</strong> Crossbar Fabric</em>

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/3-stage-clos.jpg"><img class="alignleft size-full wp-image-791" title="3-stage-clos" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/3-stage-clos.jpg" alt="" width="383" height="198" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em><strong>Figure 2.</strong> Three Stage Clos Fabric</em>

The interesting thing is as we find better ways to try and improve and cut coherent network architectures often times we do not need to look any further than the actual silicon under the hood.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/leaf-spine.jpg"><img class="alignleft size-full wp-image-792" title="leaf-spine" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/06/leaf-spine.jpg" alt="" width="383" height="198" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em><strong>Figure 3</strong>. Spine Leaf Data Center Design.</em>

I do not have time to do this post much justice there are dozens of models such as Banyan, Batcher, Benes and so on and the interactions buffering, memory logic, arbitration, queuing all being orchestrated in a multiplexed fashion at light speed that is hard to wrap ones head around. The basic understanding of whats under the hood can be applied in scaling how we put these things together in a pile and plug them into one another.

I will be working on some material soon, as I try and guess/understand upcoming changes in our hardware on the horizon and in all reality commoditization is already happening. In some cases I think we are trying to tackle software problems in hardware. Thanks goodness Moore's law is theoretically hanging on by a thread which maybe get is to an inflection point soon. Hell that is highly debatable but what isn't.

A fantastic fabric post by Ferro can be found <a title="here" href="http://etherealmind.com/what-is-the-definition-of-switch-fabric/" target="_blank">here</a>

One of my favorite books ever. I recommend to everyone except probably my mom is: <a title="Network Processors: Architecture, Programming, and Implementation (Systems on Silicon)" href="http://www.amazon.com/Network-Processors-Architecture-Programming-Implementation/dp/0123708915" target="_blank">Network Processors: Architecture, Programming, and Implementation (Systems on Silicon)</a>