+++
title = "Putting Together Provider Bridging, Provider Backbone Bridging, S-Tags and C-Tags"
date = "2013-03-03T04:38:13+00:00"
lastmod = "2014-02-18T02:56:59+00:00"
author = "Brent Salisbury"
wp_id = 5866
categories = ["Study Time"]
tags = ["Service Provider"]
description = ""
url = "/putting-together-provider-bridging-provider-backbone-bridging-s-tags-and-c-tags/"
image = "/wp-content/uploads/2013/03/PBB1.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a1cf0597f98a46482c00fa62bbc4cfd0226255f551f9ea6999b491d5083cec8a"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Putting Together Provider Bridging, Provider Backbone Bridging, S-Tags and C-Tags</h2>
Putting Together Provider Bridging, Provider Backbone Bridging, S-Tags and C-Tags: Understanding carrier bridging techniques is important, not just for provider operators, but also for engineers on the customer edge. When turning up or troubleshooting a circuit, carrier operators will ramble off C-tag and S-tag when many in the enterprise, are used to hearing Vlan ID in single tenancy deployments. More customers are transitioning to L2 circuits from carriers, to cut out carrier L3 routing that is often a complete nightmare to troubleshoot between carrier and customer. Provider bridging (QinQ) and provider backbone bridging (MAC-in-MAC) can be conceptually viewed as the layer 2 equivalent of virtual route forwarding (VRF-lite). These technologies can be signaled via MPLS. L3/VPNs have some advantages, when it comes to draining spoke sites to the Internet by reducing hub to spoke traffic. That said, most organizations drain traffic to the hub sites for policy application. This is a review of one of many ways providers carry L2 customer bridges, as less customers are willing to deal with the headache of having carriers route their traffic. Provider bridging can give the customer a dark fiber experience, which in turn, reduces OpEx to carrier and customer.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/PBB.png" >}}" alt="Provider Bridging 802.1ad"></figure>

<h2>Provider Bridging 802.1ad</h2>
Provider bridging is conceptually pretty simple, vlan stacking or QinQ (802.1Q in 802.1Q). The customer traffic is identified by a Vlan ID (VID) referred to as the C-tag (customer VID) in the 802.1Q framing format. When the C-tagged frame goes upstream to the service provider, it is encapsulated again by the carriers provider bridging edge network. Using 802.1ad encapsulation, the C-tag is then wrapped up with an S-tag (Service VID). Encapsulation in the carrier network allows for overlapping customer VIDs.
<h2>Provider Backbone Bridging 802.1ah </h2>
Just as customer VIDs need to be masked off from one another to avoid overlap, so does the carrier. Provider Backbone Bridging is also reffered to as MAC in MAC since depending on the scenario, there can be up to 5 Ethertypes doing encapsulation. Some carriers require well over 4094 Vlan IDs to support circuits. Provider Backbone Bridging or MAC-in-MAC (802.1ah) allows for overlapping of S-Tag VIDs, while provider bridging or QinQ (802.1ad) allows for overlapping C-tags. MAC-in-MAC is backwards compatible with QinQ, as they are both tightly coupled to one another. The process is very similar to L3 VPN/VRFs and RFC1918 IPv4 addresses and path isolation for the customer and virtualization of the carrier network to oversubscribe for slicing. Both QinQ and provider backbone bridging are addressed in <a href="https://www.opennetworking.org/images/stories/downloads/specification/openflow-spec-v1.3.0.pdf" target="_blank">OpenFlow v1.3</a> spec.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/PBB-Topology.png" >}}" alt="Provider Backbone Bridging"></figure>

Provider bridging can be designed in a hierarchal fashion to add scale and reduce complexity.
<h2>Additional Reading</h2>
The details are pretty deep on Provider Backbone Bridging but most vendors configurations abstract most of the nuances. In the end, just think of each layer needing a distinct value to key on, to avoid overlap and scale issues. The wikis do a nice job summarizing both 802.1ad and 802.1ah. There are various methods of extending L2 service and virtualization for customers and tenants over your network, this is just one mechanism, right, wrong or stupid. What I do highly recommend is, if you are receiving L3/VPN services from your carrier, make sure you have a good business case for doing so.  Final note, the IEEE is a joke for still charging to review their documents. Some day these will be open source problems, as standards bodies have lost their minds in hubris.


<ul>
	<li><a href="http://en.wikipedia.org/wiki/Provider_Bridge_Network" target="_blank">Provider Bridging 802.1ad</a></li>
	<li><a href="http://en.wikipedia.org/wiki/IEEE_802.1ah-2008" target="_blank">Provider Backbone Bridging 802.1ah</a></li>
</ul>

<hr>
Thanks for stopping by