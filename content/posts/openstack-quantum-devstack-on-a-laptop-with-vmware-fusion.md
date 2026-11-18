+++
title = "OpenStack Quantum DevStack on a Laptop with VMware Fusion"
date = "2012-11-07T06:52:53+00:00"
lastmod = "2014-02-18T02:51:23+00:00"
author = "Brent Salisbury"
wp_id = 3749
categories = ["In the Lab"]
tags = ["DevStack", "OpenStack"]
description = ""
url = "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/"
image = "/wp-content/uploads/2012/11/devops-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "548b74d9319d8a6b06874b07b9e9f0ee484e7be05bcaa0fc20d813316439ae45"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenStack Quantum DevStack on a Laptop with VMware Fusion</h2>
<aside class="legacy-callout">
<ul>
	<li><a href="{{< relurl "/installing-openstack-grizzly-with-devstack/" >}}" target="_blank">Installing OpenStack Grizzly with DevStack</a> : Here is an updated Grizzly DevStack tutorial since Folsom is coming to an end.</li>
</ul>
</aside>

VMware Fusion and VMware Workstation both support nested virtualization. This is great news for folks looking to either learn OpenStack, proof new concepts or do development work without needing physical hardware. The reason nested virtualization is important is to support KVM, Xen or other hypervisors you need hardware virtualization to get hooks into <a href="http://wiki.openstack.org/Quantum" target="_blank">Quantum</a> and Open vSwitch that Qemu will not support like it did in previous OpenStack releases.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/11/openstack-png2-150x150.png" >}}" alt=""></figure>

VMWare Fusion for Mac (VMWare Workstation for Windoze) is not free software but does offer trial versions but in this case you get what you pay for. VirtualBox (Oracle owned) has never seemed to show much interest in adding nested hypervisor support as articulated in this <a href="https://forums.virtualbox.org/viewtopic.php?f=1&t=20589">thread</a>. This screencast is an OpenStack Folsom install on a MacBook in about 10 minutes. Give yourself another 15 minutes or so to install <a href="http://www.ubuntu.com/download" target="_blank">Ubuntu 12.04</a>.

This configuration supports OpenStack Folsom. The next release of OpenStack will be in Spring 2013 named Grizzly. If reading this after Grizzly release at may not be compatible. In the meantime, I will keep the localrc file configuration current with Folsom.

<hr />

<h2>Steps for OpenStack DevStack Installation</h2>
<ol class="legacy-numbers">
<ol>
	<li>Install Ubuntu 12.04 or whatever the latest release is. Instructions <a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}" target="_blank">here.</a> That how-to is for VirtualBox but everything is pretty much the same. The screencast shows the two important pieces which are 2 Nics, with eth0 (Nic 1) being bridged and eth1 (Nic 2) being "private to my Mac or PC". The second "enable hypervisor applications" under Processors.<a href="{{< relurl "/wp-content/uploads/2012/11/nested-hardware-virtualization.jpg" >}}"><img class="aligncenter size-full wp-image-3750" title="nested-hardware-virtualization" src="{{< relurl "/wp-content/uploads/2012/11/nested-hardware-virtualization.jpg" >}}" alt="nested-hardware-virtualization-vm-fusion" width="499" height="158" /></a></li>
	<li>Once you have the base OS install and verify connectivity to the net and repositories with something like 'apt-get update'. Head to this post <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">OpenStack Folsom Quantum Devstack Installation Tutorial</a>.</li>
</ol>
</ol>
<hr />

<ul>
	<li>Verify HW virt support with the following:</li>
</ul>

<pre class="code-sample"><code>grep --color vmx /proc/cpuinfo</code></pre>
The output should highlight VMX in red on an Intel machine.
<h2>DevStack OpenStack localrc configuration with VMWare Fusion</h2>
The localrc file contains your OpenStack settings for the installation.
<pre class="brush: text; gutter: true">
ENABLED_SERVICES=q-meta,q-lbaas,n-obj,n-cpu,n-sch,n-cauth,horizon,mysql,rabbit,sysstat,cinder,c-api,c-vol,c-sch,n-cond,quantum,q-svc,q-agt,q-dhcp,q-l3,n-novnc,n-xvnc,q-lbaas,g-api,g-reg,key,n-api,n-crt
ADMIN_PASSWORD=openstack
MYSQL_PASSWORD=openstack
RABBIT_PASSWORD=openstack
SERVICE_PASSWORD=openstack
SERVICE_TOKEN=openstack
MYSQL_PASSWORD=password
LOG=True

The localrc configuration above is what I used for the screen cast and below is the /etc/network/interfaces file containing the two NIC configurations.
<pre class="brush: text; gutter: true">stack@ub64:~/devstack$ cat /etc/network/interfaces 
# The loopback network interface
auto lo
iface lo inet loopback
# The primary network interface
auto eth0
iface eth0 inet static
 address 192.168.1.110
 netmask 255.255.255.0
 network 192.168.1.0
 broadcast 192.168.1.255
 gateway 192.168.1.1
 # dns-* options are implemented by the resolvconf package, if installed
 dns-nameservers 128.163.1.6
auto eth1
 iface eth1 inet manual
 up ifconfig $IFACE 0.0.0.0 up
 up ip link set $IFACE promisc on
 down ip link set $IFACE promisc off
 down ifconfig $IFACE down
Then from that dir just run ./stackrc. HOST_IP is your external public eth0 address. Floating range is also on that same address range. Network gateway is the gateway for the VM, while EXT_GW_IP is the physical host gateway. Those things can be a bit confusing in Quantum. I am going to try and find some time this week to post some Quantum clarifications, or at least how I *think* they are :) After installation just point your browser at the HOST_IP. I have quite a few tutorials on creating and importing images and what not for OpenStack for learning Ops.

<h2>Download Devstack and run ./stack.sh</h2>
sudo apt-get install git
 git clone git://github.com/openstack-dev/devstack.git
 cd devstack

<h2>DevStack OpenStack Installation with VMware Fusion</h2>
<p><a href="http://www.youtube.com/watch?v=MHBAcdaUI08&hd=1">Watch video on YouTube</a></p>

<hr />

There are more details in the linked post in step #2 above along with some netmaps. The screencast shows the commands in case anyone gets stumped. I made a point of showing that you can provision floating addresses but cannot assign them as of yet. That is a committed fix in progress that can be tracked <a href="https://bugs.launchpad.net/nova/+bug/1031119" target="_blank">here</a>. Floating address provisioning can be done from the CLI as demonstrated in the <a href="http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html#floating_ip_addresses" target="_blank">OpenStack Nova CLI Guide</a>.

<a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">OpenStack Folsom Quantum Devstack Installation Tutorial</a> Has some topologies and clarity on the networking components.

Thanks for stopping by!

