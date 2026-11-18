+++
title = "Enterprise Wireless and Wired: A Byte is a Byte (Part 2)"
date = "2012-09-07T05:43:48+00:00"
lastmod = "2013-04-12T01:58:55+00:00"
author = "Brent Salisbury"
wp_id = 2495
categories = ["Speculative"]
tags = ["Cisco", "Wireless"]
description = ""
url = "/enterprise-wireless-and-wired-traffic-part2/"
aliases = ["/2012/09/enterprise-wireless-and-wired-traffic-part2", "/2012/09/enterprise-wireless-and-wired-traffic-part2/"]
image = "/wp-content/uploads/2012/08/Enterprise.Wireless.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "f8f266b7e73c0338cadb07986a810cb7440a0fce6e0d70b767ad528a363d7be3"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

Enterprise Wireless and Wired: A Byte is a Byte (Part 2): This is a second post regarding enterprise wireless and why those networks are much more <strong>manageable,</strong> (out of the box) then it's wired network brethren. I have simplified my explanation of why the current path needs adjusting and the <a href="{{< relurl "/2012/05/sdn-business-cases/" >}}" target="_blank">reasons</a> why. Enterprise, Data Center and Service Provider networks all have very different challenges, but we are fairly limited architecturally in how we tackle those unique problems. That said, all have one thing in common, the management <a href="http://etherealmind.com/openflow-software-defined-networking-routing-or-switching/" target="_blank">plane</a>. Traffic rates going through wireless controllers are pretty close and in many cases higher, than wired devices as mobile devices continue to fill our pockets. We are at a crossroads that we are calling software defined networking that can bring networks back into alignment with the rest of the computing world, well, at least the same galaxy.
<h3>Wireless Architecture and Plane Placement</h3>
Most wireless architectures in enterprises today are a centralized control plane (CP), though some are distributed to avoid hairpin traffic especially with remote sites. That begins to fall back into a wide area situation where you are fighting time and space and the inherent latency that accompanies that topology. Heller, Sherwood and McKeown recently published a white paper on found <a href="http://www.stanford.edu/~brandonh/papers/hot21-heller.pdf" target="_blank">here</a>. The advantage of having a centralized management plane (MP) is the ability to capture the <a href="http://www.youtube.com/watch?v=W734gLC9-dw" target="_blank">global view</a> of the network and enable a much more effective (de)provisioning, along with simplified performance monitoring and troubleshooting.
<h3>Enterprise Wireless and Wired: A Byte is a Byte</h3>
Centralized management does not solve policy application problems in many cases (especially multi-vendor interop). To get a bump in the wire, you either drop inline devices or push intelligence to the edge, both of those options have high TCO and associated operational overhead. We apply policy out of the box in wireless networks today because CP and MP are centralized. Centralization does not necessarily mean one box for thousands of devices, it can be segmented and containerized just as the modular networks (e.g. out and up) are to achieve scale and fault domains today. Those distributed domains would then exchange state and topology just like in todays networks. A centralized CP, using the <a href="http://tools.ietf.org/html/rfc5416" target="_blank">CAPWAP RFC 5416</a> (based off LWAPP) tunnels <strong>all</strong> traffic back to a central controller, thus has the ability to apply policy. The most popular protocol today for entertaining a standardized protocol is <a href="https://www.opennetworking.org/about/faqs" target="_blank">OpenFlow</a>. OpenFlow operates by punting the first packet to a controller for a flow to be instantiated into the switch that created the packet in even, <strong>not </strong>the entire flow being forwarded central as it would be in the market share leaders wireless <a href="http://www.cisco.com/en/US/products/ps6302/Products_Sub_Category_Home.html" target="_blank">solution</a>. Match+Action, though s/Action/Instruction/g post v1.0. I am probably beating the point to death, but we are talking similar traffic patterns in the <strong>enterprise </strong>that are being serviced completely centralized with 802.11 networks but I would recommend pads and helmet to suggest that in a room full of experts or worse dinosaur vendors. Enterprise != Data Center != Wide Area while many things are common just as many are different. Time to market has to get better with features, getting out of big brothers headlock is the first step.
<h3>The Question of Performance and Scale</h3>
Here are two examples of 7-day traffic patterns. Figure 1. is a wired uplink from a traditional core to distribution uplink. There are likely 3-5,000 wired ports south of that uplink. Figure 2. is an uplink of a wireless controller block that would have roughly 5-10,000 wireless clients south of it. I see some similarities..
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Average-Wired-Orion.jpg" >}}"><img class=" wp-image-2496 aligncenter" title="Average-Wired-Orion" src="{{< relurl "/wp-content/uploads/2012/09/Average-Wired-Orion.jpg" >}}" alt="traffic of a distribution router" width="571" height="352" /></a></p>
<em>Figure 1.</em> Traffic of an uplink into a distribution block feeding 3-5,000 wired ports.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Wireless-Controller.jpg" >}}"><img class=" wp-image-2497 aligncenter" title="Wireless-Controller" src="{{< relurl "/wp-content/uploads/2012/09/Wireless-Controller.jpg" >}}" alt="wireless controller uplink" width="548" height="312" /></a></p>
<em>Figure 2. </em>Traffic of an uplink into a wireless controller block feeding 5-10,000 wireless clients.

The next post in this three parter is showing growth over three years on a wireless network. The growth is scary fast. We are seeing %100-%200 annual growth as are our peers in the higher education, as multiple networked devices on persons continues to increase.

<aside class="legacy-callout">
<ul>
	<li>Part 1 - <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">Why Enterprise Wireless Got it Right</a></li>
	<li>Part 2 - <a href="{{< relurl "/2012/09/enterprise-wireless-and-wired-traffic-part2/" >}}" target="_blank">A Byte is a Byte</a></li>
	<li>Part 3 - <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">Enterprise 802.11 Wireless Growth</a></li>
</ul>
</aside>