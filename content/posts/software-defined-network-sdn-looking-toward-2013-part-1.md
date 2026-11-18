+++
title = "Software Defined Network (SDN) -Looking Toward 2013 - Part 1"
date = "2012-11-27T03:10:37+00:00"
lastmod = "2012-12-08T06:09:36+00:00"
author = "Brent Salisbury"
wp_id = 4353
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/software-defined-network-sdn-looking-toward-2013-part-1/"
image = "/wp-content/uploads/2012/11/brand-sdn.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "fb4b4206686b1cf8d447a16fe8fb8ef8f097a94bf1bc1afdeb077b77ffab1cbd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Software Defined Network (SDN) -Looking Toward 2013 - Part 1</h2>
As we near the end of 2012 I wanted to reflect on some things I expect to pick up speed and solidify in 2013. Q1 of 2013 will bring beta SDN software products and with the tail end of the year bringing hardware and GA products. We will begin to see just what sort of R&amp;D each vendor has been up to. Starting off let's look at some hardware.

<h2>Forwarding Abstraction</h2>
The pieces and parts of hardware required to make SDN work are still rather salient. At this point it is pretty clear to expect a couple of fairly well vetted alternatives in hardware to the status-quo by the end of 2013. Question of where and how much state remains in protocols, controllers, centrally and de-centrally will continued to be proofed by researchers and industry. The biggest challenge with regard hardware is memory allocation and width and allocation to multiple tables in hardware with OpenFlow v1.1 and greater.

There have been comments coming out of Broadcom that allude to a shift in their SDN position. Here are two quotes three months apart. Both comments are presumably with regards to the <a href="http://www.broadcom.com/press/release.php?id=s702418" target="_blank">StrataXGS</a> Trident II chipset:

<blockquote class="pullquote">“The [separate] OpenFlow specification has a lot of industry hype, but there are very few practical applications of it today because the spec is in a very preliminary stage,” <footer>Sujal Das, Broadcom EETimes 27 Aug 2012</footer></blockquote>

Three months later the message is significantly different likely from customer demand or else the previous statement was meant to not threaten OEM partners.

<blockquote class="pullquote">"If you run everything in a [central] OpenFlow controller, you have to go to that controller for every decision, and that's a bottleneck and scaling issue," said Sujal Das, director of product marketing in the group. "One needs to take a more holistic approach."
Broadcom's API effort aims to enable both OpenFlow and distributed networking protocols already in use. It hopes the interface could become an industry standard above vendor-specific efforts at <a href="http://www.eetindia.co.in/SEARCH/ART/SDN.HTM">SDN</a>APIs announced by Cisco Systems and others.
"With the changing dynamics we are increasing asked to map to higher level APIs, and that's where we are putting our work,"<footer>Sujal Das, EETimesIndia 22 Nov 2012</footer></blockquote>
This could be an attempt at some northern API definition and consolidation. If POSIX serves as an example, last time I checked, I can't take my Mac binary/source and install/compile it on a Linux kernel much less Windows. As Shenker compared OpenFlow to the x86 instruction set, abstractly, its fairly reasonable to say that holds true as OpenFlow is the closest thing so far, that is the common cross platform primitive. Having a menu of APIs to write code more efficiently than it is <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">today</a> will be important. OpenFlow is merely one choice today. It or something similar will be sought out, that allows for the dismantling of monolithic hardware devices in todays IBM early 80's paradigm of networking.

If I was to guess the API Broadcom is alluding to has something to do with multiple table allocations since it has quotes from <a href="{{< relurl "/brocade-on-sdn-at-network-field-day/" >}}" target="_blank">Curt Beckmann</a> of Brocade, the FAWG working group chair person.

Another Broadcom innovation on the horizon, is the XLP 200-series network processor (NPU) from the $3.4 Billion acquisition of NetLogic. Similar products from EZchip NPS (successor to the NP5, C-programmable) and the Cavium Octeon are all MIPS embedded processors are touting scale up to Layer7. Embedded systems on a chip (SoC) contain resources to run operating systems in an embedded chipset. Unlike fixed ASICs, which are purpose built integrated circuit (IC) that do only what they are built to do very efficiently, the NPU and SOCs can all take microcode updates or application patches in a SOC, to perform in a more general purpose manner at impressive speeds. All three are slated for mid to late 2013.

<blockquote class="pullquote">EZchip NPS - For carrier equipment, the NPS enables the migration of advanced layer 4-7 features from specialized services cards to common line cards and enables the line card with new baseline features such as application recognition and IPSec VPNs, as well as greater velocity for adding new features. For data-center equipment, the NPS allows scaling their performance to the required loads of the evolving data center for greater layer 2-7 capabilities within constrained power and space. It empowers data-center appliances as well as carrier appliances with line-rate performance for applications such as load balancing, firewall and OpenFlow/SDN (Software Defined Networks) and network virtualization.</blockquote>

The RegEx engine in the XLP 200 is quite interesting, that has pretty big security implications. Marketing press releases but both make mention of SDN strategies:

<blockquote class="pullquote">Broadcom XLP 200 - Broadcom has begun sampling its 28nm XLP 200-Series network processor for enterprise, service provider 4G/LTE, data center, cloud computing and software defined networking (SDN) equipment. The processor family, which is the world's first 28nm multicore communications processor family, promises up to 400 percent faster performance than competing solutions while lowering power consumption by up to 60 percent. The XLP 200-Series is the first to integrate a grammar processing engine, a fourth generation regular expression (RegEx) engine, and a broad range of autonomous encryption and authentication processing engines to deliver comprehensive Layer 7 deep-packet inspection (DPI) capabilities and complete offload of the compute-intensive security functions from the CPU cores.</blockquote>

The direction Broadcom, and the other handful of "merchant silicon" chipset manufacturers strategy has a downstream ripple effect. Off the shelf silicon, was one of the key enablers of the SDN conversation taking place today. I would expect Broadcom to continue to OEM with partners for the foreseeable future.

<h2>SDN Sausage Factory</h2>

While on the topic of complementary APIs, let's take a look at some projects that have been maturing over the past year. Frenetic, Procera, FML and Netcore are languages and/or frameworks that are aiming to add an abstraction layer in between application and a raw primitives, like OpenFlow. These projects could reduce the complexity of OpenFlow semantics in dealing with, packet-ins/outs, storing buffer, flushing, OFActions/Matches, consistency and all of the other complexities associated with generating proactive and reactive flows. With programmatic abstraction comes more efficiencies of scale.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/frenetic.jpg" >}}" alt="Frenetic SDN"></figure>

<strong>Figure 1</strong>. Additional APIs to abstract the low level complexities of OpenFlow instantiations.

<h2>Policy In Flows Out with Layers of Abstraction</h2>
These are essentially runtime compilers. The programming of flows needs to take place in the network operating system (NOS) rather than the application. Getting a single function put together with OpenFlow has a fair amount of complexity to it. Trying to rebuild forwarding, load-balancing, routing, firewalling or any other service in with OpenFlow functions every time you build an application is not so efficient. On top of that combining multiple mixes of each of those functions adds a whole new multilayer problem of arbitration. Using something like NetCore, written in Frenetic, provides complexity abstraction, that theoretically translates into more efficient development and less error prone software. Similar to writing a piece of Java or Python is easier and less lines of code than writing in a lower level language executing to a more primitive instruction set.

Presenting a further abstracted interface could allow for applications to push policy south, rather than complex flow details and policy. Simply put, the goal would be to take multiple actions handing it off to the runtime compiler for composition and consistency.

<blockquote class="pullquote">Networks exist in a constant state of flux. Operators frequently modify routing tables, adjust link weights, and change access control lists to perform tasks from planned maintenance, to traffic engineering, to patching security vulnerabilities, to migrating virtual machines in a datacenter. But even when updates are planned well in advance, they are difficult to implement correctly, and can result in disruptions such as transient outages, lost server connections, un- expected security vulnerabilities, hiccups in VoIP calls, or the death of a player’s favorite character in an online game. <footer><a href="http://frenetic-lang.org/publications/network-update-sigcomm12.pdf">Abstractions for Networks Update</a></footer></blockquote>

The alternative, is to incorporate some of those orchestration concepts into the OpenFlow spec itself. That said, too much at that layer gets people bristly and rightfully so, it is important to not try and boil the ocean at the primitive layer to preserve flexibility for hardware vendor <a href="{{< relurl "/the-birth-unicorn-early-openflow-meeting-notes/" >}}" target="_blank">differentiation</a> and flexibility. Just as word processors do not talk directly to low level instruction sets proper <a href="{{< relurl "/sdn-apis-this-all-feels-pretty-familair/" >}}" target="_blank">operating system layers</a> make sense in the emerging network operating system model also.

Here is an excerpt from an interview posted on a Cisco  with Jennifer Rexford, PHD Proffessor at Princeton who has lead the Frenetic project. The full interview can be found <a href="http://newsroom.cisco.com/feature-content?type=webcontent&articleId=778236" target="_blank">here</a>.


<ul>
	<li><strong>Scott Gurvey</strong>: <em>Is there anything that seems to be rising to the top as a means to design networks, control networks and program networks?</em></li>
	<li><strong>Jennifer Rexford</strong>: <em>Inside the network there's a growing interest in a technology called software defined networking and a particular technology called <a href="http://www.openflow.org/">OpenFlow</a> that provides an open interface between the control of the network and the network elements that are being controlled. And so it allows software running on a separate machine to get informed about events in the network, things going up and down, packets needing special handling, and to be able to install rules in the underlying switch hardware to decide how groups of packets should be forwarded or dropped perhaps if you don't want them in the network. That technology has been getting tremendous traction. It was developed out of Stanford. A number of vendors are starting to support it and a number of researchers, myself included, are using that as a platform to think new thoughts about the right programming abstractions for programming these type of open interfaces to the underlying hardware.</em></li>
	<li><strong>SG</strong>: <em>Doesn't this kind of clash with the concept of not having a central control point; which has always been one of the supposed graces of the Internet?</em></li>
	<li><strong>JR</strong>: <em>That's certainly true and so the idea there is, you give the programmer the illusion of a central control point because that's easier for people to think about. And then you leverage a lot of the innovation over the past twenty years in distributed systems to actually distribute and replicate that underlying functionality. So you're totally right, you do need the control to be distributed and replicated otherwise it will be a scalability bottleneck, single point of failure, single point of attack. But there are starting to be ways to do that while still presenting the programmer with a simple point of view of the world where he really thinks his code is running on a single component.</em></li>
</ul>


<strong>Example</strong> logic of a traffic steering application could be:

<ol class="legacy-numbers">
<ol>
	<li>Operator enters policy into an application with parameters around SLA, price etc.</li>
	<li>Application send policy south to a compiler either on or off the NOS platform.</li>
	<li>The compiler then feeds raw flows to a controller, either as an IPC or RPC depending on compiler location.</li>
	<li>Forwarding target (SW or HW switch) ingests flows into forwarding tables.</li>
</ol>
</ol>

If interested in more how to program your own flow decisions take a quick look <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">here</a>. It is a post to help one get started in extracting the headers from a packet-in event using the Floodlight OpenFlow controller. I have a couple of more OpenFlow programming how-tos in the works, I will get written out in the next few days.

<hr />

The next section of this two-parter will focus more on the softer side of networking.

<a href="{{< relurl "/software-defined-network-sdn-looking-toward-2013-part-2/" >}}" target="_blank">Software Defined Network (SDN) -Looking Toward 2013 - Part 2</a>

<hr />