+++
title = "Juniper Networks at Network Field Day #4"
date = "2012-11-10T07:22:22+00:00"
lastmod = "2013-01-01T03:00:19+00:00"
author = "Brent Salisbury"
wp_id = 3787
categories = ["Speculative"]
tags = ["Juniper", "Network Field Day"]
description = ""
url = "/juniper-networks-at-network-field-day-4/"
image = "/wp-content/uploads/2012/11/juniper_01.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "58b78ef8e9b3590f11cb3ae917d0347fdca3a2680b064f739653779a62ae16bd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Juniper Networks at Network Field Day #4</h2>
Juniper Networks at Network Field Day #4 Anchored the final day of <a href="http://techfieldday.com/event/nfd4/" target="_blank">NFD#4</a> organized by <a href="http://blog.fosketts.net" target="_blank">Stephen Foskett</a>, Claire Chaplais and the Gestalt IT team. We had presentations on QFabric, Mykonos, Virtual Chassis and network management automation. Below are some of my reactions to the <a href="http://www.juniper.net/us/en/" target="_blank">Juniper Networks</a> presentations and technology. I definitely recommend checking out my friends posts on their blogs with their thoughts on this and other presentations in the links at the end of the post.
<h2>Mykonos Acquisition</h2>
Is a recent acquisition by Juniper that delivers a web security product. This was a fun presentation. I looked to the right of me and <a href="http://evilrouters.net" target="_blank">Jeremy Gladdis</a> was fuzzing the web server of the demo and digging into the "Super Cookie" being placed by the Mykonos appliance onto his machine by visiting Juniper homepage. Eventually our tin foil hats came off and we all enjoyed the demo.

Juniper has been quite focused on filling out their security portfolio as of late. Strong security products are a good entry point into the enterprise. The page redirect features of Mykonos based on threat level escalation were classic. I believe one page was a redirection to the nearest lawyers office. Interestingly just this week the FTC asked for a no<a href="http://www.pcmag.com/article2/0,2817,2411916,00.asp" target="_blank"> tracking option</a> to be placed in browsers. How this affects the product I am not sure but it sounds as if the non-track is just a request in the browser which doesn't mean a whole lot anyways. Before anyone goes all tin foil hat, this is all standard practice, Junipers website was much cleaner then some of its competitors. I would conehead over Google before anyone for tricks like <a href="http://crave.cnet.co.uk/software/google-hit-by-record-fine-over-tricksy-tracking-cookies-50008863/" target="_blank">this</a>.
<h2>Juniper Virtual Chassis Stacking (VCS)</h2>
The Juniper Virtual Chassis Stacking was not necessarily sexy for some but it resonated with me as a solid technology that differentiates itself from the pack quite well. Having close to 100,000 ports in the network I am accountable for, I will always admire a solution that is focused on reducing operational overhead.

It stands out from its peers by stacking over Ethernet as opposed to the Catalyst access closet switch line that uses proprietary cabling and only stacks to 9 switches and the Brocade VDX that stacks half as many switches at 16 as compared to Juniper VCS at an impressive 32 switches in one stack. The advantage is less L2 hopping for operators to traverse to find an end system.
<h2>Juniper on Automation</h2>
- I am not going to do a deep dive here, as I want to save that for when (hopefully not <em>if</em>) some of <a href="https://twitter.com/cloudtoad" target="_blank">Derrick Winkworth's</a> concepts can be publicly available in coming weeks. We had some fun debates outside of the presentation on our own opinions on where we see SDN heading. While we differ on some concepts long term regarding SDN, in the short term, I agree with him wholeheartedly that automation enabling management and instrumentation is the path to somewhere better.

The dark broccoli forest that Derrick described, as the current state of networking was classic stuff. Just because someone from the NFD family goes and works for the vendor doesn't mean they aren't still NFD family so pretty cool seeing him up there doing the presentation and demo for the NFD team. Stay tuned in the coming weeks as I will pester Derrick for some of his automation ideas. I know the broccoli forest well, it is a dark, rigid, sleepless forest of despair. That is why I believe to my core, that networking will be radically different in the next 10 years unlike the last 10 years of arguable stagnation.
<h2>Juniper QFabric</h2>
I believe I have heard or read Juniper statements that %50 of their revenue is from the enterprise (not scouring financials if wrong, my bad). The <a href="http://www.enterprisenetworkingplanet.com/netsysm/enterprise-and-service-provider-router-and-switch-markets-post-gains.html" target="_blank">IDC</a> puts Juniper at %2.48 of the worldwide Layer 2/3 Ethernet switch market-share. This tells me that there is a lot of room to grow. HP successfully disrupted this market a few years back, not by going after high dollar ticket items first but by attacking the enterprise edge-access market. I was a bit leery when out of no where Juniper came in with this huge <a href="http://www.juniper.net/us/en/dm/datacenter/" target="_blank">QFabric</a> story in 2011, not at the solution but more that there needs to be a good foothold in an enterprise before they will take risk on some cutting edge concepts like QFabric.

I am a big fan of the concepts of the QFabric architecture. QFabric is a centralized architecture with distributed scale on the edge. I have joked more than once with a friend at Juniper that it would be a perfect OpenFlow platform. Going after enterprise makes sense, there is clearly plenty of market-share to compete with Cisco on, but sometimes you need to walk before you run. Expecting new customers to potentially adopt the heart of their IT (data center) with a new vendor or technology is clearly a longer funnel than forecasted.

I would put the MX switch up against any of its competitors in a heartbeat. I have used the MX for quite a few years now and have rarely hit limitations in hardware or software. I probably would have capitalized on those sort of foundational products to gradually transition into the data center. I very much enjoyed meeting <a href="https://twitter.com/simon_gordon" target="_blank">Simon Gordon</a> from Juniper. While clearly a scientist at heart, he did not carry the ego that can often accompany that and really seemed interested in feedback and ideas which is unique. I look forward to meeting him again someday and having time to drift off into the abstract over a beer. I have no doubt that QFabric sales will pickup because the vision and technology is there.
<h2>Juniper and SDN</h2>
The reality is every networking software and hardware manufacturer, incumbent or challenger is going to need to take a substantive risk over the next couple of years on how to execute their SDN strategy. Some companies will take a wait and see approach, this has worked in the past. That is standard operating with many expensive pivot points, before taking the financial risk have a clear business case and a snappy R&amp;D ROI. Forget the hype of SDN, this is about fundamental computer science concepts such as layered abstractions, distributed systems theory and the basic concept of machines doing X faster and more efficiently than people. When it comes to believing we need to expect more from the networking industry, with or <a href="{{< relurl "/why-we-expect-more-from-technology-providers-we-dont-have-a-choice/" >}}" target="_blank">without</a> the vendors I am completely dogmatic, bigoted whatever you want to call it in the long term.

Networking is becoming consumer driven, the days of IBM in 1982 are being put to pasture and the hyper-scales are calling the shots, with the rest of us vendor and consumer alike are riding the coattails. In getting to where we need to be, I am wide open on as long as it isn't where we are today.

The role reversal will be hard for some. The customer isn't always stupid anymore because right now, no one has the right answer, the curtain has dropped. Vendors being open and willing to really listen will be a key differentiators. The looming explosion of connectivity cannot be absorbed without some adjustments to the foundational constructs. Juniper clearly agrees or would not have undertaken the R&amp;D and risk associated with QFabric.  Juniper's message has been mixed over the past few months with regard to SDN. They are anything but alone in that because almost all companies have been also, that's why its called disruptive. Jim Duffy had a good article recently with some analysis that from a consumer perspective resonated with me <a href="http://www.networkworld.com/news/2012/102912-juniper-263766.html?page=1" target="_blank">5 things Juniper must do to reignite growth</a>.

It was great to also meet  guys that I knew from the Twitters like <a href="https://twitter.com/abnerg" target="_blank">Abner Germanow</a> and <a href="https://twitter.com/mbushong" target="_blank">Michael Bushong</a> two very smart and nice guys. I am ready to see what Juniper brings to the table on SDN. I believe they were one of the first to discuss SDN to the Network Field Day crew at NFD#2, when David Ward did a presentation when he was still with Juniper. Juniper cannot let the early QFabric issues get in the way of pacing or leading the industry on SDN. It will be another round of risks likely with much more long term implication. I fully expect to be watching the NFD#5 stream next spring and see a well articulated SDN strategy from a company that understands disruption as it is tightly wound in their heritage. Stay tuned for some hands on "stuff" in coming weeks around automation, and hopefully early next year with some beta OpenFlow code.

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/11/NFD-Logo3-150x150.png" >}}" alt="Network Field Day"></figure>Some great posts from my friends blogs on their thoughts:


<ul>
	<li><a href="http://blog.ciscoinferno.net/automating-junos" target="_blank">Anthony Burke</a></li>
	<li><a href="http://lamejournal.com/2012/10/15/juniper-mykonos-mostly-serious-web-security/" target="_blank"> John Herbert</a></li>
	<li><a href="http://networkingnerd.net/2012/11/08/juniper-land-of-unicorns-and-broccoli/" target="_blank">Tom Hollingsworth</a></li>
	<li><a href="http://blog.michaelfmcnamara.com/2012/10/juniper-networks/" target="_blank">Michael McNamara </a></li>
</ul>

<div></div>
<hr />