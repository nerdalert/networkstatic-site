+++
title = "Open vSwitch on VirtualBox"
date = "2013-03-13T00:03:06+00:00"
lastmod = "2013-03-29T05:48:32+00:00"
author = "Brent Salisbury"
wp_id = 5982
categories = ["In the Lab"]
tags = ["Open vSwitch", "Software Defined Networking", "Tutorials"]
description = ""
url = "/open-vswitch-on-virtualbox/"
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ad77ec9e4a920a8f26503d4717942d0bd63837143844b6a4a67417cbfe6794cd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Open vSwitch on VirtualBox</h2>
Here is a quick tutorial for installing Open vSwitch on VirtualBox. <a href="https://www.virtualbox.org" target="_blank">VirtualBox</a> is an open source virtualization project from Oracle. It is supported on Windows, Mac, BSD and Linux to name a few. It has a nice GUI for VM management out of the box. Open vSwitch is an open source vSwitch from <a href="http://networkheresy.com" target="_blank">Martin Casado</a>, <a href="http://benpfaff.org/papers/index.html" target="_blank">Ben Pfaff</a> and a whole <a href="http://www.ohloh.net/p/openvswitch/factoids" target="_blank">crew of awesome</a>. If you are here, OVS probably doesn't require anymore explanation, <a href="{{< relurl "/tag/openvswitch/" >}}" target="_blank">learn it</a>, love it.
<h2>Install VirtualBox</h2>
Install VirtualBox from the VirtualBox repository.
<pre class="brush: bash; gutter: true">Add the following repo to /etc/apt/sources.list 
deb http://download.virtualbox.org/virtualbox/debian precise contrib
wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | sudo apt-key add -
sudo apt-get update
sudo apt-get install dkms
sudo apt-get install virtualbox-4.2</pre>
<h2>Install Open vSwitch from repo</h2>
Install Open vSwitch from Package. This is easiest for those not familiar with compiling from source or just need basic functionality rather than the latest features.
<pre class="brush: bash; gutter: true">sudo apt-get install openvswitch-datapath-source bridge-utils
sudo module-assistant auto-install openvswitch-datapath
sudo apt-get install openvswitch-brcompat openvswitch-common openvswitch-controller</pre>
<h2>Open vSwitch Install from Source </h2>
Install dependencies and install from source on Ubuntu Linux.
<pre class="brush: bash; gutter: true">apt-get install -y git python-simplejson python-qt4 python-twisted-conch automake autoconf gcc
uml-utilities libtool build-essential git pkg-config linux-headers-`uname -r`
git clone git://openvswitch.org/openvswitch
cd openvswitch
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make &amp;&amp; make install
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make &amp;&amp; make install
insmod datapath/linux/openvswitch.ko
touch /usr/local/etc/ovs-vswitchd.conf
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db \
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,manager_options \
--private-key=db:SSL,private_key \
--certificate=db:SSL,certificate \
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach</pre>
<h2>Create Open vSwitch bridge and interfaces</h2>
To setup the virtual interfaces use Tuntap. Tuntap sets up a emulates an L2 interface. That interface will show up in the interface as a physical interface.
<pre class="brush: bash; gutter: true">ovs-vsctl add-br br0
ip tuntap add mode tap vnet0
ip link set vnet0 up
ovs-vsctl add-port br0 vnet0
ip link (View the created interface)</pre>
<hr>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/openvswitch-virtualbox.png" >}}" alt="Open vSwitch VirtualBox"></figure>
<h2>Spin up VirtualBox instances with Open vSwitch Interfaces </h2>
For testing Open vSwitch or any other hypervisor testing, I highly recommend this Linux image <a href="http://wiki.qemu.org/Testing" target="_blank">linux-0.2.img</a>. It only takes a couple of MB of memory. It is perfect for <a href="{{< relurl "/nested-kvm-hypervisor-support/" >}}" target="_blank">nested hypervisor</a> testing.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/openvswitch-VM.png" >}}" alt="Open vSwitch VM"></figure>

<h2>Connect the Open vSwitch bridge to the physical network</h2>


You can put the following into a text file and give it execute permissions with “chmod +x filename” and then run it “./filename”. If your network settings are right it should flip the IP to the bridge and not cut you off. Keyword “should” so have a way to get to the box if you cut yourself off. What is happening here is you are placing both the virtual interface "vnet0" and the physical Nic "eth0" into the same bridge "br0". You can think of a bridge as a logical grouping of virtual and physical interface much like a locally significant VLAN without the 0x8100 Ethertype framing and tag. 


<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">ovs-vsctl add-br br0
ovs-vsctl add-port br0 eth0
ovs-vsctl add-port br0 vnet0
ifconfig eth0 0 &amp;&amp; ifconfig br0 192.168.1.(X) netmask 255.255.255.0
route add default gw 192.168.1.1 br0
route del default gw 192.168.1.1 eth0</pre>

Download your test image. If using the Linux-0.2.img it needs to be converted to vdi first using the VBoxManage utility included with the VirtualBox binary.
<pre class="brush: bash; gutter: true">wget http://wiki.qemu.org/download/linux-0.2.img.bz2
bunzip2 linux-0.2.img.bz2
VBoxManage convertdd linux-0.2.img linux-0.2.vdi</pre>
<hr>

<ul>
	<li>Create a new Virtualbox instance. Choose the linux-0.2.vdi (must duplicate the VDI or else all meta-data is the same and Vbox wont load the IMG). Do this as a regular user or else you will get permissions error.</li>
	<li>Choose “use existing virtual HD”</li>
	<li>Ignore “failed to get USB blah”.</li>
	<li>If you get "dpif_linux|ERR|Generic Netlink family 'ovs_datapath' does not exist. The Open vSwitch kernel module is probably not loaded." Make sure you are adding the Open vSwitch kernel module e.g insmod datapath/linux/openvswitch.ko.</li>
	<li>Under interfaces set to “bridged interface” and choose the port on the appropriate bridge. E.g Bridge1-p2, br-head-p1 etc. Make sure it is a port and not a bridge.</li>
	<li>You can go really low on memory, I tend to just use 32mb but you can go less.</li>
</ul>

<hr />

Thanks for stopping by.