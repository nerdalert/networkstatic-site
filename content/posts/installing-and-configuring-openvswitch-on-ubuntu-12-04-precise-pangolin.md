+++
title = "Installing and Configuring OpenvSwitch on Ubuntu 12.04 (Precise Pangolin)"
date = "2012-04-16T06:00:44+00:00"
lastmod = "2013-10-21T05:33:59+00:00"
author = "Brent Salisbury"
wp_id = 376
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/installing-and-configuring-openvswitch-on-ubuntu-12-04-precise-pangolin/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8ef70cc56d7176a255b660c91b94cb10d630c6fc9199e2e9cb41d4f1eb8b2e16"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Installing and Configuring OpenvSwitch on Ubuntu 12.04 (Precise Pangolin)</h2>
<aside class="legacy-callout"><strong>Updates</strong>
<ul>
	<li>For installing OpenvSwitch on Ubuntu from package head to <a href="{{< relurl "/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/" >}}" target="_blank">OpenvSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller</a></li>
	<li>To install Open vSwitch from source head to <a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank">Configuring VXLan and GRE tunnels on OpenvSwitch</a></li>
	<li>Or use this Python App I wrote to install some different combinations of tools. Last verified working June 2013. <a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank">OpenFlow, OpenvSwitch and KVM SDN Lab Installation App</a></li>
</ul>
</aside>
<h2 class="legacy-heading">Installing and Configuring OpenvSwitch on Ubuntu 12.04 (Precise Pangolin)</h2>
Quick install how to for Installing and Configuring OpenvSwitch on Ubuntu 12.04 (Precise Pangolin) with the nightly OVS build. Before I start, I must point out the great progress the dev team has done in such a short time. All of the old gotchas in earlier releases on implementation are long gone. I am going to revisit the KVM integration in a few days as some of the inconsistencies for bringing up TAPs into hypervisors should be getting some consensus for provisioning.
<hr>
The announcement of the inclusion of OpenvSwitch into the mainline Linux kernel, coupled with some KVM enhancements to provide VLAN tagging, LACP, QoS, sFlow etc, is making some of us excited ,and others very nervous.
<pre class="code-sample"><code>
@ubuntu-12:openvswitch-HEAD-f1936eb# uname -a
Linux ubuntu-12 3.2.0-23-generic-pae #36-Ubuntu SMP Tue Apr 10 22:19:09 UTC 2012 i686 i686 i386 GNU/Linux
<em>#Ubuntu release</em>
@ubuntu-12:openvswitch-HEAD-f1936eb# lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description: Ubuntu precise (development branch)
Release: 12.04
Codename: precise
</code></pre>
For those familiar with the build you can just paste the following in your bash shell as root. To walk through the install skip the following snippet. The installation is extensively documented in the INSTALL file in the root of the tarball.
<pre class="code-sample"><code>apt-get update
apt-get install -y git automake autoconf gcc uml-utilities libtool build-essential git pkg-config linux-headers-`uname -r`
wget http://openvswitch.org/releases/openvswitch-1.10.0.tar.gz
tar zxvf openvswitch-1.10.0.tar.gz
cd openvswitch-1.10.0
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make && make install
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
<h4>System Preperation</h4>
Install dependencies:
<pre class="code-sample"><code>apt-get update
apt-get install python-simplejson automake autoconf gcc uml-utilities libtool build-essential git pkg-config</code></pre>
Download the OVS tarball <em>Note: you can also pull from the git repository but that is bleeding edge and depending on kernel releases it may need some massaging.</em>

<pre class="code-sample"><code>wget http://openvswitch.org/releases/openvswitch-1.10.0.tar.gz
tar zxvf openvswitch-1.10.0.tar.gz
cd openvswitch-1.10.0</code></pre>

<h2>Compiling Open vSwitch From Source</h2>
<pre class="code-sample"><code>./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make
make install
#Load the OVS Kernel Module
insmod datapath/linux/openvswitch.ko</code></pre>
<pre class="code-sample"><code>#If you are running a stripped version of Nix like an EC2 cloud image and get an error along the lines of this:
configure: error: source dir /lib/modules/3.2.0-23-virtual/build doesn&#039;t exist
#Pull down the headers for your kernel. 
sudo apt-get install linux-headers-`uname -r`</code></pre>
<h2>Open vSwitch Configuration</h2>
<pre class="code-sample"><code>touch /usr/local/etc/ovs-vswitchd.conf
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema</code></pre>
Run the following commands, note some dashes are two '- -' e.g. - -remote=db &amp; - -private-key

Start ovsdb-server, this stores the config into a file that is persistent even after restarts.
<pre class="code-sample"><code>ovsdb-server /usr/local/etc/openvswitch/conf.db \
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
#lsmod | grep br
#brcompat               13512  0 
#openvswitch            98196  1 brcompat</code></pre>
If they are not there try loading again and check your path to the kernel module.
<pre class="code-sample"><code>insmod datapath/linux/openvswitch.ko</code></pre>
At this point you have a fucntioning vanilla OVS install. Output should look something like this.
<pre class="code-sample"><code>ovs-vsctl show
b6d574d7-5582-4cc0-93e5-a90cf0eb0a38
root@demo-139:/home/ubuntu/ovs-vxlan# ovs-vsctl --version
ovs-vsctl (Open vSwitch) 1.8.90
Compiled Aug 19 2012 06:23:36</code></pre>
<h2>Configure Linux Networking</h2>
I have one NIC (eth1) on the same LAN segment/network/vlan.
We are attaching eth1 to br1 and applying an IP to the bridge interface.
We are attaching an IP to br2. br2 is the island that we are building a tunnel for hosts to connect on.
<pre class="code-sample"><code>ovs-vsctl add-br br1
ovs-vsctl add-br br2
ovs-vsctl add-port br1 eth1
ifconfig eth1 0
ifconfig br1 192.168.1.11 netmask 255.255.255.0
route add default gw 192.168.1.1 br1 (br1 is now the default gateway NIC instead of eth1 since we moved eth1 inside of br1 (bridge interface br1)
ifconfig br2 10.1.2.11 netmask 255.255.255.0 (no physical interface is bound here.)</code></pre>
If you have issues getting the bridge built you may need to kill the OVS processes and restart them depending on your step order.

Your Linux routing table should now look something like this:
<pre class="code-sample"><code>root@openstack2:~# route -n
 Kernel IP routing table
 Destination Gateway Genmask Flags Metric Ref Use Iface
0.0.0.0         192.168.1.1    0.0.0.0         UG    0      0        0 br1
 10.1.2.0 0.0.0.0 255.255.255.0 U 0 0 0 br2
 192.168.1.0 0.0.0.0 255.255.255.0 U 0 0 0 br1</code></pre>
You can put the following into a text file and give it execute permissions with "chmod +x filename" and then run it "./filename". If your network settings are right it should flip the IP to the bridge and not cut you off. Keyword "should" so have a way to get to the box if you cut yourself off.
<pre class="code-sample"><code>ovs-vsctl add-br br1
ovs-vsctl add-br br2
ovs-vsctl add-port br1 eth1
ifconfig eth1 0 &amp;&amp; ifconfig br1 192.168.1.(X) netmask 255.255.255.0
route add default gw 192.168.1.1 br1
ifconfig br2 10.1.2.11 netmask 255.255.255.0</code></pre>
<p style="text-align: left;">If you want your networking to be persistent over restart you can adjust /etc/network/interfaces similar to the following template.</p>

<pre class="code-sample"><code>auto br0
 iface br0 inet static
 address 192.168.1.x
 network 192.168.1.0
 netmask 255.255.255.0
 broadcast 192.168.1.255
 gateway 192.168.1.1
 #Add your physical interface to the bridge.
 bridge_ports eth0
 bridge_fd 9
 bridge_hello 2
 bridge_maxage 12
 bridge_stp off
 dns-nameservers 8.8.8.8</code></pre>
<hr>




Thanks for stopping by.