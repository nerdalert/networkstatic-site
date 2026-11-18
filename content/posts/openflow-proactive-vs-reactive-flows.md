+++
title = "OpenFlow: Proactive vs Reactive Flows"
date = "2013-01-15T06:50:19+00:00"
lastmod = "2014-02-18T03:00:58+00:00"
author = "Brent Salisbury"
wp_id = 5421
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/openflow-proactive-vs-reactive-flows/"
image = "/wp-content/uploads/2013/01/bad-decision1.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "48223477799f0892849ec713df48e7f6027bcc54ee183db3be46ab8a9695f629"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow: Proactive vs Reactive</h2>
As more people begin entering the Software Defined Networking conversation, there is still only one wire protocol that has a reasonably good chance at becoming the de-facto open SDN southbound messaging standard, OpenFlow. There is quite a bit of debate around whether or not OpenFlow can scale. Most claims that OpenFlow does not scale are probably grounded in misconception. That is not to say we do not have a long way to go, but spending the next 5-10 years debating a hardware abstraction layer would be counterproductive in the face of unmanageable networks, with exponential growth occurring annually. As forwarding abstractions in hardware continue to become more flexible, the scale debate should not be whether OpenFlow can scale as a messaging protocol, but be focused on when and if to use reactive flow based rules as opposed to proactive instantiation.
<h2>Recap of Why OpenFlow is Important</h2>
Today we have switches that operate at L2, routers that operate at L3 and firewalls that operate at L4. Some of those functions are blended together in purpose-built hardware such L3 switches. An access-list is a common function that uses <a href="http://etherealmind.com/tcam-detail-review/" target="_blank">TCAM</a> (ternary content addressable memory) to have the flexibility to match on various layers of a packets L2-L4 headers. That TCAM memory has the ability to match (0), not match(1) (the binary is counterintuitive there) or not care (wildcard). Each field or tuple is searched in parallel all in one clock cycle. So, very quickly and at "line rate" in hardware.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/tcam.png" >}}" alt="OpenFlow TCAM"></figure>
<strong><em>Figure 1</em></strong>. TCAM matching

The simplicity of OpenFlow is it was merely a mechanism to exploit TCAM tables in existing vendor switches in order instantiate whatever flows a programmer wants to push. Now with OpenFlow, one can tell a switch to match on any field and apply an action. For network operators and engineers this is policy based routing, on steroids. We can decouple logic and push a set of flow policy from off board the switch, through a TCP socket, using a structured messaging protocol to describe the policy and flow rules to put in TCAM.
<h2>OpenFlow Proactive vs. Reactive</h2>
When using OpenFlow to populate TCAM in switches there are essentially three modes of operation:
<ol class="legacy-numbers">
<ol>
	<li><em>Reactive flow instantiation</em> - When a new flow comes into the switch, the OpenFlow agent SW on the switch, does a lookup in the flow tables, either in a search ASIC if in hardware or a software flow table in the case of a <a href="http://openvswitch.org" target="_blank">vSwitch</a>. If no match for the flow is found, the switch creates an OFP packet-in packet and fires it off to the controller for instructions. Reactive mode reacts to traffic, consults the OpenFlow controller and creates a rule in the flow table based on the instruction. The problem with reactive is today's hardware has laughable amounts of CPU in it. Think iPhone 5 or PowerPC circa 2001 amount. That little guy then must do a DMA copy to replicate and encapsulate the packet. HW switches outside of NPUs or general purpose CPU vSwitches don't do this over a few thousand packet per second. Most in the hundred and some in the 10's from some rather large expensive chassis.</li>
	<li><em>Proactive flow instantiation</em> - Rather than reacting to a packet, an OpenFlow controller could populate the flow tables ahead of time for all traffic matches that could come into the switch. Think of a typical routing table today. You have longest prefix matching that will match the most granular route to a destination prefix in a <a href="http://en.wikipedia.org/wiki/Trie" target="_blank">prefix tree </a> lookup. By pre-defining all of your flows and actions ahead of time in the switches flow tables, the packet-in event never occurs. The result is all packets are forwarded at line rate, if the flow table is in TCAM, by merely doing a flow lookup in the switches flow tables. That is the same hardware that populates its forwarding tables today from "routing by rumor" in todays routing protocols and "flood and spray" layer2 learning standards. Proactive OpenFlow flow tables eliminates any latency induced by consulting a controller on every flow.</li>
	<li><em>Hybrid flow instantiation</em> - A combination of both would allow for flexibility of reactive for particular sets a granular traffic control that while still preserving low-latency forwarding for the rest of your traffic. Low-latency financial markets operate in the nano seconds, that would not be a good place for reactive forwarding today but granular security in an enterprise would possibly be reasonable if the policy was important.</li>
</ol>
</ol>
<h2>Summary</h2>
There are several proactive flow based products with proprietary protocols that have been around for a while. Hearing arguments that one scales, while OpenFlow doesn't is misleading. Rules in TCAM perform the exact same regardless of the method of instantiation. The majority of early OpenFlow deployments (at least ones I am designing) are going to be almost all proactive combined with granular selections of traffic for specific use cases being reactive. This is not to say there will never be a place for reactive forwarding with solid performance, but I think that will come in the form of embedded systems and more hardware distribution at the edge. All networks are not low-latency trading floors and Hadoop racks in data centers. I cannot tell the difference when I am surfing the Internet on a fully centralized wireless controller, to when I am wired in at 1Gb. The human brain does not register microseconds.

As the disruption that SDN represents to the way we have always done networking continues, those who prefer todays primitives over programmatic abstraction will make claims that SDN, OpenFlow and flow based forwarding doesn't scale. Ask them if the proactive access-lists in their networking hardware TCAM today scale, or if their proactive QOS policies implemented in their networking gears TCAM operate at line rate. OpenFlow is not grounded in reactive flow policy, but a protocol to exploit TCAM tables for programmatic L2-L4 forwarding flexibility, nothing more. The value will be in <a href="{{< relurl "/sdn-openflow-policy-abstractions/" >}}" target="_blank">abstraction layers</a>, services and applications.
<h2>Additional Resources</h2>

<aside class="legacy-callout"><strong>OpenFlow: Design Considerations Series</strong>Part 1 <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">OpenFlow: Proactive vs. Reactive</a>
Part 2 <a href="{{< relurl "/openflow-coarse-vs-fine-flows/" >}}" target="_blank">OpenFlow: Course vs. Fine Flows</a>
Part 3 <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies" >}}" target="_blank">OpenFlow: Hybrid Deployments</a>
Part 4 OpenFlow: SDN Looking Ahead (Pending)</aside>

For additional insight into how the forwarding abstractions are being adjusted to be more than just TCAM take a listen to this podcast with Curt Beckmann of the ONF discuss his work as the chairman of the forwarding abstraction working group (FAWG).

<ul>
	<li>Packet Pushers: <a href="http://packetpushers.net/pq-show-20-open-network-foundation-fawg-update/" target="_blank">PQ Show 20 –Open Network Foundation – FAWG Update</a></li>
</ul>



<hr />

Thanks for stopping by!

<hr />