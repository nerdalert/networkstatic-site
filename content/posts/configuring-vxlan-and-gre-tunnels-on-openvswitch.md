+++
title = "Configuring VXLAN and GRE Tunnels on OpenvSwitch"
date = "2012-07-02T06:52:13+00:00"
lastmod = "2013-10-21T05:36:18+00:00"
author = "Brent Salisbury"
wp_id = 1485
categories = ["In the Lab"]
tags = ["Open vSwitch", "OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/configuring-vxlan-and-gre-tunnels-on-openvswitch/"
aliases = ["/2012/07/configuring-vxlan-and-gre-tunnels-on-openvswitch/"]
image = "/wp-content/uploads/2012/07/Network-Tunnels.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "713d47ed5d1c0cfe60bfa25bcdf2218a6b31df38e9ab25d844ab1bd14fd5c1ec"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Configuring VXLan and GRE tunnels on OpenvSwitch</h2>
<aside class="legacy-callout"><strong>Update: VXLan Encapsulation </strong>VXLan is now upstreamed into the Master build. It is worth mentioning that is the VXLAN framing only, not the Multicast control plane functionality. So basically no need to pull from the fork anymore but pull directly from the Open vSwitch Master or 1.10+ tarball (approximately). </aside>
I have done a couple of GRE tunnel how-tos using OpenvSwitch (OVS). I had been itching to give VXLan a spin in OVS so why not ferret out someones tree on GitHub. I believe VXLan is still scheduled to officially release soon in OpenvSwitch. So here are the steps for installing, configuring tunnels on OpenvSwitch with VXLan and GRE encapsulations. At the end we will compare some of the protocols with difference MTU sizes. The results were interesting I think (for a nerd). We will be installing and then configure both GRE and VXLan encapsulated tunnels using Open vSwitch.

I like seeing some collaboration of really smart people from different companies as displayed in the GPL below.
<p class="textbox"><aside class="legacy-callout">
/* * Copyright (c) 2011 Nicira Networks.
* Copyright (c) 2012 Cisco Systems Inc.
* Distributed under the terms of the GNU GPL version 2.
* * Significant portions of this file may be copied from parts of the Linux
* kernel, by Linus Torvalds and others. */</aside></p>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/overlays3.jpg" >}}" alt="Open vSwitch Tunnels GRE and VXLan"></figure>

<em><strong>Figure 1</strong>.</em> Example of how tunnels can be leveraged as overlays.
<hr>
By the way I should probably disclaim now that huge Layer2 networks do not scale and huge Layer3 networks do. Host count in a broadcast domain/Vlan/network should be kept to a reasonable 3 digit number. Cisco is quick to point out that OTV is the solution over WAN's for extending Layer 2 networks with <a href="{{< relurl "/2012/02/otv-configuration-notes/" >}}" target="_blank">OTV</a> as the solution to extend Layer 2 Vlans. That said Overlays are flat out required to overcome Vlan number limitations and have lots of potential with programmatic orchestration.
<hr>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/ovs-fwding.jpg" >}}" alt="Open vSwitch Datapath Forwarding"></figure>
<strong><em>Figure 2.</em> </strong>OVS punts the first packet to user land for the forwarding decision and passes the data path back to the data path in the kernel for subsequent packets in the flow. slow path for the first packet then fast path for the rest.
<hr>
I dd some simple Iperf tests at the end of the post using different MTU values of 1500 and 9000 byte MTUs. The numbers are kind of fun to look at from the result. For a really nice analysis take a look at Martin's <a href="http://networkheresy.com/2012/06/08/the-overhead-of-software-tunneling/" target="_blank">post</a> at Network Heresy on comparing STT, Linux Bridging and GRE. I am going to spin up some VMs on the VXLan tunnel later this week and measure the speeds a little closer and see how GRE and VXLan stack up to one another from hosts using overlays. I just ran some Iperfs from the hypervisor itself rather than VMs. OVS also supports Capwap encapsulation that performs mac in GRE which is rather slick. Wonder why we do not hear much about that. I am going to dig in when I get back to home from the road later next week.
<hr>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/2-hosts-tunnel.jpg" >}}" alt="Open vSwitch VXLan GRE"></figure>
<em><strong>Figure 3.</strong></em> Lab Setup basically has a fake interface up with Br1. Real world Br1 would have VMs tapped on it. The video uses br1 and br2 but it got to be confusing for people so I changed it to br0 and br1 to match most peoples eth0 = br0 NIC naming in ifconfig.

<p><a href="http://www.youtube.com/watch?v=igLqghBuSb4&hd=1">Watch video on YouTube</a></p>

<em>Quick Video of the fast install below.</em>
<hr>
If you would prefer to install using packages check out this post. It will install an older version that may or may not support VXLAN framing depending on the timeline. It will support GRE.
<a href="{{< relurl "/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/" >}}" target="_blank" rel="noopener noreferrer">OpenvSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller</a>
<hr>
For those familiar with the build you can just paste the following in your bash shell as root. To walk through the install skip the following snippet. The installation is extensively documented in the INSTALL file in the root of the tarball. The current and LTS releases are located <a href="http://openvswitch.org/download/" target="_blank">here</a>.
<pre class="code-sample"><code>apt-get update
apt-get install -y git automake autoconf gcc uml-utilities libtool build-essential git pkg-config linux-headers-`uname -r`
wget http://openvswitch.org/releases/openvswitch-1.10.0.tar.gz
tar zxvf openvswitch-1.10.0.tar.gz
cd openvswitch-1.10.0
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make && make install
make modules_install
insmod datapath/linux/openvswitch.ko
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server -v --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,manager_options \
                     --private-key=db:SSL,private_key \
                     --certificate=db:SSL,certificate \
                     --pidfile --detach --log-file
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
ovs-vsctl show</code></pre>

<h2>Open vSwitch System Preperation</h2>
This is on two boxes with 64 cores and Broadcom Corporation NetXtreme II BCM57810 10G Nics to a random 10G TOR switch.
Install dependencies
<pre class="code-sample"><code>apt-get update
apt-get install python-simplejson python-qt4 python-twisted-conch automake autoconf gcc uml-utilities libtool build-essential git pkg-config</code></pre>
<hr>
Download the  Open vSwitch latest build
<pre class="code-sample"><code>
### 1.11 and 2.0 are also available via tarball ###
wget http://openvswitch.org/releases/openvswitch-1.10.0.tar.gz
tar zxvf openvswitch-1.10.0.tar.gz
cd openvswitch</code></pre>
<hr>
<h2>Compile OpenvSwitch From Source</h2>
<pre class="code-sample"><code>./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make && make install
make modules_install
insmod datapath/linux/openvswitch.ko
</code></pre>
<hr>
<pre class="code-sample"><code>#If you are running a stripped version of Nix like an EC2 cloud image and get an error along the lines of this:
configure: error: source dir /lib/modules/3.2.0-23-virtual/build doesn&#039;t exist
#Pull down the headers for your kernel. 
sudo apt-get install linux-headers-`uname -r`</code></pre>
<h2>Initial Open vSwitch Configuration</h2>
<pre class="code-sample"><code>touch /usr/local/etc/ovs-vswitchd.conf
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema</code></pre>
<hr>

Start ovsdb-server, this stores the config into a file that is persistent even after restarts.
<pre class="code-sample"><code>
insmod datapath/linux/openvswitch.ko
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db \
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,manager_options \
--private-key=db:SSL,private_key \
--certificate=db:SSL,certificate \
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file</code></pre>
<pre class="code-sample"><code>#Only need to run this the first time.
ovs-vsctl --no-wait init
#Start vswitch
ovs-vswitchd --pidfile --detach
#Verify the kernel module(s) in case you didn&#039;t earlier and get errors.
#lsmod | grep ope
openvswitch            62327  0 
</code></pre>
<hr>
*note* "brcompat" is depreciated since the OVS upstream. Output should just be "openvswitch" as a loaded kernel module. If they are not there try loading again and check your path to the kernel module. You shouldn't see it loaded in the kernel modules unless running a very old version (*cough* 1.4 on Citrix). Get to know the functionality of the network control with an SDN OpenFlow controller, setting up overlays and one of the most interesting parts of OVS in the <a href="{{< relurl "/getting-started-ovsdb/" >}}" target="_blank">configuration database (OVSDB)</a>.
<pre class="code-sample"><code>insmod datapath/linux/openvswitch.ko</code></pre>
At this point you have a fucntioning vanilla OVS install. Output should look something like this.
<pre class="code-sample"><code>ovs-vsctl show
b6d574d7-5582-4cc0-93e5-a90cf0eb0a38
root@demo-139:/home/ubuntu/ovs-vxlan# ovs-vsctl --version
ovs-vsctl (Open vSwitch) 1.8.90
Compiled Aug 19 2012 06:23:36</code></pre>
<h2>Configure Linux Networking</h2>
I have one NIC (eth0) on the same LAN segment/network/vlan.
We are attaching eth0 to br1 and applying an IP to the bridge interface.
We are attaching an IP to br1. br1 is the island that we are building a tunnel for hosts to connect on. Without the VXLAN tunnel, the two br1 interfaces should not be able to ping one another. Note: This is being setup on the same subnet, it is important to keep in mind that the VXLAN framing will allow for the tunnel to be established over disparate networks. E.g. can be done over the Internet etc.
<hr>
Configuration for Host 1

<pre class="code-sample"><code>#Host 1 Configuration
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 eth0
ifconfig eth0 0 && ifconfig br0 192.168.1.10 netmask 255.255.255.0
route add default gw 192.168.1.1 br0
ifconfig br1 10.1.2.10 netmask 255.255.255.0
ovs-vsctl add-port br1 gre1 -- set interface gre1 type=gre options:remote_ip=192.168.1.11
</code></pre>
<hr>
Configuration for Host 2
<pre class="code-sample"><code>#Host 1 Configuration
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 eth0
ifconfig eth0 0 && ifconfig br0 192.168.1.11 netmask 255.255.255.0
route add default gw 192.168.1.1 br0
ifconfig br1 10.1.2.11 netmask 255.255.255.0
ovs-vsctl add-port br1 gre1 -- set interface gre1 type=gre options:remote_ip=192.168.1.10
</code></pre>
<hr>

If you have issues getting the bridge built you may need to kill the OVS processes and restart them depending on your step order.
<hr>
Your Linux routing table and ifconfig should now look something like this:
<pre class="code-sample"><code>root@ub64:/home/brent/openvswitch# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    0      0        0 br0
10.1.2.0        0.0.0.0         255.255.255.0   U     0      0        0 br1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 br0
root@ub64:/home/brent/openvswitch# ifconfig
br0       Link encap:Ethernet  HWaddr 00:0c:29:65:fd:82  
          inet addr:192.168.1.10  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::285f:3ff:fea2:dafc/64 Scope:Link
          UP BROADCAST RUNNING  MTU:1500  Metric:1
          RX packets:622 errors:0 dropped:0 overruns:0 frame:0
          TX packets:54 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:171756 (171.7 KB)  TX bytes:3832 (3.8 KB)

br1       Link encap:Ethernet  HWaddr ea:34:7d:49:e7:49  
          inet addr:10.1.2.10  Bcast:10.1.2.255  Mask:255.255.255.0
          inet6 addr: fe80::c0a7:aaff:fe90:29dc/64 Scope:Link
          UP BROADCAST RUNNING  MTU:1500  Metric:1
          RX packets:12 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:896 (896.0 B)  TX bytes:986 (986.0 B)

eth0      Link encap:Ethernet  HWaddr 00:0c:29:65:fd:82  
          inet6 addr: fe80::20c:29ff:fe65:fd82/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1222493 errors:0 dropped:0 overruns:0 frame:0
          TX packets:53824 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:653399936 (653.3 MB)  TX bytes:4089412 (4.0 MB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:7088 errors:0 dropped:0 overruns:0 frame:0
          TX packets:7088 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:537609 (537.6 KB)  TX bytes:537609 (537.6 KB)
</code></pre>
<hr>
<h2>Troubleshooting Open vSwitch Installation</h2>
An error was sent to me by someone that looked like this below, restarting the OVS procs will clear it up:
<pre class="code-sample"><code>Aug 19 06:34:04 demo-139 ovs-vsctl: 00001|vsctl|INFO|Called as ovs-vsctl del-br br1
Aug 19 06:34:04 demo-139 ovs-vswitchd: 00026|dpif|WARN|failed to enumerate system datapaths: No such file or directory
Aug 19 06:34:04 demo-139 ovs-vswitchd: 00027|bridge|INFO|ovs-vswitchd (Open vSwitch) 1.8.90
Aug 19 06:34:20 demo-139 ovs-vsctl: 00001|vsctl|INFO|Called as ovs-vsctl add-br br1
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00028|dpif|WARN|failed to enumerate system datapaths: No such file or directory
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00029|dpif|WARN|failed to create datapath br1: No such file or directory
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00030|ofproto_dpif|ERR|failed to open datapath br1: No such file or directory
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00031|ofproto|ERR|failed to open datapath br1: No such file or directory
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00032|bridge|ERR|failed to create bridge br1: No such file or directory
Aug 19 06:34:20 demo-139 ovs-vswitchd: 00033|bridge|INFO|ovs-vswitchd (Open vSwitch) 1.8.90</code></pre>
<pre class="code-sample"><code>#Find the OVS PIDs from PS
ps -ea | grep ovs
16369 ?        00:00:00 ovsdb-server
16372 ?        00:00:00 ovs-vswitchd
16373 ?        00:00:00 ovs-vswitchd
16375 ?        00:00:00 ovs_workq
#Terminate them
kill 16369
kill 16372
kill 16375
#Then restart the OVS server
ovsdb-server /usr/local/etc/openvswitch/conf.db \
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,manager_options \
--private-key=db:SSL,private_key \
--certificate=db:SSL,certificate \
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file
#Start vswitchd (JSON DB)
ovs-vswitchd --pidfile --detach</code></pre>
<hr>
<h2>Build a GRE Tunnel in Open vSwitch</h2>
<pre class="code-sample"><code>ovs-vsctl add-port br1 gre1 -- set interface gre1 type=gre options:remote_ip=192.168.1.10
ovs-vsctl add-port br1 gre1 -- set interface gre1 type=gre options:remote_ip=192.168.1.11</code></pre>
<hr>
Adjust MTUs with % ifconfig &lt;interface e.g. br0 eth0 etc&gt; mtu 9000
#(Remember your switch needs to have &gt;= your MTU.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/ovs-gre-15001.jpg" >}}" alt="openvswitch gre tunnel"></figure>
<strong>Figure 4.</strong> Output of GRE Tunnels running with 1500 byte MTUs.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/gre-jumbo.jpg" >}}" alt="openvswitch gre tunnel jumbo"></figure>
<strong>Figure 5.</strong> Output of GRE Tunnels running with 9000 byte MTUs.

<hr />

Now delete the GRE ports
<pre class="code-sample"><code>ovs-vsctl del-port gre1</code></pre>
<h2>Configure the VXLan Tunnel</h2>
The difference here is the "type" specifying the tunnel encapsulation.
<pre class="code-sample"><code>ovs-vsctl add-port br1 vx1 -- set interface vx1 type=vxlan options:remote_ip=192.168.1.10
ovs-vsctl add-port br1 vx1 -- set interface vx1 type=vxlan options:remote_ip=192.168.1.11</code></pre>
<hr>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/vxlan-1500.jpg" >}}" alt="openvswitch VXLan tunnel vxlan mtu 1500"></figure>
<strong>Figure 6</strong> Output of VXLan Tunnels running with 1500 byte MTUs.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/vxlan-jumbo.jpg" >}}" alt="openvswitch gre tunnel vxlan"></figure>
<strong>Figure 7</strong> Output of VXLan Tunnels running with 9000 byte MTUs.

<hr />

Thanks for stopping by.

<hr />