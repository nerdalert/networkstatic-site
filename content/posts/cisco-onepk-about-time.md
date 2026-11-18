+++
title = "Cisco onePK Announcement, big Surprise or About Time?"
date = "2012-06-15T22:52:59+00:00"
lastmod = "2012-11-30T04:03:26+00:00"
author = "Brent Salisbury"
wp_id = 1162
categories = ["Speculative"]
tags = ["Cisco", "Software Defined Networking"]
description = ""
url = "/cisco-onepk-about-time/"
image = "/wp-content/uploads/2012/06/onepk.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "9ed88118cace2e7a182d29597c107b0f528aa0174a98bd62ec7003eea3907e99"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

This week Cisco announced their new strategy for engaging software defined networks (SDN) with the announcement of the the onePK (Cisco One Platform Kit). I think we saw what I think most of us <a href="{{< relurl "/2012/06/cisco-networkers-live-clus-or-whatever-we-call-it-now-sdn-predictions/" >}}" target="_blank">expected</a>. I didn't expect an DK, so that was a pleasant surprise. I know many folks especially from R&amp;E have wanted that visibility into the planes of operation of their purchased networking gear for many years now so that is a direct result of years of consumer demand that got too big to ignore. For most of us the Cisco DK is as much of a game changer as the JunOS SDK was couple years back, not much except for the corner cases. This is a major step into opening the network for integration at some level into the rest of the world of computing as opposed to the black box we have become in IT.

David Ward seems to have brought the best parts of the JunOS SDK and left behind some of the uninteresting parts in my humble opinion. Two quotes from the register- "It's going to be interesting to watch, and to see whether networking companies are going to be software companies", "not everybody finds BGP and OSPF as exciting as I do." This was a much more interesting story than TLVs in IGPs we heard last Fall when he was with Juniper at the Open Networking Summit seen <a href="http://www.youtube.com/watch?v=6qMgurC0juo" target="_blank">here</a>. He has been involved in the OpenFlow conversation from the very beginning as a contributor with Juniper. He probably knows the needs of R&amp;E as well as any vendor representative out there.

It will be fun to see everyone jump out of the woodwork and be all SDN crazy, I heart OpenFlow stickers will be all over the place. Vendors will tell you they liked it all along. That said, networks will continue to grow ever increasingly complex. The promise of abstraction to reduce complexity feels way to far away to even peak my interest, if even in the realm of possibility. We are way too far down the rabbit hole for any quick fixes. We will stack complexion and continue to make a paycheck juggling them all, but baby steps, beat no steps.

I think the only wait and see left is if Cisco gets into the <a href="{{< relurl "/2012/06/the-northbound-api-2/" >}}" target="_blank">application layer</a> which arguably they already are. There is no putting the car in reverse at this point for Cisco. They fought the consumers for ~4+ years on an exposed data plane for R&amp;E and they have capitulated.  I can taste the irony of Cisco coming to the table wanting to sell me SDN solutions now. I would argue much like the CIUS that Chambers referenced  "We should have killed Cius earlier", they should have come to the table on SDN earlier. Couldn't be happier, that I may not need to try and convince a vendor of my needs and why its not crazy to ask for such things for my organization. It was a gamble, but hats off to Cisco for taking the risk and on top of that, delivering what on the surface looks to be an elegant solution. The alternative would have been unsustainable.

This is a win for the research community and they earned this and much more to come, for many years of talking on deaf ears. Simply put, they went to the drawing board, proofed a better solution as community and submitted ideas, that will enable networks to get out of the way of innovation.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/06/features.jpg" >}}"><img class="wp-image-1163 aligncenter" title="Cisco OnePK features" src="{{< relurl "/wp-content/uploads/2012/06/features.jpg" >}}" alt="" width="493" height="382" /></a></p>
<strong>Figure 1.</strong> onePK exposed services through an API.

Pros:
<ul>
	<li>KVM integration into the Nexus 1000v (in a tie for the REST API for favorite)</li>
	<li>Not just an OpenFlow Agent some attempts at value from the dev kit.</li>
	<li>REST APIs this is fantastic!!!!!</li>
	<li>A controller proof of concept. Not much out there other than a sneak peek for the "privileged".</li>
	<li>Overlay orchestration with the 1000v.</li>
	<li> Standards based OpenStack Quantum Plug-in and REST APIs for DC orchestration ("based" may be a problem)</li>
</ul>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/06/slide1.jpg" >}}"><img class="wp-image-1437 aligncenter" title="Cisco onepk features openflow" src="{{< relurl "/wp-content/uploads/2012/06/slide1.jpg" >}}" alt="" width="509" height="283" /></a></p>
<strong>Figure 2.</strong> Subtle...

OpenFlow v1.0 Support:
<ul>
	<li>Announced support was for the ASR1000 and the ISR G2. These are for cloud tunnels presumably as part of the <a href="http://newsroom.cisco.com/press-release-content?type=webcontent&articleId=889622" target="_blank">"Cloud Connector"</a> software also unveiled.</li>
	<li>Anounced proof of concepts for the 3750X and 3560X for edge plays. Noticably missing is investment protection for the 2960 line.</li>
</ul>
Presumably more to come as things shake out. Other than the annoying the annoying "get your build on" marketing name it was a good week that will continue to keep our heads spinning.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/06/market-share.jpg" >}}"><img class="wp-image-1165 aligncenter" title="market share cisco" src="{{< relurl "/wp-content/uploads/2012/06/market-share.jpg" >}}" alt="" width="516" height="285" /></a></p>
 <strong>Figure 3.</strong> The beloved market share. I only put it there because it does represent the importance of the Gorilla embracing programmable networks.

Other announcements:
<ul>
	<li> 40Gb to the 6500. With 80Gb available per slot to the fabric not sure where this is going.</li>
	<li>40Gb to Nexus 5k.</li>
</ul>
Other Reactions:

Ivan Pepelnjak <a href="http://blog.ioshints.info/2012/06/cisco-one-more-than-just-openflowsdn.html" target="_blank">Had great analysis as always.</a>
Jason Edelman <a href="http://www.jedelman.com/1/post/2012/06/cisco-unleashes-sdn-material.html" target="_blank">has a nice breakdown of some slides.</a>