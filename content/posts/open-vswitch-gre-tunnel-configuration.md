+++
title = "Open vSwitch GRE Tunnel Configuration"
date = "2012-04-19T06:45:57+00:00"
lastmod = "2013-05-13T19:25:52+00:00"
author = "Brent Salisbury"
wp_id = 390
categories = ["In the Lab"]
tags = ["OpenFlow", "Tutorials"]
description = ""
url = "/open-vswitch-gre-tunnel-configuration/"
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a57ce3892acf204f51788f934827a9a5c684532cda35d6f0518209ae19eaf6ca"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Open vSwitch GRE Tunnel Configuration</h2>
<aside class="legacy-callout"><strong>Open vSwitch Updated Tutorial</strong>-I updated this September 20, 2012. Also adding this PDF from a instruction I did over the summer at an Internet2 conference. Download the lab here <a href="{{< relurl "/wp-content/uploads/2012/04/openvswitch.openflow.gre_.tutorial1.pdf" >}}">OpenFlow and Open vSwitch GRE Tunnel Configuration Tutorial</a>.
-Another lab building from source with video and pretty vetted is <a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}"> Configuring VXLan and GRE Tunnels on OpenvSwitch</a></aside>
<h2>Open vSwitch GRE Tunnel Screencast</h2>
<p><a href="http://www.youtube.com/watch?v=VMP4Q2XtFjw">Watch video on YouTube</a></p>

We continue to destroy our nice clean data centers to facilitate poor application architectures that do not scale in a layer 3 fashion. We continue to come up with new technologies using old architectures to turn our networks into flat data centers under the guise of “cloud mobility”. Ok sorry, I got that out of my system.
<h2>Open vSwitch and Data Center Overlays</h2>
Open vSwitch is a virtual switch or virtual Ethernet bridge (VEB) becoming quite popular and being backed by many vendors as the alternative to the virtual switches in some of the productized hypervisors like Hyper-V, VMware etc. Overlays are not new concepts, but are being used in new use cases. It is an early mechanism to uncouple the virtual from the physical. What remains to be seen, is whether this is a bridge until hardware becomes generalized or the new standard.

The OVS developers is still ironing out the control portion of OVS, with that will come the scale of L3 addressing and multipathing to each Tunnel End Point (TEP). The current code supports the GRE key lookup and forwarding while NVGRE and VXlan have at least taken a stab at the control plane, unfortunately through multicast for broadcast flooding L Next-gen ASICs will and Ethernet controllers will open the door to more plates of spaghetti.
<p style="text-align: center;"><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/l2ol3-generic-packet.jpg"><img class="size-full wp-image-391 aligncenter" title="l2ol3-generic-packet" alt="" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/l2ol3-generic-packet.jpg" width="527" height="169" /></a></p>
<strong>Figure 1. </strong> Generic look at where the headers are being modified.

I am still on the fence on where a TEP should reside, on a physical top of rack end of row network device or reside in the hypervisor. The networking guy in me would prefer that to be an S-tag in a pseudowire, but I can’t help but lean towards anything in software, moving forward to provide programmatic scale. We are on the path of the programmatic abstraction to being migrated into our network operating systems, but that is a big ship that will presumably take a while to steer.

Enough gibber on to an L2GRE configuration on an Open vSwitch. I did this because I was surprised to not see a GRE cookbook on the Open vSwitch cookbook page. <a href="http://openvswitch.org/support/config-cookbooks/">http://openvswitch.org/support/config-cookbooks/</a>

BTW why the kitchen cooking trend these days? What happened to the good old how-to? Not cloudy enough, that needed abstraction also. Do we change RTFM to RTFC? I blame the Opscode Chef Openstack installer.
<h2>Open vSwitch Installation Tutorials</h2>
<ul>
	<li>First install Open vSwitch on a couple of nodes. The following links will help you get started:</li>
</ul>
<ul>
	<li>Install from packages <a href="{{< relurl "/2012/05/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/" >}}" target="_blank">http://networkstatic.net/2012/05/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/</a></li>
	<li>Compile from source <a href="http://networkstatic.wordpress.com/2012/04/16/installing-and-configuring-openvswitch-on-ubuntu-12-04-precise-pangolin/">http://networkstatic.wordpress.com/2012/04/16/installing-and-configuring-openvswitch-on-ubuntu-12-04-precise-pangolin/</a></li>
	<li>I am using KVM for the example to spin up a tap interface for the VM to use for the TEPs. Here is a how-to for that. <a href="http://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/">http://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/</a></li>
</ul>
<a href="{{< relurl "/wp-content/uploads/2012/04/gre.openvswitch.jpg" >}}"><img class="alignleft size-full wp-image-2810" title="gre.openvswitch" alt="gre openvswitch" src="{{< relurl "/wp-content/uploads/2012/04/gre.openvswitch.jpg" >}}" width="583" height="245" /></a>

<strong>Figure 2. </strong>Here is the topology of the configuration.

<strong>Open vSwitch 1 configuration</strong>
<pre class="brush: bash; gutter: false">sudo ifconfig eth1 0
sudo ovs-vsctl add-br br1
sudo ovs-vsctl add-br br2
sudo ovs-vsctl add-port br1 eth0
sudo ifconfig br1 192.168.1.155 netmask 255.255.255.0
sudo ifconfig br2 10.1.1.1 netmask 255.255.255.0
sudo ovs-vsctl add-port br2 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.152</pre>
<strong>Open vSwitch 2 configuration</strong>

Hypervisor 2 Configuration:
<pre class="brush: bash; gutter: false">sudo ifconfig eth1 0
sudo ovs-vsctl add-br br1
sudo ovs-vsctl add-br br2
sudo ovs-vsctl add-port br1 eth0
sudo ifconfig br1 192.168.1.152 netmask 255.255.255.0
sudo ifconfig br2 10.1.1.2 netmask 255.255.255.0
sudo ovs-vsctl add-port br2 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.155</pre>
<ul>
	<li>Add KVM tap VIF script</li>
</ul>
/etc/ovs-ifup and /etc/ovs-ifdown

#Paste in the following with br1 = equalling the bridge you made in ovs-vsctl. Since we want the VM on the bridge that will get tunneled we are not using br0.
Create this script for provisioning.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">nano /etc/ovs-ifup
#+++++++++++++++++++++++++++++++
#!/bin/sh
switch=&#039;br2&#039;
/sbin/ifconfig $1 0.0.0.0 up
ovs-vsctl add-port ${switch} $1
#+++++++++++++++++++++++++++++++
chmod +x /etc/ovs-ifup</pre>
Then one for ifdown to de-provision.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">nano /etc/ovs-ifdown
#+++++++++++++++++++++++++++++++
#!/bin/sh
switch=’br2’
/sbin/ifconfig $1 0.0.0.0 down
ovs-vsctl del-port ${switch} $1
#+++++++++++++++++++++++++++++++
chmod +x /etc/ovs-ifdown</pre>
<ul>
	<li>Now spin up your VM. I use the following to boot Ubuntu off CD. The VM instance will tap br1 (bridge1) on the 10.1.1.0/24 network.</li>
</ul>
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">kvm -m 512 -net nic,macaddr=12:34:52:CC:CC:10 \
 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown \
 -cdrom /home/brent/images/ubuntu-11.10-desktop-i386.iso &amp;</pre>
<h2>Attach OpenvSwitch to a Floodlight openFlow Controller</h2>
<em>Hypervisor 1</em>
<pre class="brush: text; gutter: false">#Install the Floodlight Openflow Controller
git clone git://github.com/floodlight/floodlight.git
cd floodlight
ant
java -jar target/floodlight.jar
#Add OVS bridges
sudo ovs-vsctl set-controller br1 tcp:192.168.1.155:6633
sudo ovs-vsctl set-controller br2 tcp:192.168.1.155:6633</pre>
<em>Hypervisor 2</em>
<pre class="brush: text; gutter: false">#Install the Floodlight Openflow Controller
git clone git://github.com/floodlight/floodlight.git
cd floodlight
ant
java -jar target/floodlight.jar
#Add OVS bridges
sudo ovs-vsctl set-controller br1 tcp:192.168.1.155:6633
sudo ovs-vsctl set-controller br2 tcp:192.168.1.155:6633</pre>
Some commands to view the configuration and ports:
<div>
<div>ubuntu-12:brent# <span style="color: #008000;">ovs-appctl fdb/show bra <em><span style="color: #000000;">(generate traffic ie ping as table age out after 300 seconds)</span></em></span></div>
<div></div>
<div> port  VLAN  MAC                Age</div>
<div>    9     0  12:74:52:cc:cc:10    0 (VM 1)</div>
<div>   12     0  12:34:52:cc:cc:10    0 (VM 2)</div>
</div>
<ul>
	<li>More on how to get KVM integrated here: <a href="http://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/">http://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/</a></li>
	<li>We now should be able to ping from VM1 -&gt; VM2 and see the mac address table flood and learn one another’s ARP entries.</li>
</ul>
<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/1-bridge.jpg"><img class="aligncenter  wp-image-393" title="openvswitch vlan" alt="openvswitch vlan" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/1-bridge.jpg" width="308" height="294" /></a>

<strong>Figure 2. </strong>Now we have flattened out these two endpoints whether in the same data center or across the city/state that can be used for a live workload migration (e.g. vMotion).
<p style="text-align: center;"><a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/gre-cloud.jpg"><img class="wp-image-394 aligncenter" title="openvswitch gre tunnels" alt="openvswitch gre tunnels" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/04/gre-cloud.jpg" width="448" height="332" /></a></p>
<strong>Figure 3. </strong>There is some scale to where this can go, for either provisioning elastic compute nodes or migrating, live migrations or just fixing broken applications.