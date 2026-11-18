+++
title = "Configure an HP OpenFlow Switch for Floodlight"
date = "2013-03-16T05:20:31+00:00"
lastmod = "2013-07-07T22:48:46+00:00"
author = "Brent Salisbury"
wp_id = 6008
categories = ["In the Lab"]
tags = ["HP", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/configure-an-hp-openflow-switch-for-floodlight/"
image = "/wp-content/uploads/2013/05/openflow2.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c9322dc19ddd306d156f9a48682f6398e7710a43fdf7f2430c0cb0969d8db2a1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Configure an HP OpenFlow Switch for Floodlight </h2>
This is a revised tutorial to configure an HP OpenFlow switch for Floodlight or any other OpenFlow controller. HP revised its firmware a few months back which is great. HP has been supporting OpenFlow on its switches with generally available code longer then any other networking vendor. Other vendors with GA OpenFlow firmware are <a href="http://community.brocade.com/thread/8445?start=0&tstart=0" target="_blank">Brocade</a> and Pica8. Maturity of OpenFlow agents should be taken into account when purchasing hardware. Most agents are Open vSwitch based but vendor allocations to software development of porting OVS has been slow while waiting on large volume customer demand.

<h2>Hybrid OpenFlow Ships in the Night</h2>
Hybrid OpenFlow support is a must for any vendor. We have reviewed different <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies/" >}}" target="_blank">hybrid architectures</a> such as <a href="{{< relurl "/hybrid-openflow-using-the-normal-action/" >}}" target="_blank">normal</a> and "ships in the night". For this tutorial we will use the simple ships in the night, meaning there is one Vlan enabled with OpenFlow (VID 3) and one on the native network (VID 1). The native network on Vlan 1 is also the control channel for the FloodLight OpenFlow controller and the host on the native network. The control Vlan could just as easily be a dedicated management network.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/OpenFlow-Hybrid-HP.png" >}}" alt="HP OpenFlow Hybrid Ships in the Night"></figure>


<h2>Hybrid OpenFlow Gateways</h2>
The OpenFlow Vlan L3 gateway can be as simple as a native switch or router tapped into the Vlan with an L3 interface. OpenFlow hosts can use that interface as the default gateway to leave the SDN island. The SDN edge can also use OFPP_Normal to push flows to the normal forwarding pipeline. With one OpenFlow rule you can have all traffic processed as it normally would by the switch. HP supports the "normal" OpenFlow action. All vendors need strong hybrid OpenFlow support if they expect to be taken seriously for early SDN non-vSwitch networks.

<h2>Download and Configure The <a href="http://floodlight.openflowhub.org" target="_blank">Floodlight</a> OpenFlow Controller</h2>
Floodlight and <a href="http://www.noxrepo.org/pox/about-pox/" target="_blank">POX OpenFlow</a> controllers are both super easy to get up and running. Both can load as flood and learn <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">reactive switches or proactive</a> only configurations. For building the controller on CentOS check out a colleague <a href="https://twitter.com/buraglio" target="_blank">Nick Buraglio's</a> blog <a href="http://www.forwardingplane.net/2013/02/building-a-floodlight-openflow-controller-on-centos-6/" target="_blank">post.</a> 

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">
sudo apt-get install openjdk-7-jre git
git clone git://github.com/floodlight/floodlight.git
cd floodlight
ant
java -jar target/floodlight.jar</pre>

<hr>
<h2>Configure the HP switch for OpenFlow</h2>

The follwoing HP configuration refelcts the latest firmware. Use "show open flow ?" to view related OpenFlow operational commands. This will also tell you what flows are in hardware and software. My colleague <a href="https://twitter.com/owens_bill" target="_blank">Bill Owens</a> wrote a nice article at <a href="http://packetpushers.net/openflow-switching-performance-not-all-tcam-is-created-equal/" target="_blank">Packet Pushers</a> recently on this topic that I highly recommend.

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">; J8693A Configuration Editor; Created on release #K.15.10.0003
; Ver #03:03.1f.ef:f0
module 1 type j86yya
module 2 type j86xxa
ip routing
openflow
   enable
   controller-id 100 ip 10.1.1.10 controller-interface vlan 1
   instance &quot;OpenFlow-Orange&quot;
      member vlan 3
      controller-id 100
      limit software-rate 10000
      enable
      exit
   exit
vlan 1
   name &quot;DEFAULT_VLAN&quot;
   ip address 10.1.1.10 255.255.255.0
   exit
vlan 3
   name &quot;VLAN3&quot;
   ip address 192.168.1.210 255.255.255.0
   exit
</pre>
<hr>
<h2>OpenFlow guide from HP and additional resources</h2> HP continues to put out nice documentation regarding their OpenFlow support. Hybrid OpenFlow is pretty easy to implement. Starting out with a test/dev Vlan is a reasonably safe implementation strategy. Peel traffic off the top of the rules list and either drain traffic to a native L3 gateway or use the normal action to fork the traffic to the normal FIB. SDN is about ingesting traffic at the edge and having flexibility in classification and policy application. Use it early as a tool for niche <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">applications</a> and you will be well positioned as more robust <a href="{{< relurl "/sdn-openflow-policy-abstractions/" >}}" target="_blank">abstractions</a> come out of product pipelines.

Download latest OpenFlow guide from HP <a href="http://bizsupport2.austin.hp.com/bc/docs/support/SupportManual/c03512348/c03512348.pdf" target="_blank" rel="noopener noreferrer">HP OpenFlow Switches</a>
<hr>
HP recently announced their new NAC security application using OpenFlow called Sentinel. I am quite interested about the possibility of enterprise security and SDN. 802.1x NAC has been a non-starter due to interoperability and data plane constraints in the traditional Ethernet fabric. Take a listen to <a href="http://etherealmind.com" target="_blank">Greg</a> and <a href="http://packetpushers.net/author/ecbanks/" target="_blank">Ethan</a> talking to HP about this recently.
<a href="http://packetpushers.net/show-138-hps-sdn-products-strategy/" target="_blank" rel="noopener noreferrer">PacketPushers Show 138 – HP’s Software-Defined Networking (SDN) Strategy and Solution</a>

<hr>
Thanks for stopping by!