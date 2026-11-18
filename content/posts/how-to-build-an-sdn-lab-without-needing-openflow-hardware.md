+++
title = "How to Build an SDN Lab without Needing OpenFlow Hardware"
date = "2012-07-18T05:43:04+00:00"
lastmod = "2014-04-17T17:41:07+00:00"
author = "Brent Salisbury"
wp_id = 1765
categories = ["In the Lab"]
tags = ["Open vSwitch", "OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/how-to-build-an-sdn-lab-without-needing-openflow-hardware/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "106b708087358981d8b42741a72ab62e48ec48ee9009bfbe15a8378d5b8e91db"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>How to Build an SDN Lab without Needing OpenFlow Hardware</h2>

<aside class="legacy-callout">I no longer use much in this post. For a current lab setup please see <a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}">OpenDaylight OpenStack Integration with DevStack on Fedora</a> </aside>

How do you build a networking lab without networking equipment? Yet another plus in the column of open software driven networks. Proofing and prototyping networks today are often done with things like NETFPGA or expensive vendor manufactured hardware. Since we are beginning to build primitives, APIs and abstraction layers the value of what the software development community has had for two decades is becoming obvious to networking.

Update: For a more updated and scripted install take a peek at this post:


<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}">OpenFlow, OpenvSwitch and KVM SDN Lab Installation App</a></li>
	<li>I have lately started using the worlds greatest 8MB Linux kernel <a href="http://wiki.qemu.org/download/linux-0.2.img.bz2">linux-0.2.img.bz2</a>. Using that instead of a full blown distribution especially if <a href="{{< relurl "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/" >}}" target="_blank">nesting</a> your VMs inside your Mac or PC. Since all you need is a basic networking stack and kernel this is perfect for the networking lab.</li>
</ul>

Quit a few of us are working on wrapping our heads around what the current and future state of Software Defined Networks (SDN) will look like. To build or modify modules and applications we need a proper lab to do this in. Something I run into quite often is the idea that we need OpenFlow enabled hardware to build this lab. The great news is we absolutely do not need personally once that dawned on me a vSwitch as really all I ever need for modeling and prototyping. Once you need performance benchmarks and metrics transitioning to hardware starts making sense.

<h2>Two Easy OpenFlow Lab Options</h2>

<ol class="legacy-numbers">
<ol>
	<li>Run a Hypervisor like <a href="http://www.linux-kvm.org/page/Main_Page" target="_blank">KVM</a> or XEN with <a href="http://openvswitch.org/" target="_blank">Open vSwitch</a> managing the VM nodes. This requires Hardware Virtualization.</li>
	<li>Run multiple VM instances each running <a href="http://openvswitch.org/" target="_blank">Open vSwitch</a> and using multiple bridges to create unique Data Path IDs (DPID) that essentially appear as different hosts. This is less hardware requirements but is a bit less flexible from seeing what the host is doing. That said you could spin up dozens of vSwitches under the control of single or separate OF controllers and instantiate data paths. An example of this option is in this <a href="{{< relurl "/2012/07/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank">post</a>. All you need to do after that is attach each bridge to a controller and now data paths are built by the OF controller rather than the OVS slow path. There are quite a few controllers out there. I primarily use <a href="http://www.noxrepo.org/pox/about-pox/" target="_blank">POX</a> (Python) and <a href="http://floodlight.openflowhub.org/" target="_blank">Floodlight</a> (Java) since both have the best maintenance and community from what I have been exposed to along with easy modules to use, adjust or spin your own. The documented APIs are coming along as well. FloodLight probably has the slight edge there but I prefer Python so its a wash for me. POX does not have a monetized product attached to it (BigSwitch) which would be attractive to some folks also.</li>
</ol>
</ol>

<h2>OpenFlow Hardware Limitations</h2>

With both options you can integrate physical hardware which is essentially the SDN roadmap topology being proposed in data center solutions today. A development environment is ideal to have in software to quickly change components and designs. The other key part is that we are not contained in software by the shortcomings of hardware matches today. For example, HP switches cannot match on layer 2 fields so ether type and mac src and dest are wild carded. Other vendors can only match source OR destination IP rather than both. These constraints are due to limited amounts of TCAM and/or Software development limitations at this point. Also who wants to have to get up and move cables and soak your power bill :)
<hr />
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/Island2.jpg" >}}" alt="SDN Topology"></figure>
<strong>Figure 1.</strong> Using a physical Switch for you lab.
<hr />
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/Island2.jpg" >}}" alt="SDN Islands"></figure>
<strong>Figure 2.</strong> Using a vSwitch for your lab. Same topologies and logically similar, programmatically the same. Why is that? We finally actually have a HAL or instruction set/primitive providing abstraction. Yay!

<h2>Lab Prerequisites</h2>

The KVM requires an x86 machine with either Intel VT or AMD w/AMD-V support. Anything fairly new will have that support in the processor. There are a few older HW builds that support hardware assisted virtualization by enabling it in the bios.

This is done on a fresh install of 64-bit Ubuntu 12.04 (Precise).

<hr />

<p><a href="http://www.youtube.com/watch?v=0uKxO3NwzxI&hd=1">Watch video on YouTube</a></p>
<em>Video:</em> Installation Screencast Part I

<hr />

Uninstall network-manager if running Ubuntu desktop (optional) ,not required but you will likely have to troubleshoot past it if you don't.  This will likely cut you off if remote.

<h2>System Preparation (Optional)</h2>
<pre class="brush: bash; gutter: true">$apt-get update $apt-get dist-upgrade</pre>
<h2>Install OpenvSwitch</h2>

<pre class="brush: bash; gutter: true">$apt-get purge network-manager
 $ apt-get install openvswitch-datapath-source bridge-utils
 $ module-assistant auto-install openvswitch-datapath
 $ apt-get install openvswitch-brcompat openvswitch-common</pre>
Verify install
<pre class="brush: bash; gutter: true">$ovs-vsctl show ovs_version: “1.4.0+build0″</pre>
Processes should look something like this
<pre class="brush: bash; gutter: true">$ps -ea | grep ovs
26464 ? 00:00:00 ovsdb-server 26465 ?
00:00:00 ovsdb-server 26473 ?
00:00:00 ovs-vswitchd 26474 ?
00:00:00 ovs-vswitchd 26637 ?
00:00:00 ovs-controller</pre>
Enable bridge compatability
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">/etc/default/openvswitch-switch</pre>
and change brcompat from no to yes Change from:
#BRCOMPAT=no
TO and uncomment by removing the #:
BRCOMPAT=yes
Restart OVS
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ /etc/init.d/openvswitch-switch restart</pre>
Add your bridge, think of this as a subnet if you aren’t familiar with the term.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ ovs-vsctl add-br br-int</pre>
Add a physical interface to your virtual bridge for connectivity off box. If you don't script this part you will probably clip your connection as you zero out eth0 and apply it to br-int. You can pop the commands into a text file and make it executable with chmod +x &lt;filename&gt;,
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ ovs-vsctl add-port br-int eth0
$ ifconfig eth0 0</pre>
Zero out your eth0 interface and slap it on the bridge interface (warning will clip you unless you script it)
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ifconfig br-int 192.168.1.208 netmask 255.255.255.0</pre>
Change your default route
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$route add default gw 192.168.1.1 br-int and $route del default gw 192.168.1.1 eth0</pre>
<h2>SDN Controller Option A: FloodLight (Java)</h2>

Install dependencies, apt-get for UB and yum for RH:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$apt-get install build-essential default-jdk ant python-dev eclipse git</pre>
Clone the Github project and build the jar and start the controller:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$git clone git://github.com/floodlight/floodlight.git</pre>
cd into the floodlight directory created.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$cd floodlight</pre>
Run ant to build a jar. It will be in the ~/floodlight/target directory.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ant</pre>
Run the controller :
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$java -jar target/floodlight.jar</pre>
By default it will binds to port 6633 and all ports e.g. 0.0.0.0/0.0.0.0:6633


<h2>SDN OpenFlow Controller Option B: POX (Python)</h2>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">$ sudo apt-get install git
$ git clone http://github.com/noxrepo/pox
$ cd pox
$ ./pox.py forwarding.l2_learning
$ NOX&amp;gt;</pre>
By default it will binds to port 6633 and all ports e.g. 0.0.0.0/0.0.0.0:6633


<h2>Attach OpenvSwitch to the Controller</h2>

<pre class="brush: bash; gutter: true">$ovs-vsctl set-controller br-int tcp:192.168.1.208:6633</pre>
In the FloodLight console you will see something similar to what is directly below. The DPID is the unique Data Path Identifier (DPID) of the switch not the controller.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">[New I/O server worker #1-1] INFO n.f.core.internal.Controller - Switch handshake successful: OFSwitchImpl [/192.168.1.208:49519 DPID[00:00:ba:66:35:e8:38:48]]</pre>
The output of OVS 'ovs-vsctl show' looks something like this:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false"># ovs-vsctl show 70a40219-8725-46a8-b808-af75c642cac8
Bridge &quot;br-int&quot; Controller &quot;tcp:192.168.1.208:6633&quot; is_connected: true
Port &quot;eth0&quot;
Interface &quot;eth0&quot;
Port &quot;br-int&quot;
Interface &quot;br-int&quot; type: internal
ovs_version: &quot;1.4.0+build0&quot;</pre>

<h2>Install KVM and Integrate into OVS</h2>
<pre class="brush: bash; gutter: true">$apt-get install kvm uml-utilities</pre>
These two scripts bring up the KVM Tap interfaces into your bridge from the CLI. If you copy and paste below make sure the (') does not get formatted improperly. It should be yellow in nano. "switch=br-int" br-int is the name of your bridge in OVS.
$nano /etc/ovs-ifup  (open and paste what is below)
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">#!/bin/sh switch=&#039;br-int&#039; 
/sbin/ifconfig $1 0.0.0.0 up
 ovs-vsctl add-port ${switch} $1</pre>
In the directory /etc/ovs-ifdown open and paste what is below:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">#!/bin/sh switch=&#039;br-int&#039; 
/sbin/ifconfig $1 0.0.0.0 down 
ovs-vsctl del-port ${switch} $1</pre>
Make both files executable
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">chmod +x /etc/ovs-ifup /etc/ovs-ifdown</pre>

<hr />

<p><a href="http://www.youtube.com/watch?v=NHHJRDmiqyg&hd=1">Watch video on YouTube</a></p>
<em>Video:</em> Installation Screencast Part II

<hr />
<h2 class="legacy-heading">Spin up the VMs</h2>

Note: If you chose to use the small linux kernel replace Ubuntu image with this <a href="http://wiki.qemu.org/download/linux-0.2.img.bz2">linux-0.2.img.bz2</a>. Recommended for those comfortable configuring Linux networking from command line. Examples are:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">ifconfig eth0 192.168.1.150 netmask 255.255.255.0
route add default gw 192.168.1.1
echo nameservers 8.8.8.8 &gt;&gt; /etc/resolv.conf</pre>
<ul>
	<li>Host1</li>
</ul>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">kvm -m 512 -net nic,macaddr=00:00:00:00:cc:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</pre>
<ul>
	<li>Host2</li>
</ul>
<pre class="brush: bash; gutter: true">kvm -m 512 -net nic,macaddr=00:11:22:CC:CC:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</pre>
<ul>
	<li>Host3</li>
</ul>
<pre class="brush: bash; gutter: true">kvm -m 512 -net nic,macaddr=22:22:22:00:cc:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</pre>
Each one of those will begin loading from the ISO. I just click "Try Ubuntu" when they are booting and just run them from disk since really all we need are nodes that can test connectivity as we push static flows. If it is a more permanent test lab it would make since to install them to disk. These are your hosts you can test with.


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/ovs-tap.jpg" >}}" alt="OpenvSwitch Tap"></figure>
<strong>Figure 3</strong>.Open vSwitch Taps (Vnic/Vnet)

Onecs the VM hosts have booted up assign IP addresses to them by clicking in the top left of the Ubuntu window and type in 'terminal' no parentheses. Then give them IPs if you want to statically assign them with ifconfig.
<pre class="brush: bash; gutter: true">$sudo ifconfig eth0 192.168.1.x netmask 255.255.255.0 (on the VM)</pre>
Now that you have that, here are some example labs with the POX SDN Controller: <a href="{{< relurl "/2012/06/openflow-openvswitch-lab/" >}}">Lab installation</a>