+++
title = "The Birth of an SDN Unicorn - Early OpenFlow Meeting Notes"
date = "2012-06-21T20:06:08+00:00"
lastmod = "2013-04-05T07:21:53+00:00"
author = "Brent Salisbury"
wp_id = 1442
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/the-birth-unicorn-early-openflow-meeting-notes/"
image = "/wp-content/uploads/2012/05/openflow2.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c2dbfc58389c054f6003341a6f977b0e69103f4eac74826f056d8e4a9456e81f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The Birth of an SDN Unicorn - Early OpenFlow Meeting Notes</h2>

The Birth of an SDN Unicorn - Early OpenFlow Meeting Notes: I wanted to share something I found very fun to read. These are the OpenFlow notes from the working group meetings at Stanford from 2010. The conversations are fascinating and the notes read like a book.

<blockquote class="pullquote">"We want to create a dynamic where we have a very good base set of vendor-agnostic instructions. On the other hand, we need to give room for switch/chip vendors to differentiate." <footer>-Nick McKeown</footer></blockquote>

While fun to read, I think it's important to see what goes on in developing disruptive standards such as OpenFlow. These researchers and industry heavy weights quoted below while incredibly smart and creative are people, were able to work together on a common goal. That is often the biggest barrier. That takes some real leadership. The soft skills in IT are at least as important, as the hard skills. I tend to argue even more important.

The dialogues are great and go to show that while it may feel like working to develop and influence the next great technology is something out of reach to most, it is merely people getting together to solve a common problem.

<blockquote class="pullquote">"Work with existing silicon today; tomorrow may bring dedicated OpenFlow silicon." <footer>-David Erickson</footer></blockquote>
To name a few of the people recorded in the notes: Nick Mckeown, Martin Casado, Rob Sherwood, Scott Whyte, Guido Appenzeller, David Ericson, Joe Tardo, David Ward, Jan Medev, James Kempf, Jean Toureillhes, Rajiv Ramanathan, Ed Crabbe, Dan Talayco, Howard Greene, Michael Orr, Brandon Heller, Ben Pfaff. This meeting took place at Stanford's 104 Gates Building every Tuesday afternoon.


<h2>Early OpenFlow Meeting Notes In Chronological Order</h2>

<strong style="text-align: left;">OpenFlow Meeting Notes 2-09-2010</strong>

Agenda:

<strong>Config protocol</strong>

Ben Pfaff from <a href="http://nicira.com/">Nicira</a> presented the config protocol used in Open vSwitch. It has been proposed that the config protocol (or a slightly modified version of Nicira's version) be included in OpenFlow. The remainder of this section is a summary of that discussion.

Motivation: a binary protocol is not easily extensible and is not a good choice for representing some things

History:
<ol>
	<li>{key, value} pairs stored in a file. The entire file is sent to the datapath by the element controlling the config.</li>
	<li>Database with tables. Overcomes limitations of a flat file with {key, value} pairs. Question about how to interact with the database:</li>
</ol>
◦                    SQL or SQLite: feedback from vendors is that these options are too have weight

◦                    XML: again, somewhat heavy weight

◦                    JSON: Simple!

Solution: config protocol using JSON (JSON-RPC is a simple RPC mechanism for JSON)

Config protocol defines a schema and query language
<ul>
	<li>additional types</li>
	<li>referential integrity</li>
</ul>
The Open vSwitch schema is not appropriate for OpenFlow. The Open vSwitch schema enables configuration of elements specific to Open vSwitch and does not currently allow configuration of most OpenFlow-related elements.

Ben provided an explanation of how ovsdb-server (the database that communicates via the config protocol) interfaces with other elements in Open vSwitch. A sample message exchange was also provided.

<strong>Questions asked during discussion:</strong> Q: How to deal with columns that should reflect hardware state, particularly when the controller requests a state changed. A: Consider using a pair of columns: one is use for the requested state, one is used for the actual state.

Q: What should be accessible through the config file? (eg. should flow tables be accesible?) (Rob)

Q: Why JSON-RPC -- why not SNMP? (Jean)

Q: What are some examples of use where transactions and/or triggers are useful?
<p align="center"><strong>OpenFlow Meeting Notes 3-2-2010</strong></p>
Slides from the presentation and discussion of proposed new features are available here: <a href="http://openflowswitch.org/documents/OpenFlow_1_1_feature_proposal_part2.pdf">PDF of slides</a>

Comments raised during Glen's presentation:

Tags and Tunnels
<ol>
	<li>[Howard Green]: MPLS two-tag cases</li>
	<li>[Rob Sherwood]: 1.0 has slicing as actions, not virtual ports; isn't this inconsistent</li>
	<li>[Jean Tourrilhes]: issue with virtual ports: can't stack actions; two ports would duplicate the packet</li>
	<li>[Bob/Jean]: cross-product port space explosion if need a single virtual port to represent multiple encaps/actions; does this suggest a larger port space?</li>
	<li>[Howard]: would be good to establish how phy port, encap, and queues relate</li>
	<li>[James Kempf]: we're OK with MPLS being tags, though implemented as virtual ports now</li>
	<li>[Jean] if do tunnel, no classifier mods; if tags, do need to mod classifier</li>
	<li>[Ed] we should do this in a general way: TLV, not specific protocols</li>
	<li>[Jean] controller should know total set of ports</li>
	<li>[Howard]: MPLS multicast requires a different label on each outgoing port</li>
	<li>[Ed] LISP we can't do</li>
	<li>[James] full port state could be useful for diagnostics</li>
	<li>[Jean] worry about controller connection bandwidth: minimize cruft, esp. flow setup</li>
</ol>
Multiple Tables:
<ul>
	<li>[Jean]: what about hardware that doesn't support information passing?</li>
	<li>[Dan]: cumulative vs override?</li>
	<li>[Howard/Guido]: resubmit confusion</li>
	<li>[Rajiv]: resubmit: rename continue</li>
	<li>[Guido]: how does the controller figure out how to navigate the switch?</li>
	<li>[Howard]: what happens when you replicate a packet?</li>
	<li>[Jean]: if you rewrite headers, are they visible in the next lookup?</li>
	<li>[Dan] doesn't this argue for vlans as virtual ports? multicast on a VLAN + to a tunnel: can't do this because of ordering</li>
	<li>[Guido]: if we expose categories of pipelines, would this be sufficient? Would vendors be comfortable?</li>
	<li>[Rob]: clarify that our goal is to present a superset</li>
	<li>[Dan]: key is how to expose what a switch can do</li>
	<li>[Jean]: more concrete proposals among hardware vendors, possibly with explicit list of table capabilities</li>
	<li>[Dan]: do switches have scratchpads, and is this exposed with the above proposal so that it's usable by a controller writer?</li>
</ul>
Main debated questions:
<ul>
	<li>Do we support non-existent hardware</li>
	<li>What is the exposure format</li>
	<li>Can a controller writer get a working controller for a switch that doesn't exist yet?</li>
</ul>
◦                    Should work somehow: what's the fallback that can make use of the tables
<ul>
	<li>[Rajesh from Orange]: what are the actions my system as a whole can do? (series of atomic operations, as opposed to pipeline stages) Are we adding complexity to the implementation by supporting this general model?</li>
	<li>How does this all interact with action ordering?</li>
</ul>
<p align="center"><strong>OpenFlow Meeting Notes 3-9-2010</strong></p>
Ed Crabbe presented notes about capability advertisement (<a href="http://openflowswitch.org/documents/OpenFlow_1_1_feature_proposal_part3.pptx">PowerPoint slides</a>)
<ol>
	<li>Use case 1: tags:</li>
</ol>
◦                    Q: Doesn't features reply already do this?

◦                    A: No - doesn't allow extensibility to new tags. We

◦                    [Jean Tourrilhes]: desire to expose individual capabilities or new actions

◦                    [Howard Green]: in Ericsson's experience with MPLS, easier if the switch knows more about the packet formats

◦                    [James Kempf]: something like this is needed for a wide range of functionality

◦                    Q: does this belong in the config protocol

◦                    [Jean]: schema vs mechanism: schema is the hard part

◦                    [Guido]: now, it's easy to write a controller to cope with any reported features. In the other extreme, you may need to customize a controller to specific features.

◦                    [Atsushi Iwata]: Possibly want a general/uniform method for exposing tunnels

◦                    [Rajiv Ramanathan]: solution is virtual ports -- most general approach

◦                    [Howard]: problem of virtual ports is timescale

◦                    [Jean]: switches can create virtual ports but need to know protocol information (eg. VLAN tag, IPSec config etc)

◦                    [Guido]: Will there be a standard set of tags
<ul>
	<li>Use case 2: multiple tables</li>
</ul>
[Jean]: Need to expose match fields

[Guido]: Two extremes:

simple present/absent for coarse-grained set of features

very fine grained set of features

[Howard]: Conflicting desires:

Want controllers that work across wide variety of switches

Don't want to prevent innovation

[Uncertain who asked this question]: What are downstream neighbors? Does this allow passing information between tables in different switches?

Downstream neighbors should be translated as downstream tables in single switch
<ul>
	<li>General comments:</li>
</ul>
◦                    [Michael Orr]: appreciates idea of extensible capability set. Has been involved in projects where this has been problematic, especially with hidden assumptions.

Brandon Heller presented ideas on the design space when thinking about the table model (<a href="http://openflowswitch.org/documents/OpenFlow_1_1_design_space.pdf">PDF of slides</a>)
<ul>
	<li>[Howard Green]: proposal hasn't covered non-tables that may be in the pipeline, eg. queues</li>
	<li>[Jean Tourrilhes]: can handle other elements (at least queues) via actions</li>
	<li>[Rajiv Ramanathan/Howard]: competing desires -- exposing much about capabilities vs keeping interface to controller simple</li>
	<li>[Guido]: OpenFlow 1.0 tries to provide a lowest common denominator of features.</li>
	<li>[Guido]: Does it make sense to provide a limited set of pipeline options -- would simplify controller writer's job</li>
	<li>[Rajiv]: Makes it easier for controller writers, but shifts complexity to the HAL. Can argue that complexity should be in controller due to better compute resources.</li>
	<li>[Michael Orr]: Appreciates idea of limited set of tables (eg. L2, L3, ...) since it eliminates need to expose inner switch complexity.</li>
	<li>[Michael]: Perhaps ideal is between two extremes of where we've considered so far.</li>
	<li>[Jean]: Desire to consider use cases. Concern that we can't do what we want with current switches.</li>
	<li>[Guido]: Challenge: how to effectively use a switch given very detailed capability information?</li>
	<li>[Rajiv]: Good to have a simple base level of features, but want ability to take advantage of all features offered by chip</li>
	<li>[Michael]: Problem: exposing a simple interface and having the HAL perform optimizations upon flow insertion -- difficult to verify all combinations of flow-table entries.</li>
	<li>[Guido]: Union of feature sets of merchant silicon would be almost impossible to program to</li>
	<li>[Howard]: Desire to be able to use all features at your disposal</li>
	<li>[Dave Erickson]: Work with existing silicon today; tomorrow may bring dedicated OpenFlow silicon.</li>
</ul>
<p align="center"><strong>OpenFlow Meeting Notes 3-16-2010</strong></p>
Rajiv presented the process slides, plus a schedule for the next few months. See the <a href="http://www.openflowswitch.org/documents/OpenFlow_Meeting_03_16_2010.pdf">presentation slides</a>.

[Nick]: note that we're in this together

[KK]: question about process at the end; how does a feature get included? Will feature inclusion require an implementation?

[James Kempf]: Brought up MPLS OAM; suggested to post to list

[Michael Orr]: Should we also consider multicast? Multipath/multicast very similar.

[Ed]: Hash functions are outside of the protocol.

[Ed]: Assume that switches offer multiple hashes but we won't change the hash dynamically from within OpenFlow.

[Nick]: Equal weight: should we support non-equal weight?

[Rajiv]: Can achieve this by specifying the same port multiple times.

[Michael]: Multicast: must currently explicitly specify all ports in the flow. Could mirror the multipath idea of using logical port groups.

[Ed]: Problem of distinguishing b/w multicast and multipath groups.

[Brandon]: Logical port provides atomicity of updates -- update one logical port updates all flows that use that logical port.

[KK] Why is flow mod not sufficient? A: can't be more specific than a single field; two sets of flows, for example, might not be represented by only two prefixes

[Nikhil] +1 use case: in load balancer, what happens with existing TCP flows w/anycast?

[Joe Tardo]: are groups strictly BW, or also for reliability?

[Ed]: Switch can rehash on link failure

Fast response to failover: should switch make the decision on its own, or controller? A: this is an optimization

Add "reliability" use case?

[Nick]: Is there anything special/extra needed to support this?

[James]: OAM processing in controller or switch?

[Nick]: Question of timescales -- what value?

[James]: 20ms for link failover discovery. is this a reasonable?

[Michael]: Do we only need to deal with cases where both sides to LACP?

[Michael]: Corner cases when only one side does LACP: packet loss, black holes.

Single-sided ECMP use cases?

Explicit: no response to changes in the LAG status (outside of OpenFlow)

[Michael]: LAG defined on both sides, but autonegotiation failure can cause pkt-loss/black hole situation.

both sides speak LACP, or controller needs to learn this?

link health should run on the switch, and there's no mandate

[James]: port protection mechanism -- is there a generic mechanism?

[KK]: LLDP, BFD, etc, 802.3ag, in the switch? A: unclear that this is with the scope, and we don't want to mandate a specific design

[Rajiv]: be careful of dictating network design. Don't want to mandate a design.

[Nick]: we should run less

[James]: DT won't run a network without these reliability mechanisms… it's a matter of getting the right abstractions, plus overhead and abstraction

[James]: Another use case: datacenter network. A: Just an instance of ECMP or LAG

[Nick]: Similarity between multipath, multicast, and sampling/span.

[KK] Multi-home use case

[Nikhil]: expose hashing function discussion on how to do nondisruptive rehashing - subtract requires re-hash, add is tough

[Nikhil: hash microflows

[Jean]: should phy be part of multiple groups?

[Joe]: hw limitation for LAG, port can only be a part of one vs FT, where you may want many groups

[Jean]: when a packet arrives on a L2 bonded port, don't know which virtual interface it arrives on if physical port shared between multiple groups

[Jean]: in non fat-tree situations, we may actually want multiple overlapping groups.
<p align="center"><strong>OpenFlow Meeting Notes 3-23-2010</strong></p>
Brandon presented a proposal for multipath (L2 LAG, ECMP)

A version of the proposal can be found at: <a href="http://www.openflow.org/wk/index.php/Multipath_Proposal">Multipath Proposal</a> (Note: The proposal page will evolve as a result of discussions on the openflow-spec mailing list.)

The comments below were raised during the discussion. Comments are broadly categorized by the topic that was under discussion at the time.

Overview:
<ol>
	<li>[Howard Greene]: Presume this doesn't apply just to multipath?</li>
	<li>[Nick McKeown]: Clarification: are action buckets a set of actions?</li>
</ol>
Answer: yes
<ul>
	<li>[Nick]: Actions are applied in order in the given bucket.</li>
	<li>[Bob Lantz]: Are all actions applied?</li>
</ul>
Answer: for multipath it would be all actions in the "selected" bucket -- bucket chosen by hash
<ul>
	<li>[Christos Kolias]: How do we know how many buckets there are?</li>
</ul>
Answer: Number of buckets in a group mod is variable length. Specified as part of group mod.
<ul>
	<li>[Dan Talayco]: Is there any difference in the set of allowed actions between flows and groups?</li>
</ul>
Answer: Currently don't want to place any restrictions. A switch may not support all actions and return errors.

Advantages of implicit vs explicit groups:
<ul>
	<li>[Rob Sherwood]: Question for vendors: would group mods be atomic?</li>
	<li>[Michael Orr]: Software in switch can try to make group mod atomic, for example, by waiting for buffers to drain.</li>
	<li>[Howard]: Concern that you couldn't do the same range of things with implicit groups. (ie. explicit groups allow greater range)</li>
</ul>
Multipath and multicast:
<ul>
	<li>[Howard]: MPLS-multicast example needs multicast groups to set MPLS tags per output</li>
	<li>[Ed Crabbe]: Big fan of explicit type (multicast/multipath)</li>
	<li>[Jean Tourilles]: Proposal may be overkill for LAG but sees advantages in consistency b/w LAG and ECMP</li>
</ul>
Non-equal weight selection:
<ul>
	<li>[Howard]: Similarities to weighted round-robin</li>
	<li>[Michael Orr]: advise against including WRR in OpenFlow. Many different implementations/methods produce diff results.</li>
	<li>[Michael/Howard]: Potentially expose WRR mechanisms through config protocol</li>
</ul>
Multiple ports in a single bucket:
<ul>
	<li>[Nick]: What reason for considering not allowing multiple ports per bucket?</li>
	<li>[Nick]: Question whether hardware can support multiple buckets per port</li>
</ul>
Proposal:
<ul>
	<li>[Howard]: alternative to specifying bucket multiple times: specify weight explicity for non-equal weight</li>
	<li>[Christos]: Query on purpose of errors?</li>
	<li>[Brandon]: Allows controller to see why group mod failed and require the controller to handle it as appropriate</li>
	<li>[Ed]: Why group stats?</li>
	<li>[Jean]: counters for groups/ports likely to be similar</li>
	<li>[Michael]: May not be true for ECMP. Other traffic may share same port as ECMP traffic.</li>
	<li>[Dave]: Missing mechanism for querying groups.</li>
	<li>[Dave]: Wants floating-point values for weights in group mod.</li>
	<li>[Michael]: Proposal currently doesn't have type (multipath/multicast) for group mods.</li>
	<li>[Michael]: Suggest adding spare flag for expansion.</li>
	<li>[Dan]: Likes idea of types associated with logical ports</li>
	<li>[Dan]: Concerned about complexity of parsing each new message type</li>
	<li>[Howard]: What are virtual ports in proposal?</li>
	<li>[Brandon]: Represents special ports at top of range, such as OFPP_FLOOD</li>
</ul>
Suggestion: refer to reserved ports instead of virtual ports.
<ul>
	<li>[Howard]: Are 16-bits sufficient for port range?</li>
</ul>
Answer (consensus): no
<ul>
	<li>[Michael]: Errors for no more space for groups versus no space for more buckets in a group</li>
	<li>[Dave]: How to identify unused logical ports?</li>
	<li>[Jean]: Separate namespace for groups/logical ports?</li>
	<li>[Rob]: Namespace is common between physical and logical ports in this proposal? (Yes)</li>
	<li>[Dan]: Can logical ports be used anywhere that physical ports can be used?</li>
	<li>[Dan]: Can a logical port be the target of another logical port?</li>
	<li>[Jean]: In multicast cast, how to handle "all ports except the one you came in on"? Is it the default?</li>
	<li>[Jean]: How to force it back out the port that it came in on?</li>
</ul>
Tests:
<ul>
	<li>[Ed]: Concern about wasted effort if tests are written early and then the proposal is updated?</li>
	<li>[Bob]: Presume tests can be written late in the proposal process?</li>
	<li>[Dave]: Group mod message creates logical ports. Concern over name of group mod.</li>
	<li>[Ed]: No queue operations on groups?</li>
	<li>[Rob]: Namespace: analogous discussion for slicing. Decision made to use separate namespace. Was this the right choice? Should we use a unified approach?</li>
	<li>[James Kempf]: Agree: doesn't see a reason for different name spaces unless the mechanisms are considerably different.</li>
	<li>[Rob]: encoraging discussion on the spec mailing list</li>
</ul>
[Jean]: Qn regarding errors. HP currently doesn't return errors for features as it will fall back to software.

&nbsp;

&nbsp;
<p align="center"><strong>OpenFlow Meeting Notes 3-30-2010</strong></p>
&nbsp;

<strong>The Dell perspective</strong>

Representatives from Dell were in attendance. They gave a brief talk outlining their perspectives/interests in OpenFlow. Some points from the talk included:
<ol>
	<li>convergence -- storage, servers, etc</li>
	<li>difficulty is in building managed networks</li>
	<li>alignment between OpenFlow and their problem set</li>
	<li>"last useful thing added to Ethernet was STP, then it got worse"</li>
	<li>want things easier in the data center</li>
	<li>complexity of traffic: multiple cores and hundreds of PCI-express lanes in a server...</li>
</ol>
<strong>Multipath update</strong>

An updated proposal will be posted to the wiki, and a notice will be sent to the mailing list

<strong>Tagging/Tunneling</strong>

Definitions:

Tagging

adding a set of bits to a packet

mark with data, that info stays with a packet, between switches

Tunneling

service model of a wire

put in, come out, unchanged

wire could use tags, be stateless, stateful.

tag is do a lookup and attach gobbledigook

&nbsp;
<ul>
	<li>[Ed Crabbe] tags change quickly and are stateless</li>
</ul>
tunnels change at the speed of the configuration protocol?
<ul>
	<li>[Jean Tourrilhes] What about VLANs?</li>
</ul>
Packets go out of tunnels. Packets don't go out of tags.
<ul>
	<li>[Christos Kolias] Tunnels have an end-to-end meaning, while tags a local one (e.g., processed at every switching node)</li>
	<li>[???] tag as mechanism for a tunnel?</li>
	<li>[Martin Casado] working def: from receiver standpoint, metadata or no metadata</li>
	<li>[Martin] Nicira's usage:</li>
</ul>
hardware-accelerated overlay

have an L3 physical world w/IGP

use tunnels to create a logical world

care about which tunnel to use but not the underlying path

set up stateful tunnels

lookup 1: to ID tunnel

lookup 2: send packet out tunnel (give to OSPF)

need to be able to demux from tunnels:
<ul>
	<li>tags added on way in to tunnels</li>
	<li>tags used for lookups on way out of tunnels</li>
</ul>
high-level req't: tunnel with hw accel, tags are stateless
<ul>
	<li>[Howard Green] Can we have multiple levels of tunnels?</li>
	<li>[Guido Appenzeller] Requested clarification of differences between tags/tunnels</li>
	<li>[Martin]: tags: add and they are there at the next switch</li>
</ul>
tunnels: push in pkt, pops out at other end, no extra data in packet at far end
<ul>
	<li>[Martin]: (returning to example): Salient point: don't want to worry about how packet physically gets somewhere (and associated lookups), just want a "port"</li>
</ul>
can have situations in which we may care about the lookups
<ul>
	<li>[Jean]: Currently easy to add a vendor extension to stuff extra data into a packet</li>
</ul>
Impossible to match on vendor extension data
<ul>
	<li>[Ed]: Timescales -- fast vs slow</li>
</ul>
slow -- doesn't belong in OpenFlow

fast, simple -- belongs in OpenFlow
<ul>
	<li>[???] lookups at terminating interface</li>
	<li>[???] how many layers of lookup?</li>
	<li>[Martin]: do we have a tag that isn't part of the packet?</li>
</ul>
Multiple tables: only tags on packets

need a logical abstraction!

requirement for L3 to handle

[Jean] use case: IP in IP from Mobile IP
<ul>
	<li>[Rajiv] Basic encaps:</li>
</ul>
IP-in-IP

MAC-in-MAC

Q-in-Q

Q

MPLS
<ul>
	<li>Additional encaps:</li>
</ul>
MPLS multicast

GRE: MAC-in-IP
<ul>
	<li>[Howard] want something that looks like a port</li>
	<li>[Nick McKeown] need a method to express encaps even if not all switches support the encap.</li>
	<li>[Ed]: Need a mechanism, still working on that</li>
	<li>[Howard]: MPLS multicast -- different label per port</li>
	<li>[Jean]: use multiple levels and lookup one at a time</li>
	<li>[Guido]: complication of multiple tables and encaps working together</li>
	<li>[Jean]: no switch will have a TCAM wide enough to do all lookups in a single table</li>
	<li>[Howard] implicit or explicit knowledge of protocol (TTL ex) - in favor of that.</li>
</ul>
prefer switch to expose capabilities
<ul>
	<li>[Ed] Another challenge: action set at a given level of encapsulation</li>
	<li>[Jean] use case: MAC in UDP</li>
	<li>[Howard] queue mapping for a tunnel, for implementing a scheduling policy</li>
	<li>[Michael Orr]: how do I create/destroy a tunnel? Configuration at both end points. Controller must tell the switch of the tunnel.</li>
	<li>[Ed]: general consensus on use cases. need to identify the mechanism</li>
	<li>[Brandon]: how many levels of nesting?</li>
	<li>[Ed]: define in a way that arbitrary number of levels can be supported. Switch may support limited.</li>
</ul>
Most will provide between 1 and 3.
<ul>
	<li>[Michael]: Q-in-Q: QoS marking based on inner packet: both layers are used!</li>
	<li>[Rajiv]: Do we need support everywhere or just at end points?</li>
	<li>[Michael]: Might need access to inner tags for QoS (identify/reclassify)</li>
	<li>[Guido]: how many levels can be considered at a single table?</li>
</ul>
what combo of tags to consider simultaneously
<ul>
	<li>[Jean] tunnels one-at-a-time, tags, multiple at a time?</li>
	<li>[Howard] performance monitoring of tunnels:</li>
</ul>
802.1ag and MPLS per management

monitor tunnels by sending messages at high frequency to detect issues
<ul>
	<li>[Nick]: chip/switch vendor may design h/w to serve a given market</li>
</ul>
choice to expose features via OpenFlow or not
<ul>
	<li>[Howard] fast protection/restoration case deserves to be resolved</li>
</ul>
key feature of tunnels is what happens when a tunnel fails
<ul>
	<li>[Jean] emergency port cache (intended jokingly)</li>
	<li>[Howard] ability to take a logical port up and down</li>
</ul>
some protocols need h/w support

problem of something implicit in switch affected port status
<ul>
	<li>[Ed]: protocol can't support all mechanisms</li>
	<li>[Nick]: We're not designing silicon. Define the basic primitives that must be there to support necessary uses</li>
	<li>[Howard]: currently can't describe syntax for all mechanisms</li>
</ul>
would like fast protection to be resolved for 1.1
<ul>
	<li>[Ed] someone proposed link between active/passive links, other similar things</li>
</ul>
need some coupling between OpenFlow and config
<ul>
	<li>[Nick]: better to add features that won't be changed between revisions</li>
	<li>[James Kempf]: might be multiple ways to support fast protection. Worth investigating further.</li>
	<li>[Nick]: Can you identify a small set of primitives that are useful to different mechanisms for failure?</li>
	<li>[Howard]: desires ability to bring tunnels up/down</li>
	<li>[Jean]: problem of port space size... currently only 16-bits</li>
	<li>[Ed]: propose move to 32-bits</li>
</ul>
Add flow cookies note!!

<strong>OpenFlow Meeting Notes 4-6-2010</strong>

<strong>Detailed notes</strong>

<strong>Slide 4</strong>
<ol>
	<li>[Jean Tourrilhes] problem with controllers doing learning (eg. trunk vs physical port)</li>
</ol>
ports useful for bidirectional
<ul>
	<li>[James Kempf] proposing diffs between logical and physical ports?</li>
	<li>[Rajiv Ramanathan] propose forwarding identifier -- could be logical port, physical port etc</li>
</ul>
<strong>Slide 5</strong>
<ul>
	<li>[KK Yap] if a logical port maps to a physical port (eg. 30L -&gt; 20P), would you get a pkt in when you forward to 30L?</li>
	<li>[???] when you rcv pkt -- do you see decapsulated pkt? (without header)</li>
</ul>
<strong>Slide 6</strong>
<ul>
	<li>[Howard Green] do i have a way to send to a different tunnel should primary tunnel fail?</li>
	<li>[Howard] by whatever means -- need coupling of whatever mechanism with state (primary/secondary)</li>
	<li>[Jean] object to having VLAN in tunnel</li>
</ul>
VLAN, need second stage lookup. when adding VLAN tag could go to any port that is member of VLAN
<ul>
	<li>[Guido Appenzeller] VLANs -- 5 or 1 virtual port?</li>
	<li>[Guido] trunk lines -- additional port per VLAN</li>
	<li>[Guido] can treat VLAN as tag or port?</li>
	<li>[James] query regarding virtual ports representing processes in the ctrl plane</li>
</ul>
do logical ports need to be tied to physical ports?
<ul>
	<li>[David Ward] two types of tunnels:</li>
	<li>tied to physical port</li>
	<li>loopback -- need a secondary lookup to work out where to send pkt</li>
</ul>
want physical port to be carried with pkt
<ul>
	<li>[Jean] do you need to specify logical *and* phsyical port?</li>
	<li>[David]</li>
	<li>[David] why do tunnels need to be bi-directional?</li>
	<li>[Jean] ctrlrs expect bi-directional ports?</li>
	<li>[David] can we have associated bi-directional?</li>
</ul>
<strong>Slide 8</strong>
<ul>
	<li>[James] tag is reference to MPLS standard?</li>
	<li>[Scott Whyte] why should there be a limitation on how many levels to look at simultaneously?</li>
	<li>[Howard] shouldn't we be able to look at multiple levels at the same time if the switch lets us?</li>
	<li>[Bob Lantz] OpenFlow 2.0 -- general match. with current MPLS/VLAN tags, restrict to outermost</li>
	<li>[Scott] shouldn't restrict ourselves now</li>
	<li>[James] most chips do 2 MPLS tags right now. if chips can do, why restrict?</li>
	<li>[Jean] believes 2 VLAN tags in a lookup in modern switch chips as well</li>
	<li>[Nick McKeown] tension between interoperability and flexibility</li>
</ul>
want to be able to query switch to identify how many levels it can do
<ul>
	<li>[Jean] complexity of specifying match. arbitrary number of levels</li>
	<li>[Guido] agree with nick</li>
</ul>
litmus test -- how hard is it to communicate capabilities?

# tags to look into -- easy to communicate and exploit
<ul>
	<li>[David] need to look at multiple tags at once: load balancing on MPLS labels. Can consruct scenarios for 3 and 4 deep easily. 5 deep could also construct</li>
	<li>[Rajiv] desire to keep simple initially</li>
	<li>[Nick McKeown] not the last word on tagging and tunneling</li>
</ul>
will add more later
<ul>
	<li>[David] w - query on number of levels of tags</li>
	<li>[Howard] believes most silicon supports two levels of tags</li>
</ul>
<strong>Slide 10</strong>
<ul>
	<li>[James/Howard] initial Ericsson version could add 2 tags</li>
</ul>
multiple tables may allow pushing of 1 tag at a time

<strong>Slide 11</strong>
<ul>
	<li>[James] separate mechanisms for IP and MPLS?</li>
	<li>[Rajiv] currently thinking of a single mechanism</li>
	<li>[Scott] wants to be able to do TTL decrement on L2 pkts</li>
</ul>
<strong>Slide 13</strong>
<ul>
	<li>[Jean] could wildcard everything except the tag (deal with switches with small flow tables)</li>
	<li>[Guido] imagine edge switches and core switches (identical)</li>
</ul>
not enough state in core

use tags
<ul>
	<li>[Joe Tardo]</li>
	<li>[David] various tunnels technologies. some can carry tags</li>
</ul>
anything that can encapsulate is a tunnel

anything that put semantics on pkt is a tag
<ul>
	<li>[Howard] orthogonal - difference between MPLS tunnels vs tags?</li>
</ul>
MPLS - need to create an MPLS cross-connect in each intermediate switch
<ul>
	<li>[Guido] tunnel vs tag is local to switch</li>
</ul>
one switch can treat something as a tunnel, another can treat it as a tag
<ul>
	<li>[Rajiv] difference is how these are set up</li>
	<li>[Dan Talayco] trying to identify list of tags we want to support</li>
</ul>
or do we want to provide a general mechanism?

are tunnels how we represent more complicated things
<ul>
	<li>[James] not supporting OAM right now -- understands concerns</li>
</ul>
need to provide a way to allow switches to do those things

tunnels live long enough that we can set attributes
<ul>
	<li>[Nick] if piece of h/w has ability to insert/remove anywhere in pkt a set of bits + ability to overwrite set of bits... this covers everything we need to do</li>
</ul>
practical problem of how to build and if we want to?

dan's point - would be great if it existed today

practical point

what is mechanism to write in most general form?

sends message to ppl building chips
<ul>
	<li>[Christos Kolias] tunnels vs tags -- atm networks.</li>
	<li>[Paulie Germano]</li>
	<li>[Howard] problem of overlap between different protocols - eg. realtime requirements</li>
	<li>[Rajiv] doesn't have anything to do with timeframes</li>
	<li>[Jean] configuration of tunnels are done via another protocol...</li>
	<li>[James] OpenFlow deals exclusively with flow table. config deals with everything around it</li>
	<li>[David] could have a tag where at midpoints we only care about certain bits -- only those bits have semantics at that point</li>
	<li>[Howard] created this thing called a tunnel is because we want to punt to another protocol</li>
	<li>[Scott] going through these mechanisms because you can't have a single table</li>
</ul>
encap -- to prefilter what needs to be in the fib

next: focus on mechs. know these mechs exist. implement the ones we need. until hardware catches up
<ul>
	<li>[Nick] up till 1.0, distinciton between mech and protocols has not been particularly comlicated. spec hasnt done a good job of separating</li>
</ul>
mechanisms - add a tag, remove a tag etc.

pragmatic reasons - in 1.1 need to support particular formats
<ul>
	<li>[Howard]</li>
	<li>[Paulie] question of what has semantics on switch-to-switch basis</li>
	<li>[David] can we add into spec whether we want something to be unidirectional, bidirectional, or associated bidirectional?</li>
	<li>[Howard]</li>
	<li>[Nick] why does switch need to know direction</li>
	<li>[David]</li>
	<li>[David] allow ability to create bidi tunnels</li>
	<li>[Jean] problem of ofpp_normal</li>
</ul>
<p align="center"><strong>OpenFlow Meeting Notes 4-13-2010</strong></p>
Thanks to Yiannis Yiakoumis for taking minutes.

<strong>Mininet</strong>

Bob Lantz and Brandon Heller presented Mininet, an OpenFlow network simulator based on process virtualization.
<ul>
	<li>[Christos Kolias]: Can you run dpctl on each of these instances?</li>
	<li>[Bob Lantz]: Yes</li>
	<li>[Jan Medev]: How do you have multiple OF switches at the kernel?</li>
	<li>[Brandon Heller]: Single OpenFlow kernel module can have multiple datapaths.</li>
</ul>
<strong>Tags And Tunnels</strong>

Slides for discussion: <a href="http://openflowswitch.org/documents/OpenFlow_1_1_Tags_04_13_2010.pdf">http://openflowswitch.org/documents/OpenFlow_1_1_Tags_04_13_2010.pdf</a>
<ul>
	<li>Rajiv Ramanathan continued Tags and Tunnels discussion from last week.</li>
</ul>
◦                    Let's let tunnels outside the OF protocol and model it as a logical port.

◦                    Defer the discussion for OFPP_NORMAL and implication without tunnels to another meeting.

◦                    Brought Nicira case with IP header and OF-IP switching.
<ul>
	<li>[Jean Tourrilhes]: OFPP_NORMAL is used to OVS as a fail open.</li>
	<li>[Jan Medev]: Why specifically IP? This is an assumption that it's a router, while it could be a switch.</li>
	<li>[Jean Tourrilhes]: OFPP_NORMAL is optional. I meant to say that we have to do our best on handling a packet.</li>
	<li>[Jan Medev]: It's vendor specific.</li>
	<li>[Rajiv]: Are tunnels bidirectional? The controller understands the mappings, switch should not care.</li>
</ul>
<strong>Tags</strong>
<ul>
	<li>[Rajiv]: Tag lookup should always happen on the outermost tag. How many though? 2, 7 or n outermost tags? Let's keep it simple with as a single tag as we don't know what to do.</li>
	<li>[Rajiv]: Generic actions for tags: push, pop, swap.</li>
	<li>[Rajiv]: How many can be pushed? (proposal : unlimited)</li>
	<li>[??] We need to have generic but also specific support.</li>
</ul>
<strong>TTL</strong>
<ul>
	<li>[Rajiv]: TTL action and TTL copy between outermost and its adjacent.</li>
</ul>
Should we have a generic TTL set action?

Do we use only copy or also rewrite?
<ul>
	<li>[???] : Rewrite only is not enough. You should be able to set as well.</li>
	<li>[Rajiv]: Should we have a resubmit action?</li>
	<li>[James Kempf]: Do you need this when you have multiple tables?</li>
	<li>[Rajiv] : Yes</li>
	<li>[???]: Are there any restrictions on the hardware resubmissions? How can you debug this?</li>
	<li>[Rajiv]: This brings the capabilities report issue.</li>
	<li>[Guido] We have to make clear that this are the basic ideas - we will revisit when Multiple tables and other are discussed.</li>
	<li>[David Ward]: Swap is an atomic operation. It's not push after pop, this is broken.</li>
	<li>[???]: Is this a semantic? Or just an implementation issue?</li>
	<li>[David Ward]: Everything deployed today is built like this. You break the implementation. This has caused lots of trouble before.</li>
	<li>[David Ward]: There was a mistake that you can pop, examine and then push. This is not swap. If you try to inspect, you require all devices to be able to check everything below the label. We have to be very clear that swap is an atomic operation. Do what <a href="http://tools.ietf.org/html/rfc3031">RFC 3031</a> says about swap and nothing more than that.</li>
	<li>[Rajiv]: It seems that there is agreement to set the TTL.</li>
	<li>[Rajiv]: Shall we be able to decrement the IP TTL along with the MPLS TTL?</li>
	<li>[Rob Sherwood]: How much do you need TTL from an OF perspective?</li>
	<li>[Scott Whyte]: If you run a network you need a way to expire packets.</li>
	<li>[Rob Sherwood]: But there are packets who don't (ethernet)</li>
	<li>[Scott Whyte]: I agree - ethernet is broken.</li>
	<li>[David Ward]: IP TTL decrement and MPLS decrement is not a valid use case. What happens is that you decrement the MPLS and then you copy it to IP (MPLS trace).</li>
	<li>[???]: There are cases where this is useful.</li>
	<li>[Scott Whyte]: Isn't this this diversing from the single tag?</li>
	<li>[KK Yap]: Should we be able to set only a smaller value? Then I will have loops if I put a bigger value.</li>
	<li>[Rajiv]: You set only in the ingress, so this is not a problem. It's only when you set a tag.</li>
	<li>[David Ward]: We don't have to struggle with these - they are defined at the RFCs.</li>
	<li>[Bob Lantz]: We don't want to reimplement the same things.</li>
	<li>[Guido]: I think we should push this later, if it refers to a future network.</li>
	<li>[KK Yap]: Maybe add an errof if you add a larger TTL?</li>
	<li>[Jean Tourrilhes]: This is not the case between IP and MPLS</li>
	<li>[Guido]: Our evolution story is whether there is a very specific thing that cannot be done with this feature.</li>
</ul>
<strong>Fast Reroute</strong>
<ul>
	<li>[Brandon Heller]: This is an implementation proposal. Have an out-of-spec agent on the switch that cleans up flows based on local event. There is a question on what behaviors needed to cover fast reroute. If it's a single case, we might add a bit. Remember emergency cache which didn't do anything due to complexity.</li>
	<li>[Rajiv]: Do we want to specify a controller delete only bit on a per flow basis?</li>
	<li>[James Kempf]: Why don't do it with priority?</li>
	<li>[Rajiv]: Good idea.</li>
	<li>[Christos Kolias]: Won't they expire?</li>
	<li>[Dan Talayco]: This is not necessary, you could have flows that don't expire.</li>
	<li>[Guido]: Does this proposal change the OpenFlow standard? I assume no, so just say no change and move on.</li>
	<li>[Rajiv]: I am concerned about the priority. What if you don't have a backup flow?</li>
	<li>[Jean Tourrilhes]: How can the switch inform the controller that it changed a flow?</li>
	<li>[Scott Whyte]: Do we need to have overlapping flows?</li>
	<li>[Rob Sherwood]: Yes, i.e. a longest match prefix.</li>
	<li>[Jean Tourrilhes]: The switch could send a flow_mod.</li>
	<li>[David Ward]: In the traditional world we put this under a protection mode, and then the switch informs the controller. You can do fast reroute, fault detection.. The switch can act autonomously and non-deterministically.</li>
	<li>[Rajiv]: Instead of saying active and backup, can't we define this through priorities?</li>
	<li>[Jean Tourrilhes]: Should the protection be applied on a flow basis, or a port basis?</li>
	<li>[David Ward]: You define the ingress data, and the ports under which you have the protection mechanism.</li>
	<li>[Jan Medev]: With priorities you might not have the same match, while actie and backup clearly defines the same one.</li>
	<li>[Rob Sherwood]: A more fundamental question. TCAM will not be able to modify its contents on a high rate. This will take some time. Is this substantial difference from going to the network? If not, why to do it? So far from some measurements, network processing is 10% of the whole delay (1 out of 10 msecs).</li>
	<li>[Scott Whyte]: What would happen if you move the controller across the WAN?</li>
	<li>[Guido]: This is clear for the switches that we use. But it shouldn't be used as a principle for our design.</li>
	<li>[Rob Sherwood]: Agree. But maybe it's not as pressing given the current HW capabilities.</li>
	<li>[Scott Whyte]: It will be very helpful for remote controllers that OF enables.</li>
</ul>
[Bob Lantz]: Then the agent becomes an on-switch controller.

&nbsp;
<p align="center"><strong>OpenFlow Meeting Notes 4-20-2010</strong></p>
<strong>Multiple Tables</strong>

Slides for discussion: <a href="http://openflowswitch.org/documents/OpenFlow_1_1_Multiple_Tables_04_20_2010.pdf">http://openflowswitch.org/documents/OpenFlow_1_1_Multiple_Tables_04_20_2010.pdf</a>

Meeting minutes taken by Nick McKeown.

<strong>Topic 1: Action Buckets</strong>

An action bucket is an abstraction to hold a set of (sequential) actions.  An action bucket can be shared by different flows: Multiple flows may map to the same bucket.

Discussions:

(Howard) Q: If the action bucket holds actions executed *after* a match, how does decapsulation work when a packet arrives? (Jean) A: Decapsulation would be performed by a logical port, and therefore happens before the match. (Glen) Comment: An action bucket may contain "send to logical port"; e.g. for sending into a tunnel. (Howard) Comment: This needs to be carefully documented for clarity.

(Brandon) Q: What is the interaction between action buckets, logical ports and link up/down? (Glen) A: We don't have any current plan for protection mechanisms inside OF -- it is assumed that, if needed, a separate agent would run on the switch to indicate that a physical or logical port is up/down. (Brandon) Q: Should we standardize the interface to the "link up/down" status inside the switch? (Room) There appeared to be consensus for doing so; and for creating a common interface/method for a local or remote agent to indicate link up/down.

(Brandon) Q: If a logical/physical port goes down, what happens to its action bucket? (GLen) A: Referring to Slide 4: If a log/phy port went down, the protection group would fall back to the previous entry in the list of action buckets.

(Jan) Q: Are all actions in a bucket executed? (Glen) A: As currently defined, you are required to execute all of them (as if sequentially). Actions are the standard actions. e.g. send to port, modify header. When protected by a backup, if you can't perform actions in the Action Bucket for the Primary, you perform none of them; but you would execute all of them for the Secondary.

(Michael) Q: What triggers the change from Primary to Secondary? (Glen) A: We need a formal description of a single standard interface -- it's on the ToDo list.

Actions arising from meeting:
<ol>
	<li>The relationship between action buckets, encapsulation and logical ports needs to be documented carefully.</li>
	<li>We need a formal description of how processing is changed from Primary to Secondary.</li>
</ol>
<strong>Topic 2: Multiple Tables</strong>

Agenda for this discussion over the next few weeks:
<ul>
	<li>Use Cases</li>
	<li>High level problem space</li>
	<li>Proposed high level architecture</li>
	<li>Feedback</li>
	<li>(Rinse, lather, repeat)</li>
</ul>
This week's discussion: Use Cases
<ul>
	<li>"Typical" backbone router scenario: Lots of routes and a few QoS policies. Problem: Table needs to hold cartesian product of QOS and routes (i.e. a table entry for each &lt;prefix, QOS-level&gt; combination)  How "Multiple Tables" can help: Two separate tables - in this example, one for L3, one for QOS-level - avoids explosion.</li>
	<li>OpenFlow on existing hardware. Problem: Many switches/routers have relatively small TCAM tables; and they often restrict the fields that can be matched.  How "Multiple Tables" can help: Switches/chips commonly have at least three tables for L2, L3 and ACL matching. The goal is to allow the controller to leverage these tables (e.g. for restricted matches on one field).</li>
	<li>Deep packet inspection. Problem: If the match is fixed (i.e. the whole header is presented to the flow table) then it means having to design the table for the largest lookup; this can drastically reduce TCAM scalability.  How "Multiple Tables" can help: Breaking into multiple small tables should lead to more efficient use of the tables.</li>
	<li>Debugging/monitoring. Problem: Imagine, say, a backbone router, with a very larger number of flows (aggregated by prefix) and you want to monitor a subset of the flows (eg. count HTTP traffic). Have set of flow rules for forwarding with prefixes. Have a rule in second table that matches *all* HTTP traffic but does not have any actions associated with it.</li>
	<li>L2/L3 flexibility after installation. Problem: There is much uncertainty in datacenters (for example) about whether to use L2 or L3. Should you deploy with your network optimized for one or the other? Can you change it later?  How "Multiple Tables" can help: In principle, OpenFlow has a flat-view of the world -- you should be able to deploy now and optimize later. This would only likely be true if you have and can exploit L2 and L3 tables flexibly and separately. Having the choice to optimize for one up-front, but choose later to change; or to have a large amount of L2 and L3 co-existing, appears to give DC operators flexibility.  Question as to whether this is applicable</li>
	<li>(Michael had an example that was missed).</li>
</ul>
Discussion:

(James) Q: Current routers allow for multiple forwarding tables (one per virtual instance; for example, one per customer). Is this a use case with ramifications on multiple tables? (Room) Consensus appeared to be that this didn't warrant adding an extra use case.

The formal part of the meeting finished at this point.

Open-ended Discussion: Although the day's agenda was about use cases, the conversation turned (you might say it digressed or degenerated - depends on your point of view) to the general approach to implementation. This is probably because some people were (rightly or wrongly) guessing the mechanism that the Working Group will propose next time.

The conversation hinged - as it often does - on the tradeoff between "backward compatibility" and "laying out a new way" for chip/switch vendors to follow. As note-taker I tried to be unbiased in keeping minutes; apologies if I failed.

Some of the tradeoffs discussed:
<ul>
	<li>How concerned should we be with supporting every protocol in use today? While clearly there is consensus that we don't need to support everything, we have not agreed on a set we must support (and by implication a set we don't need to support). This could be a valuable (necessary?) exercise; else we risk taking a stand without really knowing the stand we are taking.</li>
	<li>How flexible and complex should OpenFlow mandate the switches become? There is consensus that there is a minimal set, with minimal complexity and flexibility that a switch can implement and still be called an OpenFlow switch. The question/debate is not likely to be about the minimal set; it's likely to be about how much flexibility the OF protocol can allow in a switch: Should there be a complex negotiation of what resources and programmability a switch has? If so, would this lead to too much fragmentation of different implementations? i.e. would we end up with networks that only work with Vendor X because the controller requires a feature only supported by Vendor X. On the other hand, we must allow some ability for vendors to differentiate themselves. The only conclusion here is that we have to walk this fine line mindfully: We need to support some existing protocols (but not all); we need to</li>
</ul>
More specifically:

(Nick): If there is a simple way to meet the use cases we listed, let's hear it. We can also hear something more flexible. But this would allow us to understand the tradeoffs.

(Michael): Flexibility helps to avoid surprises later.

Jan: Be careful not to introduce so much flexibility that you are tied to particular hardware -- makes controller's job a nightmare.

Nick: We want to create a dynamic where we have a very good base set of vendor-agnostic instructions. On the other hand, we need to give room for switch/chip vendors to differentiate.

&nbsp;

&nbsp;
<p align="center"><strong>OpenFlow Meeting Notes 5-18-2010</strong></p>
&nbsp;

<strong>Mutliple Table Discussion</strong>

The agenda was to recap the multiple tables proposal from last week and move forward. But (given feedback from vendors) we ended up revisiting previous assumptions and proposed architecture.

There is also a related <a href="https://mailman.stanford.edu/pipermail/openflow-spec/2010-May/001004.html">ongoing thread</a> in the mailing list.
<ol>
	<li>Slide 1</li>
</ol>
◦                    [Glen] : Simplify multiple tables proposal. Let programmers exploit hardware, but avoid solving canonicalization problem.
<ol>
	<li>Slide 2</li>
</ol>
◦                    [Glen] : High Level View

◦                    [D. Ward] : You assume that tables are not strict - they are just represented by an ID. Clarifications by accumulation of actions VS look-ups. Do counts happen at the end of the lookup or at the end of the pipeline?

◦                    [Glen] : Count happens at each flow table.

◦                    [Martin] : By default they apply at the end, unless they are explicitly forced to do there. Assumption says that the pipeline is ordered.

◦                    [D. Ward] : Writing controllers is even more difficult, you need to know the hardware internals

◦                    [Dan] : We shouldn't care about the actual hardware, but about how the switch exposes its pipeline. This could be an abstraction of the hardware.

◦                    [Martin] : This information will be passed by an out-of-band communication, the id itself is not self-explainable.

◦                    [?]: That makes it vendor specific though.

◦                    [Martin]: Yes, that's why it sucks. We expect that in a few months we'll have a better understanding on what we have to do. At the moment think of it as (the controller writer) having a datasheed which gives info for each switch.

◦                    [Joe Tardo] : You are trying to invent the Turing machine for switches. You try to define a switch description language. Why do you still involve the datasheet and don't put this in the API?

◦                    [Martin]: The switch description language is being done, on a system's design way. We still don't know what the right abstraction is. We shouldn't go into it now.

◦                    [Joe T.] : This will be error prone etc.

◦                    [Martin] : I want the documentation. If i have this, i can program the system the way I want.

◦                    [Guido] : If I want to take all the performance a switch can give, I'll need a driver in my controller which knows in depth the specifics of that switch. Maybe the vendors be providing these drivers.

◦                    [Martin] : ok - agree. Datasheet is a wrong term. We need a piece of paper that specifies what goes where. The vendor needs to expose somehow the hardware, and then a driver level sw at the controller will map simpler semantics to the network.

◦                    [Guido] : This mechanism goes away from OpenFlow philosophy of vendor ignorance. Maybe we could name this as something else than OpenFlow (Canonicalization OpenFlow 1.1 or sg like this). OpenFlow should remain vendor independent.

◦                    [Martin] : We need this to allow people continue building their controllers and gain knowledge of how we should make the canonicalization

◦                    [James Kempf] : Mentioned something about a switch description language that was not adopted - didn't get the details.

◦                    [Martin] : We already have HALs which are useful and could act as a guide on how to go there, but it's still early

◦                    [Jan Medved] : This reminds of NetConf, where evrerybody did it's own stuff - we should be careful.

◦                    [Guido] : Is there a critical mass to have vendor independent functionality? There is a danger that we will end up with a vendor-specific protocol.

◦                    [D. Ward] : A way to avoid errors in such a situation, you can provide some hints in the controller-switch information exchange.

◦                    [Jean Toureillhes] : There is already a string for that.

◦                    [D. Ward] : A string is one option, but we could have something more defining what datapath you talk to. We need a global namespace that identifies the datapath. 42 might mean different things to different people.

◦                    [Jean T] : You have the name of the datapath (string) + the version of the datapath for identification.

◦                    [Joe T.] : How do you merge actions/list of actions?

◦                    [Martin] : The semantics are that I have a set of in-order actions and I operate on that order. We just add the option to explicitly do some actions at a specific table instead of the end of the pipeline.
<ul>
	<li>Slide 3</li>
</ul>
[Glen] : Maskable metadata, table-id.

[David E] : Are the metadata available at a single table as well, or only to the multiple-tables?

[Martin] : It doesn't make any sense to have any metadata on a single-table switch.

[Bob L] : What are the semantics? Who has access to the metadata? The next table?

[Jean T] : With multiple tables you will have more wildcards. Metadata might not be known, so you'll use wildcards and exact match will not be so useful.

[Martin] : I'd like to have a better idea. The programmer would like to use it on an exact match fashion.

[Jean] : With multiple tables exact match is gone.

[James Kempf] : The routers put an extension header in front of the packet and then they send it to the switch fabric.

[Martin] : Our semantics are that we want to put to the registers what we see on the wire. Internal tags could be used internally but we don't want them in the protocol.

[Joe T.] : How can we edit actions?

[Martin] : Currently we don't expose any functionality to edit actions. Once you appended them it's done. Would be interested controller writer's take on this.

[Martin] : What about goto/resubmit?

[D. Ward] : In order to go to a table, do I have to take the metadata to go there?

[Martin] : Yes

[D. Ward] This is inefficient

[Martin] The metadata is for the controller programmer to keep some state and make a look-up based on these.

[Guido] David says that action is also information that is carried around.

[D. Ward] Key-metadata is the input, action is the output, that's why you need two different things. I want to carry the action information to my next table. Let's say I want to do it to the end of my pipeline, I need to carry this action.

[Martin] It's different. One comments on how I am saying this to you, and the other how you do it.

[Tom Edsall] The hardware will constrain what the key is.

[Martin] There are two usecases. Something which is meaningful to me, and something that I have to communicate to the switch. Metadata is the first, actions is the second.

[D. Ward] You have an input key, and you have a result that came after going to the table. Do you need to carry them both or only the first one? I think we need to carry them both.

[Martin] I am fine with this. I thought you wanted to move actions to a blob of bits.

[D. Ward] For example, I could have the same metadata, and then I can keep accumulating the actions.

[Martin] That's more expressability from the switches which is definitely fine with me. I was under the assumption that this was not supported by the vendors.

[Jean T.] How do you edit actions? Do you assume a list and then say change the "second'" action? In some cases, you only care about the last action, so the previous would be needless.

[Martin] Do all the vendors agree that we can expose the action list? This is very important for the controllers.

[Dan, David E] exposing actions is not clear. Is this by type, by sequence, ...? In general the spec is vague about whether the action is an ordered list etc.

(There was a discussion about consistency between tables, started from the ordered list, and then went to crashes etc.)
<ul>
	<li>Action Items</li>
</ul>
[Martin] : Should we remain with the existing functionality of defining the action list, or should we include add/remove semantics for actions within that? Expecting short spec-proposals from Dave W./Joe T.?

&nbsp;

&nbsp;
<p align="center"><strong>OpenFlow Meeting Notes 6-1-2010</strong></p>
&nbsp;

Apologies for any missing names - the meeting moves fast.

Jean Tourrilhes from HP Labs presented a proposal for rate limiting (<a href="http://www.openflow.org/wk/index.php/File:Rate-limiter-proposal.pdf">File:Rate-limiter-proposal.pdf</a>). There seemed to be agreement that a rate limiter or policer, regardless of its exact name, would be of value, but there were some questions about the degree of flexibility needed for marking, as well as the mechanism's behavior in some edge cases.
<ol>
	<li>[D. Ward/Jean] naming discussion: rate limiting vs shaping vs policing; apparently policing is the phrase more associated with DiffServ</li>
	<li>questions about whether bandwidth or packet rate should be used, and what happens when both are specified for a rate limiter id: is this an error?</li>
	<li>[Martin] is buffering assumed?</li>
</ol>
◦                    Answer: Buffering is handled by the queuing mechanism (in this case, slicing subsystem)
<ol>
	<li>drop rate &gt; mark rate: error?</li>
	<li>burst size: pkts or bytes?</li>
	<li>[Martin] Customer desire is shaping as much as policing.</li>
</ol>
◦                    [Jean] sure, if over, mark and then buffer in the subsequent lookup (assumes multiple tables)
<ol>
	<li>how is the max number of rate limiters conveyed to a controller writer?</li>
</ol>
◦                    [Jean] overloaded some field in the implementation. But not strong preference.
<ol>
	<li>comments that this mechanism becomes more useful in combination with a multiple tables proposal, where a first table can mark, while a second can enqueue based on the mark output.</li>
	<li>[David Ward] Suggestion to split the structures into a general rate limiter and one specific to the actions taken for packets in the three levels (ok/exceed/violate), such as IP ToS, IP exp, etc. The proposal is tied to marking DSCP bits, and could use more flexibility/extensibility to represent other current or future fields.</li>
	<li>Most of the described proposal has been implemented in the HP switch. (modulo the DifServ type markings)</li>
	<li>[KK Yap] When a rate limiter is removed which is an action of a current flow, what happens? Should the request be denied? Should the flows using the rate limiter be actively evicted?</li>
	<li>[Jean] Current implementation marks the deleted rate limiter as a zombie to prevent reuse until all flows that point to this rate limiter time out. Actively removing could be an expensive operation.</li>
	<li>Is there a way to clear stats?</li>
</ol>
◦                    [Jean] No, this is why 64-bit counters are used. This is consistent with OpenFlow.
<ol>
	<li>Who would use this?</li>
</ol>
◦                    Leon: interested, but would need multiple table support

◦                    Rob: rate-limiting to the controller to reduce DDoSes

◦                    James Kempf: media control; pushing down end-host algorithms from Alex Snoeren

◦                    Martin: generally useful
<ol>
	<li>[David Ward] Lack of flexible actions for marking is the main quibble.</li>
</ol>
After Jean's presentation, Nick talked about IP. He made a personal request to the audience that everything talked about in these meetings is to be done on an IP-free basis, so as not to prevent future standardization of OpenFlow by some standards body.
<p align="center"><strong>OpenFlow Meeting Notes 6-29-2010</strong></p>
For much of the meeting, Rajiv went through the set of posted slides:

<a href="http://openflow.org/documents/OpenFlow_1_1_Multiple_Tables_06_29_2010.pdf">6-29-2010 meeting slides</a>
<ol>
	<li>Tom E: What about dropped packets; is it possible to do actions with a dropped packet?</li>
	<li>Rajiv R: No, only counters for table hit/misses, for now.</li>
	<li>Howard Green: Hierarchical Queuing: how would we do this?</li>
	<li>Martin C: can't more an issue with OF queues than this set of actions.</li>
	<li>Jean T: Can I enqueue and output to a specific port? This would be a way to force two forwards.</li>
	<li>Brandon: Yes, this is an oversight, due to the way queues are currently implemented.</li>
	<li>Jean T: Need to rework actions.</li>
	<li>Martin C: Point taken.</li>
	<li>Dan T: If metadata isn't maskable, then don't we have a cartesian product problem with independent metadata actions? Eg. we may want to represent an L2 table hit and QoS information. Without the ability to mask we must match on both at the same time.</li>
	<li>Jean T: Metadata without a mask precludes using the metadata for two things at the same time.</li>
	<li>Rajiv/Martin: Yes, but let's solve that later, because maskable metadata makes table mapping harder. Move forward for now.</li>
</ol>
<ul>
	<li>Asher: Does decrement TTL do matching on TTL = 0/1?</li>
	<li>Answer: No, we're adding a separate match field for invalid TTL</li>
	<li>Jean T: would like a bitmap of actions (not just meta/mask) supported in table</li>
	<li>Jean T: metadata size - what should it be?</li>
	<li>Martin C: 64 bits - is this OK? What about 32 bits?</li>
	<li>Nick: Can h/w support 64 bits?</li>
	<li>Tom E: Is it necessary to have more bits than the number of entries in a table?</li>
	<li>Jean T: would like the hardware to indicate the size.</li>
	<li>Martin: Suggestion -- start with 32 bits</li>
	<li>Dan: Semantic map in driver</li>
	<li>Nick: How does the controller know there is an error and what error is it?</li>
	<li>Howard: What if the controller ignores the hints from the switch about metadata size?</li>
	<li>Ans: Should still work, possibly at the expense of performance.</li>
	<li>Tom E: Is the switch still "working" if it drops from 1 Gb/s to 1 kb/s?</li>
	<li>Ans: Right now, yes, still working. Haven't defined any requirements on performance</li>
	<li>Martin: Qn: should metadata width be described by hw or mandated?</li>
	<li>Ed: Don't think we should define. Unreasonable to expect vendors to have a set width.</li>
	<li>no strong opinions going forward - feedback wanted</li>
	<li>Joe T: would like maskable metadata</li>
	<li>Martin: if logical pipeline does not map directly to physical pipeline then masked matches greatly increase mapping complexity</li>
	<li>Rajiv: Hard to map to hardware, suggest waiting to see if we really need mask support</li>
	<li>Martin: Would anyone object to maskable metadata?</li>
	<li>Tom: Clarify -- is this for set and match, or just match?</li>
	<li>Ans: Would be for both if we had masks</li>
	<li>Brandon: Do we need a mask? Suggest waiting -- better to cover 98% of use cases now than delaying implementation to get to 99%.</li>
	<li> ???: How would we use metadata?</li>
	<li>Martin: Example: Table 1 matches dest addr, sets metadata to represent port  Table 2 matches metadata (representing output port) and QoS fields, sets output queue appropriately</li>
	<li>Bob: Qn regarding metadata. Is setting QoS directly not enough?</li>
	<li>Martin: Example: often want to use metadata to hold output port. (Can't match on output port.) Example: VRF: metadata used to select virtual routing table</li>
	<li>Bob: Can we do with separate tables?</li>
	<li>Glen: Qn: how many contexts are typically seen in VRF use cases?</li>
	<li>Howard: easilty 10k+</li>
	<li>Glen: Switch won't expose 10k+ tables, indicates the need to use metadata</li>
	<li>Jean T: if you have maskable stuff, you need to be much smarter, whereas with non-maskable, just add an index.</li>
	<li>Dan Talayco: liked proposal N-1 (typed tables) to better define convention to fit across many switches</li>
	<li>Ed Crabbe: you can push complexity up to the controller (drivers) or down to the switch.</li>
	<li>Martin: We could go down the canonicalization path but there are projects that could use this now. Suggest proceeding with proposal as is to allow real-world experience to be gained.</li>
	<li>Tom: Non-maskable metadata is a subset of maskable. Can more easily add masks later than remove.</li>
	<li>Asher: Useful to test against use cases. Can we do X, Y, or Z?</li>
	<li>Joe Tardo: Would like to see the actual controller implementation</li>
	<li>next week, the OF1.1 core group will come back with a set of recommendations for process and contributions, as well as better-specified examples.</li>
</ul>
<a href="http://www.openflow.org/wk/index.php/OpenFlow_Meeting" target="_blank">http://www.openflow.org/wk/index.php/OpenFlow_Meeting</a>

Yup thats a Unicorn blowing rainbows, Skittles and fire out of it's ass. Thanks for stopping by.