+++
title = "Cisco acquisition of Cariden"
date = "2012-11-30T03:42:34+00:00"
lastmod = "2012-12-09T22:04:33+00:00"
author = "Brent Salisbury"
wp_id = 4820
categories = ["Speculative"]
tags = ["Cisco"]
description = ""
url = "/cisco-acquisition-of-cariden/"
image = "/wp-content/uploads/2012/11/Quantum_Information_Processing.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "82b4bf09b948dc1f9e15cf20a36afca7ded8ad2764a9f379ccc7707bfe63164a"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Cisco acquisition of Cariden</h2>
<span class="drop-cap">C</span>
isco announced today the intended acquisition of Cariden, a network management software company. Cisco will purchase the self-funded Cariden for $141 million. This deal is on the heels of two other Cisco acquisitions. The purchase of the WiFi company Meraki for $1.2 billion and the cloud software company Cloupia for $125 million. Cariden has built it's business from developing network management software targeting service providers. Cariden listed it's business partners as Alcatel-Lucent, Big Switch Networks, Cisco and Juniper.

Cariden marketing focuses on capacity planning and business intelligence. The Cariden website claims to deliver the "global view" of networks. In August Cariden announced its <a href="http://www.cariden.com/about/news/details/?id=170" target="_blank">blueprint</a> for Software Defined Networking (SDN). It targeted the keywords for the service provider SDN market like, computational path elements (CPE), controller interfaces and big data components like predictive analytics.
<h2>The Cariden Take on SDN</h2>
<blockquote class="pullquote">"A full battery of Network Controllers including an OpenFlow controller interface."<footer>Cariden Introduces Blueprint for Infrastructure SDN</footer></blockquote>

Reviewing the Cariden white paper "Infrastructure SDN with Cariden Technologies" reveals a company eager to enter into the new SDN ecosystem. They were featured in the BigSwitch press release as an analytics partner.  Big data analysis of networks is fairly handicapped in todays networks. The more the network operating system (NOS) are exposed by new primitives, the more available the extracted network data will be. Customers and vendors alike are seeing the promise of shifting away from only focusing on the ip prefix destinations and think along the lines of a more flexible flow based L2-L7 model to better integrate application awareness.
<h2>From the "Infrastructure SDN with Cariden Technologies White Paper"</h2>
<em>Looking at SDN through the prism of value reveals three distinct areas of interest:</em>
<ol class="legacy-numbers">
<ol>
	<li><em>Flow Services SDN that is closely tied to microflow visibility and programming made possible by OpenFlow</em></li>
	<li><em>Virtualization SDN that is closely tied to data centers and other multitenant compute-network environments</em></li>
	<li><em>Infrastructure SDN—Cariden’s focus—that is closely tied to providing visibility and control of network resources to software applications</em></li>
</ol>
</ol>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/11/Cariden-NOS1.jpg" >}}" alt="Cariden Network Operating System"></figure>

<em>Depending on the value proposition, distinct classes of SDN have emerged, and it is useful to view their unique missions and note the services for which they typically show their benefits:</em>


<ul>
	<li><em><strong>Flow Services SDN </strong>addresses the wealth of security and visibility applications that become possible with flow-level programmability</em></li>
	<li><em><strong>Virtualization SDN </strong>provides virtual network connectivity for efficiency and agility</em></li>
	<li><em><strong>Infrastructure SDN </strong>exposes network resources for continual optimization of resources and predictable handling of diverse traffic demands</em></li>
</ul>


<em>Three key, sometimes overlooked, requirements for the NS-OS that it needs to provide are the following:</em>


<ul>
	<li><em><strong>Centralized resource mediation </strong>such that there would be a single authoritative source for keeping track of resources and issuing them to various applications</em></li>
	<li><em><strong>Predictive analytics </strong>(anticipation of network behavior upon failure states or other “what if” scenarios) to enable applications to schedule resilient bandwidth resources into the future</em></li>
	<li><em><strong>Multivendor/layer interface </strong>that provides support for a wide range of infrastructure</em></li>
</ul>
<div><em></em></div>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/11/application.jpg" >}}" alt="Cariden Applications"></figure>
<em>Classifying SDN applications by the source of value they provide is useful in making sense of the many voices around SDN:</em>


<ul>
	<li><em>The first source of value is security and other services enabled by flow-level programmability; this is Flow Services SDN. </em></li>
	<li><em>The second source of value is virtualization, which can be termed Virtualization SDN. </em></li>
	<li><em>The third source of value is exposing programmability of network resources to software applications: Infrastructure SDN. </em></li>
</ul>
<div><em><em></em></em></div>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/11/cariden-analytics.jpg" >}}" alt="Cariden Analytics"></figure>
<h2>My Thoughts: The Cisco SDN Path Forward</h2>
If I had tried to get an explanation of SDN from the ONF, or an academic SDN purist, it would probably not deviate far from the the Cariden white paper. Cariden distinctly sees the value in a decoupled NOS from the underlying physical hardware. It saw itself as a intrinsic piece of the application ecosystem leveraging OpenFlow like primitives and controller APIs for path steering, instrumentation and application deliverables. I think their leadership and vision was on point and their selling price reflected that success.

Cisco has commited to the <a href="http://packetpushers.net/pq-show-015-cisco-hybrid-switching-and-onepk-sponsored/" target="_blank">onePK</a> roadmap both proprietary and open programmable APIs and some project both internal and <a href="http://nerdtwilight.wordpress.com/2012/03/27/ciscos-latest-spin-in-reportedly-poaching-aggressively-and-not-at-cisco-this-time/" target="_blank">external</a> around SDN. This is business analytics and predictive analysis that should be able to reactively or proactively adjust topologies or do more traditional functions such as reporting functionality with a focus on capacity planning and the economics of growth.

This will clearly be integrated into the SDN onePK and eventual Insieme portfolio, the only question is will it be vertically or horizontally. Three scenarios for not just Cariden's usage, but Cisco's holistic SDN strategy could be:

<ol class="legacy-numbers">
<ol>
	<li>At the least, this will be a new network management play that has long since been missing from Cisco's portfolio. Anyone in networking can tell CiscoWorks/NetRanger and every other vendors NMS horror stories. While the core focus is SP operators, according to the last graphic, Cariden was being positioned for the data center and enterprise space.</li>
	<li> The UCS business model to networking. Cisco will incorporate this into its onePK open, yet proprietary version of SDN. Just as UCS is only compatable with Cisco x86 hardware, the same would hold true for its northbound applications such as this. To this day, a holistic view of data center analytics remains out of reach to mere mortals. Capturing resource consumption and usage to correlate storage, compute and networking in the data center is valuable to all sizes of customer base.</li>
	<li>Cisco embraces the open tent SDN strategy and re-positions itself from a custom hardware company to a software focused company in some product lines. This becomes a pluggable application into the larger SDN ecosystem agnostic to the underlying networking hardware.</li>
</ol>
</ol>
The path is still fluid for everyone, including Cisco, but the fundamental goals should be getting sinking in. The vehicle we use to get there is much less important than arrival. Adding value in software to incentives hardware sales has been the path of x86 companies for the past decade. I feel abstractions and layering, will lead networks down a similar path at some point in time regardless of the vehicles; standards bodies or open source.

It is not a reflection on developers for the trail of useless network management products over the past decade. They have done as much as can be done with the archaic primitives in today's monolithic devices. The industry is showing surprisingly quick progress as they wait on hardware that can begin delivering the products. Seeing networking vendors taking it as seriously as they are with R&amp;D commitments and large acquisitions are quantifiable steps. More manageable and efficient networks to absorb the explosive <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">growth</a> mobility presents is critical in coming years. I would like to see Cisco focus more on the enterprise but they claim to see more <a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank">demand</a> currently from service providers and thus more focused on that revenue potential.

I like this acquisition, it is relevant to their core products even if the SDN evolutions is unceremoniously murdered. It is focused on adding value in software which has good margins and addressing customer pains in managing today's scattered networks.

The Cariden white paper that the excerpts came from can be downloaded courtesy of our friends at <a href="http://www.sdncentral.com/wp-content/uploads/2012/08/Infrastructure_SDN.pdf" target="_blank">SDNCentral.com</a>