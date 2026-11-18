+++
title = "OpenVswitch and GRE tunnel notes"
date = "2012-02-14T04:18:03+00:00"
lastmod = "2012-12-01T07:21:26+00:00"
author = "Brent Salisbury"
wp_id = 174
categories = ["In the Lab"]
tags = ["KVM", "OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openvswitch-and-gre-tunnel-notes/"
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "e2a55b530f1607ed9f4e81e0aee42b84a175d3427a24361e4abc79a16c000a19"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

Here is a quick post for setting up GRE tunnels on OpenVswitch. Both Vswitch boxes are attached to an OpenFlow Beacon controller.

More up to date how-to can be found here:

<a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank"><em>Configuring VXLan and GRE tunnels on OpenvSwitch</em></a>

KVM live storage migration makes an interesting story and run at VMware tools. The dreaded layer2 data center link conversation may never go away unfortunately. It would be nice to push this to the Hypervisors rather than mucking up our pretty networks.

oVirt is looking pretty slick in recent weeks for a KVM Hypervisor virtual manager for HA, live migration, storage management, system scheduler etc. Started an install but haven't finished enough of it to test yet.

<strong>Ovswitch A</strong>
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">ovs−vsctl add−port br0 vlan10 tag=10 −− set Interface vlan10 type=internal
ovs-vsctl add-br br1
ovs-vsctl add-port br1 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.76
ovs−vsctl add−port br1 vlan10 tag=10 −− set Interface vlan10 type=internal
ifconfig vlan10 10.1.1.2 netmask 255.255.255.0 up</pre>
<strong>Ovswitch B</strong>
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">ovs−vsctl add−port br0 vlan10 tag=10 −− set Interface vlan10 type=internal
ovs-vsctl add-br br1
ovs-vsctl add-port br1 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.25
ovs−vsctl add−port br1 vlan10 tag=10 −− set Interface vlan10 type=internal
ifconfig vlan10 10.1.1.1 netmask 255.255.255.0 up</pre>
######## Output #############

/home/brent# ovs-appctl fdb/show br1
port VLAN MAC Age
3 10 9a:58:d9:fa:e2:1f 4
2 10 a6:26:6a:9f:f8:ba 4

/home/brent# ovs-dpctl show

system@br1:
lookups: hit:6813 missed:176 lost:0
flows: 0
port 0: br1 (internal)
port 2: vlan10 (internal)
port 3: gre0 (gre: remote_ip=192.168.1.76)

Destination Gateway Genmask Flags Metric Ref Use Iface
default 192.168.1.1 0.0.0.0 UG 0 0 0 br0
192.168.1.0 * 255.255.255.0 U 0 0 0 br0
10.1.1..0 * 255.255.255.0 U 0 0 0 vlan10

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/02/lab-gre.jpeg"><img class="alignleft  wp-image-176" title="lab-gre" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/02/lab-gre.jpeg?w=300" alt="" width="360" height="100" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

Some completely unscientific numbers are here. Granted this is a laptop burning a whole in my lap going to a crummy old lab box. We are going to test soon on some high end gear and see what the perf numbers are over GRE to see what kind of scale looks reasonable.

<strong>Baseline over Eth0 not in the GRE tunnel</strong>
<div>Server listening on TCP port 5001</div>
<div>TCP window size: 85.3 KByte (default)</div>
<div>------------------------------------------------------------</div>
<div>[  4] local 192.168.1.76 port 5001 connected with 192.168.1.25 port 53498</div>
<div>[ ID] Interval       Transfer     Bandwidth</div>
<div>[  4]  0.0-11.4 sec  7.75 MBytes  5.72 Mbits/sec</div>
<div></div>
<div><strong>Through the GRE tunnel</strong></div>
<div></div>
<div>^Croot@optiplex:/home/brent# iperf -s -B 192.168.10.2</div>
<div>------------------------------------------------------------</div>
<div>Server listening on TCP port 5001</div>
<div>Binding to local address 192.168.10.2</div>
<div>TCP window size: 85.3 KByte (default)</div>
<div>------------------------------------------------------------</div>
<div>[  4] local 192.168.10.2 port 5001 connected with 192.168.10.1 port 33538</div>
<div>[ ID] Interval       Transfer     Bandwidth</div>
<div>[  4]  0.0-13.1 sec  4.75 MBytes  3.05 Mbits/sec</div>
<div></div>
<div>How insane is this? We need to figure out how this scales. Redundancy is obviously not included. Too late at night to think atm.</div>
<div></div>
<div><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/02/gre-tap1.jpeg"><img class="alignleft size-full wp-image-181" title="gre-tap" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/02/gre-tap1.jpeg" alt="" width="232" height="227" /></a></div>
<div></div>