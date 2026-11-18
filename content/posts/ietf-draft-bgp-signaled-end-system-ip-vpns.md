+++
title = "IETF Draft - BGP-signaled end-system IP/VPNs Contrail"
date = "2012-09-17T03:28:29+00:00"
lastmod = "2013-10-13T18:53:56+00:00"
author = "Brent Salisbury"
wp_id = 2677
categories = ["Speculative"]
tags = ["Data Centers", "Software Defined Networking"]
description = ""
url = "/ietf-draft-bgp-signaled-end-system-ip-vpns/"
image = "/wp-content/uploads/2012/09/Traffic-Control_02.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "4f0d142ab8563ce7c1d5cbea077e1b88bc9681a030c8569f82024de012c07958"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>IETF Draft - BGP-signaled end-system IP/VPNs Contrail</h2>
There is a new IETF Draft - BGP-signaled end-system IP/VPNs draft-marques-l3vpn-end-system submitted for review. It is quite the whose who on the working group of traditional networking vanguard companies like Cisco, Juniper, Infinera, AT&amp;T labs, Verizon and a new comer to the race Contrail. Contrail is an SDN startup with series A funding at $10Mil. There are some of the best out there heading that way such as Kireeti Kompella from Juniper, Ankur Singla from Aruba (I had Arista typed edited (Oct 10- Thanks Ankur!), Pedro Marques from Google and Harshad Nakil from Cisco.  Rumor is this is a spin-in for Juniper. If you want to go straight to the draft and skip any of this post here is the <a href="http://tools.ietf.org/html/draft-marques-l3vpn-end-system-07" target="_blank">link</a>.

What jumps out on the surface the most is this draft is actually talking to a coherent control plane. I have changed my mind on what it is going on in the draft proposal about 10 times over the past 3 days that I have looked at it so it will probably change again and I am sure I missing about a dozen nuances. It is truly amazing to see how BGP has evolved through extensions to be as relevant today and in the future as ever. 

The problem is at the edge wether orchestration, policy application or scale and this looks to address that issue in software on the next-gen edge which is the hypervisor. The elegance is that instead of saying we are agnostic to what is going on in the underlying network substrate, this incorporates the substrate via widely deployed protocols such as BGP/VPNs today. There is a lot going on in this draft, ALOT. If you aren't quite clear or rusty on how network virtualization works via BGP/VPN/MPLS, I higly recommend this <a href="{{< relurl "/the-best-mpls-lecture-on-the-net/" >}}" target="_blank">Lecture</a> from Prof. Karandikar to prime or refresh the mem alloc, he gives a fantastic lecture.

<h2>draft-marques-l3vpn-end-system</h2>
<blockquote class="pullquote">This document describes how the control plane specified by BGP/MPLS IP VPNs [RFC4364] can be used to provide a network virtualization solution for end-systems that meets the requirements of large scale data-centers. It specifies how the control and forwarding functions of a Provide Edge (PE) device described in [RFC4364] can be separated such that the forwarding function can be implemented in end-systems themselves. The solution is applicable to any encapsulation that can deliver packets across an IP network as a tunneled IP datagram plus a 20-bit label.</blockquote>

<h3>Not Perfect but BGP and VPNs Scale</h3>

Before we dive into the draft, let's take a peak at where we are today from my pov at least. Until policy is pushed to the edge into software, which is nonexistent until it can be orchestrated, there is this central pile of gear applying it somewhere in the network. That can be distributed but now you are still left with a management problem of managing distributed systems with no tools that interop. Not to bore anyone with story time, but I see potential for the policy application problem that is still present today. Last year when designing a data center we leveraged BGP MPLS VPN PEs like we do with about everything anymore, for the requirement of multi-tenancy across three data centers. We have deployed BGP/VPNs in our enterprise for the last 5 years or so to support lots of different business units and compliance such as <a href="{{< relurl "/an-no-brainer-use-case-for-mpls-in-the-enterprise-pci-compliance/" >}}" target="_blank">PCI</a> and HIPAA. 

The ability to have scale, multi-tencny and operational coherency rule out many solutions in the bag of protocols we cobble in todays nework toolkit. The option I fall back too about every time are MPLS/BGP/VPNs <a href="http://tools.ietf.org/html/rfc4364" target="_blank">RFC4364</a>. Vlans, while a component of an MPLS/VPN solution in a data center is only usable south of the PE nodes. Even there you begin to open up risk. Anytime you plug in a layer 2 looped topology you begin relying on Spanning-tree or Multi-Link Aggregation Groups MPLAG(VPC, Virtual Chassis, etc). While those work there are strengths and weaknesses, a couple would be operational complexity introduced and single logical points of failure (e.g. split brain).
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/MPLS.Policy.Application.east_.west_2.jpg" >}}"><img class="aligncenter  wp-image-2737" title="MPLS.Policy.Application.east.west" src="{{< relurl "/wp-content/uploads/2012/09/MPLS.Policy.Application.east_.west_2.jpg" >}}" alt="mpls policy application east west data center" width="567" height="360" /></a></p>
<strong>Figure 1</strong>. No problems here but what happens if one VRF needs to import another VRF?
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/MPLS.Policy.Application1.jpg" >}}"><img class="aligncenter  wp-image-2736" title="MPLS.Policy.Application" src="{{< relurl "/wp-content/uploads/2012/09/MPLS.Policy.Application1.jpg" >}}" alt="MPLS in the data center" width="558" height="357" /></a></p>
<strong>Figure 2.</strong> Hair pin to apply policy in the distribution/aggregation/spine pick your architecture.
<h2>The Policy Application Problem</h2>

<h3>Not Perfect but BGP and VPNs Scale</h3>
The purpose of a "closed user-group" is to provide path isolation between different security zones, tenants, services whatever the use case may be but the net is to push multiple containers over the same physical network. Forget cloud provider data centers for a second and just think of a generic enterprise data center, most of those have at least two security zones, a frontend (DMZ etc) and a backend. The past couple of years we have been talking about 2-tier Clos, <a href="http://bradhedlund.com/2012/01/25/construct-a-leaf-spine-design-with-40g-or-10g-an-observation-in-scaling-the-fabric/" target="_blank">Spine</a> leaf, collapsed or your favorite term to maximize for east west traffic. As the east west traffic has undoubtedly increased from 95% North to close %75 East West what does not fit into this design is policy application. If your A and B endpoints live on two different security zones your east west gets punted north to a central point to have policy applied between zones. Distributing policy to the edge in the hypervisor <a href="http://blog.scottlowe.org/2012/08/17/installing-kvm-and-open-vswitch-on-ubuntu/" target="_blank">vSwitch</a> has become popular but scale and operational consistency for average shops seems a bit elusive from what I have seen so far. Something has to <a href="http://www.siliconloons.com/?p=179" target="_blank">orchestrate</a> resources  well beyond just networking resource pools.


<h3>draft-marques-l3vpn-end-system</h3>

This Proposal describes extending the tried and true MPLS/VPN framework and essentially proposes extending the provider edge (PE) or "VPN Forwarder" to the OS/Hypervisor. That would be the x86 physical server hosting VM instances. If VPN Forwarding cannot be implemented on the end system (aka Hypervisor) "it may be implemented by an externalsystem, typically located as close as possible to the end-system itself" (Top of Rack, another system etc).
<blockquote class="pullquote"><em>End-System Route Server</em> A software application that implements the control plane functionality of a BGP IP VPN PE device and a XMPP server that interacts with VPN Forwarders.
<br>
<em>Virtual Interface</em> An interface in an end-system that is used by a virtual machine or by applications. It performs the role of a CE interface in a BGP IP VPN network.
<br>
<em>VPN Forwarder</em> The forwarding component of a BGP IP VPN PE device. This functionality may be co-located with the virtual interface or implemented by an external device.</blockquote>

Required functions by a VPN forwarder:
<ol class="legacy-numbers">
<ol>
	<li>Support for multiple "Virtual Routing and Forwarding" (VRF) tables.</li>
	<li>VRF route entries map prefixes in the virtual network topology to a next-hop containing a infrastructure IP address and a 20-bit label allocated by the destination Forwarder. The VRF table lookup follows the standard IP lookup (best-match) algorithm.</li>
	<li>Associate an end-system virtual interface with a specific VRF table</li>
	<li>When the the Forwarder is co-located with the end-system, this association is implemented by an internal mechanism. When the Forwarder is external the association is performed using the mac-address of the end-system and a IEEE 802.1Q tag that identifies the virtual interface within the end-system.</li>
	<li>Encapsulate outgoing traffic (end-system to network) according to the result of the VRF lookup.</li>
	<li>Associate incoming packets (network to end-system) to a VRF according to the 20-bit label contained immediately after the GRE header.</li>
</ol>
</ol>
<h3>XMPP Signaling Protocol</h3>

In order for end systems to be aware of what routes are in its VRF based on the policy applied from the router server that meta data needs to be feed in. The protocol proposed is  Extensible Messaging and Presence Protocol (XMPP) that sourced itself out of the Jabber project in the late 90's. It is a client server framework that supports TLS and SASL for crypto. XMPP uses TCP for transport along with an abstraction into HTTP that the client can retrieved and posted via HTTP 'POST' and 'GET' on 80 and 443.

<a href="{{< relurl "/wp-content/uploads/2012/09/l3vpn.draft_.topo_.jpg" >}}"><img class="aligncenter size-full wp-image-2752" title="l3vpn.draft.topo" src="{{< relurl "/wp-content/uploads/2012/09/l3vpn.draft_.topo_.jpg" >}}" alt="sdn bgp data center" width="477" height="293" /></a>

<strong>Figure 3.</strong> XMPP is the signaling protocol between VPN forwarder (Forwarding Plane) and Signaling Gateway (Control Plane) carrying meta data.
<pre class="brush: xml; gutter: false; first-line: 1; highlight: []; html-script: false">  
#Example Snippet from the Draft
&lt;iq type=&#039;set&#039;
       from=&#039;01020304abcd@domain.org&#039;
       to=&#039;network-control.domain.org&#039;
       id=&#039;sub1&#039;&gt;
     &lt;pubsub xmlns=&#039;http://jabber.org/protocol/pubsub&#039;&gt;
       &lt;subscribe node=&#039;vpn-customer-name&#039;/&gt;
     &lt;/pubsub&gt;
   &lt;/iq&gt;</pre>
The request above, instructs the End-System Route Server to start populating the client's VRF table with any routing information that is available for this VPN. The XMPP node 'vpn-customer-name' is assumed to be a collection which is implicitly created by the End-System Route Server. Creation of a virtual interface may precede any IP address becoming active on the interface, as it is the case with VM instantiation.
<blockquote class="pullquote">When an End-System Route Server receives a request to create or modify a VPN route it SHALL generate a BGP VPN route advertisement with the corresponding information.
<br>
It is assumed that the End-System Route Servers have information regarding the mapping between end-system tuple ('system-id', 'vpn-customer-names') and BGP Route Targets used to import and export information from the associated VRFs. This mapping is known via an out-of-band mechanism not specified in this document.
In this solution, the Host OS/Hypervisor in the end-system must participate in the virtual network service. Given an end-system with multiple virtual interfaces, these virtual interfaces must be mapped onto the network by the guest OS such that applications on one virtual interface are not allowed to impersonate another virtual interface.
<br>
When VPN forwarder functionality is implemented by the Host OS/ Hypervisor, intermediate systems in the network do not require any knowledge of the virtual network topology. This can simplify the design and operation of the physical network.</blockquote>

<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/MPLS.VPN_.SDN_.RFC_.shadow.jpg" >}}"><img class="aligncenter  wp-image-2745" title="MPLS.VPN.SDN.RFC" src="{{< relurl "/wp-content/uploads/2012/09/MPLS.VPN_.SDN_.RFC_.shadow.jpg" >}}" alt="BGP-signaled end-system IP/VPNs. draft-marques-l3vpn-end-system-07 " width="593" height="405" /></a></p>
<strong>Figure 4.</strong> My interpretation of what this draft would look like.

<h2>What makes this SDN Overlay Solution unique?</h2>

We have seen quite a few data plane solutions come through. Those L2 excapsulations like <a href="http://blog.ioshints.info/2011/12/vxlan-ip-multicast-openflow-and-control.html" target="_blank">VXLan</a>, <a href="http://blog.ioshints.info/2011/09/nvgre-because-one-standard-just-wouldnt.html" target="_blank">NV-GRE</a> (Ivan does a much better job explaining the nuances than I). Those encapsulations are a part of the puzzle but do not address the control plane. Recently Broadcom anounced support for NV-GRE and VXLan in the very popular StrataXGS Trident II chipset which is the staple of almost all merchant silicon driven <a href="http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/" target="_blank">chipsets</a> (Greg's explanation is a must read if you haven't). I for one am not chomping at the bit to try and gain visibility of L2 overlays in the data center spines, Ps, aggregation etc. That feels like a re-invention of the wheel. If we are going that far why not start over.

This draft is unique in that it actually looks to standardize the control and data/forwarding <a href="http://etherealmind.com/northbound-api-southbound-api-eastnorth-lan-navigation-in-an-openflow-world-and-an-sdn-compass/" target="_blank">plane</a> components. It begins to touch on management aspects or at least a centralized point in the form of route servers as a gateway to policy application if you stuck an API on it. Prior to this draft, all I have seen from the emerging data center SDN arena, the control plane is either nothing, weak answers (multicast) or closed proprietary special sauce solutions such as Nicira (NVP) and IBM (DOVE). The alternative is OpenFlow, but there is a void in <a href="{{< relurl "/the-northbound-api-2/" >}}" target="_blank">northbound</a> applications (too early BigSwitch appears very close) that would be required to manage controllers so far. Again what we do in the data center should begin looking very different from Enterprise and Service Provider. The one thing other than IP that binds the three verticals together is the management promise. Proprietary protcols that create logical instances (MLAG, Multilink Aggregation Groups) or stacking either virtual of physical creating non-blocking fabrics are all wrapped in proprietary hardware, software and APIs. Interop is DOA.

<h2>Control Plane Components</h2>
The heart of the control plane is the Signaling Gateway (Route Server). The VPN forwarder (Hypervisor/End-System) is the forwarding plane. The signaling gateway is an application that sits on a server and interacts with the VPN forwarder via the XMPP signaling protocol described earlier. That passes meta data to identify who and what VRFs you belong to (route target) and interact with. Signalling requests from forwarder to route server via an unspecified out of band connection with the XMPP where upon arrival the signaling gateway consults the RT-Constraint Routing Information Base (RIB). <a href="http://tools.ietf.org/html/rfc4684" target="_blank">RFC4364</a> is specifically referenced for how BGP speakers exchange route target updates.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Control.Plane_.BGP_.Tiers_.jpg" >}}"><img class="size-full wp-image-2750 aligncenter" title="Control.Plane.BGP.Tiers" src="{{< relurl "/wp-content/uploads/2012/09/Control.Plane_.BGP_.Tiers_.jpg" >}}" alt="sdn bgp" width="577" height="427" /></a></p>
<strong>Figure 5.</strong> How it seems to me now, today, likely to change 15 times a day, shiny objects in the mirror may seem shinier.
<blockquote class="pullquote">The functionality present in the BGP IP VPN control plane addresses the requirements specified in the previous section. Specifically, it supports multiple potentially overlapping "groups", regular or "hub and spoke" topologies and the scaling characteristics necessary.
<br>
The BGP IP VPN control plane supports not only the definition of "closed user-groups" (VPNs in its terminology) but also the propagation of inter-VPN traffic policies [<a title="&quot;Dissemination of Flow Specification Rules&quot;" href="http://tools.ietf.org/html/rfc5575" shape="rect">RFC5575</a>]. An application of that mechanism to "end-system" VPNs is presented in [I-D.marques-sdnp-flow-spec].
<br>
Note that the signaling protocol itself is rather agnostic of the encapsulation used on the wire as long as this encapsulation has the ability to carry a 20 bit label.
<br>
Whenever the End-System Route Server receives an XMPP subscription request, it SHALL consult its RT-Constraint Routing Information Base (RIB). If the Route Server does not already have locally originated route for the route target the corresponds to the vpn-name present in the request, it SHALL create one and generate the corresponding BGP route advertisement. This route advertisement should only be withdrawn when there are no more downstream XMPP clients subscribed to the VPN.
<br>
The 32bit route version number defined in the XML schema is advertised into BGP as an Extended community with type TBD.
<br>
End-System Route Servers SHOULD automatically assign a BGP route distinguisher per VPN routing table.</blockquote>

<h3>Summary</h3>
This looks good for a data center solution. I am pretty bias when it comes to  the opportunity of working with legacy gear through BGP IP VPNs which presents a migration path. It is a holistic solution with a blueprint rooted in an open standard based framework rather than just a data plane only solution. Still lingering is the policy application problem, that is a software problem. How does east west traffic within a hypervisor know when and when not to import a host route from one VRF to another without the packet ever hitting the physical substrate and pointing north south. Can that even be done efficiently using L2-4 headers only or will that require deep packet inspection?

There is still plenty of room for differentiation in both hardware and software. The software abstraction and orchestration of both the forwarding and control plane components are still missing. That presents a good chunk of <a href="http://www.enterprisenetworkingplanet.com/datacenter/idc-sdn-a-2-billion-market-by-2016.html" target="_blank">revenue</a> and it should be able to be agnostic and decoupled from the substrate if proper primitives and APIs are present and standardized. If the VRF imports can be part of the ecosystem and be instantiated into the RIB in the signaling gateway as part of the overall data center orchestration then this becomes a compelling framework. Getting the functionality of east west policy application plus a control plane all in a standardized manner is makes it the most interesting thing I read this week. The landscape is still seems far to unstable to start expecting anything north in the form of mature orchestration, but you need a good foundation before the house if you want it to last. I expect big things from Contrail and whoever buys them in the next (X) months. This is a data center solution, not a overall solution. Last time I looked I couldn't find any Hypervisors or vSwitch in communications closets and Gigapops. These are pieces to a puzzle that are do not represent radical change but smart change.

If BGP and MPLS are all that we needed and we were just composing the legos wrong, I will be surprised. This doesn't solve application classification in a simple enough manner for me that a non-networking developer would be able to understand without a decade in networking (I can barely figure it out fwiw). Juniper has become religious over technology much like Cisco is over ASICs. This clearly appears to have their fingerprints of IP, BGP and MPLS (Father, Son and Holy Ghost).