+++
title = "Configuring an OpenFlow POX SDN Controller and HP Switches"
date = "2012-07-18T04:46:10+00:00"
lastmod = "2013-03-16T05:36:13+00:00"
author = "Brent Salisbury"
wp_id = 1754
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/configuring-an-openflow-pox-sdn-controller-and-hp-switches/"
image = "/wp-content/uploads/2012/07/unicorn-rainbow.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ef125a94dede768ddcea2c9913da17f786f8c20639313cf603ddcbf0f24612f2"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Configuring an OpenFlow POX SDN Controller and HP Switches</h2>
<hr>
There is an updated post with the newest HP OpenFlow firmware that can be found at: <a href="{{< relurl "/configure-an-hp-openflow-switch-for-floodlight/" >}}">Configure an HP OpenFlow Switch for Floodlight</a>
<hr>
Configuring an OpenFlow POX SDN Controller and HP Switches: HP has been supporting OpenFlow v1.0 with general availability longer than anyone in the industry. While there are limitations, just as most vendors will have as we start exploring exposing and/or decoupling control planes. Installing the SDN / OpenFlow controller to attach to the HP switch is very simple using open source controllers like POX and <a href="http://floodlight.openflowhub.org/" target="_blank">FloodLight</a>. Specific limitations revolve around attempting to modify multiple headers in the OFAction function. This is likely a TCAM width limitation.

POX is a Python based OpenFlow Controller developed by Murphy McCauley at UC Berkeley. POX is great for fast development proofing, along with being platform independent by virtue of being Python based. Mre information can be found <a href="http://www.noxrepo.org/pox/about-pox/" target="_blank">here</a>. I highly recommend it over NOX for learning and prototyping since Python is a more abstracted language unless you need to manage hardware resources for performance. Also the development seems to be more focused on POX. Murphy has a nice set of modules to load different features. He has some new ones in the pipe that will help with experimentation for people to get more comfortable with SDN. I really like it for terrible programmers like myself to have an interpreted option to tweak or add modules to.

Here is the algorithm for each new flow that POX follows using the L2 learning python module. This will have your switch operate similarly to your L2 forwarding switch today. Notice step 2. typically an LLDP will trigger a OFPT_PACKET_IN event which would punt the packet to the controller thus ignore if transparent.
<h2>packet-in events</h2>
<ol class="legacy-numbers">
<ol>
	<li>Use source address and port to update address/port table.</li>
	<li>Is destination address a Bridge Filtered address, or is Ethertpe LLDP? * This step is ignored if transparent = True * Yes: Drop packet to avoid forwarding link-local traffic (LLDP, 802.1x) DONE</li>
	<li>Is destination multicast? if Yes:Flood the packet DONE</li>
	<li>Port for destination address in our address/port table? No: Flood the packet DONE</li>
	<li>Is output port the same as input port? Yes: Drop packet and similar ones for a while</li>
	<li>Install flow table entry in the switch so that this</li>
	<li>flow goes out the appopriate port</li>
	<li>Send buffered packet out appropriate port</li>
</ol>
</ol>

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/Island.jpg" >}}" alt="OpenFlow Islands"></figure>

<strong>Figure 1.</strong> The Layer2 access edge can function in this manner.

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/traffic-island.jpg" >}}" alt="OpenFlow Islands"></figure>

<strong>Figure 2.</strong> The traffic flow between Vlans/Networks/bcast domains will punt to traditional routers/L3 switches to find a default gateway using an SDN switch with L2 learning. To begin integrating your L3 gateways refer to OpenFlow normal functionality. OFP_Normal
<h2>Install POX OpenFlow Controller</h2>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">sudo apt-get install git
git clone http://github.com/noxrepo/pox
cd pox
./pox.py forwarding.l2_learning</pre>
<h2>Configure the HP OpenFlow Switch</h2>
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">J8693A Configuration Editor;
Created on release #K.15.06.5008
Ver #02:10.0d:1f
hostname &quot;HP-1&quot;
module 1 type J86yyA
module 2 type J86xxA
ip routing
vlan 1
name &quot;Controller Traffic OOB&quot;
untagged 24 (To Controller Port 24)
ip address ip address (Source of Switch to Controller)
exit
vlan 10
name &quot;User Segment OF Controlled Paths Vlan10 10.100.1.10-24&quot;
untagged 10 (Port 10 Access)
tagged 1 (Trunk)
exit
vlan 20
name &quot;User Segment OF Controlled Paths Vlan20 10.200.1.10-24&quot;
untagged 11 (Port 11 Access)
tagged 1 (Trunk)
exit
openflow
vlan 10
enable
controller &quot;tcp::6633&quot; sw-rate 10000 hw-rate 10000
exit
exit
openflow
vlan 20
enable
controller &quot;tcp::6633&quot; sw-rate 10000 hw-rate 10000
exit
exit</pre>
There is a problem with the values in the OFPT_HELLO version being sent from the HP firmware and does not send an explanation in the OFPHFC_COMPATIBLE optional ASCII explanation but it still negotiates and works. I have not seen a new firmware release from HP since February for the 3500, humph :/
<pre class="brush: bash; gutter: true">% ./pox.py forwarding.l2_learning
 POX 0.0.0 / Copyright 2011 James McCauley
 DEBUG:core:POX 0.0.0 going up...
 DEBUG:core:Running on CPython (2.7.3/Apr 20 2012 22:39:59)
 INFO:core:POX 0.0.0 is up.
 This program comes with ABSOLUTELY NO WARRANTY. This program is free software,
 and you are welcome to redistribute it under certain conditions.
 Type &#039;help(pox.license)&#039; for details.
 DEBUG:openflow.of_01:Listening for connections on 0.0.0.0:6633
 Ready.
 POX&gt;
 POX&gt; ERROR:openflow.of_01:[Con 1/176766955434440384] OpenFlow Error:
 [Con 1/176766955434440384] Error: header:
 [Con 1/176766955434440384] Error: version: 1
 [Con 1/176766955434440384] Error: type: 1 (OFPT_ERROR)
 [Con 1/176766955434440384] Error: length: 20
 [Con 1/176766955434440384] Error: xid: 9
 [Con 1/176766955434440384] Error: type: OFPET_BAD_REQUEST (1)
 [Con 1/176766955434440384] Error: code: OFPBRC_BAD_TYPE (1)
 INFO:openflow.of_01:[Con 1/176766955434440384] Connected to 00-9c-02-b2-76-c0|628</pre>
<ul>
	<li>Next will be how to setup an <a href="{{< relurl "/how-to-build-an-sdn-lab-without-needing-openflow-hardware/" >}}" target="_blank">SDN lab without any hardware.</a></li>
</ul>