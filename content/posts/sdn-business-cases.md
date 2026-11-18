+++
title = "SDN Use Cases"
date = "2012-05-23T10:35:29+00:00"
lastmod = "2014-02-08T05:12:20+00:00"
author = "Brent Salisbury"
wp_id = 588
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/sdn-business-cases/"
aliases = ["/2012/05/sdn-business-cases/"]
image = "/wp-content/uploads/2013/01/bad-decision1.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "974c6cef062fce5a18bc5acc6b422cf87c75043b3482d4f2da2fb92f63a68ac2"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN Use Cases</h2>
We have a few problems in networking. The following document are some SDN use cases that have come up over the past recent months/years. New abstractions in networking should enable solutions we never thought possible due to the monolithic nature of networking gear today (Mainframe 1980). This is all coming from a person who thinks MPLS can squeeze orange juice out of a lemon and am not a change for change sake guy.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/change-is-bad1.jpg"><img class="alignleft size-full wp-image-697" title="Change-is-bad" alt="" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/change-is-bad1.jpg" width="330" height="260" /></a>

I compiled some SDN use cases from some of the best in the industry which deserve credit (or deny association) helping me get to where I am today and  for facilitating conversations and provoking questions about the status quo. I might have even had an orignal thought or two regarding software defined networking and where we are and should be heading with SDN enablement.
<h2 class="legacy-heading">Today's Network</h2>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/05/sdn-osal-abstraction21.jpg" >}}" alt="OpenFlow Abstraction"></figure>

<strong>Figure 1.</strong> <em>We are missing the fundamental fundamental abstraction layers Operating Systems require for scale and coherency.</em> <em></em>We are operating far to close to the hardware to scale. While I love programming networks more than most things in life, there are major scale issues. If you are a company that has significant growth like Universities see with 2x growth annually on wireless and can scale engineering resources to support that, you are an outlier. Most of us cannot. Staff is staying flat or shrinking due to budgets reduction  while networks exponentially grow.

<ul>
	<li>Do systems administrators configure their services in x86 Bios? Guess what? We do.</li>
	<li>Generic components decomposed into resources to consume anywhere, anytime.</li>
	<li>Abstraction of Forwarding, State and Management.</li>
	<li>Forwarding: Networking gear with flow tables and firmware.</li>
	<li>State: Bag of protocols destruction.</li>
	<li>Management: Orchestration, CMDB etc. Join the rest of the data center (and world)</li>
</ul>

<h3>The Enterprise Network</h3>
The current “big picture” requirements the network (at my personal institution enterprise"ish" with some SP characteristics and a regional network around the state)

<strong>1.1.</strong> Routing and switching architectures and protocols.

<strong>1.1.1.</strong> Ability to quickly provision or reroute additional bandwidth and flow capacity. Raw capacity can be achieved by scaling out with Link Aggregation Groups (LAG), Multichassis-LAG(MLAG) and scaling up with interface upgrades to 10/40/100Gb, all leveraging Equal Cost Multi-Pathing (ECMP).

<strong>1.1.2.</strong> MPLS/VPN (RFC4364) support through LDP for label mapping and distribution on all Provider Edge(PE) nodes.

<strong>1.1.3.</strong> Support RSVP-TE extensions for signaling for inter-domain LSPs on all PE nodes. OAM functionality may be a need in the future from this path also.

<strong>1.1.4.</strong> Network Virtualization is delivered today at scale, via MPLS/VPNs at layer3 and MPLS/VPLS/Pseudowires at layer2. There are many other virtualization technologies but these are the de facto choice by the industry for ultimate scale on packet switched networks.

<strong>1.1.5.</strong> The ability to deliver these same virtualized services over service provider networks or the regional state owned network to remote customer premise sites around the state. This is accomplished by creating virtual circuits over other autonomous networks emulating local LAN circuits.

<strong>1.1.6.</strong> Support for typical enterprise technologies to support controller based 802.11(x), appropriate POE to edge ports and security measures on the ports to protect the network integrity and service delivery to name a few examples.
<h2>SDN in the Data Center </h2>
<strong></strong><strong>2.1</strong>. Continue down the path of 2-teir, spine-leaf topologies, to meet scale and capacity needs. More or newer spine nodes, may be required as East-West traffic continues to grow. Big Data clustering, will increase E-W traffic utilizations as North-South continues to proportionality decrease. Even more reason to avoid and 3-tier architectures and the need for spines to be feature rich.

<strong>2.2.</strong> Scale to the next tier of bandwidth 10/40Gb, as server buses can utilize those speeds or dense VM farms requiring large links and interconnects.

<strong>2.3.</strong> When TRILL becomes ratified by the IETF, begin migrating away from Spanning-Tree Protocol (STP) to TRILL. Avoid pre-standard vendor locks, but do procure network components that have TRILL support in hardware, as TRILL availability gets closer.

<strong>2.4</strong> Nicira looks to solve this problem by pushing the L2 adjacency problems to the hypervisor, tunneling or overlaying (debatable whether used interchangeably) over the physical infrastructure. I had someone say to me this week, "why would you want MPLS in the data center with NV-GRE and VXLAN?" Made me a sad panda or maybe just cranky. Thats another topic I reckon.

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/dci1.jpg" alt="Data Center Interconnect"></figure>

<strong>Figure 2.</strong> <em>Data Center Interconnects. Both are bad since bridging does not scale but data center and cloud mobility are driving these needs.</em>

<strong>2.4.</strong> Data Center Interconnects (DCI) is a very fluid topic. There are two appropriate options for out environment including cloud readiness and mobility. A deep pro and con analysis of the two following approaches are beyond the scope of this document.

<strong>2.4.1.</strong> Design aggregation encapsulation DCI points, between data centers and cloud providers on network spine nodes.

<strong>2.4.2.</strong> The second approach is having the software vSwitch within Hypervisors build those tunnel end points and perform the encapsulation in software.

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/management-plane.jpg" alt="SDN Management Plane"></figure>

<strong>Figure 3.</strong><em> Fabric is the backplane. </em>
<h2>Use cases for SDN broken down by 3 planes and a security section.</h2>
“Merchant Silicon” or “off the shelf” silicon, is where a networking hardware vendor will purchase pre-fabricated Chipsets, ASICs, NPUs, memory etc. rather than doing a fab or fab-less custom silicon build with a foundry. There are many reasons beyond the scope of this document as to why but they are all business decisions involving cost of R&amp;D, time to market and what I call “good enough” performance. The merchant silicon chip vendors such as Fulcrum, Intel, EzChip, Broadcom and a long list of others, have attained performance levels not quite at a custom silicon fabrication but “good enough”, to outweigh the economic and time to market penalties associated with going to a foundry for customization. This same business model has been the reality in the x86 market for over a decade. Even now vendors who have been perennially known for the custom silicon, are beginning to revise history with claims their company core values revolve around software. This is foundationally one of the big victories of a decoupled network OS from the hardware, it is the commoditization of software. If a company wants to purchase software from one commercial provider and purchase the hardware from another that has not been a possibility.

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/commodity-switches.jpg" alt="Commodity Merchant Silicon Switches"></figure>

<strong>Figure 4.</strong> <em>(Picture source: Greg Ferro, Etherealmind.com) Leading switch vendors all running the same Broadcom chipset in their low-latency data center Ethernet products. Each will have a different story justifying their price points. Those value propositions tend to revolve around firmware and software.</em>

<strong>3.1.</strong> Explore commodity hardware for not only edge customer facing switches but also PE distribution network nodes. This NextGen architecture must be able to scale in the following categories and ideally meet a 6-7 year hardware lifecycle.

<strong>3.2.</strong> In today’s service provider networks the intelligence is pushed to the edge of the network onto the PE nodes. The PE node is a very expensive piece of gear since it is applying policy and ingress/egress encapsulation and de-encapsulating. The ability to decouple the control plane, allows for a PE node hardware lifecycle to be less concerned with control plane features, and more focus on speeds and feeds being appropriately sized.

<strong>3.3.</strong> Decoupling the control and management plane from hardware reduces hardware down to a smaller denominator than we currently deal with in hardware evaluation.

<strong>3.4.</strong> In order to leverage networking hardware we need the ability to insert forwarding decisions made from software, presumably some sort of centralized or distributed controller. That would need to come in the form of an agent with an exposed API, running in either the NOS or firmware of a networking device.

<strong>3.5.</strong> Many vendors today support an SDN agent, in the form of OpenFlow v1.0. Some examples are Arista Networks, Brocade Communications, Cisco, Force10, Extreme Networks, Hewlett-Packard, IBM, Juniper Networks, NEC, Nokia-Siemens, Pronto Networks. There have also been new venture capital startups revolving around merchant silicon “white box” switches.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/05/tuple-11.jpg" >}}" alt="OpenFlow Tuples"></figure>

<strong>Figure 5.</strong> <em>A 10-Tuple field that could have an action taken supported in OpenFlow V1.0. MPLS label support was demonstrated at the Open Networking Summit in April 2012.</em>

<strong>3.6.</strong> The limitations in forwarding, for most switches shipping with the OpenFlow agent is TCAM row size. As next generation commodity ASICS and NPUs begin shipping with more memory capabilities the n-tuple matching abilities will increase. TCAMs are very powerful in application but also expensive and power hungry. We expect the dialogue around SDN will bring innovation to that market. TCAM operation is opposite of typical memory lookups. It performs a multi-match operation in one clock cycle and then forwards after classification to the next logic.
<h2>SDN and the Management Plane </h2>
<em>The irony when examining the management plane is that we already have an SDN of sorts deployed today. How is defining a flow datapath based on the first packet and inserting that flow into a forwarding base in TCAM, counting the statistics and terminating the session when it is complete and different from a typical VOIP manager deployment? VOIP example. Call comes in the controller establishes the connection, collect counters and hand the session of to the endpoints in a setup/teardown only role. This is very similar especially in the centralized management plane in wireless controllers that is the standard in wireless deployments today. What critical technology in an enterprise does not have centralized management except for the network components? Most shops are growing exponentially and staying flat or even decreasing staff. It is completely unsustainable.</em>

<strong>4.1.</strong> OpEx savings from centralized or distributed SDN controller management from troubleshooting, provisioning/de-provisioning, capacity planning and so on.

<strong>4.2.</strong> Configuration management has been pushed and failed repeatedly from SNMP to NetConf with a couple in between. The command line interface (CLI) differences between vendor operating systems is far to great, to have successful CLI scripting management products.

<strong>4.3.</strong> Collecting statistics in a central repository would and will be extremely valuable to service, cloud and content providers.

<strong>4.4.</strong> MPLS-TE (Traffic Engineering) is a big pain point for providers today. This allows for the exporting of the huge network statistic data sets to a Hadoop, Hana, Mongodb for analysis and decision making on how best to empirically route your traffic across LSPs.

<strong>4.5.</strong> Energy efficiency use cases for power conservation would be reasonably easy to implement if long periods of downtime were exceptable. An enterprise could programmatically turn down segments of the network across the campus, as students leave for vacation or faculty for holidays, based on port and switch usage.

<strong>4.6</strong>. Provisioned yet not used IP addresses, switch ports, VM instances are a problem with no solutions in site. These huge configuration management problems could be solved, by exploring the data usage based solely on framing headers. If 90% of a virtual machines traffic for the past 30 days is ARP broadcasts, it is likely safe to say based on policy, that the VM instance is soaking or even steeling precious centralized resources and requires de-provisioning.

<strong>4.7.</strong> Last and possibly most important, in our view, is not only the decoupling of the NOS, but the abstraction and integration in to the rest of the computing ecosystem rather than being on an island of rumors where it has been over the last 30 years. 4.8. Configuration Management Database. Centralization would allow for coherency in CMDB management. It would present network in a more manageable view to hand north to orchestration.
<h2>SDN and Security Use Cases </h2>
<strong>5.1.</strong> The mere fact that every flow could be exposed and aggregated to a controller(s) with IP headers is a security Ops dream. It is complete awareness at all degrees of traffic across an enterprise.

<strong>5.2.</strong> Today in order to do a deep packet inspection on a packet with any amount of reasonable scale you either put an in line tap or mirror a port. That has now attached you to the fire hose to parse through millions of packets per minute or even second to find the needle on the bottom of the ocean floor. That is completely cost prohibitive in most environments especially R&amp;E.

<strong>5.3</strong>. If we have flow visibility and control we can now pick out the needle in the stream based on a tuple or multiple tuples in the header and along with sending it out the egress destination port on a switch we also send another copy of that flow to an IDS for DPI. Now to see a flow(s) of interest, we do not need an IDS farm that scales up to 40-100Gb of aggregate traffic to parse through noise to get to the valuable data that is significant to our business.

<strong>5.4.</strong> This may be the only hope at a coherent path to a manageable network access control (NAC) framework. NAC is a total disaster of one failure after another in today's solutions. 802.1x on paper sounds great. The majority of 802.1x deployments never get past a logging or 'fail open' stage.
<h2>The Control Plane</h2>
<p style="text-align: center;"><em>The data plane is being lumped in this category since most NOS and network hardware have pushed the data plane in with the control plane to update the forwarding information base (FIB) for fast lookup for ingress traffic.</em></p>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/05/RIB-LIB-LFIB-FIB.jpg" >}}" alt="OpenFlow Tuples"></figure>

<strong>Figure 6.</strong> An example of ingress operation and table interactions. Each different base play a part in creating the FIB and LFIB (label forwarding information base).

<strong>6.1.</strong>If you took a traditional big chassis based distributed forwarding switch and decoupled each piece of it across a data center and replaced the supervisor with an SDN controller in software you would have an exact replica of one another logically but a completely decoupled architecture. *Note, that is almost exactly what the Juniper Q-Fabric data center solution is but with proprietary components and protocols.

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/sdn-controller1.jpg" alt="OpenFlow Controller"></figure>

<strong>Figure 7.</strong><em> The OpenFlow SDN framework is very similar to typical distributed forwarding chassis architecture. The fundamental difference is the I/O between the control and forwarding planes is done over an Ethernet fabric as opposed to buses on a backplane.</em>

<strong>6.2.</strong> Having the ability to programmatically determine forwarding paths based on header information has some benefit only if the value is being delivered from the application layer orchestrating the forwarding decisions.

<strong>6.3.</strong> The ability to act on any tuple in a header we could essentially provision and orchestrate devices quickly as a load balancer, firewall.

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/tuples.jpg" alt="OpenFlow Tuples"></figure>

<strong>Figure 8.</strong> <em>TCAM allows for matching with a 1 or 0 and a * “don’t care” mask bit. The TCAM cycle above would look like 111**111* for a match or 001**101* for not matching. (I may have butchered this image a bit, but I am swamped on time to fix atm.) I believe a correct combination of NPU, limited ASIC and increased external TCAM would provide huge value. More research required. I am avoiding asking NDA questions around this so I can speak to it.</em>

<strong>6.4.</strong> QOS policies that would be too complex to manage decentralized, could fall back into the realm of reality for shops already overworked by being managed programmatically.
<p style="text-align: center;"><strong>6.5.</strong> Equal Cost Multi-Pathing (ECMP) could be operated down to the flow and actionable on multiple tuples rather than just a destination address.</p>
<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/mpls-core.jpg" alt="SDN Path Steering"></figure>

<strong>Figure 9.</strong> <em>The ability to re-route traffic based on utilization is done at a rudimentary level with MPLS-TE (Traffic Engineering) but complexity and time spent brings a high cost. SDN could allow for this data to be heuristically analyzed and implemented, thus lowering operational cost and improving service delivery.</em>

<strong>6.6.</strong>The ability to programmatically divert traffic to different Label Switch Paths (LSP) based on any criteria is one the primary reason service and content providers are early adopters at this point. Google has begun putting OF links in production.

<blockquote class="pullquote">I think what we find exciting is OpenFlow is pragmatic enough to be implemented and that is actually looks like it has some legs and can realize that promise,” he said. However, he added, “It’s very early in the history and too early to declare success.” “We were already going down that path, working on an inferior way of doing software-defined networking,” says Hölzle. “But once we looked at OpenFlow, it was clear that this was the way to go. Why invent your own if you don’t have to?” “The cost that has been rising is the cost of complexity — so spending a lot of effort to make things not go wrong. There is an opportunity here for better network management and more control of the complexity, and that to me is worth experimenting with,” Hölzle said. “The real value is in the [software-defined network] and the centralized management of the network. And the brilliant part about the OpenFlow approach is that there is a practical way of separating the two things: where you can have a centralized controller and it’s implementable on a single box and in existing hardware that allows for a range of management and things that are broad and flexible.<footer>Urs Hölzle</footer></blockquote>

<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/google-sdn.jpg" alt="Google SDN"></figure>

<em><strong>Figure 10.</strong> Google’s current SDN implementation. This is a hybrid implementation along with MPLS/BGP/RSVP LSPs on the same paths.</em>

<strong>6.7.</strong> OpenvSwitch is an open source vSwitch that we will be leveraging in future production OpenStack deployments. This fills the networking component in our zero licensing cost data center and cloud orchestration strategies sought today.

<strong>6.8.</strong> Hypervisor integration is vital. Explore SDN integration into its OpenStack proofing through the OpenvSwitch project. SDN coupling with the Hypervisor may be the missing link in data center orchestration.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/05/data-center-orchestration.jpg" >}}" alt="Data Center Orchestration"></figure>

<strong>Figure 11.</strong><em> Broken provisioning and de-provisioning workflows today.</em>

<strong></strong> <strong>6.9.</strong> Cloud and application mobility challenges in security, mobility, profiling

<strong>6.10.</strong> Applications, whether rolled in house or purchased as bolt on modules from vendors, will be the key ingredient to value differentiation.

<strong>6.11.</strong>Network virtualization implementation to scale is delivered today, via MPLS/VPNs described in RFC4364. Extensions in MP-BGP distribute customer tags to other PE nodes in the MPLS domain. Multi-tenancy controller implementations can be instantiated into SDN networks by creating slices. The GENI FlowVisor project can possibly provide that functionality and one step further would be self provisioned slices while the network substrate is managed globally by a central entity.
Would a provider role look like this?

<ul>
	<li>Initial slice provisioning, group, UID, RBAC to gear/APIs.</li>
	<li>Software life-cycling.</li>
	<li>Global port allocation</li>
	<li>Allocate inter and intra bandwidth allocations for slices. Would analytics not take care of the rest? Sliver or tenant users/administrators should be able to input their application priorities and profiling as opposed to the 'global administrator'.</li>
</ul>

<p style="text-align: left;"><strong>6.12.</strong> The benefit of consolidation around the OpenFlow protocol besides standardization, is that it is not a reinvention of the wheel in a new encapsulation that will require completely different hardware standards, but has interoperability and investment protection to manufacturers and customers.</p>
<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/geni.jpg" alt="OpenFlow Slicing"></figure>

<em><strong>Figure 12.</strong> Example of leveraging the GENI FlowVisor project or a commercial product as the develop and extending SDN agent API(s) to the KyRON (State of Kentucky's Regional network) routers (Typical R&amp;E type hierarchies). I would expect commercialized projects to begin hitting the market for multi-tenancy towards the end of 2012 leveraging northbound APIs.</em>

<strong>6.13.</strong> Planning needs to encompass the statewide network and the ability to reach Internet2 to facilitate researchers.
<h2>SDN Challenges </h2>
<p style="text-align: center;">This list could go forever but bottom line is networks are growing exponentially while operational budgets are not. We either reduce services or SLAs or ignore the problems and what for desperate, reactive change.</p>
<figure class="legacy-figure"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/vmvssdn.jpg" alt="VM SDN"></figure>

<em><strong>Figure 13.</strong> These are not new ideas. Integration of the network the network into the ecosystem is glaringly absent industry wide.</em>

<strong>7.1.</strong> Control plane scale in flows per second. This is up to vendors to innovate in hardware lookup tables.

<strong>7.2.</strong> Controller software. Our SDN path as a production service provider must be one that is commercialized products delivering robust networking scale and operational support. <strong>7.3.</strong> We can do much of the forwarding decision making today with existing IGP and EGP routing protocols.

<strong>7.4.</strong> Consolidation from vendors around standards based protocols. Routing and signaling protocols work today because they are standardized.

<strong>7.5.</strong> A migration path is essential. We have production networks where we must be able to interoperate and deliver services during a proofing or migration phase. Fortunately the majority of the networking gear supporting SDN has the ability to isolate SDN Vlans from native routing and witching Vlans. This enables a multi-tenant environment with test and development, along side production networks.

<strong>7.6.</strong> TCAM sizing- The HP Procurve switches we have for proofing can support a 7-tuple match. The limitation on that hardware is it does not have enough bits in its Ternary Content Addressable Memory (TCAM). This is being addressed in future switch releases with added capacity. The missing 3 tuples are source and destination layer 2 headers and the ethertype field, since all ethertype are assumed to be IP on that platform currently. External TCAM sources on the switch will improve flow table sizes. Here is a slide deck on some of the topics. Feel free to take anything out of it. I used other peoples slides for some of it. <a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/brent-openx-v1-1.pptx">SDN-Slidedeck</a>