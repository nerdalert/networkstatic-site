+++
title = "Be The Steamroller Not The Road"
date = "2013-03-19T04:41:52+00:00"
lastmod = "2013-03-20T04:10:51+00:00"
author = "Brent Salisbury"
wp_id = 6033
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/be-the-steamroller-not-the-road/"
image = "/wp-content/uploads/2013/03/Change2.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "adf94a4abf223d56e06ff638e5746d48a1be1534bf518af20fa532f0b467eddc"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Be The Steamroller Not The Road</h2>
<blockquote class="pullquote">“Once a new technology rolls over you, if you're not part of the steamroller, you're part of the road.”<footer>-Stewart Brand</footer></blockquote>
I always chuckle when I hear SDN or OpenFlow "bigots". I find that it is normally vendors being flippant towards SDN in general are from a handful of camps:
<hr>



<ul>
	<li>Incumbent vendors, realizing the days of high profit margins, through vertical integration on commodity silicon are coming to an end.</li>
	<li>Companies who think proprietary southbound protocols is a good place to try and differentiate. The irony is, most of those are doing flow based forwarding with proprietary messaging protocols. Net is, the same flexibility and maybe even better than OF, but using closed wire protocols. So it makes sense, of course they trash OF because they want to separate themselves using the same concepts and be the "innovator". I personally think the application layer is the place to focus to be effective. I am expecting Intel to own the <strong>edge </strong>hardware market someday, but thats for another day.</li>
	<li>Then there is the a-typical IT guy, that hates change. Hey, thats understandable. I like stability as much as the next fear of failure driven person. Server guys freaked out over server virtualization, mainframe guys hugged their water cooled monoliths all the way to the dumpster, but at the end of the day, IT abstraction doesn't shrink jobs. Horizontalization creates jobs and enables innovation.</li>
</ul>

<hr>
When people spend time to understand that OpenFlow is merely an open messaging protocol to instantiate flow based forwarding. <a href="http://etherealmind.com/sdn-use-case-firewall-migration-in-the-enterprise/" target="_blank">Flow based forwarding</a> integrates L4 into forwarding decisions. L4 adds rudimentary application awareness. OpenFlow is merely a means of forwarding L1-L4 in a single protocol. Thats not to say you don't need other protocols. OpenFlow has no awareness of port provisioning etc. That leaves plenty of room for differentiation in the management plane and actually building <a href="http://blog.ioshints.info/2013/03/nec-programmableflow-scalability.html" target="_blank">applications</a> to control the network. Odds are, one vendors SDN solution isn't much different from the next when you look under the hood. Outside of performance, look for application differentiation, not who has the best flow-based forwarding protocol.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/DC-SP-SDN.png" >}}" alt="SDN in the Data Center and Service Provider"></figure>


A vendor agnostic southbound forwarding abstraction is all OpenFlow is. Creating network operating systems and extracting state to run programs against is much more interesting but we don't get there without a few key protocols.
<hr>
<blockquote class="pullquote">“The people who resist change will be confronted by the growing number of people who see that better ways...are available thanks to technology.”<footer>-Bill Gates</footer></blockquote> So be open minded, understand most of us don't care wether it is OpenFlow or not, but we also don't want to wait around for another 6,000 RFCs and a dozen more <a href="http://www.networkworld.com/news/2013/031413-dell-sdn-267725.html" target="_blank">consortiums</a> (which I happen to be encouraged by OMG and Daylight) to define something everyone unanimously agrees is a flawless abstraction. The good news is, the consumers will consolidate with or without consensus from product managers. If it isn't OpenFlow for flow based forwarding, pick something else, just pick something. So for my fellow biggots, that still remember what they learned in <a href="http://www.youtube.com/watch?v=eXsCQdshMr4" target="_blank">computer science 101</a>, that layered abstractions hide irrelevant details to manage complexity, I salute you. We want applications to efficiently control the network, not the best mousetrap.