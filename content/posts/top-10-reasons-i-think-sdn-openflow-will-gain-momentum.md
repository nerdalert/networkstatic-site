+++
title = "Top 10 Reasons I think SDN Openflow will gain momentum"
date = "2011-11-04T03:24:38+00:00"
lastmod = "2013-07-30T04:59:51+00:00"
author = "Brent Salisbury"
wp_id = 33
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/top-10-reasons-i-think-sdn-openflow-will-gain-momentum/"
image = "/wp-content/uploads/2012/10/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ca598fe505ec76a757802ab6cd0acdd93889e38622cfffc0194b1bc5dfc6639f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Top 10 Reasons I think SDN Openflow will gain momentum </h2>
<ol class="legacy-numbers">
<ol>
	<li>Ridiculously high profit margins in the networking hardware market.</li>
	<li>Content deliverers needing the flexibility that SDN’s claim to deliver in their data centers. To do anything they want with their network traffic, as opposed to trying to orchestrate the ever growing list of protocols and encapsulation methods in closed proprietary network operating systems.</li>
	<li>Merchant Silicon- The typical lead time of developing custom ASICs is measured in numerous years. Off the shelf silicon can bring products in a fraction of the time. Custom silicon will still be used in many cases but chips and TCAM will need to be standardized to some degree. Hardware commoditization is likely inevitable just as it was in the x86 market. The Nexus 3064 is a classic example of reacting to Arista’s takeover of the low latency switching fabrics on financial trading floors where data availability advantages are measured in microseconds. Net is, this will bring the profit margins much closer to the x86 market.</li>
	<li>Cisco and Juniper both signaling there will be at least some synergy with their product and SDN. We are likely to hear both of those companies repeat quite often that they have always been “software companies”. JunOS and IOS are the staples of both of those companies. They will stay ahead of it rather than sticking their heads in the sand in order to stay relevant. Fun trivia, the pilot switch used over two years ago by the Stanford research team was a Cisco Cat6500.</li>
	<li>SDN can be deployed in a similar module horizontal fashion in the same way we bolt on growth today. MPLS compliments SDN incredibly well since it is another method of virtualization that can manipulate traffic in granular and dynamic ways. Proper abstraction layers are absent from networking. Monolithic devices with proprietary hardware, software and APIs will die the way IBM PCs did in the early 80s. Very few companies have been able to sustain high margins for commodity parts, except for Apple. That is differentiation in software, not silicon. That is what networking vendors will have to evolve to or lose market share.</li>
	<li>I think SDN will be able to deliver the latest and greatest features significantly faster. It will also deliver or integrate protocols like TRILL, MPLS etc. I have a dream that I never hear “that is not supported in hardware” again.</li>
	<li>A potential open standard OpenFlow as a base. However, I fully expect for vendors to have proprietary bells and whistles and pre-standards in their controller software. Standards bodies are slow and imbalanced, begin moving towards open source development models.</li>
	<li>Simplified management and operations which will drive down OpEx much like we see with DevOps in hyper-scale business models today. Capture the entire infrastructure architecture by looking at significantly less devices to get a quicker holistic view of the network instead of crawling through thousands of devices loosely coupled by a bag of protocols. It would be nice to hit the print button of a controller to give a dynamic view of the network rather than digging up a 5 year old map and figuring out what is still there.</li>
	<li>Security- Instead of punting your east-west data center traffic north for an expensive security policy application it could be done in the flow lookup routine along with every other black box we put in the data center i.e. load balancer, NAT etc.</li>
	<li>Blah blah cloud.</li>
</ol>
</ol>
<hr>
Predicting the future is often as easy as looking at the past, no crystal ball required.
<hr>