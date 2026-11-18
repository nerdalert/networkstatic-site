+++
title = "HP Announces Their SDN Controller"
date = "2012-10-03T02:05:49+00:00"
lastmod = "2012-11-27T17:13:52+00:00"
author = "Brent Salisbury"
wp_id = 2902
categories = ["Speculative"]
tags = ["HP", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/hp-announces-their-sdn-controller/"
image = "/wp-content/uploads/2012/10/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "be01199d553198232de9fc34e7de1db6f3dabca15de383d701fc2f9ab94e1347"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>HP Announces Their SDN Controller</h3>
Hp announces their SDN controller at Interop: HP is not new to the OpenFlow conversation. HP was one of the first, if not the first networking companies to make their OpenFlow enabled switch firmware agent GA (generally available) in 16 products in 2011 and now up to 24 products in 2012. HP has also long supported the <a href="http://groups.geni.net/geni/wiki/GENIRacksHome" target="_blank">GENI</a> project which is an <a href="http://www.nsf.gov" target="_blank">NSF</a> project to leverage prototyped networks fir research. Likely the most recognized project that from GENI was Flowvisor, which is the concept of slicing and arbitrating networks to create virtualization. Yes, <a href="{{< relurl "/ietf-draft-bgp-signaled-end-system-ip-vpns/" >}}" target="_blank">MPLS/BGP/VPNs</a> do that also, but the difference is an exposed northbound API that allows for self provisioning.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/sdn-agility-hp.jpg" >}}"><img class="size-full wp-image-2911 aligncenter" title="sdn-agility-hp" src="{{< relurl "/wp-content/uploads/2012/10/sdn-agility-hp.jpg" >}}" alt="sdn-agility-hp" width="531" height="321" /></a></p>
<strong>Figure 1.</strong>  Hitting all the high points. Open, Abstract, Standards, Automation, Agility, Dynamic, Orchestration, check. Throw in a "Paradigm" or two and its bingo.

There was <a href="http://blog.ioshints.info/2012/03/grumpy-monday-hp-and-openflow.html" target="_blank">criticism</a> of where HP was going with their strategy which I tended to agree with. Delivering commodity switches but not delivering anything in the form of controller or application was missing the economic promise and void in the market. There is a great deal more margin in software than there is merchant silicon. HP and SDN have the recipes to bring good products to market.

<a href="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Layers.jpg" >}}"><img class="aligncenter size-full wp-image-2912" title="HP-SDN-Layers" src="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Layers.jpg" >}}" alt="HP-SDN-Layers" width="531" height="321" /></a>

<strong>Figure 2.</strong> HP SDN Layers.
<blockquote><span style="font-size: small;">"We(HP) are introducing the industry’s first complete and open-standards-based software-defined network technologies across all three critical SDN layers—infrastructure, control and application layers with a “single control plane” that enables enterprises and cloud providers to simplify and maximize agility across data center, campus and branch networks."</span></blockquote>
<h4>FloodLight OpenFlow Controller Base</h4>
What I have heard is the HP solution is built on top of FloodLight the SDN OpenFlow controller. FloodLight was developed and open sourced by <a href="http://www.bigswitch.com/leadership/" target="_blank">BigSwitch</a> one of the two original SDN venture cap startups in SDN. I am under NDA with HP and most other network vendors but have not talked to anyone at HP about SDN since this summer and then it was hardware focused. Sounds like FloodLight is quickly becoming the de facto base for OpenFlow controllers. While I prefer Python, I am really happy to see an cross platform and modular framework becoming a base for products. I heard a while back IBM was leveraging either FloodLight or BigSwitch in their SDN product. Presumably that could be the Layer3 component to the IBM <a href="http://searchnetworking.techtarget.com/feature/IBM-DOVE-Big-Blue-enters-the-network-virtualization-battleground" target="_blank">DOVE</a> networking strategy. OpenFlow, MPLS some brand new label+meta data, is irrelevant. The promise is decoupling the OS and building proper abstraction layers. Pick something and lets go.
<h3>RESTful API</h3>
The RESTful API calls of the FloodLight and HP's controllers are encouraging. <a href="http://nerdtwilight.wordpress.com/2012/09/18/northbound-api-the-standardization-debate/" target="_blank">Brad</a> and <a href="http://blog.ioshints.info/2012/09/sdn-controller-northbound-api-is.html" target="_blank">Ivan</a> have been writing about what if any uniformness comes from the industry with northbound facing programatic interfaces. We are quickly falling in trace behind OpenStack. It is appropriate since we are easily 5-10 years behind in the x86 market.
<ul>
	<li><a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}" target="_blank">Example</a> of RESTful API calls are at the bottom of this to get an idea of what they look like in a networking context.</li>
	<li><a href="{{< relurl "/floodlight-openflow-controller-screencast-with-hp-switches/" >}}" target="_blank">Example</a> of attaching an HP switch to a FloodLight OpenFlow controller.</li>
</ul>
Another interesting aspect to the HP announcement is bringing a few applications along with it. Jim Duffy had a good <a href="http://www.networkworld.com/news/2012/100212-hp-sdn-262928.html" target="_blank">preview</a> of what HP will be bringing with their SDN strategy in 2013. Security is one of the targeted applications with the product. Exposing forwarding tables allows for flow instantiation natively using layers 2-4. This opens up the ability to leverage switches for much more than mac address forwarding, flooding and storing. Edgy security classification may actually have a prayer to be realistic and not a total kludge like it is with today's 802.1x solutions. It's not a knock on the developers, their hands are tied with a completely inflexible platform to develop on top of.

<a href="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Cloud.jpg" >}}"><img class="aligncenter size-full wp-image-2913" title="HP-SDN-Cloud" src="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Cloud.jpg" >}}" alt="HP-SDN-Cloud" width="531" height="321" /></a>

<strong>Figure 3.</strong> Clearly looking to integrate hybrid cloud options into their OpenStack public cloud.

HP has a large <a href="{{< relurl "/the-hp-public-cloud-and-openstack/" >}}">investment</a> in their public cloud offering. You can bet there will be hooks to facilitate elastic cloud computing.

<a href="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Ecosystem.jpg" >}}"><img class="aligncenter size-full wp-image-2914" title="HP-SDN-Ecosystem" src="{{< relurl "/wp-content/uploads/2012/10/HP-SDN-Ecosystem.jpg" >}}" alt="HP-SDN-Ecosystem" width="531" height="321" /></a>

<strong>Figure 4.</strong> I would be remiss if I didn't write about all things magical here and not say the "E" word. Ecosystem, there I feel better, thanks.

There has been plenty of networking and virtualization vendors going after the Data Center but hardly any articulating a strategy for the Enterprise <a href="{{< relurl "/enterprise-wireless-and-wired-traffic-part2/" >}}" target="_blank">Campus</a> or the Service Provider space. There will hopefully be a day that we see solutions a bit more tailored to the problems needing to be solved that is something better than a particular combination of protocols. When we run out of scale or have new needs the answer is always another protocol.
<h4>Not Just the Data Center</h4>
HP appears to be having two product offerings. One will be for the data center and the other will be for the enterprise campus. HP was vital in creating the competition and reducing <a href="http://www.networkworld.com/community/blog/will-cisco-ever-regain-those-switching-margin" target="_blank">margins</a> in the edge switch market over the past couple of years. HP was indirectly responsible for entire product lines from incumbents, such as the Cisco Catalyst 2960 that was introduced as a low cost access closet switch and provided lifetime software upgrades for free after losing a few big deals to HP. HP has a deep background in software and obviously they see the opportunity to capitalize on that base. The stakes are even higher now for companies to commit or be left behind.
<h4>Good to be Ahead of the Curve</h4>
This is another brick in the path to networking horizontalization from a huge company with a deep bench. The road will be littered with the indecisive, risk adverse and arrogant. I expected Dell and HP to take a wait and see approach, I was wrong on the HP front. I still think Dell will buy BigSwitch, but I also thought they were going to buy Brocade but the bought Force10, oops. Good to see folks thinking about SDN solutions other than the Data Center since apparently the world is not made up of HyperScale cloud and content providers, shocking!

&nbsp;