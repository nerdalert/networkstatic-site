+++
title = "BigSwitch Announces SDN GA Products and Pure Disruption"
date = "2012-11-13T06:15:45+00:00"
lastmod = "2012-11-26T16:55:01+00:00"
author = "Brent Salisbury"
wp_id = 3909
categories = ["Speculative"]
tags = ["Big Switch", "OpenFlow"]
description = ""
url = "/bigswitch-announces-sdn-ga-products-and-pure-disruption/"
image = "/wp-content/uploads/2012/11/disruption-sdn1.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ea4f9ab28a139282c20d2abfab2e59e079a3d1a5800c9c7be6b26355a77df96b"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

BigSwitch Announces SDN GA Products and Pure Disruption: Today BigSwitch announced it's first product line that is generally available. For those unaware, <a href="http://www.bigswitch.com" target="_blank">BigSwitch Networks</a> is a VC whose heritage was deeply seeded by researchers and PHD's from Stanford, UC-Berkeley along with, product managers and executives from traditional networking companies. BigSwitch recently received round B venture cap funding from <a href="http://www.networkworld.com/news/2012/103112-big-switch-funding-263846.html" target="_blank">Goldman Sachs</a>, who was recently accepted as a member of the <a href="https://www.opennetworking.org" target="_blank">Open Networking Foundation</a>.

Before we dive into the product announcements, I want to point out what I consider BigSwitch's largest contribution to the <a href="http://groups.google.com/a/openflowhub.org/d/forum/floodlight-dev" target="_blank">community</a> and that is the open source OpenFlow controller FloodLight. Just as Nicira who was recently <a href="http://blog.ioshints.info/2012/07/vmware-buys-nicira-hypervisor-vendor.html" target="_blank">acquired</a> by VMWare open sourced their vSwitch <a href="http://openvswitch.org" target="_blank">Open vSwitch</a>, BigSwitch did the same with FloodLight. In the spirit of enabling horizontalization these projects allow researchers, consumers and even competitors to leverage R&amp;D from these startups. We have enough concepts to keep us going for the foreseeable future, it is time to start executing them as more products continue to emerge.
<h2>BigSwitch Product Announcements</h2>

<hr />

<h3>I. Big Virtual Switch</h3>
<blockquote>"Big Virtual Switch dynamically provisions Virtual Network Segments to make the network as agile and dynamic as your other cloud infrastructure."</blockquote>
<div>
<ul>
	<li>Improve compute utilization by 25% to 50%</li>
	<li>Rescue stranded compute capacity providing up to 50%+ more VMs per rack</li>
	<li>Improve VM density, drive down power &amp; cooling costs</li>
	<li>Reduce cost of building out new data center infrastructure</li>
	<li>Support a range of topologies including: hypervisor switch overlays, physical switches or any combination of the above.</li>
</ul>

<hr />

<div><strong>The Big Virtual Switch (BVS)</strong> concept is fairly straightforward. Reduce the network substrate to elements that except forwarding instantiations regardless of whether it is physical or virtual. The complexity of policy is pushed to single or multiple (modular scale) centralized points for policy orchestration and 3rd party application plugin. While one approach is to build overlays over complex networks reducing some complexity, the BigSwitch approach is to extract the complexity from the network substrate and push it into controllers.</div>
</div>
<p style="text-align: center;"> <a href="{{< relurl "/wp-content/uploads/2012/11/hybrid.jpg" >}}"><img class="aligncenter  wp-image-3929" title="bigswitch-virtualization" src="{{< relurl "/wp-content/uploads/2012/11/hybrid.jpg" >}}" alt="bigswitch-virtualization" width="545" height="158" /></a></p>
<strong>Figure 1.</strong> Big Virtual Switch, consolidation proposes flexibility to existing constraints and  increased operational simplicity.

<hr />

<h2>II. Big Network Controller</h2>
"Big Network Controller<strong> </strong>is the Open SDN application platform and includes an open programming interface, open core controller based on Floodlight, and open protocols to deliver unified network intelligence, programmability and scalability."

<ul>
	<li>Common network abstraction on network infrastructure</li>
	<li>Normalized policy and functions across fabric</li>
	<li>Standards-based and open core architecture</li>
	<li>Enterprise class manageability, scalability and resiliency</li>
</ul>

<div></div>

<hr />

<div><a href="{{< relurl "/wp-content/uploads/2012/11/3-tier-compact-2.jpg" >}}"><img class="aligncenter  wp-image-3910" title="BigSwitch-Controller" src="{{< relurl "/wp-content/uploads/2012/11/3-tier-compact-2-982x1024.jpg" >}}" alt="BigSwitch-Controller" width="508" height="529" /></a></div>
<div><strong>Figure 2</strong>. The network OS as a platform for the first time.</div>
&nbsp;
<div></div>
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/11/bvs-pure-overlay.png" >}}"><img class="aligncenter size-full wp-image-3932" title="bvs-pure-overlay" src="{{< relurl "/wp-content/uploads/2012/11/bvs-pure-overlay.png" >}}" alt="bvs-pure-overlay" width="542" height="198" /></a></div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/11/pure-openflow.png" >}}"><img class="aligncenter size-full wp-image-3933" title="pure-openflow" src="{{< relurl "/wp-content/uploads/2012/11/pure-openflow.png" >}}" alt="pure-openflow" width="542" height="258" /></a></div>
<div></div>
&nbsp;
<div><a href="{{< relurl "/wp-content/uploads/2012/11/hybrid-network.png" >}}"><img class="aligncenter size-full wp-image-3934" title="hybrid-network" src="{{< relurl "/wp-content/uploads/2012/11/hybrid-network.png" >}}" alt="hybrid-network" width="542" height="291" /></a></div>
<div></div>
&nbsp;
<div><strong>Figure 3</strong>. The <a href="{{< relurl "/hybrid-sdn-deployments/" >}}" target="_blank">hybrid</a> approach is critical for flexibility and adoption.</div>

<hr />

<h3>III. Big Tap</h3>
<blockquote>"Big Tap delivers monitoring functions to your Open SDN. Big Tap provides cost-effective, enterprise-wide network visibility, optimizing the utility of your security tools, performance tools, and network packet brokers."</blockquote>
<strong>Big Tap</strong> looks to be an early Application plugin for the Big Network Controller platform. Extracting interesting traffic from large pipes is not a cheap venture by todays standards. Mix in bundles of high speed links (LAG) thus multiple physical taps and now you just broke your projects target TCO. BigTap relieves many of those constraints. Much broader distribution of select inspection is something that is interesting to ITSec.

<a href="{{< relurl "/wp-content/uploads/2012/11/bigtap.png" >}}"><img class="aligncenter size-full wp-image-3938" title="bigtap" src="{{< relurl "/wp-content/uploads/2012/11/bigtap.png" >}}" alt="bigtap" width="542" height="258" /></a>

<strong>Figure 4.</strong> BigTap integration. <a href="{{< relurl "/the-potential-impact-of-software-defined-networking-sdn-on-security/" >}}">Security</a> has tremendous possibilities for true actual infrastructure integration that is not cost prohibitive like most purpose built security silicon today.

Big Tap leverages a simple concept of OpenFlow and that is the ability to have fine grained flow control on as little or as much of your data flows as you want. The days of the destination prefix being the only relevant field in networks is coming to a close. There are dozens of relevant headers contained in the Layer 2-4 tuples that have value if orchestrated properly.

<hr />

<h2>Ecosystem Partners</h2>
A major of Software Defined Networking has always been enabling agility to networking whether features, scale, elasticity and so on through horizontalization. Simply put, breakdown the vertical of one size fits all approach to networking today. Along the way breakdown the silos created by closed proprietary APIs. When we begin introducing abstraction layers to networking ecosystems and partnerships will churn innovation. The lynch pins and choke points that have traditional been the barrier, either evolve or become irrelevant. Just as the <a href="{{< relurl "/sdn-apis-this-all-feels-pretty-familair/" >}}" target="_blank">x86</a> market in 1982 began decoupling software innovation from the underlying hardware,  networking appears to be heading down the same path.

The ecosystem partnership in this announcement is broad. Some of those companies will certainly fall out when and if they go off and develop their own controller or application, that may fork from the <a href="{{< relurl "/hp-announces-their-sdn-controller/" >}}" target="_blank">Floodlight</a> trunk. I think there is room for three or four controllers (network OS) just as we have three or four predominant x86 server operating systems. The promise is in the 3rd party applications that these partners will be focusing on delivering or reselling their switch hardware supporting OpenFlow primitives.

The partner list is impressive: A10 Networks, Arista, Broadcom, Brocade, Canonical, Cariden, Citrix, Cloudscaling, Coraid, Dell, Endace, Extreme, F5, Fortinet, Gigamon, Infoblox, Juniper, Mellanox, Microsfot, Mirantis, Nebula, Palo Alto, Piston Cloud, Radware, StackOps, ThreatStop and Armour.

The potential of the ecosystem applications is as large as the imagination can go when it comes to instantiating flows with L2-4 headers exposed like a blank canvas. The forwarding can be pushed into software switches (Open vSwitch) in hypervisors or into hardware to be forwarded at line rate. The other unique proposition is extracting the networking <a href="http://yuba.stanford.edu/~nickm/papers/headerspace-nsdi12.pdf" target="_blank">global view</a> and leveraging <a href="http://etherealmind.com/northbound-api-southbound-api-eastnorth-lan-navigation-in-an-openflow-world-and-an-sdn-compass/" target="_blank">big data</a> analytics techniques for uses cases like instrumentation, management, orchestration integration and even predictive analysis.

<hr />

<h3>Pricing</h3>
The pricing appears to be able to facilitate either CapEx or OpEx needs. Enterprises tend to be a bit more CapEx oriented, while Providers are looking to pay on consumption that is being resold. Price points appear low to get your feet wet, first hit for free is probably their somewhere too.

<ul>
	<li>Big Virtual Switch- Starts under $4200/month</li>
	<li>Big Tap- Starts under $500 month</li>
	<li>Big Network Controller- Starts under $1700/month</li>
</ul>


<hr />

<h3>What This Means For OpenFlow</h3>
Announcing GA products is a big step for a VC startup. This means customers are in the pipeline, the support process is established and most importantly the products are shipping. Those are also typically pre-requisites to an acquisition.

There will be a public proofing of what OpenFlow can do in the form of a product. Forwarding on general purpose gear is the future and purpose built hardware for general use is the past. OpenFlow is not the final answer but nothing in computing ever is. If we do not consolidate on a wire protocol to interact with some form of southbound hardware abstraction layer (HAL), I would hesitate to think much was accomplished. Primitives such as the OpenStack Quantum API are far and few between. Even in the case of <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">Quantum</a> it is acting as a higher layered  HAL for provisioning and de-provisioning.  The NDAs will come undone regarding their products and we will begin seeing the performance analysis and scale of OpenFlow as a wire protocol. I believe it is plenty good enough for now <strong>if</strong> numbers like those below hold up.

<ul>
	<li>250K packet-in per second</li>
	<li>1000 concurrent switches</li>
	<li>32000 virtual network segments (tenants)</li>
</ul>


<hr />

<h3>Closing Thoughts</h3>
The SDN road is longer than the hype may suggest, but in retrospect evolve fairly rapidly due to consumer demand. It is product announcements like this and other companies big and small in the coming year that will officially transition SDN from perceived hype into a fork in the road. The C-levels and VPs inside of infrastructure that still think SDN has only has interest in academia and hyper-scale corner cases are playing roulette with market shares.

Protocols are not going anywhere. The need for inter-domain routing will always be there. The need for stitching SDN islands together across traditional networks will be just as important. The concepts and now products being offered are reducing the need to go through the inefficient drawn out process of developing yet another protocol to solve  problems. Intra-domain forwarding can be simplified with these ideas.

There is varying statistics of 300-500 million IP connected mobile devices in 2012 with predictions at a staggering 25-50 Billion by 2020. Absorbing exponential growth within the current infrastructure constraints of hardware and software being one monolithic entity appears unrealistic. The concepts are grounded in fundamental computer science principles of layered abstraction, modular scale and programmatic interactions.

Many have vacillated on OpenFlow's potential, if they were ever open minded enough to conemplate it at all. BigSwitch has stayed true to it's initial goal of producing an OpenFlow controller that operates with both virtual and physical switches and delivered the first round of many products to come. This is pure disruption, but from the looks is the ecosystem partners everyone is hedging their bets and in the end the consumer wins.

Thanks for stopping by!
<hr>