+++
title = "Getting Started OpenFlow OpenvSwitch Tutorial Lab : Setup"
date = "2012-06-15T05:50:49+00:00"
lastmod = "2014-02-15T07:12:22+00:00"
author = "Brent Salisbury"
wp_id = 1074
categories = ["In the Lab"]
tags = ["KVM", "Open vSwitch", "OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openflow-openvswitch-lab/"
aliases = ["/2012/06/openflow-openvswitch-lab/"]
image = "/wp-content/uploads/2012/06/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "def3ed38c32e7a79efea154916fa8da533ea3d0d63bfdcf758ea588bee0ad161"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Getting Started OpenFlow OpenvSwitch Tutorial Lab : Setup</h2>


<aside class="legacy-callout">For a more up to date tutorial as anything more then 6 months old is outdated in the world of SDN Please see:
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}">OpenDaylight OpenStack Integration with DevStack on Fedora 20</a></aside>


I wrote a Python OpenFlow installation app to automate an OpenFlow KVM and Open vSwitch setup found at:
<a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank" rel="noopener noreferrer">OpenFlow, OpenvSwitch and KVM SDN Lab Installation App</a>

<hr />

<h2 class="legacy-heading">Getting Started OpenFlow OpenvSwitch Tutorial Lab - Setup:</h2>

<hr />

Getting Started OpenFlow OpenvSwitch Tutorial Lab : This is an OpenFlow Tutorial using OpenvSwitch and Floodlight <a href="{{< relurl "/pox-openflow-controller-installation-screencast/" >}}" target="_blank">controller</a> but any other controller or switch can be used. I have had some requests on some scenarios so I put this together. Adding a few more flexible components. Getting to know all of these packages like KVM, OpenvSwitch are going to be pretty big in the future ecosystem orchestrations.

The video doesn't have any sound, I am tight on time, sorry. I think it should be pretty straightforward and the video may help if you get stuck. Probably a couple typos here and there I will try and catch over the weekend. We are lacking good lab material on these topics right now so maybe this will save a couple folks some time.

<hr />

<h2>Prerequisites</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/OF-logo1-150x150.jpg" >}}" alt=""></figure>

The KVM requires an x86 machine with either Intel VT or AMD w/AMD-V support. Anything fairly new will have that support in the processor. There are a few older HW builds that support hardware assisted virtualization by enabling it in the bios. Pretty much Googling your machine for hardware virtualization will let you know. Qemu can be run on non VT HW but the machines will probably get brutalized by a few host VMs. When you are setting up the vSwitch either have an out of band or be on it physically. Be careful when you are adding multiple interfaces to bridges since you can spin up a bridging loop pretty quickly unless you have STP on. I recommend a test/dev network or mom's basement network. If not BPDUguard is your friend :) This is done on a fresh install of 64-bit Ubuntu 12.04 (Precise).

Quick screencast. I highly recommend considering using a small Linux Kernel named <a href="http://wiki.qemu.org/download/linux-0.2.img.bz2" target="_blank">linux-0.2.img.bz2</a> from <a href="http://wiki.qemu.org/Testing" target="_blank">Qemu</a> if using a laptop or <a href="{{< relurl "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/" >}}" target="_blank">nested</a> hypervisor.


<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/network-interfaces.jpg" >}}" alt=""></figure>

<hr />

<pre class="code-sample"><code>$nano /etc/network/interfaces
Add in your configuration to the file to your physical interface and save the file.
Restart networking. If the configuration is off this will cut you off.
$/etc/init.d/networking restart
$route -n will display your default route if you are having connectivity issues.
$apt-get update
$apt-get dist-upgrade</code></pre>
<h2>Install OpenvSwitch</h2>
<pre class="code-sample"><code>
$ apt-get install openvswitch-datapath-source bridge-utils
$ module-assistant auto-install openvswitch-datapath
$ apt-get install openvswitch-common
Verify install
$ovs-vsctl show
ovs_version: “1.4.0+build0″
Processes should look something like this
$ps -ea | grep ovs
26464 ? 00:00:00 ovsdb-server
26465 ? 00:00:00 ovsdb-server
26473 ? 00:00:00 ovs-vswitchd
26474 ? 00:00:00 ovs-vswitchd
26637 ? 00:00:00 ovs-controller
$ /etc/init.d/openvswitch-switch restart</code></pre>

<hr />

Add your bridge, think of this as a subnet if you aren’t familiar with the term.

Add a physical interface to your virtual bridge for connectivity off box. If you don't script this part you will probably clip your connection as you zero out eth0 and apply it to br-int. You can pop the commands into a text file and make it executable with
chmod +x script.sh
<pre class="code-sample"><code>$ ovs-vsctl add-br br-int
$ ovs-vsctl add-port br-int eth0
$ ifconfig eth0 0
#Zero out your eth0 interface and slap it on the bridge interface
#(warning will clip you unless you script it)
$ifconfig br-int 192.168.1.208 netmask 255.255.255.0
#Change your default route
$route add default gw 192.168.1.1 br-int and $route del default gw 192.168.1.1 eth0</code></pre>

<hr />

<h2>Install FloodLight OpenFlow Controller and Attach OpenvSwitch</h2>
Install dependencies, apt-get for UB and yum for RH:
<pre class="code-sample"><code>apt-get install build-essential default-jdk ant python-dev eclipse git</code></pre>
Clone the Github project and build the jar and start the controller:
<pre class="code-sample"><code>$git clone git://github.com/floodlight/floodlight.git
cd into the floodlight directory created.
$cd floodlight
Run ant to build a jar. It will be in the ~/floodlight/target directory.
$ant
Run the controller :
$java -jar target/floodlight.jar
By default it will binds to port 6633 and all ports e.g. 0.0.0.0/0.0.0.0:6633</code></pre>

<hr />

<h2>Attach OpenvSwitch to the Controller</h2>
<pre class="code-sample"><code>$ovs-vsctl set-controller br-int tcp:192.168.1.208:6633</code></pre>

<hr />

In the FloodLight console you will see something like this:
<pre class="code-sample"><code>[New I/O server worker #1-1] INFO n.f.core.internal.Controller - Switch handshake successful: OFSwitchImpl [/192.168.1.208:49519 DPID[00:00:ba:66:35:e8:38:48]]</code></pre>
&nbsp;

<hr />

The output of OVS 'ovs-vsctl show' looks something like this:

<hr />

<pre class="code-sample"><code># ovs-vsctl show
70a40219-8725-46a8-b808-af75c642cac8
Bridge "br-int"
Controller "tcp:192.168.1.208:6633"
is_connected: true
Port "eth0"
Interface "eth0"
Port "br-int"
Interface "br-int"
type: internal
ovs_version: "1.4.0+build0"</code></pre>

<hr />

<h2>Install KVM and Integrate into OVS</h2>
<pre class="code-sample"><code>$apt-get install kvm uml-utilities</code></pre>
These two scripts bring up the KVM Tap interfaces into your bridge from the CLI. If you copy and paste below make sure the (') does not get formatted improperly. It should be yellow in nano. "switch=br-int" br-int is the name of your bridge in OVS.
$nano /etc/ovs-ifup  (open and paste what is below)

<pre class="code-sample"><code>#!/bin/sh
switch='br-int'
/sbin/ifconfig $1 0.0.0.0 up
ovs-vsctl add-port ${switch} $1</code></pre>
$nano /etc/ovs-ifdown (open and paste what is below)

<pre class="code-sample"><code>#!/bin/sh
switch='br-int'
/sbin/ifconfig $1 0.0.0.0 down
ovs-vsctl del-port ${switch} $1</code></pre>
Make both files executable
chmod +x /etc/ovs-ifup /etc/ovs-ifdown


<hr />

http://www.youtube.com/watch?v=NHHJRDmiqyg

<h2 class="legacy-heading">Boot the Guest Virtual Machines</h2>

<hr />

<ul>
	<li>Host1</li>
</ul>
<pre class="code-sample"><code>kvm -m 512 -net nic,macaddr=00:00:00:00:cc:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</code></pre>
<ul>
	<li>Host2</li>
</ul>
<pre class="code-sample"><code>kvm -m 512 -net nic,macaddr=00:11:22:CC:CC:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</code></pre>
<ul>
	<li>Host3</li>
</ul>
<pre class="code-sample"><code>kvm -m 512 -net nic,macaddr=22:22:22:00:cc:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom ubuntu-12.04-desktop-amd64.iso</code></pre>
Each one of those will begin loading from the ISO. I just click "Try Ubuntu" when they are booting and just run them from disk since really all we need are nodes that can test connectivity as we push static flows. If it is a more permanent test lab it would make since to install them to disk.

While those are spinning up let's install curl.
<pre class="code-sample"><code>$apt-get install curl</code></pre>

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/ovs-tap.jpg" >}}" alt=""></figure>

<strong>Figure 1.</strong> OVS Taps

<hr />

One they are up assign IP addresses to them by clicking in the top left of the Ubuntu window and type in 'terminal' no parentheses. Then give them IPs if you want to statically assign them with ifconfig.
<pre class="code-sample"><code>sudo ifconfig eth0 192.168.1.x netmask 255.255.255.0</code></pre>
<p><a href="http://www.youtube.com/watch?v=0uKxO3NwzxI">Watch video on YouTube</a></p>

<hr />

Check out the rest of the tutorials in this series:




<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank">Getting Started OpenFlow OpenvSwitch Tutorial Lab – Setup</a></li>
	<li><a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #1</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-2/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #2</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-3/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #3</a></li>
</ul>

<hr>
Thanks for stopping by.

