+++
title = "SDN APIs- I Think I Have Seen This Movie Before"
date = "2012-07-09T04:08:42+00:00"
lastmod = "2013-01-19T07:51:09+00:00"
author = "Brent Salisbury"
wp_id = 1568
categories = ["Speculative"]
tags = ["Northbound API", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/sdn-apis-this-all-feels-pretty-familair/"
aliases = ["/2012/07/sdn-apis-this-all-feels-pretty-familair/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "68a760ec059a342a6fd9f0f8a8ed268c5fab70327eba63cec4cf758b1cef490c"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN APIs- I Think I Have Seen This Movie Before:</h2>
<a href="{{< relurl "/wp-content/uploads/2012/07/old-movie1.jpg" >}}"><img class="alignright size-full wp-image-1869" title="SDN old movie" alt="" src="{{< relurl "/wp-content/uploads/2012/07/old-movie1.jpg" >}}" width="331" height="293" /></a>  To see the future of SDN and arguably the future of networks, the roadmap is in our rear-view mirror. Like with most things the past holds the clues to the future and computing cycles fit that mold well. The Northbound API is starting to get some attention as there has been recent milestones in announcements regarding SDN support.

There have been some new SDN products and support being disclosed, the biggest coming last month from Cisco with it's onePK announcement which implies there will be SDN support in all future product lines under onePK(OpenFlow v1.0). Roy Chua over at SDN Central had a great post summarization some of the infant APIs in existence today and made the point, "In the ensuing competition between the different APIs, we will see true evolution towards really useful NBAPIs. The alternative, if we sit around and debate in committees, is stagnation and irrelevancy" <a href="http://www.sdncentral.com/sdn-blog/openflow-northbound-api-olympics/2012/07/" target="_blank">OpenFlow Northbound API – A New Olympic Sport</a>. When we (the networking community) are trailing the rest of the computing world after a decade of proprietary hardware, software and APIs you don't need to be a psychic to take a good guess at what the future holds because I think we have seen this movie before, it's just a little bit different this time around.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/07/Posix1.jpg" >}}"><img class="aligncenter size-full wp-image-1687" title="Posix SDN API Abstraction Layers" alt="" src="{{< relurl "/wp-content/uploads/2012/07/Posix1.jpg" >}}" width="443" height="439" /></a></p>
<strong>Figure 1</strong>. Do we need a new roadmap that is better than the compute frameworks today to catch up to the rest of the world?

I think we are pretty set down the path of establishing a good set of APIs for the decoupling of the control plane from networking hardware. That forms an abstraction or set of primitives that can have a common method of control and instantiation into future networking devices.

<h2>Operating System API and Primitives</h2>

To fully begin to realize the next step in SDN will be to move applications out of a network controllers as modules and create yet another layer containing applications. The reasons are the same as any other reason for distributing applications for scale, performance, etc. To interact with an operating system many moons ago something called POSIX (<strong>P</strong>ortable <strong>O</strong>perating <strong>S</strong>ystem <strong>I</strong>nterface) was created. This was done by the IEEE and generally speaking it was to create a uniform set of APIs for an application developer to have portability between various operating systems conforming to those set of primitive interfaces. An example is, if you build an application on Linux OS using POSIX functions you could port that code reasonably easily to OS X, BSD, even Windows (Cygwin) and any other OS exposing POSIX APIs. Windows uses another core OS API called Win32 as opposed to POSIX.

How much inefficiency is there for software developers having this duplicative efforts? Thats for another time. Are we considerably worse off today having two major competing camps, windows and Unix? It is hard to discount the power of competition and the market pressures driving companies to differentiate from competitors.


<h2>Competition Drives Innovation</h2>

<a href="{{< relurl "/wp-content/uploads/2012/07/rear-view2.jpg" >}}"><img class="alignleft size-medium wp-image-1681" title="rear-view sdn" alt="" src="{{< relurl "/wp-content/uploads/2012/07/rear-view2-300x198.jpg" >}}" width="300" height="198" /></a>The point is, it doesn't have to be the same, and for that matter we may not want it to be the same, but it will likely condense over time. We will likely start out with quite a few Northbound APIs  and trim the last to a couple, two-three or however can survive. It may not even matter because how often do we sit around debating operating system primitives except for emerging frameworks like the mobile OSs. The desire to eliminate competition will be no different than the operating systems that have been weeded out over the years. See IBM OS/2, Microsoft BOB, Netware and the best Microsoft Windows 98 Blue Screen of death live demo when Gates was demoing Win98 <a href="http://www.youtube.com/watch?v=fA4BnCtaW0s&feature=related" target="_blank">plug and play</a>. All of these OS's had brilliant engineers working on them but natural selection happens.

<h2>SDN Crystal Ball Not Necessary</h2>

If history holds true we will start out with many and end up with a few. It is hard to argue at this point that in order to move forward and leave networks to the next generations that are something other than fragile closed inflexible couplings. The message from the community is we want the flexibility that we have in software to transcend to the network to fit our business needs, choices not answers. Vendors may save some cycles and cash by focusing on the application rather than the API unless, they have a good shot at being the last few standing and capturing the bounty of the vendor control or lock, depending on your levels of pessimism. We are already seeing our systems brethren putting together a better northbound API in the OpenStack Quantum project then we in networking have been able to conceive in the past 10 years. It is up to us to articulate what is expected and even develop the architectures and code with the early primitives we have.
<hr>
Thanks for stopping by.
<hr />