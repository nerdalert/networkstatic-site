+++
title = "OpenFlow: SDN Hybrid Deployment Strategies"
date = "2013-01-21T07:22:27+00:00"
lastmod = "2014-02-18T02:54:11+00:00"
author = "Brent Salisbury"
wp_id = 5477
categories = ["Speculative", "Study Time"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/openflow-sdn-hybrid-deployment-strategies/"
image = "/wp-content/uploads/2013/01/Risk.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "9e2aac39f063e7abb829fee9bb1bbaff7f45b87fe02c6d463635dde4bb586392"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow: SDN Hybrid Deployment Strategies</h2>
This series of posts, has been focused on reviewing some practical OpenFlow SDN deployment strategies. Early SDN, will be hybrid networks and early niche applications to begin understanding how to integrate pockets of SDN, mitigate risks and most importantly understand the technology to properly scale solutions. If you try and put 5,000,000 access-lists into a kit that can only do 2,000 rules, does that mean access-lists do not scale? Or does that mean bad designs do not scale? Risk of network instability and pressure of constant availability, has networking trapped in a less than ideal situation. Absorption of the oncoming onslaught of <a href="http://www.cisco.com/en/US/solutions/collateral/ns341/ns525/ns537/ns705/ns827/white_paper_c11-481360_ns827_Networking_Solutions_White_Paper.html" target="_blank">growth on the horizon</a> along with uptake in cloud adoption will be hit and miss at best.
<h2>3 Key OpenFlow Hurdles</h2>
<ol class="legacy-numbers">
<ol>
	<li><strong>Performance - Pre-Populating Flows:</strong>Pre-populating the flow tables at boot or at policy creation in a proactive manner instead of reacting with packet-in events. The only thing centralized at that point is your management engine, in order to define and push policy and topology awareness to the holistic network.  More on that topic in <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">OpenFlow: Proactive vs. Reactive</a>.</li>
	<li><strong>Scale - Flow Rule Allocations:</strong>Early OpenFlow enabled hardware is limited in the amount of wildcard flow rules to 750-3,000 depending on vendor. Some vendors such as NEC, have external TCAM that supports tens of thousands of rules. Early designs need to take that into account and be judicious if the amount of coarse vs fine flows chosen to pre-populate into flow tables. Peel niche applications or selective traffic with granular flows and drain the rest of the traffic with broad flows. This will make more room for interesting traffic. More on this topic in <a href="{{< relurl "/openflow-coarse-vs-fine-flows/" >}}" target="_blank">OpenFlow: Course vs. Fine Flows</a>.</li>
	<li><strong>Risk - Hybrid Architectures:</strong> A ships in the night strategy is a pretty straightforward approach to new networking architectures.  Hybrid features from the OpenFlow agent on the switch are critical to maintain logical path and process isolation between legacy networks and OpenFlow enabled Vlans, bridges and interfaces. Hybrid path isolation is well understood and documented. That should may be enough risk reduction for many to introduce early use cases of SDN applications or pockets of exploratory test/dev. The rest of this article is focused on the hybrid component.</li>
</ol>
</ol>
<h2>Mitigate Risk and Innovate</h2>
Hybrid deployments are intrinsic to reducing risk. Hybrid networks are not a new concept. Hybrid techniques should be well understood after consolidating many traditionally parallel network services, into a converged architecture. We slowly introduced services like VOIP and wireless along with deploying virtualization overlays with MPLS. New SDN deployments wether tunneled overlays or logical isolations, will be the important first steps  of innovative progress.
<h2>Hybrid SDN Networks: Keys to Unlocking Progress</h2>
The most important thing to begin thinking about SDN enabled networks, is helping colleagues, leadership and community understand that almost all risk can be mitigated by using engineering hybrid native forwarding and SDN enabled forwarding networks. The risk lies in vendor firmware on the SDN enabled switch. Since most of the agents are ported Open vSwitch that should offer some stability. All early OpenFlow enabled gear is sharing forwarding hardware between native and SDN pipelines so any planning needs to incorporate existing configurations, particularly QOS and ACLs.
<h2>8 Hybrid Strategy Considerations</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/Hybrid-OpenFlow-SDN.png" >}}" alt="Openflow SDN Hybrid"></figure>

Figure 1. An example of a simple topology from a post last year on <a href="{{< relurl "/hybrid-sdn-deployments/#!prettyPhoto" >}}" target="_blank">hybrid SDN</a>.

Think modules, those are the building blocks of scale. Some of the following eight points may help develop your modules strategy to integrate into your environment.

<ol class="legacy-numbers">
<ol>
	<li><strong>Hybrid Physical Isolation:</strong> - Parallel networks make little since outside of test/dev, unless it is part of a hardware lifecycle strategy. If replacing some distribution switches it may make sense to do a phased physical deployment. Many MPLS migrations follow this path.</li>
	<li><strong>Hybrid Logical Isolation:</strong> Isolate at the Bridge/Vlan. It is as simple as having a Vlan for the legacy packet forwarding and a Vlan to attach to an OpenFlow controller. Any vendor that does not have this option should be avoided unless you are well ahead of the power curve. Almost all vendors have the ability to operate with a legacy and OF vlan.</li>
	<li><strong>Self-Provisioning Multi-Tenancy: T</strong>he switch can have multiple controllers for early multi-tenancy. If you have one physical topology and desire multiple operators this can be achieved by simple creating two vlans or bridges. On each Vlan A attach it to controller A and on Vlan B attach it to controller B.</li>
	<li><strong>Self-Provisioning Multi-Tenancy (Alt)</strong>: The alternative multi-tenant option is logical "<a href="http://www.openflow.org/wk/index.php/Slicing" target="_blank">slicing</a>" in a single controller (rather than two separate) to allocate tenancies or "slices". Think of this as VRFs. The advantages are similar such as overlapping IPv4 address space but eventually overlap on any tuple. This is not a trivial task being the arbiter of policy and permissions on a single switch much less moving up the stack into controller federations. Controller maturity will lead to consolidated self-provisioning. I don't expect that to be solved anytime soon. Inter-AS forwarding table exposure would likely be horrific. SW APIs make much more sense outside of administrative boundaries.</li>
	<li><strong>Native and SDN Network Redistributions:</strong> This is a very salient topic over the past couple of years. Today we focus on packet routing, SDN tends to revolve around application aware flow forwarding, but how do the two intersect? The answer is, the same way. Controllers will either use static routes that will be transformed into flows to drain out of pockets of SDN or protocols to peer with the legacy networks IGP (e.g. OSPF, RIP, LDP etc). Redistribution from SDN islands will merely have the preferred routes from RIBs pushed into forwarding tables almost identical to how FIBs are produced today.</li>
	<li><strong>Protecting the native Network</strong>: For early testing some vendor are including software and hardware rate-limiting features. These options can offer protection from the native network and act as a governor until a design is fully understood and vetted. Open vSwitch running on hardware also offers QOS mechanisms that can limit traffic on a bridge.</li>
	<li><strong>Full SDN Integration Using Proactive Flows</strong>: Rather than logically Isolating OF and native pipelines in a ships in the night manner, putting all hosts into an OpenFlow Vlan/bridge. Now you can use granular matches for something like traffic steering interesting traffic to a preferred path and let the rest of the traffic match in coarse default pre-populated proactive flows. I would suspect Google did something similar to this in their OpenFlow deployment of data center backhauls, but I have not been privy to any insight.</li>
	<li><strong>Full SDN Integration Using OFP Normal</strong>: The long term goal, may be to fully integrate the SDN and native pipelines. Having flexible handoff between pipelines, would allow for matching in the OF pipeline and then passing the forwarding pipeline for a flow to the non-OF pipeline, or vice versa. The <a href="http://blog.ioshints.info/2012/06/hybrid-openflow-brocade-way.html" target="_blank">Brocade MLX</a> is a good example of this pipeline processing. OpenFlow Normal and Local are described in more detail in the next two sections. These features should be key deliverables for vendors wanting to lead in the OpenFlow space.</li>
</ol>
</ol>
<h2>OpenFlow Normal Actions</h2>
These are critical actions. As multi-table pipelines solidify out of the ONF and particularly the Forwarding Abstraction Working Group <a href="http://packetpushers.net/pq-show-20-open-network-foundation-fawg-update/" target="_blank">(FAWG)</a> in coming weeks, vendors will have good articulations on how to properly implement OF pipelines moving forward. Any vendor not integrating these components, will possibly be limiting the customers flexibility. These are key concepts for RFP/RFI consideration around future hardware.

<blockquote class="pullquote">"Two optional OpenFlow hybrid capabilities per spec v1.3 are hybrid interactions between the OF and Non-OF pipelines. These features are critically important to phased migrations and early use cases. OFP LOCAL: Represents the switch’s local networking stack and its management stack. Can be used as an ingress port or as an output port. The local port enables remote entities to interact with the switch and its network services via the OpenFlow network, rather than via a separate control network. With a suitable set of default flow entries it can be used to implement an in-band controller connection. OFP Optional: NORMAL: Represents the traditional non-OpenFlow pipeline of the switch (see 5.1). Can be used only as an output port and processes the packet using the normal pipeline. If the switch cannot forward packets from the OpenFlow pipeline to the normal pipeline, it must indicate that it does not support this action."<footer>OpenFlow Spec v1.3</footer></blockquote>
<h2>"OpenFlow and Non-OpenFlow Pipelines</h2>
<blockquote class="pullquote">OpenFlow-compliant switches come in two types: OpenFlow-only, and OpenFlow-hybrid. OpenFlow-only switches support only OpenFlow operation, in those switches all packets are processed by the OpenFlow pipeline, and can not be processed otherwise. OpenFlow-hybrid switches support both OpenFlow operation and normal Ethernet switching op- eration, i.e. traditional L2 Ethernet switching, VLAN isolation, L3 routing (IPv4 routing, IPv6 routing...), ACL and QoS processing. Those switches should provide a classification mechanism outside of OpenFlow that routes traffic to either the OpenFlow pipeline or the normal pipeline. For example, a switch may use the VLAN tag or input port of the packet to decide whether to process the packet using one pipeline or the other, or it may direct all packets to the OpenFlow pipeline. This classification mechanism is outside the scope of this specification. An OpenFlow-hybrid switch may also allow a packet to go from the OpenFlow pipeline to the normal pipeline through the NORMAL and FLOOD reserved ports."<footer>OpenFlow Spec v1.3</footer></blockquote>

<h2 class="legacy-heading">Summary</h2>

Focusing on performance, scale and a hybrid integration may be some places to start for those looking to get early testbeds or use cases going. Approaching your vendor and requesting OpenFlow agents or in the case of some early leaders just downloading the OF agents firmware is an easy start that doesn't require any purchases. There are very few vendors anymore, that do not have public or beta OpenFlow code. There are also controllers available in alpha and beta programs from networking vendors. Tell your field account teams what you want and hold them to delivering. If they don't deliver, keep them accountable. For those without hardware, I will link to some software only SDN labs that do not require hardware below.

<aside class="legacy-callout"><strong>OpenFlow: Design Considerations Series</strong>Part 1 <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">OpenFlow: Proactive vs. Reactive</a>
Part 2 <a href="{{< relurl "/openflow-coarse-vs-fine-flows/" >}}" target="_blank">OpenFlow: Course vs. Fine Flows</a>
Part 3 <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies" >}}" target="_blank">OpenFlow: Hybrid Deployments</a>
Part 4 OpenFlow: SDN Looking Ahead (Pending)</aside>

<h2 class="legacy-heading">Additional Resources</h2>

<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank">OpenFlow, Open vSwitch and KVM SDN Lab Installation App</a>.</li>
	<li><a href="http://floodlight.openflowhub.org" target="_blank">FloodLight Tutorials</a>.</li>
	<li><a href="https://openflow.stanford.edu/display/Beacon/Home" target="_blank">Beacon tutorials</a> from David Erickson  are really good, especially if interested in module development.</li>
	<li><a href="https://www.opennetworking.org/images/stories/downloads/specification/openflow-spec-v1.3.0.pdf" target="_blank">OpenFlow Spec v1.3</a> from the <a href="https://www.opennetworking.org" target="_blank">ONF</a>.</li>
</ul>


<hr />

Thanks for stopping by!

<hr />