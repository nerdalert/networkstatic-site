+++
title = "Brent's Technology Bookmarks from June"
date = "2014-06-21T04:55:41+00:00"
lastmod = "2014-06-22T06:43:26+00:00"
author = "Brent Salisbury"
wp_id = 7397
categories = ["In the Lab", "Tools"]
tags = ["Bookmarks", "Networking", "technology"]
description = ""
url = "/brents-technology-bookmarks-from-june/"
image = "/wp-content/uploads/2014/06/cat_are_you_fucking_kidding_me-.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "315eabeda8790c04233a6099ced6d8ed96c53e8c244f37a996c7e1991e2cf58f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h1>Brent's Technology Bookmarks from June</h1>
Lots going on in the past couple of months. While current projects have me pretty busy I wanted to share some good reads and interesting developments in the industry. In no particular order:

<hr />


<ul>
	<li><a href="http://www.coverfire.com/articles/queueing-in-the-linux-network-stack/" target="_blank">Queueing in the Linux Network Stack</a> - This is a fantastic breakdown of buffer management in the Linux networking stack.</li>
	<li><a href="http://www.sdncentral.com/news/google-open-source-help-policy-based-sdn/2014/06/%20f" target="_blank">Google Wants Open-Source Help for Policy-Based SDN</a> from the guys over at SDN Central. I'm glad to see Google recognizes it needs to participate in a broader open source networking community to drive their architectural agendas. Hope to see them jump into OpenDaylight with us and get some oxygen on their models. How tightly coupled models and platforms are is still something that needs debate in my opinion. The article also makes me want to revisit <span style="color: #000000;">protobufs to see if any of the RPC code has been open sourced. </span></li>
	<li>Facebook has been a huge supporter of the <a href="http://www.opencompute.org" target="_blank">Open Compute Project</a> and this week announced further adoption of the whitebox evolution. Since networking is roughly in the mid-1980s when it comes to embracing the inevitability of a commoditized network hardware world. That said, incumbent vendors are quite adept at <a href="http://www.networkworld.com/article/2169117/lan-wan/facebook-open-compute-project-has--weaknesses---cisco-ceo-says.html" target="_blank">slowing</a> down and managing disruption to avoid going the way of Sun. I have been pretty steadfast on believing that those who run whitebox/ODM manufactured compute today will be the aggressive adopters on the networking front. This will drive down the disproportionate (compared to compute) margins of networking kit. OEMs can surely add enough value to makeup for the single digit/teen margins to stay status quo.</li>
	<li>A fun read to remind us to keep our pessimism in check or ending up having some amusing quotes someday. <a href="http://thenextweb.com/shareables/2010/02/27/newsweek-1995-buy-books-newspapers-straight-intenet-uh/#!qmSFr" target="_blank">Newsweek in 1995: Why the Internet will Fail.</a></li>
	<li>Next are a dozen things this fella learned from the VC king Marc Andreessen (lesser known, cut his teeth as the author of the Mosaic browser from his time at NCSA). <a href="http://25iq.com/2014/06/14/a-dozen-things-ive-learned-from-marc-andreessen/" target="_blank">A Dozen Things I’ve Learned From Marc Andreessen</a></li>
	<li>A classic and tragic story on why your backups should probably not reside in the same cloud platform as your production systems. <a href="http://www.theregister.co.uk/2014/06/18/code_spaces_destroyed/" target="_blank">Code Spaces goes titsup forever after attacker nukes its Amazon-hosted data</a></li>
	<li> Google also made the headlines with their growing support of the hottest topic since Chuck Norris's beard Docker. For Google, their GCE cloud strategy appears the same, don't compete with Amazon on their field (IaaS) but change the rules of the game and compete at the application layer. There is so much margin left and Google will continue to drive the <a href="{{< relurl "/does-the-cost-of-cloud-iaas-intersect-the-local-vm/" >}}" target="_blank">race to zero</a>. Read more from their blog about the update: An update on container support on <a href="http://googlecloudplatform.blogspot.com/2014/06/an-update-on-container-support-on-google-cloud-platform.html" target="_blank">Google Cloud Platform</a>.</li>
	<li>I may have another hero to add to my collection. Former FCC Commissioner Michael Copps speaking at the Library of Congress spoke the truth about the tragic state of broadband in the US. <a href="http://consumerist.com/2014/06/18/former-fcc-commissioner-we-should-be-ashamed-of-ourselves-for-state-of-broadband-in-the-u-s/" target="_blank">Former FCC Commissioner: “We Should Be Ashamed Of Ourselves” For State of Broadband In The U.S.</a></li>
	<li>The only worthwhile thing I have seen the FCC do since <a href="http://www.lightreading.com/regulation/meet-tom-wheeler-net-neutrality-procrastinator-in-chief/a/d-id/709264" target="_blank">Wheeler</a> (a former Cable lobbyist) took over as chairman was covered in this article <a href="http://www.thewire.com/technology/2014/06/fcc-redefines-internet-speed/371961/" target="_blank">FCC May Redefine What It Means to Have 'Broadband' Internet</a>. Bringing the broadband benchmarks out of the 90's is important in many different ways that are too long to list so take a peek and tell these dummies why a strong National (and Global for that matter) broadband infrastructure isn't just important for watching NetFlix movies to future generations. They are fracturing and it may well be worth throwing some support towards the <a href="http://www.lightreading.com/regulation/fcc-split-on-net-neutrality-plans-/d/d-id/709100" target="_blank">dissenters</a> with enough backbone to push back on the lobbyist culture in US politics.</li>
	<li>One more from Google that presents empirical data on the impact of build time breakage in software development <a href="http://static.googleusercontent.com/media/research.google.com/de//pubs/archive/42184.pdf">Programmers’ Build Errors: A Case Study (at Google)</a>. Something we all love :)</li>
	<li>A post from one of my favorite blogs Network Heresy where Martin Casado frequently has folks from his staff guest blog. Here <a href="http://blog.scottlowe.org" target="_blank">Scott Lowe</a> and Tim Hinrichs discuss the hot topic of policy in <a href="http://networkheresy.com/2014/06/19/on-policy-in-the-data-center-the-solution-space/" target="_blank">On Policy in the Data Center: The solution space</a>. Another pal, <a href="https://twitter.com/dvorkinista" target="_blank">Mike Dvorkin</a> is also working on the policy problem from many years of obsessing and numerous implementations, namely UCS Manager. I don't have any links but will dig some up in a future post to share both sides. I avoid looking at company names, ideas are either bullshit mouse traps or not. Both of these select camps understand the importance open source plays in adoption. No migration path, no adoption.</li>
	<li>There was also a nice writeup on Martin's <a href="http://www.informationweek.com/cloud/infrastructure-as-a-service/why-goldilocks-zone-of-data-center-security-makes-sense/a/d-id/1269304" target="_blank">Goldilocks Zone</a> security concepts. Someday I will be out of the low levels in ODL when we stabilize with feature parity and really start grinding security and policy implementations, rather then the rudimentary OS services I'm working on currently. Take a look at it. I fundamentally believe that SDN solving the disaster of security application today is a core business and technological deliverable. If I'm not mistaken, his original SDN/OF work was to better segment/secure research networks and some .gov work, he understands the space as well as anyone out there.</li>
	<li>Netflix is probably the biggest broadband consumer advocate in existence (arguably 100x more productive then the FCC). Here is a nice<a href="http://ispspeedindex.netflix.com/usa" target="_blank"> speed index</a> they recently started publishing to the <a href="http://www.fierceonlinevideo.com/story/verizon-fios-speed-drops-netflix-isp-index-despite-peering-deal/2014-06-09" target="_blank">chagrin of a few carriers</a>.</li>
	<li>Lastly, my favorite is an <a href="https://secure.mysociety.org/admin/lists/pipermail/developers-public/2011-October/007647.html" target="_blank">informational packet</a> from the legend of the free software world, Richard Stallman. It outlines his speaker visits and what he requires if he is visiting as a guest speaker. Stallman on cats in the house where he will be staying, and this quote makes him even more awesome <em>"I like cats if they are friendly, but they are not good for me; I am somewhat allergic to them. This allergy makes my face itch and my eyes water. So the bed, and the room I will usually be staying in, need to be clean of cat hair. However, it is no problem if there is a cat elsewhere in the house--I might even enjoy it if the cat is friendly."</em></li>
</ul>


<hr />

Thats all for now. Have a great weekend.