+++
title = "Hybrid OpenFlow Using The Normal Action"
date = "2013-02-21T02:22:56+00:00"
lastmod = "2014-02-18T02:56:54+00:00"
author = "Brent Salisbury"
wp_id = 5819
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/hybrid-openflow-using-the-normal-action/"
image = "/wp-content/uploads/2013/02/normal-OF.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "09b8ff05856886c5cce0ec46ac21a7d9d2905e863955ed1243bb5101da38db11"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Hybrid OpenFlow Using The Normal Action</h2>
Hybrid OpenFlow Using The Normal Action: When a new technology is introduced in networking, it is not uncommon for most to transition that new technology into their network for test/dev or production by starting with small chunks at a time. <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies/" >}}" target="_blank">Hybrid OpenFlow </a>deployments will used by many of us as a place to start with SDN with fairly low risk and flxible enough to integrate into existing architectures. Just a minimal edge deployment of OpenFlow provides the flexibility to apply new policy techniques never before possible outside of software switching. If you compare a hybrid OpenFlow edge to the overlay data center architectures, not much is different. Using the OpenFlow Normal action, represents the default route of hybrid flow based forwarding at the edge. The disruption and CapEx is fairly low since the hybrid model is still using traditional networks as you aggregate upstream into the native network. <a href="{{< relurl "/openflow-coarse-vs-fine-flows/" >}}" target="_blank">Classify</a> and then forward.

Overlay tunneling in the data center gets the attention because it can solve layer 2 adjacency requirements for live workload migrations (vMotion). Tunneling is where much focus has been, when the true innovation, is the classification at the edge before the flows get stuffed into tubes. There are very few, if any, good reasons to extend layer2 networks in that same manor in enterprise and provider networks, other than more broken L2 applications. That said, take aways the tunnels, s/vSwitch/HW Switch/g and you are left with an SDN edge attached to a native forwarding core. The main difference is, one edge device is virtual in a <a href="http://openvswitch.org" target="_blank">vSwtich</a> and the other is a physical switch (more on that in a future post). The commonality between virtual and physical is they can both be reduced to a forwarding target with similar primitives between the two for object instantiation. A key method for enabling a seemless transition is the OpenFlow normal forwarding action (OFPP_NORMAL). Proper processing at the edge to push into an LSP or any other data path at aggregation, is interesting in and of itself.

Early OpenFlow is a tool for a handful of <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">applications</a> to exploit. Now that the primitives are exposed, we can start writing code to solve problems, instead of adding a new RFC on the top of the 6,000+ others. While operation orders and any needs for recirculation are fuzzy, OFP normal allows you to peel traffic with essentially an ACL. That redirects traffic toward your early application, whether it is programmatic PBR, duplicating output ports for tapping or just an early test/dev environment. Just as the name implies, the action specified in a <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">proactive</a> flow rule or flowmod, if reacting to a packet in, instructs the packet to be sent to the "normal" forwarding pipeline for forwarding. The normal action is listed in <a href="{{< relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" >}}" target="_blank" rel="noopener noreferrer"> Download OpenFlow v1.3 </a>
 spec as an optionally supported action. There is a hybrid working group, at least still listed at the ONF that doesn't appear to have anything coming out of it. Most vendors are supporting the OF Normal action (or a really, really good front patch story), if they don't support a hybrid path, they would be a tough sell for most of the colleagues I collaborate with. 

<blockquote class="pullquote">NORMAL: Represents the traditional non-OpenFlow pipeline of the switch (see 5.1). Can be used only as an output port and processes the packet using the normal pipeline. If the switch cannot forward packets from the OpenFlow pipeline to the normal pipeline, it must indicate that it does not support this action.<footer>OpenFlow v1.3 Spec</footer></blockquote>


<h2>OpenFlow Hybrid Pipeline</h2>

What the normal action means for early OpenFlow deployments is, an application can push some specific flow rules to peel off traffic for something like a traffic steering or a tapping application to be matched. If that traffic is not matched it would have a rule as a catch all at the end to forward that packet to the normal forwarding pipeline. 


<h2>OpenFlow Pipeline</h2>



<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/OpenFlow-Pipeline-650x452.png" >}}" alt="OpenFlow Pipeline"></figure>


<h2>Hybrid OpenFlow Pipeline using the Normal Action</h2>


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/Normal-Pipeline.png" >}}" alt="Hybrid OpenFlow Pipeline"></figure>

What the normal action translates to, is the ability to redirect "interesting traffic" that you want to push into an OpenFlow application, if there is not a match by the OpenFlow flow rules, it matches the normal action for typical packet forwarding.

The normal action pushed into an HP 3500yl with all fields wildcarded as a default match at the end of a flow rule set (think ACL), looks like the following. That one flow rules tells the switch to process packets normally. I think it is important that it is understood from an operations perspective. Match whatever you want to match for early applications and let the rest go. Notice that the flow rule is processed in hardware as displayed in the following output:


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/openflow-normal-rule-650x212.png" >}}" alt="Hybrid OpenFlow Normal Rule"></figure>


When you are looking at early SDN and OpenFlow enabled gear, I think it is vital to have features like normal support to be able to adjust architectures as needed. In summary, one flow rule can turn have traffic act as it normally would. On top of that, add your early use cases without the need to reinvent the wheel. In summary, hybrid techniques allow for early explorations of the new found freedoms that open systems present, by cherry picking traffic for particular applications, while still performing traditional functionality in packet forwarding for routine operations.

<h2>Next, Adding the Normal Action to Flow Tables</h2>

In the next post, we will walk through instantiating that normal flow rule for those new to OpenFlow. To do so we will be using the application <a href="http://openflow.marist.edu/avior.html" target="_blank">Avoir</a>, developed by our friends at Marist University. It is a great OpenFlow GUI that sits atop the FloodLight controller and uses the <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">static flow pusher</a> module for OpenFlow rule instantiation. 

<hr>
Thanks for stopping by!
<hr>