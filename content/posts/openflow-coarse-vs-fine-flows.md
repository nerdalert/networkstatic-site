+++
title = "OpenFlow: Coarse vs. Fine Flows"
date = "2013-01-20T06:09:03+00:00"
lastmod = "2014-02-18T03:00:01+00:00"
author = "Brent Salisbury"
wp_id = 5452
categories = ["Speculative", "Study Time"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/openflow-coarse-vs-fine-flows/"
image = "/wp-content/uploads/2013/01/Flow-factory2.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a21ccb1c1ff982f6a82a84d388f4220ad4ed76118029f4c898e97e22985cd39b"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow: Coarse vs. Fine Flows</h2>
OpenFlow: Coarse vs. Fine Flows - This series of posts, is to shed light on some illogicalities surrounding the SDN discussion. I will highlight what I propose, will achieve performance and scale when implementing flow based forwarding designs. Soon these debates, will no longer be conceptual or limited deployments in only the <a href="http://www.extremetech.com/internet/140459-networking-is-getting-better-and-thats-partly-thanks-to-google" target="_blank">hyper-scale</a> networks, as more of us begin real-life implementations. The last post <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">OpenFlow: Proactive vs Reactive Flows</a>, was an attempt to point out some fallacies that OpenFlow performance is weak compared to today's flood, learn, route and filtering methods. After reviewing some  facts that pre-populating flows proactively via OpenFlow into a switches flow table, eliminates the need to punt the first packet of each new flow into a controller. Packet forwarding now takes place at wire speed with L2-L4 policy implemented. The second misnomer, is flow based forwarding does not scale. Bad designs are what do not scale.  In this article, we will examine the second factor in finding performance and scale in initial OpenFlow SDN: coarse vs. fine flow scaling.
<h2>OpenFlow Matching</h2>
OpenFlow allows a off-board x86 server create a TCP socket with the switch in order to exploit TCAM memory, creating flow tables rules for line rate forwarding. Just as today's routers and switches have limited numbers of access-list and QOS policies, the same applies to the number of flow table lines are available. This is especially true with the current OpenFlow enabled hardware since it is being retro fitted to exploit the TCAM that is traditionally used for QOS and access-lists.

The matching of fields in in OpenFlow can either be an explicit match or a wildcard match. A wildcard match means the  switch does not care what the value is in the specified field. An explicit match is a binary match, it matches or doesn't.
<h2>Eye on the Chipset Foundries</h2>
Foundry chipset fabrication is a funnel measured in years, not months. 2013 will bring more capable hardware and more agreement on how flow table abstraction should occur in hardware leading to larger and more flexible flow tables in hardware. Until then, when choosing proactive flow table rules, it will be very important to use appropriately sized rules, so as not to overrun the limited length and width in TCAM flow tables. If you have router today that supports x-number of rules, your don't plan to use x+n when designing the architecture. <em>See the appendix at the bottom of the post for required OpenFlow matching in spec v1.3.</em>
<h2>OOpenFlow: Fine vs Coarse Flow Policy</h2>
Fine or Granular flows mean just as they sound, very precise flow table rules that match on a very specific set of traffic. In traditional IP routed IPv4 prefix driven networks, this would be the equivalent of a /32 host route. Since OpenFlow and SDN networks operate using flow based forwarding it allows for much more granularity then L3 prefixes. Granularity can mean matching specific values in fields ranging across Ethernet (L2-Data), IP (L3-Network), TCP/UDP ports (L4-Transport).

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/OpenFlow-Granular.png" >}}" alt="OpenFlow Granular"></figure>

<em><strong>Figure 1.</strong></em> OpenFlow 10-Tuples Granular Flow Match. This is a fine match since it is looking for one very specific flow. This is early application awareness.
<h2>OpenFlow: Coarse Flows</h2>
Coarse flows, are flow rules that will match a broad set of flows. This is very similar to the concepts of route summarization in layer3 routing. Route summarization and CIDR allowed the Internet to scale to what it is today. Search ASICs would not be able to hold Internet routing tables if all routes in the Internet tables were a /24 prefix. Summarizing Internet routes into coarse prefixes like a /8,/9/10 etc reduces forwarding tables to the 450,000 routes in today's Internet tables, rather than a potential 4,294,967,296 host routes.

One of the fundamental transformation that flow based forwarding presents, is the inclusion of layer4 <a href="{{< relurl "/what-are-ethernet-ip-and-tcp-headers-in-wireshark-captures/" >}}" target="_blank">transport headers</a> as another point to make forwarding match + action logic, being done programmatically. This also adds more possible combinations of forwarding rules which is all the more reason to get our arms around the need for broad course flows that will match the majority of traffic for forwarding. Programmatic policy is vital to manage the enormous combinations that can come from matching 12+ L2-L4 fields.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/OpenFlow-Coarse.png" >}}" alt="OpenFlow Coarse"></figure>

<strong><em>Figure 2</em></strong>. OpenFlow 10-Tuples Coarse Flow Match. This matches a very wide range of flows. This could be even larger networks like /2, /3 that acts very much like default routes today but require very few flow rules. This is how we will deploy SDN on today's limited hardware using proactive flows.

Flow based forwarding through a protocol like OpenFlow, conceptually consolidates functionality of various types of purpose built hardware into a common mechanism. In theory the same methods to push L2-L4 in many cases can be simplified into one instantiation into the flow table(s). That is the fundamental disruption to the networking hardware market that has quite high profit margins on networking kits. Go take a look at the only BU in the black along with services in HP and Dell's quarterly earning, spoiler, networking gear.

<hr />


<ul>
	<li>A quick review of some components L2-L4 components:</li>
</ul>


<ul>
	<li>Layer2 - Switching (VLAN,MAC,src/dest Port) Done is SRAM/DRAM CAM. Cheap fast, exact match lookups on keys. This will begin to be leveraged with OpenFlow for large L2 tables not needing wildcard TCAM lookups.</li>
	<li>Layer2 1/2 - <a href="{{< relurl "/the-best-mpls-lecture-on-the-net/" >}}" target="_blank">Label Switching</a> (Routers, L3 Switches, MPLS, LSP, FEC, LIB, <a href="http://notanothernetworkblog.net/2012/08/02/mpls-vpn-label-basics-the-lib-the-lfib-and-the-ribs/" target="_blank">LFIB</a>)</li>
	<li>Layer3 - Routing (Routers, L3 Switches, VRFs, IPv4 and IPv6 routing)</li>
	<li>Layer4 - UDP/TCP Ports (Typically handled w/ Firewalls)</li>
</ul>

<h4>Summary</h4>
What the point of this series of posts, is to help folks begin understand scale and performance issues that are relevant when talking about software defined networks and OpenFlow specifically. When designing SDN architectures in 2013, we are doing so by exploiting limited resources in the hardware since it was not designed to do flow based forwarding at scale. However, overall those limitations revolve around the number of flow rules, the number of tuples (header fields ex. tcp, mpls label etc) or the combination of matching and rewrites (ex. match vlan10, change to vlan20) that can be done at wire speed.

When someone says centralized control planes do not scale, that is anything but an accurate statement. Those reluctant to open and honest conversations around SDN are looking to protect revenue or comfortable with the "way we have always done it" mentality. Technology like anything else when discussed in absolutes is rarely grounded in facts.

The promise is in the policy abstractions and applications not how we push flow into hardware. Time would be much more well spent in integrating big data and analytics into maximizing efficient network resource allocations and scale for the looming mobile explosion of 25-50 billion IP enabled mobile devices in 2020. Expecting radical change overnight is unrealistic and ill-advised in the uptime at all cost networks being operated today. But waiting for <a href="http://www.theverge.com/2012/3/13/2867569/verizon-lte-network-outages-march" target="_blank">widespread infrastructure failures </a>carries just as much and arguably more risk.

Wether or not we use OpenFlow or MPLS as the wire protocol is religious. The key is the ability to push flows in a conceptually simple manner. Simplicity will lead to uptime and modular scale. Do we wait another five years to figure out how to create the perfect southbound protocol from a <a href="{{< relurl "/sdn-openflow-policy-abstractions/" >}}" target="_blank">policy factory</a> to a forwarding target? I rather hope not, too many more important problems to solve before we get to 50 billion.

As Shenker put it in his Keynote at Ericsson Research,  <a href="http://www.youtube.com/watch?v=WVs7Pc99S7w" target="_blank">An attempt to motivate and clarify Software-Defined Networking (SDN)</a>

<blockquote class="pullquote">"Think of OpenFlow as the x86 instruction set. Is the x86 instruction set the right answer? No, its good enough for what we use it for, then why bother changing. Thats what OpenFlow is. It's the instruction set that we happen to use, but we shouldn't get hung up on getting it exactly right."<footer>Scott Shenker UC Berkely</footer></blockquote>
<h4>Additional Resources</h4>
The rest of this series of articles will be gluing these concepts together into a reference architecture.
<aside class="legacy-callout"><strong>OpenFlow: Design Considerations Series</strong>Part 1 <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">OpenFlow: Proactive vs. Reactive</a>
Part 2 <a href="{{< relurl "/openflow-coarse-vs-fine-flows/" >}}" target="_blank">OpenFlow: Course vs. Fine Flows</a>
Part 3 <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies" >}}" target="_blank">OpenFlow: Hybrid Deployments</a>
Part 4 OpenFlow: SDN Looking Ahead (Pending)</aside>

[
<h4>Appendix: Required Match Fields in OpenFlow Spec v1.3</h4>
<div class="table-scroll"><table>
<table style="border-collapse: collapse; table-layout: fixed; width: 442pt;" width="442" border="0" cellspacing="0" cellpadding="0"><colgroup> <col style="mso-width-source: userset; mso-width-alt: 4565; width: 107pt;" width="107" /> <col style="mso-width-source: userset; mso-width-alt: 14293; width: 335pt;" width="335" /></colgroup>
<tbody>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt; width: 107pt;" width="107" height="15"><a name="delete_table"></a>OXM_OF_IN_PORT</td>
<td style="width: 335pt;" width="335">Ingress port. This may be a physical or switch-defined logical port.</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_ETH_DST</td>
<td>Ethernet source address. Can use arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_ETH_SRC</td>
<td>Ethernet destination address. Can use arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_ETH_TYPE</td>
<td>Ethernet type of the OpenFlow packet payload, after VLAN tags.</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_IP_PROTO</td>
<td>IPv4 or IPv6 protocol number</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_IPV4_SRC</td>
<td>IPv4 source address. Can use subnet mask or arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_IPV4_DST</td>
<td>IPv4 destination address. Can use subnet mask or arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_IPV6_SRC</td>
<td>IPv6 source address. Can use subnet mask or arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_IPV6_DST</td>
<td>IPv6 destination address. Can use subnet mask or arbitrary bitmask</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_TCP_SRC</td>
<td>TCP source port</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_TCP_DST</td>
<td>TCP destination port</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_UDP_SRC</td>
<td>UDP source port</td>
</tr>
<tr style="height: 15.0pt;">
<td style="height: 15.0pt;" height="15">OXM_OF_UDP_DST</td>
<td>UDP destination port</td>
</tr>
</tbody>
</table>
</table></div>

<hr />

Thanks for stopping by.

<hr />