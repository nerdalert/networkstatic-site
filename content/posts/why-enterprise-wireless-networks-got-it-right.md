+++
title = "Why Enterprise Wireless Networks Got it Right"
date = "2012-08-12T22:33:06+00:00"
lastmod = "2013-01-26T01:47:58+00:00"
author = "Brent Salisbury"
wp_id = 2039
categories = ["Speculative"]
tags = ["Cisco", "Software Defined Networking", "Wireless"]
description = ""
url = "/why-enterprise-wireless-networks-got-it-right/"
aliases = ["/2012/08/why-enterprise-wireless-networks-got-it-right/"]
image = "/wp-content/uploads/2012/08/Enterprise.Wireless.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c62e5e93ca7fac4fc9920f012f5a2d27b7a393887dae248a283e6ba0976b747a"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Why Enterprise Wireless Networks Got it Right</h2>


I wanted to post some 802.11 wireless usage numbers and device breakdowns. These are two week University usage numbers in August of 2012. This period is right before students return so I wanted a baseline to capture the diff when students 25,000+ students come back with the ever growing amount of 802.11 wireless enabled BYOD hidden in pockets and purses. Apple is 50%+ in all categories other than total traffic by vendor where is is slightly less ~%45, which I would speculate is due to so many of those devices being mobile devices that would likely consume less traffic or more mobile optimized traffic loads. Most of these numbers will likely come close to doubling in the next few weeks has been pretty typical over the past few years.
<h4>Before the Pictures</h4>
While I love to look at aggregate data like this, this post was not to point out that Apple dominates in this demographic. The purpose of this post is to exemplify in what I believe to be, the desperate need for a centralized approach to managing medium and large scale enterprise networks. I am so used to people parroting entrenched enterprise networking vendors explain all of the reasons why centralization would never work I don't bat an eyelash anymore. All the while the same manufacturing naysayers are making huge profits on centralized 802.11 wireless delivery. The fastest growing space in the average medium to large campus network is wireless with a centralized controller. Collapsing forwarding and RF management into one or more centrally managed and orchestrated Borgs has been the only thing that has kept large scale 802.11 Ethernet deployments coming close to a functional service.

<blockquote class="pullquote">"The idea that one generic controller will be able to control every forwarding decision on a plethora of network types is seductive, but in the end unlikely.  The idea that many applications on many types of controllers can integrate and optimize local forwarding decisions is compelling and well grounded in history."<footer><a href="http://blogs.cisco.com/getyourbuildon/history-as-a-guide-to-sdns-coming-evolution/">History as a guide to SDN’s coming evolution</a></footer></blockquote>


I learned long ago to never say never. I agree we should learn from history and I am quite fond of trying to not make the same mistake too often (rarely successful). I recall a company that said the same very thing about the wireless market needing to stay distributed and was one of the last to adjust products to reflect that centralization in 802.11 had won hands down.
<h4> It's the Management Stupid</h4>
Down the road, when we reflect on this period, for networking to even contemplate staying the course in a completely distributed decentralized fashion (within an administrative domain), will sound just as unmanageable as someone today saying x86 virtualization and wireless centralization is inferior to standalone and decentralized. The Internet will always be decentralized and as it likely should be by virtue of crossing administrative domains, but that doesn't mean we need to model the Internet in our internal administrative domains to have functioning serviceable networks. We can achieve distributed failure, state distribution and loop free topologies just as the wireless technologies have proven without the use of Inter-AS protocols and architectures.
<h4>SDN Can Solve the Edge Problems</h4>
Core networking gear is not something we touch daily, tag in swap, pop, done. My buddy <a href="http://www.noxrepo.org/pox/about-pox/" target="_blank">Murphy McCauley</a> at UC-Berkeley describes it as simply solving the problem of the edge. I think thats spot on from enterprises to service providers. I am putting my money on evolution as opposed to another decade of proprietary hardware, software and APIs. SDN will solve many of the edge problems that keep the network "in the way" of IT and business. At the top of my problem list is management (not this <a href="http://gregferro.com/im-a-nerd-hugs-are-not-necessary/?utm_campaign=I'm%20a%20Nerd,%20Hugs%20are%20Not%20Necessary.%20" target="_blank">management</a>, lol my favorite post of the week had to plug it) To name a few of the many challenges both technical and more often than not operational in the Enterprise is, flipping Vlans, managing what few features should be there, multi-tenancy, provisioning/de-provisioning, security/QOS policy and capacity planning. Along the way we may actually learn to do something with value with the vast amounts of data we let die as the logs rollover with no one ever having any analytics to have touched it. In the meantime we can look to the wireless market and technology drivers who saw the need to manage client RF along with the litany of operational issues and thank them for providing an innovative roadmap.
<h4>On to the Pictures!</h4>
<a href="{{< relurl "/wp-content/uploads/2012/08/Agregate-new.jpg" >}}"><img class="alignleft size-full wp-image-2040" title="Aggregate Wireless Summary" src="{{< relurl "/wp-content/uploads/2012/08/Agregate-new.jpg" >}}" alt="" width="392" height="121" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em>Figure 1.</em> (14-day 8/12) Aggregate usage for a campus zone.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Summary.jpg" >}}"><img class="wp-image-2041 aligncenter" title="Wireless Client Device Summary" src="{{< relurl "/wp-content/uploads/2012/08/Summary.jpg" >}}" alt="" width="554" height="396" /></a></p>
<em>Figure 2.</em> (14-day 8/12) 802.11 client 802.11 wireless device summary by vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Session-Time-Vendor1.jpg" >}}"><img class="wp-image-2048 aligncenter" title=" 802.11 Session-Time-Vendor" src="{{< relurl "/wp-content/uploads/2012/08/Session-Time-Vendor1.jpg" >}}" alt="" width="558" height="429" /></a></p>
<em>Figure 3.</em> (14-day 8/12) 802.11 client session time by vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Sessions-by-Vendor.jpg" >}}"><img class="wp-image-2043 aligncenter" title="Total wireless sessions by Vendor" src="{{< relurl "/wp-content/uploads/2012/08/Sessions-by-Vendor.jpg" >}}" alt="" width="524" height="396" /></a></p>
<em>Figure 4</em>. (14-day 8/12) 802.11 client sessions by vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Traffic-by-Vendor.jpg" >}}"><img class="wp-image-2044 aligncenter" title="802.11 Traffic by Vendor" src="{{< relurl "/wp-content/uploads/2012/08/Traffic-by-Vendor.jpg" >}}" alt="" width="506" height="346" /></a></p>
<em>Figure 5.</em> (14-day 8/12) 802.11 client traffic by vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Clients-by-Vendors.jpg" >}}"><img class="wp-image-2045 aligncenter" title="802.11 wireless clients by Vendor" src="{{< relurl "/wp-content/uploads/2012/08/Clients-by-Vendors.jpg" >}}" alt="" width="520" height="381" /></a></p>
<em>Figure 6.</em> (14-day 8/12) 802.11 client breakdown by vendor

I would love to be able to compile neat breakdowns like this with the gear and software we already purchase from wireline products. Someday maybe. Exciting and fun times to say the least, get involved!
<aside class="legacy-callout">
<ul>
	<li>Part 1 - <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">Why Enterprise Wireless Got it Right</a></li>
	<li>Part 2 - <a href="{{< relurl "/2012/09/enterprise-wireless-and-wired-traffic-part2/" >}}" target="_blank">A Byte is a Byte</a></li>
	<li>Part 3 - <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">Enterprise 802.11 Wireless Growth</a></li>
</ul>
</aside>