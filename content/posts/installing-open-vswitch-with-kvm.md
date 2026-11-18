+++
title = "Installing Open vSwitch with KVM"
date = "2012-02-03T02:50:10+00:00"
lastmod = "2013-04-28T22:42:07+00:00"
author = "Brent Salisbury"
wp_id = 163
categories = ["In the Lab"]
tags = ["KVM", "Open vSwitch", "Tutorials"]
description = ""
url = "/installing-open-vswitch-with-kvm/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "abae13cc3d659b8a0c9779f86c2a005d15899cb8680f1bf0725ef90cab2ec212"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Installing Open vSwitch with KVM</h2>
This tutorial is for installing Open vSwitch with KVM in order to replace traditional hypervisor Ethernet switching using Linux bridging with Open vSwitch.

<aside class="legacy-callout"><strong>Updates</strong><ul>
	<li>
For installing Open vSwitch on Ubuntu from package head to <a href="{{< relurl "/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/" >}}" target="_blank">Open vSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller</a></li>
	<li>To install Open vSwitch from source head to <a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank">Configuring VXLan and GRE tunnels on OpenvSwitch</a></li>
</ul>
</aside>
<h2>Installing Open vSwitch on Ubuntu with KVM</h2>
I rebuilt this box becuase as fun as it was to setup OpenStack (I think) there are a million modules that would take more time to clip out rather than just rebuilding. Anyone gotten Nova integrated into Open vSwitch yet? That will be a great marriage for nailing up cloud nodes through tunnels dynamically. I expect  Open vSwitch to be an important not just to Vmware moving forward with software defined networking but more importantly setting a trend for open source software (OSS) project in networking.

Pulled some deps for some other things but here is history.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">sudo apt-get install python-simplejson python-qt4 python-zopeinterface python-twisted-conch automake autoconf gcc kvm uml-utilities virt-manager qemu-kvm kvm-pxe uml-utilities</pre>
Basically just my bash history.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">./boot.sh (apt-get install libtool will fix autoconf errors)
./configure --with-linux=/lib/modules/`uname -r`/build
make
make install
insmod datapath/linux/openvswitch.ko</pre>
Check for loaded ovs module
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">lsmod | grep open
lsmod | grep bridge
rmmod bridge
mkdir -p /usr/local/etc/openvswitch</pre>
Start OpenvSwitch
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db --remote=punix:/usr/local/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,manager_options --private-key=db:SSL,private_key --certificate=db:SSL,certificate --bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach -log--files
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --log-file --detach -v</pre>
Configure a bridge and add eth0 to the new bridge. Think locally significant Vlans.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">sudo ovs-vsctl add-br br0
ovs-vsctl add-port br0 eth0
ovs-vsctl list port</pre>
Change your eth0 IP to your new br0 interface.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">ifconfig eth0 0
ifconfig br0 x.x.x.x netmask 255.255.255.0
route add default gw 192.168.1.1 br0</pre>
Outside interface is now your br0.

These two scripts bring up the KVM Tap interfaces into your
bridge from the CLI.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">$ cat /etc/ovs-ifup
#!/bin/sh
switch=&#039;br0&#039;
/sbin/ifconfig $1 0.0.0.0 up
ovs-vsctl add-port ${switch} $1</pre>
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">$ cat /etc/ovs-ifdown 
#!/bin/sh
switch=&#039;br0&#039;
/sbin/ifconfig $1 0.0.0.0 down
ovs-vsctl del-port ${switch} $1
#Then make executable
chmod +x /etc/ovs-ifup /etc/ovs-ifdown</pre>
Here are some KVM examples. Starting with the CD is easiest.
No build needed for testing.

BOOT HD IMG
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">kvm -m 1024 -hda /media/Storage/imgs/centos.kvm -net nic,macaddr=00:11:22:CC:CC:C5 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown &amp;amp;</pre>
OS Install
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">kvm -m 512 -hda /media/Storage/imgs/centos.kvm -net nic,macaddr=00:11:22:CC:CC:C5 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom /media/Storage/vm-images/CentOS-6.2-x86_64-LiveCD.iso &amp;amp;</pre>
CD Boot
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">kvm -m 512 -net nic,macaddr=00:11:22:CC:CC:10 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -cdrom /HD/Storage/vm-images/ubuntu-11.10-desktop-amd64.iso &amp;amp;</pre>
Make an Image from CD
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">qemu-img create -f qcow2 /media/Storage/imgs/uCentOS-6.2.img 6G</pre>
Somewhere a VM if broken on the spinup will still allocate a tap.

<h2>Installing Open vSwitch with KVM Errors</h2>
If you get this kvm: -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown: Device 'tap' could not be initialized
Just delete the tap0. Need to dig into a work around cleaner than scripts.
ovs-vsctl del-port tap0

<hr>
Thanks for stopping by
<hr>