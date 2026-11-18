+++
title = "Setting Up Overlays on Open vSwitch"
date = "2014-03-06T07:58:22+00:00"
lastmod = "2014-06-13T12:15:38+00:00"
author = "Brent Salisbury"
wp_id = 7334
categories = ["In the Lab"]
tags = ["Open vSwitch", "OpenFlow", "OpenStack", "Software Defined Networking"]
description = ""
url = "/setting-overlays-open-vswitch/"
image = "/wp-content/uploads/2014/03/Network-Overlay.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "e910145c06b78c091da0cd11083620f6afb1ace1c2b92135e53bd509da14e69e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Setting Up Overlays on Open vSwitch </h2>

Most "SDN" solutions involve overlays or at the least HW overlay gateways/ToR of some type. Some sell overlays terminating in hardware, others sell overlays terminating in the server. The encaps include standards like GRE, VXLAN and soon to be <a href="http://tools.ietf.org/html/draft-gross-geneve-00" target="_blank">Geneve </a>(Generic Network Virtualization Encapsulation: basically the good parts of the other encaps evolved). While none of these overlay networks should ever be setup by hand like we provision networks currently today, if you are trying to get a good understanding of OVS and overlays for proofing something before you code it this may be helpful. Before we do any coding to automate provisioning, it helps to work out any potential blocking ahead of time. OVS is the reference SDN datapath from developers who I regard as the best in the business. If you invest time into evolving your network, OVS is the place to start.

Rather then type out a bunch of details, I did a detailed drawing of how things can look w/ example addresses. This isn't necessarily a good beginner how-to for OpenFlow, Open vSwitch etc, but if you are looking to understand how to decouple the physical constraints of current generation networks, OVS and overlays are the only rational architecture that is actually implementable in the brownfield data center today. These are things I think you need to understand cold if you are developing or operating (or both) overlay solutions. For architecture, understanding the picture and not the implementation details is probably helpful if dealing with OpenStack in particular. A decent OpenStack integration will abstract the details but understanding them is going to be important to those working on cloud infrstructures. 

<h2> Setting Up Overlays on Open vSwitch Tutorial </h2>
This is for three Hypervisors running nested Hypervisors. Basically take a box, install KVM and boot three hosts on it. Then grab a small linux distribution like <a href="https://launchpad.net/cirros" target="_blank">Cirros</a>. Libvirt is handy for this but too low level to mix into this overview. Google for it, lots of documentation out there for it.

The topology will look something like the following:

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/03/Overlays-Blog-650x494.jpeg" >}}" alt="SDN Overlays"></figure>

I have different subnets to emphasize the flexibility overlays present. You don't need to add physical eth0 interfaces into a bridge for this. your TEP only needs to use any address on the Linux host that can reach the destination tunnel endpoint. Adding Ethernet NICs to the bridge is necessary if you are setting up a gateway host to redistribute overlay traffic into another non-overlay network.

I highly recommend only doing the configuration portion if you are new to flow forwarding and OpenFlow unless you learn through troubleshooting and are willing to work through issues which is awesome and a great way to learn. Google is your friend, I know it is mine. If you do configuration (OVSDB) only change key=flow to key=10 or some number. key=flow means the OpenFlow v1.3 flowmod will set the tun_id using the OXM extension. set_tunnel_id is as advanced as OpenFlow gets on the tunnel side which is a downside and why we are currently implementing NXM extensions in ODL. This is another good example why many of us feel there needs to be a separate software OF spec for those of us who desire to move faster then the silicon foundries. This is a totally <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">proactive</a> setup, meaning it can have or not have a controller. You can use (or script) client commands to implement the scenario which is actually what the OpenStack OVS plugin does. Alternatively you can use open source controllers such as OpenDaylight and RYU or commercial controller from Vmware (NSX).

The example will setup a full mesh of tunnels, attach a VM to br0 and all VMs on that segment should ping. I recommend Open vSwitch 2.0 or higher to ensure feature availability w/vxlan etc. Also if you are new to Open vSwitch or Linux networking I recommend just installing and tinkering around with merely adding bridges, ports and how hypervisors integrate into OVS, as tunnels will be a bit confusing to start with. 

<a href="{{< relurl "/install-open-vswitch-networking-red-hat-fedora-20/" >}}" target="_blank" rel="noopener noreferrer"> Install Open vSwitch v2 from Source on Red Hat Fedora 19</a>
<pre class="code-sample"><code>
Host1:
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=flow options:local_ip=192.168.1.180 options:remote_ip=192.168.1.181 ofport_request=10
ovs-vsctl add-port br0 vxlan1 -- set Interface vxlan1 type=vxlan options:key=flow options:local_ip=192.168.1.180 options:remote_ip=192.168.1.182 ofport_request=11
Host2:
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.183 options:remote_ip=192.168.1.182  ofport_request=10
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.182 options:remote_ip=192.168.1.183 ofport_request=10
Host3:
ovs-vsctl add-port lib vxlan -- set Interface vxlan type=vxlan options:key=flow options:local_ip=flow options:remote_ip=flow ofport_request=10
ovs-vsctl add-port lib vxlan1 -- set Interface vxlan1 type=vxlan options:key=flow options:local_ip=192.168.1.182 options:remote_ip=192.168.1.180 ofport_request=11
To test with a ping, the easiest way is to find a way to get a VM spun up. You can use namespaces and what not also to get an L3 interface for testing.

Find MAC Addresses w/a normal rule and looking at the fdb table when you have VMs running and in an OVS bridge with a tap interface:

[crayon lang="bash" ]
sudo ovs-ofctl -O OpenFlow13  add-flow br0 " priority=0, actions=normal"
sudo ovs-appctl fdb/show 
=========== For the Example, MAC Addresses are as follows ===========
TEP1-192.168.1.180
------------------
 port  VLAN  MAC                Age
    2     0  00:00:00:00:00:01   11
TEP2-192.168.1.181
------------------
 port  VLAN  MAC                Age
    2     0  00:00:00:00:00:05    3
    1     0  00:00:00:00:00:04    3
TEP3-192.168.1.182
------------------
 port  VLAN  MAC                Age
    1     0  00:00:00:00:00:08   24</code></pre>

<pre class="code-sample"><code>
==================
Host 192.168.1.180
------------------
ovs-vsctl add-br br0
ovs-vsctl set bridge br0 protocols=OpenFlow13
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=flow options:local_ip=192.168.1.180 options:remote_ip=192.168.1.181 ofport_request=10
ovs-vsctl add-port br0 vxlan1 -- set Interface vxlan1 type=vxlan options:key=flow options:local_ip=192.168.1.180 options:remote_ip=192.168.1.182 ofport_request=11
------------
Add OpenFlow Flowmods using 3 tables, Classifier, Ingress, Egress. That is an implementation choice not a requirement.
------------
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=10, actions=goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=11 actions=goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,in_port=2,dl_src=00:00:00:00:00:01 actions=set_field:5->tun_id,goto_table=1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,priority=16384,in_port=1 actions=drop"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:08 actions=output:11,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:04 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:05 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:10,output:11,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=8192,tun_id=0x5 actions=goto_table:2"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,tun_id=0x5,dl_dst=00:00:00:00:00:01 actions=output:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=8192,tun_id=0x5 actions=drop"</code></pre>

<pre class="code-sample"><code>
==================
Host 192.168.1.181
------------------
ovs-vsctl add-br br0
ovs-vsctl set bridge br0 protocols=OpenFlow13
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=flow options:local_ip=192.168.1.181 options:remote_ip=192.168.1.182 ofport_request=10
ovs-vsctl add-port br0 vxlan1 -- set Interface vxlan1 type=vxlan options:key=flow options:local_ip=192.168.1.181 options:remote_ip=192.168.1.180 ofport_request=11
------------
Add OpenFlow Flowmods using 3 tables, Classifier, Ingress, Egress. That is an implementation choice not a requirement.
------------
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=10 actions=goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=11 actions=goto_table:2"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,in_port=1,dl_src=00:00:00:00:00:04 actions=set_field:5->tun_id,goto_table=1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,in_port=2,dl_src=00:00:00:00:00:05 actions=set_field:5->tun_id,goto_table=1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,priority=16384,in_port=1 actions=drop"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,priority=16384,in_port=2 actions=drop"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:08 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:02 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:01 actions=output:11,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:10,output:11,goto_table:2" 
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=8192,tun_id=0x5 actions=goto_table:2"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,tun_id=0x5,dl_dst=00:00:00:00:00:04 actions=output:1 VM1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,tun_id=0x5,dl_dst=00:00:00:00:00:05 actions=output:2 VM2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:1,output:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=8192,tun_id=0x5 actions=drop"</code></pre>

<pre class="code-sample"><code>
==================
Host 192.168.1.182
------------------
ovs-vsctl add-br br0
ovs-vsctl set bridge br0 protocols=OpenFlow13
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.183 options:remote_ip=192.168.1.182  ofport_request=10
ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.182 options:remote_ip=192.168.1.183 ofport_request=10
------------
Add OpenFlow Flowmods using 3 tables, Classifier, Ingress, Egress. That is an implementation choice not a requirement.
------------
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=10 actions=goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,tun_id=0x5,in_port=11 actions=goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,in_port=1,dl_src=00:00:00:00:00:08 actions=set_field:5->tun_id,goto_table=1,tun_dst:ip:1.1.1.1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=0,priority=16384,in_port=1 actions=drop"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:01 actions=output:11,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:02 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:04 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,tun_id=0x5,dl_dst=00:00:00:00:00:05 actions=output:10,goto_table:2"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:10,output:11,goto_table:2" 
ovs-ofctl add-flow -O OpenFlow13 br0 "table=1,priority=8192,tun_id=0x5 actions=goto_table:2"

ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,tun_id=0x5,dl_dst=00:00:00:00:00:08 actions=output:1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:1"
ovs-ofctl add-flow -O OpenFlow13 br0 "table=2,priority=8192,tun_id=0x5 actions=drop"</code></pre>

Verify your flows are installed and counters are incrementing if you have a guest VM attached to a port. An example from an OpenStack deloyment I had running locally in a VM while writing this is:
<pre class="code-sample"><code>
$ sudo ovs-ofctl -O OpenFlow13  dump-flows br-int
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x0, duration=51452.798s, table=0, n_packets=54499, n_bytes=5752542, tun_id=0x5,in_port=10 actions=goto_table:2
 cookie=0x0, duration=51452.787s, table=0, n_packets=52544, n_bytes=5060832, in_port=1,dl_src=00:00:00:00:00:08 actions=set_field:0x5->tun_id,goto_table:1
 cookie=0x0, duration=51452.781s, table=0, n_packets=0, n_bytes=0, priority=16384,in_port=1 actions=drop
 cookie=0x0, duration=51452.757s, table=1, n_packets=0, n_bytes=0, priority=8192,tun_id=0x5 actions=goto_table:2
 cookie=0x0, duration=51452.773s, table=1, n_packets=52469, n_bytes=5057682, tun_id=0x5,dl_dst=00:00:00:00:00:01 actions=output:10,goto_table:2
 cookie=0x0, duration=51452.764s, table=1, n_packets=75, n_bytes=3150, priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:10,goto_table:2
 cookie=0x0, duration=51452.735s, table=2, n_packets=52469, n_bytes=5057682, priority=8192,tun_id=0x5 actions=drop
 cookie=0x0, duration=51452.75s, table=2, n_packets=52466, n_bytes=5057556, tun_id=0x5,dl_dst=00:00:00:00:00:08 actions=output:1
 cookie=0x0, duration=51452.742s, table=2, n_packets=2108, n_bytes=698136, priority=16384,tun_id=0x5,dl_dst=ff:ff:ff:ff:ff:ff actions=output:1</code></pre>

Here are some helpful aliases/commands that I use for client commands.

<pre class="code-sample"><code>
### OVS Aliases ###
alias novh='nova hypervisor-list'
alias novm='nova-manage service list'
alias ovstart='sudo /usr/share/openvswitch/scripts/ovs-ctl start'
alias ovs='sudo ovs-vsctl show'
alias ovsd='sudo ovsdb-client dump'
alias ovsp='sudo ovs-dpctl show'
alias ovsf='sudo ovs-ofctl '
alias logs="sudo journalctl -n 300 --no-pager"
alias ologs="tail -n 300 /var/log/openvswitch/ovs-vswitchd.log"
alias vsh="sudo virsh list"
alias ovap="sudo ovs-appctl fdb/show "
alias ovapd="sudo ovs-appctl bridge/dump-flows "
alias dpfl=" sudo ovs-dpctl dump-flows "
alias ovtun="sudo ovs-ofctl dump-flows br-tun"
alias ovint="sudo ovs-ofctl dump-flows br-int"
alias ovap="sudo ovs-appctl fdb/show "
alias ovapd="sudo ovs-appctl bridge/dump-flows "
alias ovl="sudo ovs-ofctl dump-flows br-int"
alias dfl="sudo ovs-ofctl -O OpenFlow13 del-flows "
alias ovls="sudo ovs-ofctl -O OpenFlow13  dump-flows br-int"
alias dpfl="sudo ovs-dpctl dump-flows "
alias ofport=" sudo ovs-ofctl -O OpenFlow13 dump-ports br-int"
alias del=" sudo ovs-ofctl -O OpenFlow13 del-flows "
alias lsof6='lsof -P -iTCP -sTCP:LISTEN | grep 66'
alias vsh="sudo virsh list"
alias ns="sudo ip netns exec "</code></pre>

To setup overlays using OpenStack, OpenDaylight, Open vSwitch, OpenFlow, OVSDB, lol thats a lot of Opens, see the following:

<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}" target="_blank" rel="noopener noreferrer">OpenDaylight OpenStack Integration with DevStack on Fedora</a>

For more regarding OVS and flow forwarding using OpenFlow and/or OpenFlow/Nicira extensions take a look at Ben Pfaff's latest draft of OpenFlow/OVS fields in Open vSwitch. This is what in my opinion OpenFlow should look like in order to facilitate overlays with open standards in the Data Center. Don't confuse overlays with hypervisor networking only. By far the majority of SDN data center implementations use overlays regardless of whether the TEP terminates on the soft vSwitch or the ToR physical switch. Cisco ACI for example setup TEPs in their leaf HW nodes using some sort of signaling which I have no idea about beyond overlays and a few bits in the VXLAN header to be keyed on for application classification. 
I am a developer on the OpenDaylight projejct and we managed to get basic overlay functionality implemented but we have certainly hit the wall on adding functionality without using NXM extensions. Long story shot, if the OpenFlow specification is to stay relevant (which Dan Pitt and company work hard to do so) it needs to address these functions in the spec rather then in OF-Config only. For example, IPv4 Tunnel Src/Dest is a very obvious one. The current ONF answer would be use OF-Config, in OpenDaylight we solved it using the awesomeness of the OVSDB protocol (<a href="https://datatracker.ietf.org/doc/rfc7047/" target="_blank">RFC 7047</a>) from Pfaff and Davie. 

For for those in networking digging under the covers of SDN or developers implementing SDN solutions, I think its important to weigh in on this topic. Some incumbents would be fine with an outcome of SDN to be so fragmented that it resembles SNMP MIBs with little overall impact/disruption. I for one will use whatever protocol required as long as it is open and more important supported by the data plane. It would be nice if it is an agreed upon "standard" but that doesnt mean I need a committee of people not engaged with community. A community defacto can also be a standard and often a much more meaningful standard at that. Take a look at the document, Ben has added a ton of details that have only come from experience of being on the forefront of SDN from his leadership and development in the Open vSwitch project.

<a href="http://benpfaff.org/~blp/ovs-fields.7.pdf" target="_blank" rel="noopener noreferrer">OpenFlow and Open vSwitch Fields 2nd Draft via benpfaff.orf</a>

Cya!