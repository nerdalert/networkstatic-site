+++
title = "OpenvSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller"
date = "2012-05-28T05:32:54+00:00"
lastmod = "2013-10-15T01:18:15+00:00"
author = "Brent Salisbury"
wp_id = 768
categories = ["In the Lab"]
tags = ["Open vSwitch", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/"
aliases = ["/2012/05/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/"]
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "48c157508043fb39c82dad68e1c8ecff0711d7ea46979098f5b513f6f48e57de"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenvSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller</h2>
<a href="{{< relurl "/wp-content/uploads/2012/05/Openvswitch1.jpg" >}}"><img class="alignright" title="Openvswitch framework" alt="" src="{{< relurl "/wp-content/uploads/2012/05/Openvswitch1-300x254.jpg" >}}" width="300" height="254" /></a>OpenvSwitch Configure from Packages and Attaching to a Floodlight OpenFlow Controller: Couple folks have asked about installing OpenvSwitch from packages on Ubuntu 12.04 as opposed to from source. The default repos have v1.4 up so almost at the latest v1.4.1. OVS will be the de facto vSwitch in the hyper-scale providers in the future in my opinion. As Vmware's Nicira acquisition merges it will percolate into the enterprise. So its a good time to learn software switching and OVS is the best platform to start with.

<h2>OpenvSwitch Configure from Packages</h2>

This is currently not building on Ubuntu 13.04 w/ 3.8.0-29-generic. Give installing from the tarball a run. Detailed instructions are located in the INSTALL file in the root of the release. A post covering the build and overlay tunnels can be found at the following link:

<a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}">Configuring VXLAN and GRE Tunnels on OpenvSwitch</a>



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
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server -v --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,manager_options \
                     --private-key=db:SSL,private_key \
                     --certificate=db:SSL,certificate \
                     --pidfile --detach --log-file
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
ovs-vsctl show</code></pre>

<em>If running an Ubuntu 12.x distribution the following may still work.</em>

<pre class="code-sample"><code>
$apt-get install openvswitch-datapath-source bridge-utils
$module-assistant auto-install openvswitch-datapath 
$apt-get install  openvswitch-switch openvswitch-common openvswitch-controller</code></pre>
<hr>
Verify install
<pre class="code-sample"><code>$ ovs-vsctl show
 ovs_version: &quot;1.4.0+build0&quot;</code></pre>
Processes should look something like this
<pre class="code-sample"><code>$ ps -ea | grep ov
 26464 ? 00:00:00 ovsdb-server
 26465 ? 00:00:00 ovsdb-server
 26473 ? 00:00:00 ovs-vswitchd
 26474 ? 00:00:00 ovs-vswitchd
 26637 ? 00:00:00 ovs-controller</code></pre>
<hr>
Restart OVS (probably not necessary)
<pre class="code-sample"><code>$ /etc/init.d/openvswitch-switch restart</code></pre>
You can see the version of OVS and the configuration using the following.
<pre class="code-sample"><code>$ ovs-vsctl show</code></pre>
Add your bridge, think of this as a subnet or container for VLAN IDs if you aren't familiar with the term. Each DPID is a separate data plane that appears as a separate switch to something like an OpenFlow controller.
<pre class="code-sample"><code>$ovs-vsctl add-br br0</code></pre>
<hr>
Add a physical interface to your virtual bridge for connectivity off box. If you don't script this part you will probably clip your connection as you zero out eth0 and apply it to br0. You can pop the commands into a text file and make it executable with chmod +x.
<hr>
You can edit the /etc/network/interfaces file for it to be persistent through reboots or use ifconfig from the CLI but it will be temporary. If learning, just use ifconfig, it is good to know Linux networking for the future.
<pre class="code-sample"><code>auto br0
 iface br0 inet static
 address 192.168.1.208
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
This will add the physical port (eth0) to the logical bridge (br0).
<pre class="code-sample"><code>ovs-vsctl add-port br0 eth0</code></pre>
Once you edit the file restart networking. *This will cut you off but you should be able to attach to the br0 (bridge) address you added on the same subnet.
<pre class="code-sample"><code>$/etc/init.d/networking restart</code></pre>
<hr>
After you restart networking your ifconfig and route -n should look something like this.
<pre class="code-sample"><code> ifconfig
 br0 Link encap:Ethernet HWaddr 0e:85:8b:d1:4b:44
 inet addr:192.168.1.208 Bcast:172.31.247.255 Mask:255.255.254.0
 inet6 addr: fe80::c85:8bff:fed1:4b44/64 Scope:Link
 UP BROADCAST RUNNING PROMISC MULTICAST MTU:1500 Metric:1
 RX packets:156 errors:0 dropped:0 overruns:0 frame:0
 TX packets:103 errors:0 dropped:0 overruns:0 carrier:0
 collisions:0 txqueuelen:0
 RX bytes:14218 (14.2 KB) TX bytes:15524 (15.5 KB)
 eth0 Link encap:Ethernet HWaddr 52:54:00:11:11:11
 UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
 RX packets:27460 errors:0 dropped:0 overruns:0 frame:0
 TX packets:19673 errors:0 dropped:0 overruns:0 carrier:0
 collisions:0 txqueuelen:1000
 RX bytes:64786777 (64.7 MB) TX bytes:1518312 (1.5 MB)</code></pre>
<pre class="code-sample"><code>route -n
 Kernel IP routing table
 Destination Gateway Genmask Flags Metric Ref Use Iface
 0.0.0.0 172.31.246.1 0.0.0.0 UG 100 0 0 br0
 169.254.0.0 0.0.0.0 255.255.0.0 U 1000 0 0 br0
 172.31.246.0 0.0.0.0 255.255.254.0 U 0 0 0 br0</code></pre>
<h4>Manually using ifconfig if you didn't edit /etc/network/interfaces</h4>
Zero out your eth0 interface and slap it on the bridge interface
(warning will clip you unless you script it)
<pre class="code-sample"><code>$brctl add-br br0 if you do not have a br0 interface from ovs.
 $ifconfig eth0 0
 $ifconfig br0 192.168.1.208 netmask 255.255.255.0
 #Change your df route
 $route add default gw 192.168.1.1 br0 and 
 $route del default gw 192.168.1.1 eth0</code></pre>
Show the bridging tables
<pre class="code-sample"><code># ovs-appctl fdb/show br0
 port VLAN MAC Age
 1 0 00:1d:09:aa:71:16 47
 1 0 00:9c:02:b2:76:c0 18
 1 0 68:a8:6d:11:9b:8e 13
 0 0 00:50:56:25:21:68 9
 1 0 10:40:f3:94:e0:82 5
 1 0 00:23:69:62:26:09 0</code></pre>
<hr>
<h2>Connect OpenvSwitch to the the OpenFlow Controller</h2>

<pre class="code-sample"><code>ovs-vsctl set-controller br-int tcp:192.168.1.208:6633</code></pre>
<h2>Attaching to a Floodlight OpenFlow Controller</h2>
<a href="{{< relurl "/floodlight-openflow-controller-screencast-with-hp-switches/" >}}"> http://networkstatic.net/floodlight-openflow-controller-screencast-with-hp-switches/
</a>

Output from the Floodlight controller:
<pre class="code-sample"><code>&lt;strong&gt;00:38:05.808&lt;/strong&gt; [New I/O server worker #1-1] INFO n.f.core.internal.Controller - New switch connection from /192.168.1.155:43966
 &lt;strong&gt;00:38:05.825&lt;/strong&gt; [New I/O server worker #1-1] DEBUG n.f.core.internal.Controller - HELLO from OFSwitchImpl [/192.168.1.155:43966 DPID[?]]
 &lt;strong&gt;00:38:05.828&lt;/strong&gt; [New I/O server worker #1-1] DEBUG n.f.core.internal.Controller - Features Reply from OFSwitchImpl [/192.168.1.155:43966 DPID[?]]
 &lt;strong&gt;00:38:05.839&lt;/strong&gt; [New I/O server worker #1-1] INFO n.f.core.internal.Controller - This controllers role is null - not sending role-request-msg
 &lt;strong&gt;00:38:05.839&lt;/strong&gt; [New I/O server worker #1-1] DEBUG n.f.core.internal.Controller - Config Reply from OFSwitchImpl [/192.168.1.155:43966 DPID[00:00:00:50:56:25:21:68]] confirms miss length set to 0xffff
 &lt;strong&gt;00:38:05.846&lt;/strong&gt; [New I/O server worker #1-1] INFO n.f.core.internal.Controller - Switch handshake
 successful: OFSwitchImpl [/192.168.1.155:43966 DPID[00:00:00:50:56:25:21:68]]
 &lt;strong&gt;00:38:05.848&lt;/strong&gt; [main] DEBUG n.f.core.internal.Controller - Dispatching switch update OFSwitchImpl
 [/192.168.1.155:43966 DPID[00:00:00:50:56:25:21:68]] true
 &lt;strong&gt;00:38:05.848&lt;/strong&gt; [main] DEBUG n.f.s.StaticFlowEntryPusher - addedSwitch OFSwitchImpl
 [/192.168.1.155:43966 DPID[00:00:00:50:56:25:21:68]]; processing its static entries</code></pre>
Any who, plug away with a hypervisor and build the next-gen of computing! No need to wait on someone to hand it to us. Get rich while you are at it :0 Make it rain and stuff.
<hr>
<strong>Add KVM and build instances using taps from OVS:</strong>
<a href="https://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/" target="_blank"> http://networkstatic.net/installing-openvswitch-on-ubuntu-11-10-with-kvm/</a>
<strong>Or Quantum and OpenStack for the more adventurous:</strong>
<a href="{{< relurl "/openstack-essex-and-quantum-installation-using-openvswitch-from-scratch/" >}}" target="_blank"> http://networkstatic.net/openstack-essex-and-quantum-installation-using-openvswitch-from-scratch/</a>