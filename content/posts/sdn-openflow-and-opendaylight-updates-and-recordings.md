+++
title = "SDN, OpenFlow and OpenDaylight Updates and Recordings"
date = "2013-04-29T02:27:34+00:00"
lastmod = "2014-02-18T02:52:33+00:00"
author = "Brent Salisbury"
wp_id = 6429
categories = ["Study Time"]
tags = ["Intel", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/sdn-openflow-and-opendaylight-updates-and-recordings/"
image = "/wp-content/uploads/2013/04/stop-cant-do-it-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "5873477dd2ff9e557964127f3efc4bfcc0bef48f76826a6367666afa44dcf69e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN, OpenFlow and OpenDaylight Updates and Recordings</h2>
It's been a busy few weeks in the SDN debate. I am posting some SDN updates from April along with some recordings from various events. The Open Networking Summit held its event. Only a few of the videos have posted so far. The keynotes and presentations that stuck out to me were, Rose Schooler from Intel, Bruce Davie from Nicira/Vmware, Nick Mckeown, Rob Sherwood from BigSwitch and most importantly the OpenDaylight technical steering committee (TSC) Q&amp;A.

<hr />

<h2>OpenDaylight Q&amp;A Audio Recording</h2>
The highlight of ONS and hands down the entire year is the OpenDaylight consortium. The project is open source (OSS) where each vendor has one vote. Value is measured by quality and quantity of code. Measuring a vendors contribution to the OpenDaylight project is quite easy by looking at the <a href="https://git.opendaylight.org/gerrit/gitweb?p=controller.git;a=log" target="_blank">ODP project commits</a>. The days of SDN message control and closed circles has served its purpose but will fade in relevance. Hard to compete with OSS without a large tent and community support. OpenStack set the course for networking and incumbents seem to be learning from OpenStack misses. Point in case, Cisco starting OSS consortiums rather then Vmware avoiding OpenStack until post Nicira acquisition.

<hr />

The audio is from my handheld recorder so quality is what it is. I think its fairly listenable though.

<hr />


<a href="{{< relurl "/wp-content/uploads/2013/04/OpenDaylight-QA.mp3" >}}" target="_blank" rel="noopener noreferrer">Download OpenDaylight Q&amp;A from ONS 2013 Audio</a>

<hr />

In my opinion, this is what will take SDN from closed and siloed planning, that focuses on data center and cloud, to a community effort that anyone who wants to contribute now has the opportunity. Some of the members of the TSC have impressive track records of OSS contribution and understand the model well.

While this does presumably reduce the number of controller platforms early, this doesn't bother me early on. In order to transition from talk and hype, it requires code and working products. To get there, we need a platform that everyone can focus interoperability efforts on. Otherwise the fragmentation would hurt margins and slow adoption. Once standards are truly agreed upon, differentiation will be abundant in the application. Pluggable north and southbound offers vendor opportunity while still allowing the consumer to transition away from vertically integrated products if they so desire. Regardless of the semantics of comparing networking to computing, we are transitioning similarly to those markets. Microsoft is developing office for IOS and Android. That's a pretty big signal the OS/platform is irrelevant.

While every vendor has their own strategic interests to be involved in ODP, I am impressed and optimistic on success. The transparency is aggressive and it will allow for scrutiny of any company sandbagging or worse aiming for derailment. Vendors will still pursue vertical integration wether through management plane or pre-standards. That is fine with me. If a company's <a href="http://etherealmind.com/sdn-use-case-firewall-migration-in-the-enterprise/" target="_blank">use case</a> decides the value outweighs the mousetrap. The litmus test is interoperability. OpenFlow is still the key to that component for edge ingestion and classification.
<h2>SDN and Consistency Models</h2>

<hr />

I am also posting some recordings from a recent Internet2 meeting in DC. The vendors are Cisco, Juniper and Brocade. The recordings are pretty reflective of current vendor strategies at the moment. One day they are talking about the great things coming and the next is explaining why SDN is too hard and networks will become so fragile they will fail. I would simply counter that by quantifyng how fragile networks are today. We build systems and networks to fail. To say SDN is going to break because of poor software stability, is to have not been on the other side of a TAC call to AsiaPac lately. Waiting on an outsourced developer to compile an engineer drop of firmware to fix one of the hundreds of RFCs required to run thousands of distributed control planes. The consumer happens to be pretty smart these days. No need to warn us of the perils of SW.

Vendors are beginning to beat the consistency model fear drum. In networking we essentially use two components from distributed systems theory; eventual and immediate consistency.
<h2>Eventual Consistency in SDN Networks</h2>

<hr />

<a href="http://en.wikipedia.org/wiki/Eventual_consistency" target="_blank">Eventual consistency</a> - When a change in state occurs all elements will "eventually" become consistent with one another. The Internet operates in this fashion via BGP. Intra-domain updates also occur in this manner.
<h2>Eventual Consistency in SDN OpenFlow Networks</h2>

<hr />

Proactive OpenFlow flow policy operates using an eventually consistent model. The forwarding element comes online, attaches to a controller and the controller installs state into the switch via OF flowmods. Once state is pushed into the switch, the switch can be disconnected since the only thing that will remove proactive flow rules with idle and hard timers of zero is a reboot or another flowmod deleting all flows on the element. Proactive is a logical early migration approach since conceptually it is no different from a routing engine receiving updates from a neighboring switch via OSPF, BGP, etc.
<h2>Immediate Consistency in Current Generation Networks</h2>

<hr />

<a href="http://en.wikipedia.org/wiki/Immediate_consistency" target="_blank">Immediate consistency</a> - When updates occur, they are visible to all participants immediately. An example of immediate consistency in today's networks are wireless controllers and VoIP controller headends. When a phone or an AP boots up and attaches to a controller and has immediate consistency upon attachments. This is because all state resides centrally.
<h2>Immediate Consistency in SDN OpenFlow Networks</h2>

<hr />

In Openflow immediate contsistency occours when running the controller with a reactive flow policy. Since no state is stored in the forwarding element, just as in the previous examples, when a switch attaches to an SDN controller, state is immediately consistent.

<hr />

Both deployment models have pros and cons. Proactive is the logical first step since that is how we operate networks today. The difference being a reduction in control points into a decentralized model rather then a fully distributed model. That allows for graphing into NIBs for forwarding policy abstraction. That is all realistically still pretty far out. Near term is enabling OF on the network edge essentially replicating what is taking place in data centers today. Just as simple services like security are distributed to the DC edge in vSwitches, that same model is fairly easy to setup in the PE or access closet edge switch.

<hr />

Q. What is the table miss policy in <a href="http://openvswitch.org" target="_blank">Open vSwitch</a>?
A. <a href="{{< relurl "/hybrid-openflow-using-the-normal-action/" >}}" target="_blank">OFPP_Normal</a>.

<hr />

Once your SDN island is established, you can then integrate it into the native network. Some examples of island integration are the following.
<ol class="legacy-numbers">
<ol>
	<li><a href="http://www.networkcomputing.com/data-networking-management/openflow-test-deployment-options/240152428" target="_blank">Gateways</a> - Gateways have a bad connotation from data center chokepoints. Gateways could be as simple as a pair of PE or distribution nodes.</li>
	<li><a href="{{< relurl "/hybrid-openflow-using-the-normal-action/" >}}" target="_blank">OFPP_Normal</a>. I like normal for the flexibility of both native and OF paths in one box.</li>
	<li>Much more interesting integration comes in the form of <a href="https://sites.google.com/site/routeflow/" target="_blank">RouteFlow</a> cutting RIB-&gt;FIB-&gt;Flows.</li>
</ol>
</ol>

<hr />

More on reactive and proactive flow policy: <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank" rel="noopener noreferrer">OpenFlow: Proactive vs Reactive Flows</a>

<hr />

Recordings of the Internet2 session. Warning, lots of FUD. It appears the vendors will captiualte once they see our networks running SDN and OpenFlow. All vendors have an open invatation to swing by my office and I can show them 1,000+ production OpenFlow ports. Not just a seperate physical network either, DNS, E-mail lots of short lived flows all mixed in with the general Facebook, Youtube, NetFlix and general surfing traffic. There are some believing existing gear should be ripped and replaced. They are probably the same that scoff at hybrid networks. Most of these folks haven't operated networks in 20 years if ever. Not to say they aren't brilliant, but ideal and realistic are on opposite axis. In my opinion, to say there is not any incremental SDN path short of forklifting kit will slow progress towards adoption. I have heard there are networks outside of Google, Amazon and Facebook believe it or not.

Apologies for poor audio here also. The recording was from a laptop in the audience recording. May cause nerdrage.

<hr />


<a href="{{< relurl "/wp-content/uploads/2013/04/Internet-OpenFlow-SDN-Part1-Amp.mp3" >}}" target="_blank" rel="noopener noreferrer">Internet2 Vendor SDN Audio Session Part 1</a>

<hr />


<a href="{{< relurl "/wp-content/uploads/2013/04/Internet-OpenFlow-SDN-Vendors-Part2-amp.mp3" >}}" target="_blank" rel="noopener noreferrer">Internet2 Vendor SDN Audio Session Part 2</a>

<hr />

<h2>Intel at the ONS</h2>
The Sea Cliff reference switch containing the FM6000 chipset from the Fulcrum acquisition is probably hands down the best OpenFlow capable chipset on the market today. That is the only chip I am aware of that can perform flowmods in the OF pipeline. Other multi-table pipelines can just perform accrued actions once at the end of the pipeline and would require re-circulation to execute a second action-set. The also anounced a partnership with Vmware that would allow for Nicira/Vmware NVP flowmods to the Intel DPDK (datapath dev kit). That could be quite interesting.
<hr>
There are not many videos posted from the ONS so far, but of the ones up so far, Rose Schooler from Intel is worth watching. They clearly have their eye on owning the entire physical fabric, end to end.

<hr />

<p><a href="http://www.youtube.com/watch?v=wdPh2WP-47g">Watch video on YouTube</a></p>

<hr />

If my future was edge hardware, I would be transitioning to services ASAP. Intel is an organization that has done this before. Application specific datapath hardware will continue to get pushed deeper into the core by companies like Intel and Broadcom.

<a href="http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/ethernet-switch-fm6000-sdn-paper.pdf" target="_blank" rel="noopener noreferrer">Intel FM6000 Chipset</a>

<hr />

<h2 class="legacy-heading">OpenDaylight Community Input</h2>

Links from the community. Thats community that isnt getting paid to be community, but operators that can program, engineer, architect and all around proverbial, masters of complexity.

<ul>
	<li><a href="http://mrfogg97.blogspot.com/2013/04/opendaylight-sdn-on-windows.html" target="_blank">OpenDaylight SDN on Windows</a></li>
	<li><a href="http://www.forwardingplane.net/2013/04/openflow-hybrid-its-a-must-not-an-option/" target="_blank">OpenFlow Hybrid. It’s a must, not an option.</a></li>
	<li><a href="http://packetpushers.net/openflow-switching-performance-not-all-tcam-is-created-equal/" target="_blank">OpenFlow Switching Performance: Not All TCAM Is Created Equal</a></li>
	<li><a href="http://www.dasblinkenlichten.com/installing-opendaylight-on-centos/" target="_blank">Installing OpenDaylight on CentOS</a></li>
</ul>

<hr>
Get involved with <a href="http://wiki.opendaylight.org" target="_blank">ODP</a>. My money is on that. If it wasn't ODP then what? Let me be clear, if ODP was a closed consortium like the ones we have, made up of vendors, I would fully expect failure. A Linux Foundation OSS project with this level of transparency can and will be policed by the community for delivering. Rob Sherwood said something very poignant in last weeks TSC meeting, "Our only power in the TSC can do is say no, if we do that early we will discourage more developers". There are clearly some people on the TSC that realize the brevity of what they are doing and there are even more of us in the community that believe in the OSS path. OpenStack is coming to networking, ideally hardware wars don't ruin it.

<hr />

Thanks for stopping by.