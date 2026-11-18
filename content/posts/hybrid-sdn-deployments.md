+++
title = "Hybrid SDN Deployments"
date = "2012-10-19T02:01:09+00:00"
lastmod = "2013-01-02T23:08:35+00:00"
author = "Brent Salisbury"
wp_id = 3246
categories = ["In the Lab"]
tags = ["Software Defined Networking"]
description = ""
url = "/hybrid-sdn-deployments/"
image = "/wp-content/uploads/2012/10/sdn-naming.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "22292389c9d3905b50f6ceec13f6f3d194766b0153f1db0c43d03c8dec9009a6"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Hybrid SDN Deployments</h2>
The concept of a hybrid SDN deployments using and interacting with legacy networks has come up quite a bit recently in the industry. This idea that a rip and replace or physical overlay network in order to evolve networks in some cases is not often grounded in fact. When we replaced Token ring, ATM and before my time Decnet/Thinnet those were absolutely hardware forklifts because we were gutting everything from framing/cells/tokens down. When we joyously ripped protocols like IPX and AppleTalk we did not need to replace hardware since those were encapsulations on top of ethernet. Look at standalone wireless to wired deployments, all achievable.

The point is, existing investments are protected to some degree. There is risk involved with anything, so measure it. When someone takes on an MPLS  migration on their network that can be done with a new batch of seed gear to slowly migrate to or it can be done in a hybrid fashion and isolate traffic logically. Both are equally relevant the difference is tolerance for risk based on the software a vendor provides for it's network elements. I will go through a couple of options and logical topologies.

<h2 class="legacy-heading">We Have Evolved Before</h2>

Since any software defined network (SDN) strategy being discussed today is grounded in Ethernet and IP (other than optical conversations of course) has some ability to be leveraged by existing hardware in a dual purpose fashion when/if the vendor starts shipping an agent to support the mechanism. This is all assuming it is gear relatively new and if the vendor decides to support it. <a href="http://www.sdncentral.com/products-technologies/sdn-openflow-tcam-need-to-know/2012/07/" target="_blank">Hardware</a> certainly will play a big role as we wait and see the direction vendors gamble on. We are starting to see hardware that is flexible enough to support traditional IP pipelines and hardware that can support OpenFlow <a href="http://blog.ioshints.info/2012/05/brocade-yet-another-sdn-strategy.html" target="_blank">pipelines</a>.

Let me also disclaim that I do understand that SDN does not equal != OpenFlow, got it. I am all ears to hear the <a href="{{< relurl "/ietf-draft-bgp-signaled-end-system-ip-vpns/" >}}" target="_blank">alternatives</a>. As Scott Shanker pointed out in a great talk OpenFlow is not the right answer but it is probably a good place to start and compared it the infamous x86 instruction set, it is far from the best but it is a primitive that is good enough for now. It doesn't matter to me, use tags and for that matter in the Service Provider <a href="{{< relurl "/new-ietf-sdn-drafts/" >}}" target="_blank">Alto/CPE</a> plays probably make the most sense anyways.

SP, Ent and DC all have very different problems yet all related by disproportionate support and exponential growth being absorbed while managing the networks in the same manner as we did 15 years ago. The key is abstraction and programmability via primitives not the wire protocols.
<h2>We got SDN Hardware, Now What?</h2>
Ok great, so now what do we do if we get hardware and want find use cases? Well we have some primitive mechanisms for data plane and control plane path isolation today.

Data Plane- Vlans, we all use them, some of us far too much. From a building distribution (BDF) down you can easily have an SDN Vlan along with your regular Vlan. I can't imagine very many switch vendors will go too far build OpenFlow only switches. Some want that but I think there is a great deal of proofing and maturity that needs to happen to see if OpenFlow or any other decoupled control plane is the right way to go. Don't take away the old tool but give us new ones that can support new frameworks.
<h2>SDN Data Plane Isolation</h2>
The diagram is pretty simple. A Vlan for OpenFlow and regular Vlans for the legacy network. This example is Layer2 only. The default gateway will still be a routed interface on your upstream router. The controller will learn mac addresses via flooding just as a Layer2 learning switch. It does give you the ability to rewrite headers and manipulate traffic and header policy. Depending on the controller would be the deciding factor on whether to change something like the next hop address or answer arps in the controller software to do more advanced things like path isolation between tenants in the same broadcast domain. See the OpenStack Quantum diagram at the bottom of the post as an example.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/Hybrid-Openflow.jpg" >}}" alt="Openflow SDN Hybrid"></figure>

<strong>Figure 1.</strong> L2 isolation, the Layer3 gateway is still just a regular router.</a>

 Basic L2 learning simple start. Start with building isolated Vlans and attach them to a controller running L2 learning and forwarding only. Another option is proofing SDN scenarios in <a href="{{< relurl "/how-to-build-an-sdn-lab-without-needing-openflow-hardware/" >}}" target="_blank">software only</a>.

<h2>Control Plane Isolation</h2>
This is a bit trickier depending on what you want to do. If it is scale pockets of SDN over a backbone it is pretty easy. Use a layer3 path isolation technique like BGP/VPNs, VRFs, Tags, Pseudowires etc. The concept of the controller being a route redistribution point can be tricky to conceptualize. Just think of it as a redistribution point between native to magical.
<ol class="legacy-numbers">

<ol>
	<li>The first way to do this would be just extending your SDN network into a VRF and let that interconnect differnt pockets of SDN modules hanging off your backbone. The controller does not need to be aware of the legacy network RIBs, you just need a gateway or two to point a default route or super-netted to avoid garbage collection by the controller with a 0/0 route.</li>
	<li>Have the controller peer to the native IGP/iBGP/MPLS domains. That is trickier, I would guess most vendors and even a Google or two as described a while back with the LSR aware Quagga unshrouding in 2010 at <a href="http://www.nanog.org/meetings/nanog50/abstracts.php?pt=MTYzNSZuYW5vZzUw&nm=nanog50" target="_blank">Nanog</a>. For now I the abilities being made available minus this are still mind bending over what we can do by programmaticly instantiating our flows into hardware.</li>
</ol>
</ol>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/10/hybrid-sdn-scale.jpg" >}}" alt="SDN Hybrid Control and Data Plane"></figure>

<strong>Figure 2.</strong> Either scale out further by tying the islands together with an overlay at L2 w/VPLS, PW,Vlans or at L3 with VRFs,BGP/VPNs.
<h2>Hybrid SDN Deployments Summary</h2>
With the Data Plane implementation I have all I need to make the DNS mapping to policy -&gt; flow <a href="{{< relurl "/sdn-using-dns-naming-for-classification/" >}}" target="_blank">project</a> a couple of interns and I are writing. I can say match X and send it out port Y based on this policy.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/SDN-Path-Steering.jpg" >}}" alt="SDN Named Path Steering"></figure>

<strong>Figure 3</strong>. Data Plane isolation offers plenty of opportunity just by itself especially in the data center.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/SDN-Quantum.jpg" >}}" alt="SDN Quantum"></figure>

<strong>Figure 4.</strong> Some are already leveraging the same concepts in OpenStack <a href="https://github.com/openstack/quantum/tree/master/quantum/plugins" target="_blank">Quantum</a> and may not realize it. The only difference is the edge is the hypervisor instead of a HW switch.

<hr>
Either way we do have some tools in use today that allow for us to build hybrid networks without buying testbeds or throwing away existing investments in some cases. There is obvious risk in software bugs, but I happen to be working one nasty little bug at the moment and it has nothing to do the Unicorn next generation networks and everything to do with too many protocols for software developers to keep up with delivering and vetting properly.

<hr />

Thanks for stopping by.

<hr />