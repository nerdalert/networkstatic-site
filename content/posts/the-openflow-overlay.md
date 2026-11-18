+++
title = "The OpenFlow Overlay"
date = "2013-06-30T06:06:02+00:00"
lastmod = "2014-02-18T02:57:29+00:00"
author = "Brent Salisbury"
wp_id = 6709
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/the-openflow-overlay/"
image = "/wp-content/uploads/2013/06/incrementalism1.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "fa381e2865f19e859e4942de79e14ba00340b6faa603979b244140d256344982"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The OpenFlow Overlay</h2>
Integrating SDN beyond the data center is still the wild west. The needs are very similar, traffic classification and policy instantiation at the edge. Data center solutions then abstract the underlying network with tunneling/encapsulation mechanisms to achieve IP mobility among other things. Outside the data center, some may care about choosing a forwarding path beyond the SPF calculation accounting for other constraints and some may not. What everyone does care about is the edge. SDN in DC is being defined today, flow based forwarding on the edge (wildcarding available), exact match forwarding in the core (CAM/LPM). Whether enterprise security services or provider service insertion to generate new revenue it is all about the edge. How do we begin to integrate SDN without replacing our networks and without vendor applications to do it? Using a similar approach to data center solutions that Martin Casado and team pioneered using DC tunnels, we can use VID, VPLS and in one case I'm pinning specific flows for tapping over GREs (just as a <a href="http://etherealmind.com/integrating-overlay-networking-and-the-physical-network/" target="_blank">DC overlay</a> would but in edge HW) to avoid having to deal with the native core.

<hr />

Since IP mobility is less of a concern rather then pathing I can replace L2 tunnels with application specific OpenFlow overlay flows. That doesn't mean it needs to be OpenFlow. <a href="http://blog.ioshints.info/2013/06/scott-shenker-on-openflow-and-sdn.html" target="_blank">Scott Shenker</a> (a co-founder at Nicira along with Casado and McKeown) recently made a powerful point that <em>(paraphrasing) "the OpenFlow edge can solve any problem that someone would be willing to pay for"</em>.

Evolving towards a simple identifier or even metadata, that describe the forwarding path at the aggregation mainly to avoid wildcard matching is a logical path described by Martin and others publication <a href="http://webcache.googleusercontent.com/search?q=cache:wD34yzeE8PMJ:yuba.stanford.edu/~casado/fabric.pdf+%22+Fabric:+A+Retrospective+on+Evolving+SDN%22+filetype:pdf&cd=1&hl=en&ct=clnk&gl=us" target="_blank">Fabric: A Retrospective on Evolving SDN</a> (Google Cache). While it is DC focused, the affect to enterprise is reducing lookups to CAM as opposed to the much more expensive TCAM. I translate the concept to be similar to how MPLS FECs (Forwarding Equivalency Class) and RSVP for pre and reallocation of paths. Nothing solves QoS by current means short of pushing policy to in-box processes. I don't expect that to change but if it does it will happen on the edge also.

I freely admit that I have been negligible on keeping up with the flurry of Provider overlay work in standards bodies so the next coming maybe be right there. But..for now to determine pathing we are stuck with complex protocols living in the closed monolith. The path forward in the core may be coupled protocols with the SDN API approach. API interoperability or even commonalities is not something I am optimistic on, at least in the near term. Open network operating systems are more then likely a requirement to get to a widely adopted, interoperable SDN API landscape (e.g. vendor agnostic NOS). Self provisioning (see <a href="http://www.openflow.org/downloads/technicalreports/openflow-tr-2009-1-flowvisor.pdf" target="_blank">Rob Sherwood's publication</a>), virtualization or dare I say data analytics of those paths are the eventual goal. That debate is for another day. Flow based forwarding offers the granularity needed for edge services and OpenFlow is as good a messaging for it as any.

Until we have some abstracted simplicity to the core of the network, I humbly submit there are some use cases the application flow aware forwarding in the aggregation makes sense, particularly without de facto SDN API approaches. One such use case we are working on is bypassing (expensive) firewalls or any other control plane in the data plane black box for trusted data backup traffic. The tradeoff is the complexity of multiple control protocols and hardware involved for something like traffic engineering as compared to the also complex software algorithms to manage flow forwarding. That is why I am interested in having a fairly easy mechanism of getting a base network that has the ability to install OpenFlow forwarding rules as a tool overlaid on top of a fully functioning network full of the plethora of protocols we know, love and hate underneath. Applying graphing functions to labels to ease that complexity of forwarding is something someone is undoubtedly working on but probably isn't going to be solved in the near term.
<h2>OpenFlow as a Tool</h2>
OpenFlow is a tool. It opens up new ways to design networks. Like anything else, it only makes sense if using it to solve problems in IT (e.g. save money or make money). I have some specific requirements that don't necessarily fall into the category to Shenker's point. The architects role will become significantly more important and complex with new distribution models. There are two basic use cases that begin solving many problems some of us experience today. It also presumes you are rolling the code yourself or working with some vendor beta applications:
<ol class="legacy-numbers">
<ol>
	<li>Ingest, classify and forward traffic at the edge of the network for policy and services.</li>
	<li>Flow forwarding for specific applications across multiple nodes either end to end or hacked through native forwarding networks. I say hacked for a reason. Pushing a flow through say a native VLAN requires turning off mac-address learning and STP to basically BUM traffic a P2P circuit. Provider bridging (QinQ) cannot get here soon enough.</li>
</ol>
</ol>
<h2>L2 VLANs Still Suck</h2>
BUM traffic is what I consider one of the harder/hardest problems outside of controlled data centers with known quantities. Particularly problematic when dealing with physical hardware limitations. 1million flow rules vs. Trident+ 750-3k rules. There are three options and none of them are wonderful other then the obligatory drop. Register, react or flood, but thats a rabbit hole. For now, I am resigned to flooding since current wiring closet switches have limited ability to <a href="http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/ethernet-switch-fm6000-sdn-paper.pdf" target="_blank">process packets</a> over a single serial bus only to run into a CPU as powerful as your smart phone. For the next few months I am leaving it with "normal" flooding. The drawback is Spanning-Tree (shocking). So it leaves us doing VLAN translation to stitch between VIDs.

L2 is still a problem (as <a href="http://blog.scottlowe.org/2013/06/20/thinking-out-loud-the-future-of-vlans/" target="_blank">Scott Lowe</a> pointed out recently) for gateway resolution from a client. If we Proxy ARP requests we can handle the client gateway requests and set/rewrite the dMAC which requires flexible silicon. Registration in Ethernet would be lovely someday.
<h2>The OpenFlow Overlay Design</h2>
Its pretty simple, put in a table miss policy of normal on the edge nodes if you are only interested in edge processing, service insertion or the edge nodes and nodes end to end. This means the device matches everything that wasn't matched by a higher priority. OpenFlow is an ordered list keyed off of the rule priorities. Keep in mind, if you use TCAM for OpenFlow, depending on the agent you are probably taking away capacity or capability all together for functions such as ACLs that use that same TCAM. Hybrid kit is also required but I haven't run across many boxes that don't support OFP_Normal or something very similar such as Brocade's Hybrid OF pipeline.

Rules are as simple as popping in a match all rule with the lowest priority to use <a href="http://www.networkcomputing.com/data-networking-management/how-to-set-up-floodlight-and-test-openfl/240152558" target="_blank">OpenFlow normal</a>. This default drain is similar to a default gateway in prefix routing like so:
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/06/OFP_normal.png" >}}" alt="Hybrid OpenFlow Normal "></figure>

Once a handful of devices have that rule in place, you can then begin instantiating OpenFlow rules to add policy on the edge or even stitch a forwarding path to bypass black boxes or manage a custom constraint based SLA.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/06/OFP_normal_rules.png" >}}" alt="Hybrid OpenFlow Normal With Applications"></figure>

What this leaves you with is a an underlay that works exactly the same as it always did but adds the ability to put OpenFlow instructions to manipulate particular traffic proactively or even reactively at a small scale and plenty of tolerance for issues using current HW. Again, it doesn't need to be end to end but minus an encap better then VLANs or setting next hops its a hack.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/06/The-OpenFlow-Overlay.png" >}}" alt="OpenFlow Overlay"></figure>

As part of the order of operations each packet is matched against TCAM so performance is the same as it would normally be. As applications are devloped by vendors or rolled yourself functionality using OpenFlow will start becoming clear where it makes sense. The OpenFlow doesn't scale stuff nonsense is only when you use the wrong tool in the wrong place. OpenFlow is capable of operating at both ends of the state distribution model (fully and eventual consistency). Hardware constraint and use cases should determine the use.

<hr />

<h2>Deployment Considerations</h2>
There is a laundry list of what to look out for. Well over a books worth ironically :) A couple things that are basics for the simple framework above are the following:

<ul>
	<li>Controller placement isn't that big of a deal since all flows are pushed proactively. There may or may not be a learning curve for networking folks running a server.</li>
	<li>Failure scenarios should be tested. The nice thing of proactive flows is rules stay put until a flowmod is sent to remove it or the network element reboots.</li>
	<li>Understanding vendor OF firmware is incredibly fragmented (to be expected). Your best bet is to learn Open vSwitch since many have it under the hood or at least similar datapaths in the form of ships in the night bridges (br0, br1 etc).</li>
</ul>


<hr />

While this is not a purist look at OpenFlow usage, it is what I see as a common sense, low risk approach to establishing a framework. It also allows for existing infrastructure investment protection that many of us need, <strong>IF</strong> your vendor writes the firmware for it. This leaves a network or some edges of your network with capabilities such as:

<hr />


<ul>
	<li>Manipulate the forwarding tables to install flows to solve some problems.</li>
	<li>Add simple desegregated services to your network (TAP, FW, NAC, IDS etc.)</li>
	<li>Establish a testbed for you to develop or deploy some control or policy applications.</li>
</ul>


<hr />

Many of those problems do not require hundreds of thousands of flow rules but rather dozens of flows. This isn't advocating that everyone should go do this. It is hacking and developing at this point until the majorities vendors retrain and sell the products. Reference architectures will be few and far between since industry verticals have diverse needs, so will the solutions (que the progressive integrators). We are close to seeing vendor supported applications come to market outside of the data center but to leverage those it will need the network to become a platform rather then the rigid model it is today. Take a look at the open source community network centric <a href="http://www.sdncentral.com/comprehensive-list-of-open-source-sdn-projects/" target="_blank">projects out there</a>.

<hr />

Here is a couple of videos from a series of quick and dirty labs I put together. This is a simple example of adding services to the disaggregate edge of the network without needing much in the way of hardware capabilities or compute resources.

<em>You can try this lab yourself with the following downloads:</em>

<ul>
	<li><a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank">OpenDaylight SDN Controller</a> (<em>Option #1</em> for the simple installation)</li>
	<li><a href="http://mininet.org/download/" target="_blank">Mininet switch emulator</a> or a hardware swich with an OpenFlow agent</li>
</ul>

<em>Part 1 is a quick overview of the concepts</em>
[youtube url="http://youtu.be/_GD-kWJ87CQ" width="520"]
<em>Part 2 is a simple lab using OpenDaylight and Mininet</em>
[youtube url="http://youtu.be/3Bln7tIFgZE" width="520"]

<aside class="legacy-callout"><strong>Get Started!</strong>: Check out this post for instructions:  <a href="{{< relurl "/installing-mininet-opendaylight-open-vswitch/" >}}" target="_blank">Installing Mininet, OpenDaylight and Open vSwitch</a></aside>

<a href="{{< relurl "/installing-mininet-opendaylight-open-vswitch/" >}}" target="_blank" rel="noopener noreferrer"> Installing Mininet, OpenDaylight and Open vSwitch</a>
<hr>
Feel free to hit ping me or better jump on irc.freenode.net #opendaylight #openvswitch #openflow and interact with peers and even contribute. Thanks for stopping by!