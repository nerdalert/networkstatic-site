+++
title = "Plexxi Capacity Planning Done Right"
date = "2013-01-06T02:28:25+00:00"
lastmod = "2014-02-10T02:25:25+00:00"
author = "Brent Salisbury"
wp_id = 5354
categories = ["Speculative"]
tags = ["Software Defined Networking"]
description = ""
url = "/plexxi-capacity-planning-done-right/"
image = "/wp-content/uploads/2013/01/optical.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "9c0e221e89fd288d1e4b68b5a74d2c743636ab5a7df34067e0a374a6a2c1ca23"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Plexxi Capacity Planning Done Right</h2>
I try and get a daily dose of at least a few minutes of a PacketPushers podcast to keep up with latest networking products and trends. In <a href="http://packetpushers.net/show-126-plexxi-affinity-networking-with-marten-terpstra-sponsored/" target="_blank">Show 126 Plexxi &amp; Affinity Networking With Marten Terpstra</a> Greg and Ethan meet with Marten Terpstra of Plexxi and dug into the new GA product offering from Plexxi.
<h2>Plexxi Affinity Networking</h2>
Plexxi defines "affinitized traffic" as traffic that matches a proactively installed rule. That rule forwards the data plane traffic based on a <a href="http://www.sdncentral.com/products-technologies/sdn-openflow-tcam-need-to-know/2012/07/" target="_blank">TCAM</a> rule rather than a destination mac address in a MAC address to port Key-&gt;Value mapping. This is different from OpenFlow in how a controller interacts with the switch. In OpenFlow, the first packet of the flow comes into the switch and a packet-in event is created. That event involves the switch encapsulating the first packet of the flows fields/tuples and punts it to the controller. Plexxi focuses on configuration management by pre-populating forwarding/flow tables.
<h2>Broadcom ASICs in the Switch x86 in the controller</h2>
Plexxi uses Broadcom ASICs, presumably the Trident+ or 2 chipset. Flow table scale is still a problem in today's <a href="http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/" target="_blank">merchant silicon</a>. Off the shelf top of rack geared silicon only supports around ~3,000-6,000 wildcard flows. Typical BCAM (binary content addressable memory) is used for example in mac address tables. An example of BCAM logic is a key with a value such as a mac address in a key-&gt;value pair. That key would either match or not match a value (binary). If a frame comes in destined for a mac address it is either in the tables or not. If it is not the switch floods all ports for that destination until it is learned. Ternary CAM can return either a match, a doesn't match or something often referred to as a "don't care bit". The don't care bit is denoted with a wildcard.
<h2>Example of TCAM Flow table Wildcard Matching in SDN </h2>
If I have a simple 4 tuple rule consisting of src_mac, dest_mac, src_ip and dest_ip a flow table could match:
<ol class="legacy-numbers">
<ol>
	<li>src_mac: *</li>
	<li>dest_mac: 00:00:C0:FF:FF:EE</li>
	<li>src_ip: *</li>
	<li>dest_ip: 172.16.1.20</li>
</ol>
</ol>
In that example src_mac and src_ip are wild carded meaning ignore those values and the two source addresses have explicit values. That rule would take up one flow entry in a flow tables. 5,000 flow tables begin draining very quickly considering a single host can have thousands of flows at any given time. presumably, just as in OpenFlow programming and design for scale, coarse flow rules are being installed to large swaths of traffic rather than large amounts of individual flows. This is very similar to access lists in traditional networks.
<h2>Lambda Driven Fabric</h2>
The new twist that Plexxi offers is built in <a href="http://en.wikipedia.org/wiki/Wavelength-division_multiplexing" target="_blank">Wave Division Multiplexing</a> (WDM) Coarse WDM specifically. A simple way of thinking of WDM is passing light through a prism, each color that breaks out is a color or wave with an associated frequency that is measure in nanometers (NM) in space between waves. In traditional chassis along with stackable (virtual and physical) switches control channels are setup for management and FIB or flow table downloads. That is almost always a proprietary encapsulating or messaging. I am assuming Plexxi sets up a lambda or two (if not in a physical ring topology) for controller to switch communications.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/plexxi-sdn.jpg" >}}" alt="Pexxi Network Controller"></figure>

<em>Figure 1. </em>Plexxi Controller Architecture.
<h2>What Plexxi is</h2>

<ul>
	<li>Traffic Engineering on Steroids.</li>
	<li>Affordable physical overlays via lambdas.</li>
	<li>Layer2 Ethernet flooding and learning.</li>
	<li>Capacity planning in the data center with WDM.</li>
	<li>Network management through a proprietary API (RESTful) that will be published. That said there isn't such thing as a "standardized" northbound API today other than the Quantum OpenStack API.</li>
	<li>A bus made up of Ethernet waves.</li>
	<li>One channel/wave/lambda.</li>
	<li>Broadcom ASICs.</li>
</ul>

<h2>What Plexxi isn't</h2>

<ul>
	<li>Reactive forwarding. All flows are proactively installed into TCAM from the controller into the switch.</li>
	<li>Controllers are not involved in the Data Path other than the initial download or update of the switches TCAM proactive flows.</li>
	<li>Layer3 forwarding until Q1. May already be supported, I have an inquiry and will update when I hear back. I have also asked</li>
	<li>L4 port matching but it is roadmapped.</li>
	<li>Does it do L2-L4 header re-writes? Also will find that out and update the post.</li>
	<li>Does the Plexxi logic have any sense of the local/normal FIB pipeline in a hybrid fashion?</li>
</ul>

<h2>My Thoughts</h2>
I had one of those oh duh moments. This is truly bandwidth on demand. Operationally capacity planning is a train wreck today. QOS is unmanageable and unless a highly disciplined agile operations to add capacity as thresholds are exceeded. To add capacity whether scaling out in bundles or scaling up with replacing links not only requires technical efficiency but also budgetary planning.

Photonic switching which is a fancy way of saying lambda switching eliminates the need for O-E-O conversions (O being Optical and E being Electrical). Every time a frame or packet is forwarded in and out of a switch or router feed via optics that conversion takes place. Photonic switching eliminates the conversion which has economic and theoretically performance implications. Since Plexxi plumbs a wave through multiple switch hops in a ring it is an optical path from A to Z. Cabling and 3-tier, 2-tier architectures are all conceptually simplified.

As the cost of optical continues to go down, WDM should continue to be a viable solution for bandwidth scaling in data centers. Optical networking is already pervasive in WAN architectures. Fiber availability continues to become more scarce. NSPs are still relying on fiber builds from the dotcom boom of the 1990's where possible to avoid the CapEx associated with investing in optical infrastructures. Fiber scarcity will continue to increase as mobile back hauls drains availability. NSP CTO types are bullish on SDN. I think what Plexxi is doing in the data center, is a precursor to service providers are looking for out of SDN. It is creating a multi-layer SDN strategy.

Flow based forwarding while conceptually straightforward are not easy to program. There are not piles of reusable code lying around GitHub to implement. It is networking from scratch. The nuances of ARPs, broadcasts, multicasts that need to be dynamically allowed for operations are not trivial. That is a primary reason I lean towards open source or dare I say standardized to pave the way if new abstraction layers are going to be the future.

Plexxi brings something different which is the optical twist. Promises of application awareness is a good vision but I don't see anything from anyone yet that solves the problem at the edge of data classification through analytics. I expect other vendors especially ones that have optical business units are soon to follow. From someone who gets aggravated about saturated links that should never happen but the long funnel of scaling out or up links is often not executed in time I appreciate the simplicity of the approach. I will interested to see if Plexxi stays its current proprietary controller to hardware proactive architecture, *if* vendors loosely agree on a framework and carriers adopt multi-layer SDN strategies that integrate optical, MPLS and IP. That is the beauty of commercial silicon, the differentiation is in software along with the flexibility for vendors to adjust their architectures in software rather than heading to the foundry to re-spin ASICs. Service provider architectures scale and they buy in large volume, that s why I run MPLS in data centers, doh did I say that? :)
<h2>Additional Resources</h2>
More Plexxi Information:

<ul>
	<li><a href="http://packetpushers.net/show-126-plexxi-affinity-networking-with-marten-terpstra-sponsored/" target="_blank">Show 126 – Plexxi &amp; Affinity Networking With Marten Terpstra</a></li>
	<li>Discuss the show at the <a href="http://forum.packetpushers.net/showthread.php/499-Show-126-–-Plexxi-amp-Affinity-Networking-With-Marten-Terpstra-–-Sponsored" target="_blank">Packet Pushers Forum </a></li>
	<li><a href="http://www.networkworld.com/news/2012/120512-plexxi-264789.html" target="_blank">Backed by $48M, startup Plexxi unveils SDN wares</a> - Jim Duffy</li>
	<li><a href="http://www.plexxi.com" target="_blank">Plexxi Website and Whitepapers</a></li>
</ul>


I also recommend a few normal switch deep dive podcasts since they are very similar conceptually.
<ul>
	<li><a href="http://packetpushers.net/show-118-juniper-mx-series-sponsored/" target="_blank">Show 118 – Juniper MX Series </a></li>
	<li><a href="http://packetpushers.net/show-64-catalyst-6500-supervisor-2t-deep-dive-with-cisco-tmes-patrick-warichet-scott-hodgdon/" target="_blank">Show 64 – Catalyst 6500 Supervisor 2T Deep Dive With Cisco TME’s Patrick Warichet + Scott Hodgdon</a></li>
	<li><a href="http://packetpushers.net/pq-show-11-brocade-vdx-8770-technical-deep-dive/" target="_blank">Show 11 – Brocade VDX 8770 – Technical Deep Dive</a></li>
</ul>

Some Related OpenFlow Topics:

<ul>
	<li><a href="http://packetpushers.net/big-switch-networks-demos-big-virtual-switch-big-tap/" target="_blank">Show 128 – Big Switch Networks Demos Big Virtual Switch &amp; Big Tap</a></li>
	<li><a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank">SDN Use Cases for Service Providers (NFV)</a></li>
	<li><a href="http://blog.ioshints.info/2013/01/openflow-review-traditional-network.html" target="_blank">OpenFlow Review: Traditional Network Devices</a>-IosHints</li>
</ul>


<hr />

Thanks for stopping by.

<hr />