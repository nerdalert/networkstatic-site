+++
title = "More Vendors Define Their SDN Strategy"
date = "2013-02-09T05:03:16+00:00"
lastmod = "2014-02-18T02:54:54+00:00"
author = "Brent Salisbury"
wp_id = 5758
categories = ["Speculative"]
tags = ["Big Switch", "Cisco", "Intel", "Software Defined Networking"]
description = ""
url = "/more-vendors-define-their-sdn-strategy/"
image = "/wp-content/uploads/2013/02/vendor-confusion.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "5def5041887154a52af6f05f4cc3a86f24a701c484fa1760e6b2998a6239f472"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>More Vendors Define Their SDN Strategy</h2>
It was a busy week in SDN. Some pretty significant revelations gave us good directional indications for SDN in 2013. Most significantly is SDN is getting enough traction to drive significant investment and tough decisions to be made by the networking incumbents. As more vendors define their SDN strategy, we will see an increasing amount of commercial products, rather than slideware.
<h2>Cisco ONE Webcast Series: An Introduction to OpenFlow</h2>
Cisco is giving an introductory WebEx lead by Dave Ward of Cisco and Matt Davy who recently left R&amp;E for an SDN startup. Not much to say here, the webinar title speaks for itself. The most amusing thing I heard in reaction to this from a colleague was, "Cisco wants to teach us OpenFlow? @!#$! we teach them OpenFlow." After reassuring him hell didn't freeze over, we both agreed this is a positive sign. I am not expecting the presentation is to explain why OpenFlow is only suitable for Google or academics doing research projects, so certainly looking forward to it. I am personally looking forward to the presentation to help encourage more people to begin thinking about the SDN potential to their business, not the mechanism.


<ul>
	<li>An introduction to OpenFlow: protocol, features, and future evolution</li>
	<li>Introducing OpenFlow into existing networks</li>
	<li>Cisco innovations across Enterprise and Service Provider portfolios</li>
	<li>Best practices and recommendations for customers evaluating OpenFlow enabled networks</li>
	<li>Live Q&amp;A</li>
</ul>

Registration for February 14th (WebEx): <a href="http://tools.cisco.com/gems/cust/customerSite.do?METHOD=L&LANGUAGE_ID=E&SEMINAR_CODE=S17515&PRIORITY_CODE=000105112" target="_blank" rel="noopener noreferrer">Cisco ONE Webcast Series: An Introduction to OpenFlow</a>
<h2>Daylight: Another SDN Consortium</h2>
Over the past few weeks there has been talk of a new SDN consortium being formed. A couple days ago Palmer at SDN Central, wrote a post about this group codenamed "Daylight". As he points out in his post, it has potential impact in the balance of SDN leadership in the fledgling SDN market. The two principal vendors are Cisco and IBM with their respective <a href="{{< relurl "/more-details-about-the-cisco-one-controller-announced/" >}}" target="_blank">ONE</a> and <a href="http://searchnetworking.techtarget.com/feature/IBM-DOVE-Big-Blue-enters-the-network-virtualization-battleground" target="_blank">DOVE</a> SDN products currently in development. Both of those SDN strategies rely heavily on OpenFlow to instantiate forwarding.

Palmer also points out that the controller of choice is JAVA based. If this group is leveraging an open source Java platform as a base, that narrows the field to FloodLight (BigSwitch) and Beacon (David Erickson). Floodlight was originally built using Beacon OF packages. I would take a wild guess that this project won't be using FloodLight.

<blockquote class="pullquote">Our understanding is the controller will be JAVA based, 100% open-sourced under an Apache 2 license and will include critical features such as high-availability and clustering. We’ve been told that the initial release is focused on datacenter networks and that control models for other market segments, such as service providers, are futures.<footer>Shining the Spotlight on Daylight</footer></blockquote>

SDN Central: <a href="http://www.sdncentral.com/companies/spotlight-on-daylight-sdn-consortium-open-source-controller/2013/02/" target="_blank" rel="noopener noreferrer">Shining the Spotlight on Daylight</a>
<h2>Intel Invests In Big Switch</h2>
Just when you think this vendor led consortium, looking to cut down disruptive SDN startups had landed a KO punch, BigSwitch received round B funding from Intel, to the tune of $6.5 Million. Incumbent networking vendors pride themselves in being hardware companies even though much of the silicon found in today's products comes from merchant silicon ODMs. A major disruptive threat of SDN is disaggregating the traditional monolithic networking hardware onto off the shelf components. This Intel investment could be a prequel of things to come if ODMs begin selling whitebox switches.

Intel missed the boat on ARM and will pay the price until they catch up. With the resources from <a href="http://nerdtwilight.wordpress.com/2011/07/19/intels-fulcrum-buy-validates-merchant-silicon-rise-of-cloud/" target="_blank">2011 acquisition of Fulcrum</a>, it could be tempting when hyper-scales come knocking as the PC core market continues to evaporate. It is worth adding, that just a few weeks ago, the same day of a less than glowing earnings report, there was word of a foundry deal from Cisco with Intel.

<blockquote class="pullquote">"Data center operators need programmable and cost-effective, merchant silicon-based networking architectures to meet their data center economic and operational objectives," said Bryan Wolf, managing director of Intel Capital, in a statement announcing its $6.5m injection into Big Switch. "At Intel Capital," he said, "we're looking for companies creating the most disruptive data center solutions, and Big Switch Networks open software-defined networking product suite is a leading solution in data center network virtualization."<footer><a href="http://theregister.co.uk/2013/02/08/intel_invests_in_big_switch_networks/">Intel stuffs more dough down Big Switch Network&#x27;s trousers</a></footer></blockquote>

More From Tech Crunch: <a href="http://techcrunch.com/2013/02/08/big-switch-raises-6-5m-from-intel-capital-gains-attention-for-next-generation-networking-challenges-cisco/" target="_blank" rel="noopener noreferrer">Big Switch Raises $6.5M From Intel Capital</a>

Dell Announces SDN Products (Finally)

Dell has been talking about SDN for a while, that was about it, talking. Dell finally announced some top of rack OpenFlow enabled switches. In fairness, it is probably safe to assume, that the transition to a private company slowed the SDN announcement.

What is missing from the OpenFlow enabled product lines are the campus edge switches. They are not alone in going after the data center and missing a chance to cut into enterprises with the lack of POE access switches. They are not alone in this slow adoption of access switches. That gap will benefit Cisco and HP who have announced at least, one or two devices to enable OpenFlow, from each product line to support early customer field trials.

I like the ideas that Dell is exploring. Figuring out how to improve performance in the slow path with more CPU, adds much needed flexibility to the network edge.

More information about the Dell split data plane strategy from Rajesh Narayanan of Dell.
Split Data Plane (Deck): <a href="http://www.ewsdn.eu/presentations/EWSDN_Rajesh.pdf" target="_blank" rel="noopener noreferrer">MacroFlows and MicroFlows: Splitting the SDN Data Plane</a>

Split Data Plane (Whitepaper): <a href="http://www.xflowresearch.com/xfi/download/file?fname=Split_Data_Plane_EWSDN_Oct_2012.pdf" target="_blank" rel="noopener noreferrer">Split SDN Data Plane</a>

More From Network World: <a href="http://www.networkworld.com/news/2013/020713-dell-data-center-266484.html" target="_blank" rel="noopener noreferrer">Dell strengthens data center line with OpenFlow support, high-end Ethernet switch</a>
<h2>OpenFlow Hardware Abstractions </h2>
In a great blog post on the Packet Pushers website my colleague and friend <a href="http://packetpushers.net/author/bowens/" target="_blank">Bill Owens</a> posted a very interesting article about the realities of the state of OpenFlow hardware today. I expect this to vastly improve over the next 12 months as networking vendors begin to shift away from hedging their bets and start putting their chips on the table. Progressive engineers like Bill are integrating and characterizing what the path to SDN networks will be. Vendor reference architectures are mythology. The pervasive information silos created by NDA's and "community" information hoarding, will leave it up to consumers to define SDN. The pace of SDN is to fast for disintegrating NDAs to hold up. .

<blockquote class="pullquote">It’s obvious that the controller’s job becomes much more difficult when these quirks and customizations are considered; the value of a standard mechanism for programming flows on a switch is substantially eroded. And unfortunately the situation only gets worse as we look deeper into the protocol, but that’s a matter for the next installment.<footer>OpenFlow Switching Performance: Not All TCAM Is Created Equal</footer></blockquote>

Packet Pushers Community Blog: <a href="http://packetpushers.net/openflow-switching-performance-not-all-tcam-is-created-equal/" target="_blank" rel="noopener noreferrer">OpenFlow Switching Performance: Not All TCAM Is Created Equal</a>

<hr />

2013 will be a soap opera in networking. Might even get a little weird, should be fun. Thanks for stopping by, oh and yes, thats a cat reading the news :)

<hr />