+++
title = "The Control Plane, Data Plane and Forwarding Plane in Networks"
date = "2012-09-27T03:52:40+00:00"
lastmod = "2013-08-31T06:18:24+00:00"
author = "Brent Salisbury"
wp_id = 2875
categories = ["Study Time"]
tags = ["Tutorials"]
description = ""
url = "/the-control-plane-data-plane-and-forwarding-plane-in-networks/"
image = "/wp-content/uploads/2012/09/network-planes.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "35dc54d76a4c5e4e036aab8c872de407b7320661d00f3d55248315c82851496e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The Control Plane, Data Plane and Forwarding Plane in Networks</h2>
The Control Plane, Data Plane and Forwarding Plane in Networks is the heart core DNA in today's networking hardware to move IP packets from A to Z. The Management plane is another vital component but also widely excepted as user to hardware interaction. These planes of operation are the building blocks of the layered architecture that networks have evolved to today. By abstracting data to conform to these constructs is how the Internet works today. If I could rewind a dozen years I would probably have made myself write the concepts of Control, Data and Forwarding planes on the chalkboard a few thousands times rather than spending the first couple of years of my career trying to understand the incredible complexities of networks backwards with a weak foundation.

Working with some interns this week I was walking through these "planes" with them and as I have in the past got to "Data Plane" and "Forwarding Plane". It seems a bit nascent from time to time what the difference, if any is between the forwarding and data plane. I thought it might be helpful to cobble together some definitions from some of my favorite books, a couple of RFCs and some drawings, so I don't have to fumble around every semester with poor explanations. Kicking off with fast path, slow path, BCAM and Trie lookups doesn't do anyone any good. So lets look at some pictures instead. <em>Disclaimer much of this can be semantics which tend to get tedious and boring so, well sorry.</em>
<h2>Control Plane</h2>
The control plane is the component to a router that focuses on how that one individual box interacts with its neighbors with state exchange. The Routing Information (data)Base (RIB) and Label Information Base (LIB) are processed in software and used to populate FIB(forwarding information base) and the LFIB. Vendors can implement these in different fashions on how those tables are partitioned between multiple routing instances. For example, a router has a BGP and OSPF adjacencies, those routing protocols have different algorithms to determine what a chosen path to a network would be. Building  the topology or global view as that particular router sees it from its point of view. That is fairly important to recognize that its "global view" is from its perspective of either the IGP or EGP.
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/junos-tables2.jpg" >}}"><img class="wp-image-2882 aligncenter" title="junos-tables inet.0 inet6.0 inet.3 mpls.0" alt="junos-tables inet.0 inet6.0 inet.3 mpls.0" src="{{< relurl "/wp-content/uploads/2012/09/junos-tables2.jpg" >}}" width="420" height="280" /></a><strong>Figure 1</strong>. Juniper's RIB tables are isolated into well defined groups for each routing instance. This can be helpful if/when you need to import routes from one instances table to another. Another way to think of that is importing or exporting from one MPLS/VPN VRF A to VRF B.</p>
In today's networks we have taken distribution of state to the extreme. For your average router (minus MLAG, Virtual Chassis proprietary technologies etc) every box has the ability to stand alone. A routers control plane may as well be standalone from it's neighbor as if each one is in a separate administrative domain. While link state flooding protocols have administrative awareness through things like areas in ISIS and OSPF or Autonomous Systems (ASN) in BGP policy application is pretty rudimentary at best with such a high level of distribution and low levels of abstraction.

Here is an excerpt from a good read, High Performance Switches and Routers (2011):

<blockquote class="pullquote">The control plane functions include the system configuration, management, and exchange of routing table information. These are performed relatively infrequently. The route controller exchanges the topology information with other routers and constructs a routing table based on a routing protocol, for example, RIP (Routing Information Protocol), OSPF (Open Shortest Path Forwarding), or BGP (Border Gateway Protocol). It can also create a forwarding table for the forwarding engine. Since the control functions are not performed on each arriving individual packet, they do not have a strict speed constraint and are implemented in software in general. <footer><a href="http://www.amazon.com/High-Performance-Switches-Routers-Jonathan/dp/0470053674">High Performance Switches and Routers (2011) Chao &amp; Liu</a></footer></blockquote>

The Control plane feeds the forwarding/data plane with what it needs to create its forwarding tables and updates topology changes as they occur. Those are pretty low even in large networks single to at most I would speculate double digit per second changes. This is the reason the control plane can often be thought of as the "slow path" in legacy route once switch many packet switching architectures. A list of functions performed in traditional routing engines/route processors are the following:




<ul>
	<li>Allocates resources to the forwarding engine/plane.</li>
	<li>Routing state</li>
<li>ARP handling is always processed by general purpose processor located in the routing engine.</li>
	<li>Security functions to secure the control plane access. Telnet, ssh, AAA etc.</li>
	
	<li>Establishes and maintains management sessions, such as Telnet connections</li>
	<li>Routing state to neighboring network elements.</li>
	<li>Vendor and platform specific stacking, clustering, pairing etc.</li>
</ul>


<h2>Data Plane and Forwarding Plane</h2>
I am starting this off with saying I am using data and forwarding planes interchangeably.
<p style="text-align: center;"> <a href="{{< relurl "/wp-content/uploads/2012/09/flow3.jpg" >}}"><img class="aligncenter  wp-image-2885" title="control data lfib fib rib" alt="control data lfib fib rib" src="{{< relurl "/wp-content/uploads/2012/09/flow3.jpg" >}}" width="580" height="597" /></a></p>
<strong><em>Figure 2.</em></strong> The Planes separated and typical packet logic into these information bases.

<a href="{{< relurl "/wp-content/uploads/2012/09/Control-Plane.jpg" >}}"><img class="aligncenter size-full wp-image-2894" title="Control forwarding data Plane" alt="Control forwarding data Plane" src="{{< relurl "/wp-content/uploads/2012/09/Control-Plane.jpg" >}}" width="514" height="343" /></a>

<strong><em>Figure 3</em>.</strong> Lets break the control and data forwarding plane up. Green circle = Control Plane Routing Protocols Purple box = Switches and forwarding data plane.

The data plane is the workhorse of the switching elements in our networks. It has the responsibility of parsing packet headers (or cells, SONET) in high speed search ASICs. It manages QOS, filtering, encapsulations, Queuing, Policing all of the reasons we had and still do in many cases purpose built silicon or custom ASIC designs.

The data/forwarding plane must do those operations in the "Fast Path" to keep up with performance needs in data centers and core networks.  Acheiving that sort of performance is often done with varying compoenets of memory types whether Trie based BCAM, <a href="http://www.sdncentral.com/products-technologies/sdn-openflow-tcam-need-to-know/2012/07/" target="_blank">TCAM</a>, NPU and even FPGA is starting to post impressive numbers. Merchant silicon manufacturers are really starting to key in on programmability of data center commodity switching providing programmability that allows for vendors to differentiate in programmability of that silicon. Arista and Cisco just this past week released new low latency switches with <a href="http://www.networkworld.com/news/2012/091912-arista-262570.html" target="_blank">Arista</a>'s 7150S leveraging the Alta Intel/Fulcrum chipset while Cisco's <a href="http://searchnetworking.techtarget.com/news/2240163640/Cisco-Nexus-3548-and-Arista-7150-Duelling-ultra-low-latency-switches" target="_blank">3358</a> was a custom spun or likely fabless ASIC.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/OVS-Path.jpg" >}}"><img class="aligncenter  wp-image-2883" title="openvswitch control data path plane" alt="openvswitch control data path plane" src="{{< relurl "/wp-content/uploads/2012/09/OVS-Path-1024x430.jpg" >}}" width="614" height="258" /></a></p>
<strong><em>Figure 4</em>.</strong> Slow and Fast path in a software vSwitch (for those that have a Control Plane). In the early days of SDN so far the Control Plane is the special sauce or vendor differentiation.

Fast and Slow path is a pretty reasonable way to look at control and data planes. Control Plane has limited updates to the FIB or LFIB in the case of Label Forwarding (same concepts) while the forwarding plane is looking up prefixes and getting called infinitely more times per second thus the need for very fast search ASICs or similar performance chips.

Forwarding data planes typically come either centralized or distributed. This means the forwaring engine is either centrally located across the ethernet fabric/crossbar or pushed all the way to the edge. The more performance required the more that distributed forwarding is pushed to the edge. How we design networks is merely a <a href="{{< relurl "/ethernet-switch-fabric-cards/" >}}" target="_blank">macro</a> of what is happening on the board.
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/forwarding-engines.jpg" >}}"><img class="aligncenter  wp-image-2884" title="packet forwarding engine centralized decentralized" alt="packet forwarding engine centralized decentralized" src="{{< relurl "/wp-content/uploads/2012/09/forwarding-engines-1024x618.jpg" >}}" width="614" height="371" /></a><strong><em> Figure 5.</em></strong> Centralized and Decentralized Forwarding Engines.</p>
<p style="text-align: left;">Search ASICs and NPU are pushing more towards the edge for greater scale and policy application performance. Sounds awfully familiar to whats happening in wireless <a href="http://www.networkworld.com/news/2012/092612-aruba-wi-fi-262825.html" target="_blank">today</a>. Clearly control(lers) are heading to the edge with intelligence for performance. That said we need to ability to oversubscribe rather than buying unused capacity. That covered in the 2nd part of this post.</p>

<h2>Management Plane</h2>
Telnet, SNMP, SSH, XML, stone tablet and chisel, thats some of how we orchestrate and operate networks today, well except for the <a href="{{< relurl "/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">wireless</a> market. It is pretty simple today. I think that says a lot about the industry right now for that matter. If we get anything out of the next few years it will be simplification of network operations and management from abstraction, orchestration and/or automation. There have been some interesting thoughts and IETF draft submissions lately around the operational plane. One submitted by Martin, Pfaff and crew (read <a href="http://networkheresy.com/2012/09/15/remembering-the-management-plane/" target="_blank">blog</a> or raw <a href="https://datatracker.ietf.org/doc/draft-pfaff-ovsdb-proto/" target="_blank">draft</a>) around OVSDB which looks promising.

<h2 class="legacy-heading">Where Is It All Going?</h2>

Well the question is do we decouple and if so how much? I am going to fork that off to another Part2 blog post because that will be the interesting guessing game. Do we extract the control plane and if so how central or distributed does it need to be. Stay tuned for that in the next few days. In the meantime if you have not watched Ferro describing Control, Data and Management planes on Ivan's site at <a href="http://demo.ipspace.net" target="_blank">http://demo.ipspace.net</a>. It is one of the most articulate lectures I have ever seen on the topic so check it out <a href="http://demo.ipspace.net/get/OpenFlow" target="_blank">here</a>, click the videos tab and it is video 1.

<hr />