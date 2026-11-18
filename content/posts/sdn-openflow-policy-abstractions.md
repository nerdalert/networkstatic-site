+++
title = "SDN OpenFlow Policy Abstractions"
date = "2013-01-09T07:21:38+00:00"
lastmod = "2014-02-18T03:00:53+00:00"
author = "Brent Salisbury"
wp_id = 5376
categories = ["Programming", "Study Time", "Tools"]
tags = ["OpenFlow", "Programming", "Software Defined Networking"]
description = ""
url = "/sdn-openflow-policy-abstractions/"
image = "/wp-content/uploads/2013/01/Flow-Factory4.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "1b39ca9a1aef558b7416322e01511a100bc6d2c3a24dc091bc751a7a439fe6d8"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN OpenFlow Policy Abstractions : Frenetic Netcore Procera</h2>
SDN OpenFlow Policy Abstractions : Abstraction layers are a fundamental principle in computer science. It is a core pillar in creating efficiencies through layered, modular scale. Proper abstraction layers are also where the networking train came off the tracks. Network operators program network devices using proprietary APIs one device at a time. In today's networks, when we push policy to network elements, the control loop is anything but tight. Basic worthwhile operational tools never made it to market, in large part due to a lack of layered abstractions.

Networking is made up of vertically integrated components today that resemble the monolithic mainframes of the 80's. As we continue the debate around SDN solutions and agnostic forwarding abstractions such as OpenFlow, are merely building blocks that are not magic bullets. What OpenFlow does offer, is a low level network instruction set agnostic to the vendor and likely flexible enough to serve as a base abstraction as it evolves. With a consistent set of primitives we can write controllers and applications that can control forwarding and/or extract valuable information about the state of your network. Operators nailing up static flows for traffic forwarding would be as unmanageable as throwing out your <a href="http://mellowd.co.uk/ccie/?p=1929" target="_blank">IGPs</a> and hand crafting not just L3 forwarding but L1-L4 forwarding. State distribution will stay decentralized depending on scale, just likely not fully distributed because it just doesn't make much sense any longer inside an administrative domain, we made it through the cold war. 
<h2>SDN is More Then Just Pushing Flows, That Needs Abstraction</h2>
When looking to stitch a flow across your network, it would be quite cumbersome to handcraft the OpenFlow policy across each element in the network when you can abstract the flow implementation policy with another layer. Frenetic, Netcore and Procera are all SDN OpenFow policy abstractions that uses abstraction layers to hide the details that are unimportant and only present relevant information to upper layers. If you need a forwarding path from A-&gt;Z, rather than stitching by hand flows A-&gt;B-&gt;C-&gt;D-&gt;E...-&gt;Z, you should be able to push a policy A-&gt;Z and have the details of everything in between implemented without dealing with the irrelevant semantics of accomplishing that policy. It's pretty comp sci 101 but we had unique challenges in the past that warranted this architecture and extreme levels of control distribution. As more business logic is expected out of the network, some levels of control will divorce the physical. If we don't the complexity and feature ransom would lead to even more complexity in an already borderline unmanageable network of today. Everything will route and overlays (either HW or SW) will rule the day. The value and at the same time problem of OpenFlow is its low level abstraction. The policy abstractions in this post are aimed at abstracting much of those complexities.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/sdn-flow-policy-factory.jpg" >}}" alt="SDN OpenFlow Policy Factory"></figure>

Openflow is the current popular method of instantiating forwarding rules into network forwarding objects over TCP rather then a vendors proprietary protocol. Programming static flows by hand, is even less scalable than operators using static routes in their networks, rather than using IGPs to dynamically exchange a <a href="http://mellowd.co.uk/ccie/?p=788" target="_blank">RIB</a> state. Statically programming flows by hand in anything other than a <a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank">lab</a> would be unmanageable. Routing is based on Layer 3 prefixes, flow based forwarding is based on a wide variety of L2-L4 headers. The added variables exponentially increases the amount of combinations in a networking devices Flow tables available in hardware <a href="http://www.sdncentral.com/products-technologies/sdn-openflow-tcam-need-to-know/2012/07/" target="_blank">TCAM</a> or a vSwitch (Ex. <a href="http://openvswitch.org" target="_blank">Open vSwitch</a>) software flow table today.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/SDN-Policy.jpg" >}}" alt="SDN OpenFlow Policy Factory"></figure>

In order to move forward in leveraging the benefits of proactive (<a href="{{< relurl "/floodlight-openflow-controller-using-the-static-flow-entry-pusher/" >}}" target="_blank">pre-populating flow tables</a>) there needs to be expressive languages and compilers to ingest high level networking policy and grind that into large number of flows required to execute the policy.

<hr />

<h3>Examples of Objects Requesting Programmatic Policy Sources:</h3>

<ul>
	<li>User Interface (UI)</li>
	<li>Analytics Platforms</li>
	<li>Instrumentation Software</li>
	<li>Resource Orchestration</li>
	<li>Anything else that can make API calls.</li>
</ul>


<hr />

<h2>Frenetic: Transform Policy to OpenFlow Flows</h2>
<aside class="legacy-callout"><strong>Frenetic: A Language for High-Level Reactive Network Control</strong>Frenetic: high-level language for programming distributed collections of network switches. Frenetic provides a declarative query language for classifying and aggregating net- work traffic as well as a functional reactive combinator library for describing high-level packet-forwarding policies. Unlike prior work in this domain, these constructs are by design fully compositional, which facilitates modular reasoning and enables code reuse. This important property is enabled by Frenetic’s novel runtime system which manages all of the details related to installing, uninstalling, and querying low-level packet-processing rules on physical switches.</aside>

Frenetic Slidedeck: <a href="http://frenetic-lang.org/publications/splendid-isolation-hotsdn12-slides.pdf" target="_blank">Frenetic: A Programming Language for OpenFlow Networks</a>

Frenetic Whitepaper: <a href="http://www.cs.princeton.edu/~jrex/papers/frenetic12.pdf" target="_blank">Languages for Software-Defined Networks </a>
<div title="Page 1">

&nbsp;

</div>

<hr />

<h2>Procera: Reactive Policy Layer</h2>
<aside class="legacy-callout"><strong>Procera: A Language for High-Level Reactive Network Control</strong>Procera: The key features of the Procera policy language are (1) a core language based on functional reactive programming, (2) event com- prehensions to manipulate event streams, (3) windowing and aggregation signal functions, (4) the use of function values to represent high-level policy.</aside>

Procera Slidedeck: <a href="http://conferences.sigcomm.org/sigcomm/2012/slides/sdn/session2/02-talk.pdf" target="_blank">Procera:A Language for High-Level Reactive Network Control</a>

Procera Whitepaper: <a href="http://ecee.colorado.edu/~ekeller/classes/fall2012_sdn/papers/procera_hotsdn_2012_voellmy.pdf" target="_blank">Procera: A Language for High-Level Reactive Network Control</a>

<hr />

<h2>NetCore: High Level Forwarding Policy Abstraction</h2>

It is worth noting E. Crabbe of Google references Netcore in most of his presentations regarding SDN at the IETF.
<aside class="legacy-callout"><strong>NetCore: A Language for High-Level Reactive Network Control</strong>NetCore: A simple static forwarding policy. NetCore is a declarative language for specifying high-level packet-forwarding policies. The NetCore compiler and runtime system handle the details of translating these policies to switch-level rules and issuing commands to install the generated rules on switches.</aside>

NetCore Whitepaper: <a href="https://www.cs.princeton.edu/~dpw/papers/ncore-popl12.pdf" target="_blank">A Compiler and Run-time System for Network Programming Languages</a>

<hr />

<h2 class="legacy-heading">Video: Frenetic: A Programming Language for OpenFlow Networks</h2>

Jen Rexford of Princeton giving a wonderful presentation on Frenetic. Her thought leadership is phenomenal to say the least.

<hr />

<p><a href="http://www.youtube.com/watch?v=mZMy8e1vCIo">Watch video on YouTube</a></p>

<hr />

<h2 class="legacy-heading">Additional Resources from Brilliant Leaders and Effective Researchers</h2>
<ol class="legacy-numbers">
<ol>
	<li><a href="http://packetpushers.net/pq-show-20-open-network-foundation-fawg-update/" target="_blank">PQ Show 20 – Open Network Foundation – FAWG Update</a> --Packet Pushers Podcast</li>
	<li><a href="http://www.cs.princeton.edu/~jrex/publications.html" target="_blank">Jen Rexford Publications </a> -Princeton</li>
	<li><a href="http://yuba.stanford.edu/~casado/publications.html" target="_blank">Martin Casado Publications </a>-Vmware/Stanford/Nacira Co-founder</li>
	<li><a href="http://www.cs.cornell.edu/~jnfoster/" target="_blank">Nate Foster Publications </a>-Cornell</li>
	<li><a href="https://netsys.cs.berkeley.edu/pubs/Scott-Shenker.html" target="_blank">Scott Shenker Publications </a>-UC Berkeley/Nacira Co-founder</li>
	<li><a href="http://tiny-tera.stanford.edu/~nickm/papers.html" target="_blank">Nick McKeown Publications </a>-Stanford/Nacira Co-founder</li>
</ol>
</ol>

<hr />

Thanks for stopping by!

<hr />