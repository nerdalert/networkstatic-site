+++
title = "Software Defined Network (SDN) -Looking Toward 2013 - Part 2"
date = "2012-11-27T03:19:50+00:00"
lastmod = "2013-04-06T23:05:06+00:00"
author = "Brent Salisbury"
wp_id = 4554
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/software-defined-network-sdn-looking-toward-2013-part-2/"
image = "/wp-content/uploads/2012/11/standards.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "53f93de99680c9ecdb5a1b6ad45be8a035cf90de089513f96d58f0d2c59a216a"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Software Defined Network (SDN) -Looking Toward 2013 - Part 2</h2>
In the second part of the two parter I am looking at some of the softer sides of the networking futures and what I expect to see in the coming year. Click <a href="{{< relurl "/software-defined-network-sdn-looking-toward-2013-part-1/" >}}" target="_blank">here</a> for Part I.
<h2>SDN for HyperScale and Everyone Else</h2>
Today Google back-hauls their inter-data center traffic using its implementation of OpenFlow called G-Scale. While a fairly fixed set of flow patterns they have so far been the largest example of  an SDN extracted control plane deployment to date.

<blockquote class="pullquote">OpenFlow is the most significant change to the networking game since he first came to Google more than a decade ago. -Urs Hölzle Senior VP of technical infrastructure and Google Fellow <a href="http://www.wired.com/wiredenterprise/2012/11/big-switch/" target="_blank">Wired</a> 13 Nov 2012.</blockquote>

Others, such as large carriers are very focused on CapEx reduction. Read how the Service Providers have approached SDN in a white paper from IETF85 summarized <a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank">here</a>.

For the rest of the world, which makes up an overwhelming majority of the market-share, most are waiting to see what comes out the door as a polished product. There is still much confusion consumer and vendor a like how SDN deployments would occur in a hybrid fashion.

Economies of scale saving are just that, significantly less at smaller scale. Outside of hyper-scale, white box CapEx savings are not as important or significant due to scale as more traditional needs. Vendor support, performance and availability for hospitals, finance, manufacturing and most service providers will top the list. Networks and services down mean lost revenue, production and lives. The incessant desire to reduce cost by all means requires much more discipline and process than most can achieve. Before you can run a hyper efficient business like Amazon, the aforementioned fundamental core metrics need to be 5-star across the board. Walk before you run.

<h2>NetOps and DevOps</h2>

NetOps is a term being thrown around by marketing and cloudy pundits wanting to wrap the promise of SDN into a sales deck. DevOps is still in incubation but it's roots come from agile software development life cycles being applied to infrastructure provisioning. At worst this is the combination of buzzwords like IaaS, Cloud and SDN all being mashed together into one big fail sandwich.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/devops-netops.jpg" >}}" alt=""></figure>
<strong>Figure 2. </strong>Programmatic APIs providing hooks into primitive network elements will enable agility in service and product provisioning.

How the life-cycle will apply to networking is the blending of networking into storage and compute. If you are a really big shop you can fire enough people to automate everything is a not the case. Operators will focus more on much needed policy and orchestration, rather than the repetitive insanity of pushing policy state to scattered systems. This same cycle happened with x86 virtualization. SDN at it's worst failure will at the very least provide proprietary APIs to do more automation. That said, SDN is not only about automation, that is vendors looking to redefine what is needed and protect market-share.

Developers and operators hand in hand spreading good will all over the network. We have been hearing silo tear downs since the advent of the "converged fabric". The only technology that will bring that is removing the human element, but we still have another few decades until <a href="http://en.wikipedia.org/wiki/Technological_singularity" target="_blank">singularity</a>.

<h2>What Does OpenStack Mean to Networking?</h2>

Some of us have held a position for a while that the direction and process that is happening in the OpenStack community is a prelude to what the networking industry will be facing at the large scale provider layer. It is open source, shared and forces differentiation in areas of business that actually count like customer service, price, SLAs etc rather than proprietary protocols, extension, encaps, APIs or anything else that is not directly serving the business.

<blockquote class="pullquote">What is OpenStack Quantum?
Quantum is an OpenStack project to provide "networking as a service" between interface devices (e.g., vNICs) managed by other Openstack services (e.g., nova).<footer><a href="http://wiki.openstack.org/Quantum">OpenStack Wiki</a></footer></blockquote>

OpenStack is a global collaboration of developers and cloud computing technologists producing the ubiquitous open source cloud computing platform for public and private clouds. The project aims to deliver solutions for all types of clouds by being simple to implement, massively scalable, and feature rich. The technology consists of a series of <a href="http://www.openstack.org/projects/">interrelated projects</a> delivering various components for a cloud infrastructure solution.

OpenStack Quantum, headed by Dan Wendlandt of Nicira/VMWare is a prime example of how networking can blend into the rest of the computing world with software abstractions. Vendors will and are modeling their orchestration solutions after this blueprint. Just as the applications world has been living in an API driven environment, so will networking begin to think along these lines. An example would be inter-domain orchestration. BGP extensions will only get us so far. Concepts like Alto and IRS in the pipeline, AS to AS interactions will be happening pragmatically via APIs on x86 hardware, not from the tired CLI UIs we have used for 20 years.

If the world becomes driven by open source projects rather than standards, the OpenStack model will be the future of networking standards. I am not sure I would bet against this from happening either. As standards bodies become <a href="http://tools.ietf.org/wg/trill/" target="_blank">less</a> agile and the end of the monolithic networking hardware comes near, Horizontalization will begin taking hold. We are trending behind compute by a decade. It may be worth tracking the OpenStack project, for a possible prelude to networks.


<h2>Closing Thoughts</h2>

The path forward conceptually has already been paved by other areas of <a href="{{< relurl "/sdn-apis-this-all-feels-pretty-familair/" >}}" target="_blank">computing</a>. Networking will continue to merge into computing. This shift in methodologies, makes it fairly reasonable to predict that where networking will head next. The outcome of the current data center "stack wars" will likely prelude what happens with networking.

<strong>SDN Trends I Expect In 2013:</strong>

<ol class="legacy-numbers">
<ol>
	<li>OpenStack becomes the de-facto for cloud providers as an Open Source standards body.</li>
	<li>Cisco UCS goes head to head with VMWare. UCS bills advantage of being hypervisor agnostic.</li>
	<li>Hyper-scale networking lean towards pure commodity or even whitebox switches, much like Facebook builds their own custom <a href="https://www.datacenterknowledge.com/archives/2012/06/27/facebook-server-storage-designs/" target="_blank">servers</a> today. switches look more towards the Broadcoms with primitive APIs rather than the OEM partners. These are organizations that save millions on a 1-point delta in a PO.</li>
	<li>The rest of the world continues buying from traditional vendors and leverage finished SDN products rather than rolling their own applications leveraging exposed APIs.</li>
	<li>Network management and automation are marketed under the guise of SDN.</li>
	<li>Incumbents turn to standards bodies, while disrupters turn to open source.</li>
</ol>
</ol>
<div>Not only does the network need to get <a href="{{< relurl "/sdn-and-openflow-quotes-from-some-of-the-best/" >}}" target="_blank">out of the way</a> but IT as a whole, needs to get out of the way of business and be an enabler, not a roadblock.</div>

<hr />

For more information regarding the Open Networking Foundation (ONF) Forwarding Abstraction Working Group (FAWG) Curt Beckmann the Chair of the FAWG working group recently did an update for the community. I will update this post with a link as soon as it posts.

<h2>Prologue</h2>

As I was finishing this post, I was chatting with my friend and fellow blogger <a href="http://blog.ciscoinferno.net" target="_blank">Anthony Burke</a>. A mutual friend of ours relayed a bad day he was having.

<ul>
	<li>Friend: Someone fat fingered a core router</li>
	<li>Friend:Then rolled back.</li>
	<li>Friend: Ops rolled back with an old config.</li>
	<li>Friend:Now everything f*****.</li>
</ul>

We both empathized with him because this is the peril of our beloved industries technology today. While some proclaim that distribution is the only path forward, current mechanisms are quickly being outpaced by growth. Processes alone cannot scale and operate networks.

This is a product of human involvement without proper programmatic abstractions and has happened to anyone in network dozens if not hundreds of times. It human error avoidance does not discriminate, even the most disciplined in process like <a href="http://aws.amazon.com/message/65648/" target="_blank">Amazon</a> and <a href="http://www.networkworld.com/news/2012/080412-microsoft-blames-last-week39s-azure-261402.html" target="_blank">Azure</a> are vulnerable.

We have no central programmatic control over the network today outside of cobbled together homegrown applications. There is a lot of money to be made in the application layer, that most <a href="http://packetpushers.net/why-network-engineers-are-sick-of-sdn-and-what-vendors-can-do-about-it/" target="_blank">vendors</a> took the wait and see approach in 2010-2011 and began scrambling in 2012 with resources and acquisitions.

<hr />
Thanks for stopping by.
<hr />