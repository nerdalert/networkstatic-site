+++
title = "SDN Product Rundown from September"
date = "2013-09-22T19:57:20+00:00"
lastmod = "2013-09-22T19:57:20+00:00"
author = "Brent Salisbury"
wp_id = 6885
categories = ["Speculative"]
tags = []
description = ""
url = "/sdn-product-rundown-september/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "34978f95928a35c5793410a206977f1750f5ba433088310a7c84b80dd04da62f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN Product Rundown from September </h2>
What an exciting time to be in networking. This past month of September has been a blur of SDN product announcements and emerging strategies. At the top of the heap was the <a href="http://www.networkcomputing.com/next-generation-data-center/commentary/networking/inside-vmware-nsx/240161109" target="_blank">NSX</a> announcement from a software company in Vmware that encapsulated Nicira's SDN push. I am an unabashed Casado fan boy so whatevers. Humility and genius is lightning striking twice. The blinders are off and now there is a steady pipeline of fantastic ideas (both new and old) that are starting to gain traction from software and hardware startups and even incumbent hardware vendors. I had the honor of spending the week with friends from Network Field Day and SDNCentral to debate product, architectures and the futures of networking.

<h2>Harnessing Data with Plexxi</h2>

First up is <a href="{{< relurl "/plexxi-capacity-planning-done-right/" >}}" target="_blank">Plexxi networks</a>. The exciting aspect of Plexxi has always been data driven analytics. There is an unbelievable amount of data from networking, storage and compute that goes to waste in our data centers. Ultimately we can have all of the mechanisms to provision and control the network, but if we cannot extract, relate and present the data in a functional manner it is still an operation hand crank. Mutating the network based on predictive or realtime data analysis will not get the glares and eye rolls in the room that it used to.

Take a look at the Plexxi recording and see what <a href="https://twitter.com/cloudtoad" target="_blank">@cloudtoad</a> and gang are brewing.

<p><a href="{{< relurl "/wp-content/uploads/2013/09/sdncentral-v3.pptx" >}}">Download the document</a></p>

<a href="http://techfieldday.com/appearance/plexxi-presents-at-networking-field-day-6/" target="_blank" rel="noopener noreferrer">Plexxi at NFD#6</a>


<h2>SwitchLight and Open Systems</h2>
If you told a sysadmin that he needs to buy a particular OEMs server hardware in order to run Microsoft Exchange, he would laugh you out of the data center. Not networking though, hardware is akin to a Mac laptop or last remnants of P-Series hardware. There is not enough value in switch firmware to sustain this model but it will take time and silicon abstraction. I have written extensively on BigSwitch over the past few years. They have retooled a bit into something I am quite excited about with their SwitchLight OS. It is essentially Linux with Broadcom 3rd party drivers on commodity switches. There is another startup with a similar approach named Cumulus (if reading, still waiting on kit, ehem). There is plenty of room here particularly if some snatches up Cumulus which seems likely. Monetization comes in the form of subscription software updates.

Up the stack BSN seems to be focusing on the application rather then the platform these days which is probably a good move. BSN is still focused on the hard but important task of controlling all traffic, not just overlay. I will always like the idea of only traffic I want to forward in a data center to forward. That is the longterm path to reducing the fragility of Ethernet DCs. I had a chance to speak with Prashant Gandhi after the session and I like what he is doing now that he is at BigSwitch from Cisco.

<p><a href="{{< relurl "/wp-content/uploads/2013/09/BSN-NFD6.pdf" >}}">Download the document</a></p>

<a href="http://www.bigswitch.com/products/switch-light" target="_blank" rel="noopener noreferrer">Check Out The SwitchLight Project</a>


<h2>Carrier SDN with Nuage</h2>
Nuage is a spin-in for Alcatel/Lucent. I normally zone out during demos, I didn't during theirs as they demoed OpenStack integration with their platform. The target customer for Nuage are carrier clouds that have existing MPLS networks. It is attractive for tenant isolation to extend from the PE down with MPLS distinguishers. I was impressed with the product. It will be interesting to see of the parent company with hardware DNA can execute this. I would like to see their functionality brought to an OpenDaylight platform, ideally by them. Reason being, I dont think there is very much room in the platform space. The kernel wars made that apparent. Value is the app not the platform. I know I would have little tolerance for interop issues with single vendor platforms. I see room for three, OpenDaylight, NSX and <!--?-->. The data plane is no different. We essentailly have one reference implementation in <a href="http://openvswitch.org" target="_blank">OVS</a> with maybe another emerging someday in <a href="http://www.projectfloodlight.org/indigo-virtual-switch/" target="_blank">Indigo</a>. We essentially haGreat presentation by these guys, check it out.

<p><a href="{{< relurl "/wp-content/uploads/2013/09/Nuage_NFD6_TechFieldDay_12sep13.pdf" >}}">Download the document</a></p>


<a href="http://techfieldday.com/appearance/nuage-networks-presents-at-networking-field-day-6/" target="_blank" rel="noopener noreferrer">Nuage at Network Field Day 6</a>

<hr />

<h2>Don't Sit on the Sidelines</h2>
If you are passionate about the future of networks, go shape it. This is a once every 20 year disruption. Projects with good community on IRC to get started are ODL and OVS. OpenStack that is great of course but what it needs is network control and thats where network pros are needed. As the walls continue to come down, rough consensus and working code via OSS is what I believe in.
<hr>

<ul>
	<li><a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank">OpenDaylight</a> - irc.freenode.net #opendaylight </li>
	<li><a href="http://openvswitch.org/support/" target="_blank">Open vSwitch</a> - irc.freenode.net #openvswitch </li>
</ul>
