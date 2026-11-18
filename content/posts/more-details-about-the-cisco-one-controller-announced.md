+++
title = "More Details About The Cisco ONE Controller Announced"
date = "2013-02-05T00:29:30+00:00"
lastmod = "2014-02-18T02:54:48+00:00"
author = "Brent Salisbury"
wp_id = 5707
categories = ["Speculative"]
tags = ["Cisco", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/more-details-about-the-cisco-one-controller-announced/"
image = "/wp-content/uploads/2013/02/Paul-Baran-Distributed-Comm-Systems.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "51eaaedccbbd9d4bd4bc9cf8a4c2df0e12013e06fc194a04cbc8741ba30f8140"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>More Details About The Cisco ONE Controller Announced</h2>
Cisco has begun further unveiling more details about the Cisco ONE controller, currently in early beta. The announcement, specifies new SDN applications and hardware support for a select few existing products and new ones like the Catalyst 3850. Also recently announced, is the new <a href="http://www.networkcomputing.com/data-networking-management/cisco-nexus-6000-first-impressions/240147690" target="_blank">Nexus 6000</a> switching product, along with a NAM module for the Nexus 7000. The Nexus 6000 is 96-ports of 40Gb low latency data center switch. Lastly, the Nexus 1000v support for Hyper-V integration into Microsoft System Center VM Manager and VXLan gateway support, both calculated moves in high stakes, data center virtualization chess. The big announcement is the software and will be for some time to come. With the Open Networking Summit coming up in April, it isn't far fetched to expect the Java open source controller from the "<a href="{{< relurl "/more-vendors-define-their-sdn-strategy/" >}}" target="_blank">Daylight</a>" multi-vendor consortium to be announced relatively soon.

<h2 class="legacy-heading">Key Cisco ONE Controller Announcements</h2>

<ul>
	<li>A new Cisco ONE Software Controller supports a highly available, scalable and extensible architecture; the industry’s first multiprotocol interfaces with One Platform Kit (onePK) and OpenFlow; consistent management, troubleshooting and security features; and built-in applications that include network slicing functionality for enabling logical partitioning of network resources. In addition, the ONE Controller will interact with Cisco networking applications such as Custom Forwarding and Network Tapping.</li>
	<li>Expanded platform support for Cisco onePK developer environment with Nexus 3000, Nexus 7000 and ASR 9000.</li>
	<li>Solutions for overlay networks including Nexus 1000V support for VXLAN Gateway; Nexus 1000V support for Microsoft Hyper-V and integration with Microsoft System Center VM Manager; virtual Network Analysis Module (vNAM) for network analysis and monitoring of virtualized and oud geoud workloads</li>
	<li>Expanded platform support for OpenFlow with Nexus 3000, Nexus 7000, ASR 9000 and Catalyst 6500.</li>
</ul>

<h2>The Cisco ONE and OpenFlow</h2>


Cisco has publicly committed to supporting OpenFlow since its announcement of the onePK last year. In order to do flow based forwarding, it only makes sense for consumers to expect a common mechanism to interact with hardware. The value should be well up the stack, but to get a proper stack, software developers need a common set of primitives.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/cisco-one-controller.png" >}}" alt="Cisco One Controller for OpenFlow"></figure>

There are some glimpses of deployment strategies from Cisco. Anything other than niche cases appear to be leveraging <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">proactive flow instantiation</a>. Reactive models on the above diagram allude to embedded systems.

<blockquote class="pullquote">“We want to meet developers where they are—this is not a controller tied to any particular technology,” said Shashi Kiran, senior director of data center and cloud networking at Cisco. “OnePK can take advantage of our hardware features [but] OpenFlow needs to work against a more abstract switch model,” <footer><a href="http://eetimes.com/electronics-news/4406200/Cisco-packs-ASICs-at-40G--phbraces-OpenFlow">EETimes.com</a></footer></blockquote>

OpenFlow support will be delivered alongside the proprietary APIs through the onePK development kit, residing as firmware on the network device. Early OpenFlow agents are available under NDA on the Nexus 3000.
<h2>Cisco ONE Applications</h2>
Cisco and others developing OpenFlow controllers are all focused on delivering applications north of the controllers. This is the promise of SDN, applications and APIs to automate and manage networks more efficiently. OpenFlow by itself offers nothing other than a mechanism to have a blank canvas to instantiate forwarding. Applications are the key to provisioning this policy. Cisco joins a small group of vendors, with beta SDN controllers in early customer trials today. Cisco is openly discussing a <a href="{{< relurl "/more-vendors-define-their-sdn-strategy/" >}}" target="_blank">hybrid approach</a> to OpenFlow which should translate into native and OpenFlow pipeline integration. The hybrid SDN working group at the ONF appears to have disintegrated. This is going to leave much more of architecture definitions up to the community, not the pay community 1%ers, but the real community of architects and engineers who are dealing with real problems.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/cisco-one-controller-openflow-hybrid.png" >}}" alt="Cisco ONE OpenFlow hybrid Strategy"></figure>


<ul>
	<li>In the onePK slide below, Data Plane instantiation are handled with OpenFlow.</li>
</ul>


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/cisco-one-controller-openflow.png" >}}" alt="Cisco ONE OpenFlow Controller"></figure>


<h2 class="legacy-heading">Three applications announced</h2>
<ol class="legacy-numbers">
<ol>
	<li><strong>Network Tapping</strong> - This has become the low hanging fruit in the OpenFlow controller market. Big Switch has a similar product Big Tap. This application was arguably conceived from the FlowScale project that came out of research and education. When matching traffic and adding an action it is fairly easy to add another port to the forwarding action. This should make those in the security blackbox market nervous.</li>
	<li><strong>Custom Forwarding</strong> - Path steering is L2-L4 policy based routing on steroids. Traffic engineering today is carries significant management overhead for traffic classification and link coloring. Path steering using OpenFlow offers new tools to have granular control.</li>
	<li><strong>Network Slicing</strong> - This is another unique space from commercial vendors to delve in to. This  is flow based multi-tenancy. Setting up multiple flow spaces allows for a new form of network virtualization. The controller or slicer is now the arbiter of multiple tenancies instantiating flows. This concept came from the GENI R&amp;E project from the FlowVisor application.</li>
</ol>
</ol>
It is worth noting, that much of heritage of these applications source from academia and NSF funded projects. While at times research and education loses its way, it is encouraging to see such relevance again.

<h2 class="legacy-heading">My Thoughts</h2>

Cisco appears to be split into two camps, hardware and software. The custom silicon path at some point will likely taper down over the next few years as general purpose usage, reserving custom ASICs for more niche applications. The ONE seems to be the chosen platform for Cisco's future of networking.

Still in stealth is the Cisco funded Insieme. Presumably at some point, Insieme point be spun back in with a product. I think what comes out of Insieme should be software, but clearly Cisco is still going after the hardware differentiation for now. There will undoubtedly be a software component with that, how that will integrate into the ONE controller will be interesting.

One potential pain point is, the apparent absence of the Catalyst 3750-X in the supported hardware roadmap. The ONE controller was <a href="http://newsroom.cisco.com/press-release-content?articleId=892363" target="_blank">announced</a> in June of last year, claiming support for the Catalyst 3750-X. That appears to no longer be the case. This will disappoint some, since that is an easy to come by switch, that would serve as early lab and POC development. Also, existing hardware support is important for many IT budgets. Lastly, there needs to be more POE enabled OF switches. Almost everyone to a tee, has top of rack OF enabled, DC switches with Trident+ chipsets, but the vendor support falls in half when it comes to edge switches with POE support. 

The 3750-X product line is way to new to be written off as being capable of supporting OpenFlow. I am pretty sure, the <a href="http://www.openflow.org/wk/index.php/Configuring_HP_Procurve" target="_blank">HP 3500yl</a>, has less hardware capability under the hood than the 3750-X and it has had a OF agent for almost two years now. It would seem investment protection is lacking in that product line, if SDN development on that platform has halted to presumably focus on the <a href="http://searchnetworking.techtarget.com/feature/Cisco-Live-London-Uncle-John-promises-to-fix-Cisco-security-strategy" target="_blank">Catalyst 3850</a>. I hope to see the 3750-X reappear. I have an inquiry in to Cisco on this and will update as I hear back.

<blockquote class="pullquote">Cisco will provide proof-of-concept OpenFlow v1.0 agents on the Cisco Catalyst 3750-X and 3560-X Series Switches. <footer>Cisco Announces Open Network Environment to Unleash Application-Driven Network Programmability</footer></blockquote>

Proponents of the networking industry putting proper abstraction layers in place argue that current constraints do not offer enough forwarding flexibility. The march up the networking stack for business aware networks requires more routing prefixes. The simplest conceptual method needs to be loosely agreed upon as a forwarding abstraction. That does not necessarily mean the best, since that often turns into never getting anywhere. "Good enough" worked in the x86 world and will also work in networking. That is the importance of OpenFlow.

Introducing software into networks will create more efficiency but will also create a great deal more complexity not less. For better or worse, the business requires more flexibility that can no longer be delivered with strictly monolithic devices. The foundation needs to be as simple as possible, in order to support the layers of software that will rest atop. It is easy for some to be flippant and dismissive of OpenFlow. I don't by a car based on the wheels, but I tend to prefer my cars to have wheels. If not OF then what? Another 5 -10 years to amass support around the perfect wire protocol seems unlikely. Cisco at the very least is hedging their bets. Clearly there are some within Cisco taking risk and evangelizing evolution.

I have used this product in beta, obviously under NDA. I can say, I like it. Cisco is figuring out how to embrace an open wire protocol, while attempting to not commoditize their products. In order to start <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies/" >}}" target="_blank">designing</a> and architecting SDN networks outside of DevOps environments, consumers need commercial products, with commercial support. onePK is to OpenFlow what the FabricPath pre-standard is to Trill. That is added value and agile applications. Support the basics and add proprietary values in the form of network management and customization. Cisco did this remarkably well in the x86 market with UCS. 

Another card yet to be played, that Cisco is holding is the well established optical BU. There are few companies that can run the entire L1-L7 stack. Optical integration represents programmatic <a href="{{< relurl "/plexxi-capacity-planning-done-right/" >}}" target="_blank">bandwidth on demand</a>.

Overall, Cisco has stuck to its commitment and stayed within the ballpark on its timelines of delivering its SDN strategy. Cisco is supporting OpenFlow in a controller, regardless of speculation, the proof is in the products. Times are changing and so is Cisco, this is another brick in the road to abstraction. 

<h2 class="legacy-heading">Additional Analysis</h2>

<aside class="legacy-callout">
<a href="http://www.networkcomputing.com/virtualization/ciscos-one-controller-debuts-targets-sdn/240147798" target="_blank">Cisco's ONE Controller Debuts; Targets SDN</a> -Network Computing
<a href="http://www.networkworld.com/news/2013/020413-cisco-nexus-266361.html" target="_blank">Cisco fills out SDN family with 40G switch</a> -Network World
<a href="http://cdn.eetimes.com/electronics-news/4406200/Cisco-packs-ASICs-at-40G--embraces-OpenFlow" target="_blank">Cisco packs ASICs at 40G, embraces OpenFlow</a> -EETimes
</aside>