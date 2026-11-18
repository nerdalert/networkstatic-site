+++
title = "Programming the NSP: Vendors on SDN for SP Operators"
date = "2012-12-02T19:00:26+00:00"
lastmod = "2012-12-09T21:41:12+00:00"
author = "Brent Salisbury"
wp_id = 4911
categories = ["Speculative"]
tags = ["Service Provider", "Software Defined Networking"]
description = ""
url = "/programming-the-nsp-vendors-on-sdn-for-sp-operators/"
image = "/wp-content/uploads/2012/12/nsp-world-sdn.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "4da9f49f8c4d46cbfb4f22dbf6fb0abc2db0bb035ea3fff2c4af74b209a7fe23"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Programming the NSP: Vendors on SDN for SP Operators</h2>
<span class="drop-cap">L</span>
ast week we looked at what the Network Service Provider Customers are looking for from vendors in the  <a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank"><em>Network Virtualization Function (NFV)</em></a>. This week, let's take a look at what the vendors were proposing in October at the SDN &amp; OpenFlow World Congress. Some of the vendor and ONF white papers were posted recently which is nice to see. The keynote was streamed but everything else was members only. These new groups need to generate revenue to maintain bodies and hold conferences and their businesses. That said, it generates more  long tail interest about the events when the lecture recordings are posted for viewing after the fact, like the <a href="http://www.youtube.com/user/OpenNetSummit" target="_blank">Open Networking Summit</a> and <a href="http://nerdtwilight.wordpress.com/2012/11/17/for-your-sdn-reading-pleasure/" target="_blank">SIGCOMM</a> conferences.
<h2>NSP Optical and Ethernet Market Share</h2>
Below is the NSP global market share for optical transport along with the core and edge router market as od 3Q2012.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/12/NSP-Network-Marketshare1.jpg" >}}"><img class="aligncenter  wp-image-4933" title="NSP-Network-Marketshare-2012Q3" src="{{< relurl "/wp-content/uploads/2012/12/NSP-Network-Marketshare1.jpg" >}}" alt="NSP-Network-Marketshare-2012Q3" width="542" height="246" /></a></p>
<h2>Huawei SDN SOX Strategy</h2>
Huawei presented on <em>SOX - A Generalized and Extensible Smart Network Openflow Controller (X)</em>. Huawei has been quite busy with IETF <a href="{{< relurl "/new-ietf-sdn-drafts/" >}}" target="_blank">draft</a> submissions on Alto and SDNi this year. Huawei has large market share in Transport, LTE and NSP route and switch gear.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/12/Huawei-SOX1.jpg" >}}"><img class="aligncenter  wp-image-4932" title="Huawei-SOX-SDN" src="{{< relurl "/wp-content/uploads/2012/12/Huawei-SOX1.jpg" >}}" alt="Huawei-SOX-SDN" width="517" height="284" /></a></p>
<strong>Figure 1</strong>. Huawei SOX Architecture.

<a href="{{< relurl "/wp-content/uploads/2012/12/Huawei-testbed.jpg" >}}"><img class="aligncenter size-full wp-image-4913" title="Huawei-openflow-testbed" src="{{< relurl "/wp-content/uploads/2012/12/Huawei-testbed.jpg" >}}" alt="Huawei-openflow-testbed" width="468" height="310" /></a>

<strong>Figure 2</strong>. Huawei testbed focusing on forwarding target neutrality and interoperability with uniform primitives.
<h2>Juniper Network Programability for the NSP</h2>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/12/NSP-Juniper-Application.jpg" >}}"><img class="aligncenter  wp-image-4914" title="NSP-Juniper-Application-sdn" src="{{< relurl "/wp-content/uploads/2012/12/NSP-Juniper-Application.jpg" >}}" alt="NSP-Juniper-Application-sdn" width="502" height="190" /></a></p>
<strong>Figure 3</strong>. This is an important graphic from Juniper. It says to me, they are going to support what large NSPs want. <em>(Click to enlarge)</em>

I noticed Juniper is moving away from using the term SDN in their paper. Might be differentiation, or customer burnout on hearing it. Fine with me, but for now it's just  easier than some derivative of programmatically evolving networks through standardized open API or open source primitives. SDN is easier for now, but possibly as annoying as "cloud" for some. Apologies for abusive semantics, but its all we have for now. Though "programmable networks" (PN) is more syllables and two letter acronyms never seem to stick. It does beat a marketing term that means nothing outside of that vendor like some others are doing. Anything is better than SOS. It looks like a good path to freedom.
<h2>Programming the NSP: Vendors on SDN for SP Operators</h2>
<h2>Brocade SDN Data Center Fabrics</h2>
Brocade presented two papers one was <em>Exploring Software-DefinedNetworking with Brocade. </em>Tying the Brocade VCS/VDX fabric, Cloud Orchestration and SDN together was first demonstrated at <a href="http://techfieldday.com/video/brocade-openstack-demo/" target="_blank">Network Field Day #4</a>. <a href="http://etherealmind.com" target="_blank">Ferro</a> and <a href="http://www.ipspace.net/Main_Page" target="_blank">Pepelnjak</a> just did a podcast review of the VDX <a href="http://packetpushers.net/pq-show-17-reviewing-the-brocade-vdx-launch-with-ivan-pepelnjak/" target="_blank">here</a>.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/brocade-ostack-sdn.jpg" >}}" alt=""></figure>
<strong>Figure 4. </strong>Brocade on the holistic data center.
<h2>My Thoughts</h2>

There was further articulation for the NSP from vendors, but everything still tracks with the <a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank">NFV document</a> the NSPs published last month. Operators need to the ability to push multi-layer technical and business policy into the proverbial meat grinder, have consistency and arbitration checks performed while  complexity through abstraction. Scale will come with modularity just as it is in everywhere else of compute. The mechanism is irrelevant but the goal should wherever hardware or software ingestion is to be alikeness or even if we dare to dream, uniformity.
<h2>Additional Reading Resources and White Papers</h2>
There are dozens of documents to review on the <a href="http://www.layer123.com/downloads" target="_blank">SDN &amp; OpenFlow World Congress site</a>. Thanks to <a href="http://www.layer123.com" target="_blank">http://layer123.com</a> for publishing the conference papers.
<hr />
Thanks for stopping by.