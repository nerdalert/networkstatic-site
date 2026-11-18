+++
title = "OpenDaylight OpenStack Integration with DevStack on Fedora"
date = "2014-02-07T06:32:25+00:00"
lastmod = "2015-05-11T00:39:38+00:00"
author = "Brent Salisbury"
wp_id = 7176
categories = ["In the Lab", "Programming"]
tags = ["Open vSwitch", "OpenDaylight", "OpenStack", "Tutorials"]
description = ""
url = "/opendaylight-openstack-integration-devstack-fedora-20/"
image = "/wp-content/uploads/2013/05/OpenDaylight-Logo-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "2be105f6123c38c5e1c1f7dbeeca9bd5545174d47cfc425114db3d9a78d5061c"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2 class="legacy-heading"> OpenDaylight OpenStack Integration with DevStack on Fedora </h2>

The following is a walk through of the OVSDB project within OpenDaylight for OpenStack integration. There are a couple of bugs so it is not for the faint of heart. It is intended for those looking to get their development environment up and running. We will have videos and what not walking through the installation and code reviews of the implementation. It was developed by folks from various vendors and users in the community. Some are in companies that aren't dedicating resources to the project but are doing it in their personal time. Both <a href="https://twitter.com/MadhuVenugopal" target="_blank">Madhu</a> and I are maintaining this post to keep it as accurate as possible and up to date with our own individual notes as we move into the next phase of development for Helium. Madhu is going to do a separate Fedora 19 post on a new blog he is setting up which I am pumped about! Until then, keep an eye out for Fedora19 and Fedora20 specific instructions below.
<h2 class="legacy-heading"> Recordings of the Installation </h2>

The following are some late night / early morning recordings from Madhu and me. In case anyone gets stuck and wants to follow along at home. They are all done on our laptops so resources are a bit tight. For questions and issues please send them to the OVSDB Listserv so that one of us or other awesome folks in the community can assist since our Q/A bandwidth is focused there to try and build a good collective of knowledge to share. If you have further interest in the project, just assisting others in the Listserv, documenting and code contributions are all amazing and much appreciated and respected.


<ul>
	<li>OpenStack/OpenDaylight/OVSDB Installation Part 1 - Configuring VirtualBox and VM Fusion</li>
</ul>


<p><a href="http://www.youtube.com/watch?v=37CTb9KJ3x8">Watch video on YouTube</a></p>


<ul>
	<li>OpenStack/OpenDaylight/OVSDB Installation Part 2 - Stacking and Spinning up Multi-Node OpenStack w/the OpenDaylight Controller</li>
</ul>


<p><a href="http://www.youtube.com/watch?v=0APNbgiRD8o">Watch video on YouTube</a></p>


<ul>
	<li>For more OpenDaylight / OVSDB videos and weekly Hangouts please see our YouTube channel:</li>
</ul>


<a href="http://www.youtube.com/channel/UCMYntfZ255XGgYFrxCNcAzA/feed" target="_blank" rel="noopener noreferrer">OpenDaylight OVSDB Channel</a>
<h2 class="legacy-heading"> OVSDB Project Control and Management Logic </h2>

No standards were hurt in the making of this recording. The only southbound protocols we used in the OVSDB project OpenStack implementation were <a href="https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.3.0.pdf" target="_blank">OpenFlow v1.3</a> and <a href="http://datatracker.ietf.org/doc/rfc7047/" target="_blank">OVSDB</a>. We chose not to use any extensions or the use of agents. Open vSwitch supported the necessary OpenFlow v1.3 and OVSDB functionality we required for this architecture. Those of us in the OVSDB project are pretty agnostic to southbound protocols as long as there is a healthy adoption so as not to waste our time and based on open standards such as OpenFlow v1.3, RFCs 7047 (Informational OVSDB RFC) and/or de facto drafts like <a href="http://datatracker.ietf.org/doc/draft-mahalingam-dutt-dcops-vxlan/" target="_blank">draft-mahalingam-dutt-dcops-vxlan</a> (VXLAN framing). We are keen to see NXM extension functionality upstream into the OpenFlow specification. OVS ARP responder is something we are beginning to work on proofing now. NXM and OXM extensions merging for ARP and Tunnel feature parity would make our design and coding lives easier. The overall architecture looks something like the following. I have hardware TEPs in the diagram. We have cycles to help hardware vendors implement the hardware_vtep database schema (assuming they prescribe to open operating systems):

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/02/Overlay-OpenDaylight-OVSDB-OpenFlow.png" >}}" alt="OVSDB OpenFlow OpenDaylight Overlay"></figure>

The provider segmentation keys used in the encap (GRE key/VNI) is a hash of Network and Tenant ID since as long as we are subnet bound, networks will always need to support multi-tenant logical networks until we eradicate L2 all together. The design is flexible and as generic as possible to allow for any vendor to add differentiation on top of the base network virtualization. Of course, we have plenty to do between now and stability, so moving right along.


<ul>
	<li>A quick visual of the OVSDB Neutron implementation code flow itself and how it ties into the controller project and OpenStack is the excellent diagram Madhu did:</li>
</ul>



<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/02/OVSDB-Architecture.png" >}}" alt="OVSDB OpenDaylight Architecture"></figure>
<h2 class="legacy-heading"> Configure the Fedora Images for your Environment </h2>

There are two options for images. Fedora 19 and Fedora 20. We tend to recommend F19 due to an issue with MariaDB and hostnames in the F20 VM. More on that when we edit the hostname in the tutorial. For assistance with getting the stack going please ping the <a href="https://lists.opendaylight.org/mailman/listinfo/ovsdb-dev" target="_blank">OVSDB Listserv</a> and check the archives for answers.

Download the pre-built image we made that contains OpenDaylight, DevStack installing Ice House OpenStack, Open vSwitch all on Fedora:

Fedora 19 based all-in-one VM:
<pre class="code-sample"><code>curl -O https://wiki.opendaylight.org/images/HostedFiles/ODL_Devstack_Fedora19.zip
$ unzip ODL_Devstack_Fedora19.zip
# Two files contained
ODL-Devstack-Fedora19-disk1.vmdk
ODL-Devstack-Fedora19.ovf</code></pre>

or if you prefer, you can download Fedora 20 based all-in-one VM:

<pre class="code-sample"><code>$ curl -O https://wiki.opendaylight.org/images/HostedFiles/OpenDaylight_DevStack_Fedora20.ova</code></pre>

Clone this Virtual Machine image into two images. One is for the Control (This VM runs both the OpenStack Controller and OpenDaylight Controller) and the other for the Compute instance. If you use VM Fusion the vanilla image works as is with no need to change any adaptor settings. Use the 'ip addr' configuration output as a reference in the next section. I recommend using SSH to connect to the host rather then using the TTY interface.

<aside class="legacy-callout"><strong>VirtualBox NIC Network Caveats</strong>If using VirtualBox During the cloning process, reinitialize the mac-addresses to get ensure you have a unique address. and it is recommended to use Host-Only network Adapters as opposed to NAT network adapters. I usually use a different hypervisor for test/dev and managed to blow up a demo at the Summit by using NAT w/Vbox.</aside>

Here are two screenshots with VirtualBox network adaptor examples. The first are the two networks you can create. vxboxnet0 is there by default. Create the 2nd network with the +w/a nic picture in the following example. Note: you have to manually fill in the DHCP server settings on the new network. Refer to the existing if unsure of the values to use. When complete the host OS should be able to reach the guest OS.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/02/VirtualBox-HostOnly-Networks.png" >}}" alt="Virtual Box Network DHCP"></figure>

The second example is what the VirtualBox NIC setup can look like without have to deal with the NAT Network option in VirtualBox. VM Fusion has integrated hooks in to resolve the need for host only etc. NAT and Host only work fine with NAT so the host can reach your networks default gateway and get to the Inets as needed. With host only that is not the case but it is plenty to run the stack and integration.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/02/VirtualBox-HostOnly-Nics.png" >}}" alt="Virtual Box Host Only NIC Configuration"></figure>

Boot both guest VMs write down the four IP addresses from both NICs. You will primarily only use one of them other then a gateway or out of band SSH connectivity etc.

If you are using the Fedora 19 VM, then please use the following credentials to login:
<pre class="code-sample"><code>Login: fedora
Passwd: opendaylight</code></pre>

If you are using the Fedora 20 VM, then please use :
<pre class="code-sample"><code>Login: odl
Passwd: odl</code></pre>

Oops :)

In this example the configuration of the IP addrs are as follows:

<pre class="code-sample"><code>Openstack Controller IP == 172.16.86.129
Openstack Compute IP == 172.16.86.128
OpenDaylight Controller IP == 172.16.86.129</code></pre>

Record the IP addresses of both of the hosts:

Controller IP addresses:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ ip addr
1: lo: loopback,up,lower_up, mtu 65536 qdisc noqueue state UNKNOWN group default
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: &lt;broadcast,multicast,up,lower_up&gt; mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
link/ether 00:0c:29:35:0b:65 brd ff:ff:ff:ff:ff:ff
inet 172.16.47.134/24 brd 172.16.47.255 scope global dynamic eth0
valid_lft 1023sec preferred_lft 1023sec
inet6 fe80::20c:29ff:fe35:b65/64 scope link
valid_lft forever preferred_lft forever
3: eth1: &lt;broadcast,multicast,up,lower_up&gt; mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
link/ether 00:0c:29:35:0b:6f brd ff:ff:ff:ff:ff:ff
inet 172.16.86.129/24 brd 172.16.86.255 scope global dynamic eth1
valid_lft 1751sec preferred_lft 1751sec
inet6 fe80::20c:29ff:fe35:b6f/64 scope link
valid_lft forever preferred_lft forever</code></pre>

Compute IP addresses:

<pre class="code-sample"><code>[odl@fedora-odl-2 ~]$ ip addr
1: lo: &lt;loopback,up,lower_up&gt; mtu 65536 qdisc noqueue state UNKNOWN group default
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: &lt;broadcast,multicast,up,lower_up&gt; mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
link/ether 00:0c:29:85:2d:f2 brd ff:ff:ff:ff:ff:ff
inet 172.16.47.133/24 brd 172.16.47.255 scope global dynamic eth0
valid_lft 1774sec preferred_lft 1774sec
inet6 fe80::20c:29ff:fe85:2df2/64 scope link
valid_lft forever preferred_lft forever
3: eth1: &lt;broadcast,multicast,up,lower_up mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
link/ether 00:0c:29:85:2d:fc brd ff:ff:ff:ff:ff:ff
inet 172.16.86.128/24 brd 172.16.86.255 scope global dynamic eth1
valid_lft 1716sec preferred_lft 1716sec
inet6 fe80::20c:29ff:fe85:2dfc/64 scope link
valid_lft forever preferred_lft forever</code></pre>

Go to the home directory of the user id odl:
<pre class="code-sample"><code>$ cd ~/</code></pre>

Start the OVS Service (DevStack should start this svc but I have seen this not on occasion fwiw). This startup script can be loaded at startup of OVS to load at the OS init.

<pre class="code-sample"><code> sudo /sbin/service openvswitch start </code></pre>

Configure the /etc/hosts file to reflect your controller and compute hostname mappings. While not necessarily required it can cause issues for Nova output.

Verify the OpenStack Controller /etc/hosts file. The only edit is adding the compute IP to hostname mapping. E.g. x.x.x.x fedora-odl-2

<pre class="code-sample"><code>[odl@fedora-odl-1 ~]$ sudo vi /etc/hosts
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4 fedora-odl-1
172.16.86.128 fedora-odl-2
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6 </code></pre>

You will need to edit the compute nodes /etc/hosts from fedora-odl-1 to fedora-odl-2:
<pre class="code-sample"><code> [odl@fedora-odl-2 ~]$ sudo vi /etc/hosts
$ cat /etc/hosts
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4 fedora-odl-2
172.16.86.129 fedora-odl-1
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6</code></pre>

Then change the compute hostname from (compute only):
<pre class="code-sample"><code>
$ sudo vi /etc/hostname
# Change to:
$ cat /etc/hostname
fedora-odl-2
$sudo vi /etc/sysconfig/network
#Change HOSTNAME=fedora-odl-1 to HOSTNAME=fedora-odl-2
$sudo hostname -b fedora-odl-2</code></pre>

Then reboot the cloned Compute node for the change to take affect:

<pre class="code-sample"><code> sudo shutdown -r now</code></pre>
After the host restarts verify the hostnames like so:

<pre class="code-sample"><code> $ hostname
fedora-odl-2</code></pre>

Unfortunately, in the Fedora 20 VM, if you comment out "#127.0.0.1 localhost fedora-odl-1" you will blow up MySql. (Thanks for digging into that Vijay!) So avoid doing any changes to the host name locally resolving to 127.0.0.1. Mestery has a link on one of his blogs to this issue also. Net is, leave localhost. If you change it and try and revert back it will still get angry.

<pre class="code-sample"><code>An unexpected error prevented the server from fulfilling your request. (OperationalError) (1045, "Access denied for user 'root'@'fedora-odl-1' (using password: YES)") None None (HTTP 500)
2014-02-10 04:03:28 + KEYSTONE_SERVICE=
2014-02-10 04:03:28 + keystone endpoint-create --region RegionOne --service_id --publicurl http://172.16.86.129:5000/v2.0 --adminurl http://172.16.86.129:35357/v2.0 --internalurl http://172.16.86.129:5000/v2.0
2014-02-10 04:03:28 usage: keystone endpoint-create [--region ] --service
2014-02-10 04:03:28 --publicurl 2014-02-10 04:03:28 [--adminurl ]
2014-02-10 04:03:28 [--internalurl ]
2014-02-10 04:03:28 keystone endpoint-create: error: argument --service/--service-id/--service_id: expected one argument
2014-02-10 04:03:28 ++ failed</code></pre>
<h2 class="legacy-heading"> Start OpenDaylight Controller on the OpenStack Controller Node </h2>

<pre class="code-sample"><code>$ cd odl/opendaylight/</code></pre>

Check that the configuration is set for OpenFlow v1.3 with the following to ensure that ovsdb.of.version=1.3 is uncommented:

<pre class="code-sample"><code>$ grep ovsdb.of.version configuration/config.ini
ovsdb.of.version=1.3</code></pre>

If it is not uncommented, adjust the config.ini file to uncomment the line ovsdb.of.version=1.3
The file is located at /home/odl/opendaylight/configuration/config.ini
<pre class="code-sample"><code>### Before ###
# ovsdb.of.version=1.3
### After ###
ovsdb.of.version=1.3</code></pre>

Or, simply paste the following:

<pre class="code-sample"><code>
sudo sed -i 's/#\ ovsdb.of.version=1.3/ovsdb.of.version=1.3/' /home/odl/opendaylight/configuration/config.ini</code></pre>

Lastly, start the ODL controller w/ the following:
<pre class="code-sample"><code>./run.sh -XX:MaxPermSize=384m -virt ovsdb -of13</code></pre>

When the controller if finished loading here are some typical messages in the OSGI console:

<pre class="code-sample"><code>2014-02-06 20:41:22.458 UTC [pool-2-thread-4] INFO o.o.controller.frm.flow.FlowProvider - Flow Config Provider started.
2014-02-06 20:41:22.461 UTC [pool-2-thread-4] INFO o.o.c.frm.group.GroupProvider - Group Config Provider started.
2014-02-06 20:41:22.507 UTC [pool-2-thread-4] INFO o.o.c.frm.meter.MeterProvider - Meter Config Provider started.
2014-02-06 20:41:22.515 UTC [pool-2-thread-6] INFO o.o.c.m.s.manager.StatisticsProvider - Statistics Provider started.</code></pre>

You can verify the sockets/ports are bound with the following command. Ports 6633, 6640 and 6653 should all be bound and listening:

<pre class="code-sample"><code>$ lsof -iTCP | grep 66
java 1330 odl 154u IPv6 15262 0t0 TCP *:6640 (LISTEN)
java 1330 odl 330u IPv6 15392 0t0 TCP *:6633 (LISTEN)
java 1330 odl 374u IPv6 14306 0t0 TCP *:6653 (LISTEN)</code></pre>
<h2 class="legacy-heading"> Configure the DevStack for the OpenStack Controller </h2>

Make sure all bridges are removed only if you have previously "stacked"
<pre class="code-sample"><code>$sudo ovs-vsctl show</code></pre>

Once the OpenDaylight Controller is running, stack the OpenStack Controller:

If you are using the Fedora 19 VM :

<pre class="code-sample"><code>$ cd ~/
$ cd devstack
$ cp local.conf.control local.conf
$ vi local.conf</code></pre>

For the Fedora 20 VM :

<pre class="code-sample"><code>$ cd ~/
$ cp local.conf.control devstack/local.conf
$ cd devstack
$ vi local.conf</code></pre>

Edit the local.conf you just copied with the appropriate IPs. Replace all instances with brackets to the Daylight SDN controller, the OpenStack controller IP or the Openstack compute IP (Compute ethX address is only on the compute node). In this example I am using the addresses for eth1 on the guest VM. Again ensure you have IP reachability between controller and compute API services when troubleshooting issues.

In the local.conf you will see four lines that require the hardcoding of an IP address. You can always replace some of those w/ variables but we thought it important to help understand the DevStack configuration and Neutron REST call to the ODL OpenStack API implemented in org.opendaylight.controller.networkconfig.neutron.implementation.

<pre class="code-sample"><code>
SERVICE_HOST=
HOST_IP=
VNCSERVER_PROXYCLIENT_ADDRESS=
url=http://:8080/controller/nb/v2/neutron</code></pre>

The following is the OpenStack controller local.conf for this tutorial:

<pre class="code-sample"><code>[[local|localrc]]
LOGFILE=stack.sh.log
# Logging Section
SCREEN_LOGDIR=/opt/stack/data/log
LOG_COLOR=False
# Prevent refreshing of dependencies and DevStack recloning
OFFLINE=True
#RECLONE=yes

disable_service rabbit
enable_service qpid
enable_service n-cpu
enable_service n-cond
disable_service n-net
enable_service q-svc
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service quantum
enable_service tempest

Q_HOST=$SERVICE_HOST
HOST_IP=172.16.86.129

Q_PLUGIN=ml2
Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight,logger
ENABLE_TENANT_TUNNELS=True
NEUTRON_REPO=https://github.com/CiscoSystems/neutron.git
NEUTRON_BRANCH=odl_ml2

VNCSERVER_PROXYCLIENT_ADDRESS=172.16.86.129
VNCSERVER_LISTEN=0.0.0.0

HOST_NAME=fedora-odl-1
SERVICE_HOST_NAME=${HOST_NAME}
SERVICE_HOST=172.16.86.129

FLOATING_RANGE=192.168.210.0/24
PUBLIC_NETWORK_GATEWAY=192.168.75.254
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
RABBIT_PASSWORD=rabbit
QPID_PASSWORD=rabbit
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin

[[post-config|/etc/neutron/plugins/ml2/ml2_conf.ini]]
[agent]
minimize_polling=True

[ml2_odl]
url=http://172.16.86.129:8080/controller/nb/v2/neutron
username=admin
password=admin</code></pre>

Verify the local.conf by greping for the IP prefix used:

<pre class="code-sample"><code>$ grep 172.16 local.conf
HOST_IP=172.16.86.129
VNCSERVER_PROXYCLIENT_ADDRESS=172.16.86.129
SERVICE_HOST=172.16.86.129
url=http://172.16.86.129:8080/controller/nb/v2/neutron</code></pre>

Finally execute the stack.sh shell script:
<pre class="code-sample"><code>$ ./stack.sh</code></pre>

You should see activity in your OSGI console as Neutron adds the default private and public networks like so:

<pre class="code-sample"><code>osgi&gt; 2014-02-06 20:58:27.418 UTC [http-bio-8080-exec-1] INFO o.o.c.u.internal.UserManager - Local Authentication Succeeded for User: "admin"
2014-02-06 20:58:27.419 UTC [http-bio-8080-exec-1] INFO o.o.c.u.internal.UserManager - User "admin" authorized for the following role(s): [Network-Admin]</code></pre>

You will see more activity as ODL programs the OVSDB server running on the OpenStack node.

Here is the state of Open vSwitch after the stack completes and prior to booting a VM instance. If you do not see the is_connected: true boolean after Manager (OVSDB) and Controller (OpenFlow) something has gone wrong and check that the controller/manager IPs are reachable and the ports are bound using the lsof command listed earlier:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ sudo ovs-vsctl show
17074e89-2ac5-4bba-997a-1a5a3527cf56
Manager "tcp:172.16.86.129:6640"
is_connected: true
Bridge br-int
Controller "tcp:172.16.86.129:6633"
is_connected: true
fail_mode: secure
Port br-int
Interface br-int
type: internal
Port "tap1e3dfa54-9c"
Interface "tap1e3dfa54-9c"
Bridge br-ex
Controller "tcp:172.16.86.129:6633"
is_connected: true
Port "tap9301c38d-d8"
Interface "tap9301c38d-d8"
Port br-ex
Interface br-ex
type: internal
ovs_version: "2.0.0"

Here are the OpenFlow v1.3 flow rules for the default namespace ports in OVS (qdhcp / qrouter):

[crayon lang="bash" ]OFPST_FLOW reply (OF1.3) (xid=0x2):
cookie=0x0, duration=202.138s, table=0, n_packets=0, n_bytes=0, send_flow_rem in_port=1,dl_src=fa:16:3e:fb:4a:32 actions=set_field:0x2-&gt;tun_id,goto_table:10
cookie=0x0, duration=202.26s, table=0, n_packets=0, n_bytes=0, send_flow_rem in_port=1,dl_src=fa:16:3e:2e:29:d3 actions=set_field:0x1-&gt;tun_id,goto_table:10
cookie=0x0, duration=202.246s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=1 actions=drop
cookie=0x0, duration=202.302s, table=0, n_packets=0, n_bytes=0, send_flow_rem dl_type=0x88cc actions=CONTROLLER:56
cookie=0x0, duration=202.186s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x1 actions=goto_table:20
cookie=0x0, duration=202.063s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x2 actions=goto_table:20
cookie=0x0, duration=202.14s, table=20, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x1 actions=drop
cookie=0x0, duration=202.046s, table=20, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x2 actions=drop
cookie=0x0, duration=202.2s, table=20, n_packets=0, n_bytes=0, send_flow_rem priority=16384,tun_id=0x1,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1
cookie=0x0, duration=202.083s, table=20, n_packets=0, n_bytes=0, send_flow_rem priority=16384,tun_id=0x2,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1
cookie=0x0, duration=202.211s, table=20, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:2e:29:d3 actions=output:1
cookie=0x0, duration=202.105s, table=20, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x2,dl_dst=fa:16:3e:fb:4a:32 actions=output:1</code></pre>

Next up is stacking the compute node.
<h2 class="legacy-heading"> Configure the OpenStack Compute Node </h2>

The compute configuration steps are virtually identical to the controller other then the configurations and that it does not run the Daylight controller.

If you are using the Fedora 19 VM :

<pre class="code-sample"><code>$ cd ~/
$ cd devstack
$ cp local.conf.compute local.conf
$ vi local.conf</code></pre>

For the Fedora 20 VM :

<pre class="code-sample"><code>$ cd /home/odl/
$ cp local.conf.compute devstack/local.conf
$ cd devstack
$ vi local.conf</code></pre>

Edit the local.conf you just copied with the appropriate IPs in the devstack directory on the compute host like the following example with your controller and compute host IPs:

<pre class="code-sample"><code>[[local|localrc]]
LOGFILE=stack.sh.log
#LOG_COLOR=False
#SCREEN_LOGDIR=/opt/stack/data/log
OFFLINE=true
#RECLONE=yes

disable_all_services
enable_service neutron nova n-cpu quantum n-novnc qpid

HOST_NAME=fedora-odl-2
HOST_IP=172.16.86.128
SERVICE_HOST_NAME=fedora-odl-1
SERVICE_HOST=172.16.86.129
VNCSERVER_PROXYCLIENT_ADDRESS=172.16.86.128
VNCSERVER_LISTEN=0.0.0.0

FLOATING_RANGE=192.168.210.0/24

NEUTRON_REPO=https://github.com/CiscoSystems/neutron.git
NEUTRON_BRANCH=odl_ml2
Q_PLUGIN=ml2
Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight,linuxbridge
ENABLE_TENANT_TUNNELS=True
Q_HOST=$SERVICE_HOST

MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
RABBIT_PASSWORD=rabbit
QPID_PASSWORD=rabbit
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin

[[post-config|/etc/neutron/plugins/ml2/ml2_conf.ini]]
[agent]
minimize_polling=True

[ml2_odl]
url=http://172.16.86.129:8080/controller/nb/v2/neutron
username=admin
password=admin</code></pre>

Or check the conf file quickly by grepping it.

<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ grep 172 local.conf
HOST_IP=172.16.86.128
SERVICE_HOST=172.16.86.129
VNCSERVER_PROXYCLIENT_ADDRESS=172.16.86.128
url=http://172.16.86.129:8080/controller/nb/v2/neutron</code></pre>

And now stack the compute host:
<pre class="code-sample"><code>$ ./stack.sh </code></pre>

Once you get the stack working SNAPSHOT the image :-) If you break a fraction of the things that I do, when I touch them snapshots can be a handy timesaver. Also leaving DevStack "offline=true" and "reclone=no" except for when you need to pull a patch. Get to your functioning stack and it is rock solid and incredibly useful and necessary in my experience. I would say we merry few consumed by this project are laser focused on simplification, not dragging along every use case under the sun starting out. Lets do the basics right and well while we have the chance.

The state of OVS after the stack should be the following:

<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ sudo ovs-vsctl show
17074e89-2ac5-4bba-997a-1a5a3527cf56
Manager "tcp:172.16.86.129:6640"
is_connected: true
Bridge br-int
Controller "tcp:172.16.86.129:6633"
is_connected: true
fail_mode: secure
Port br-int
Interface br-int
ovs_version: "2.0.0"</code></pre>

Next up, verify functionality.
<h2 class="legacy-heading"> Verifying OpenStack is Functioning </h2>

Verify the stack with the following on either host. First we will list that there are two KVM hypervisors registered with Nova. *Note openrc will populate the proper Keystone credentials for service client commands. These can be viewed using the export command from your shell:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ . ./openrc admin admin
[odl@fedora-odl-1 devstack]$ nova hypervisor-list
+----+---------------------+
| ID | Hypervisor hostname |
+----+---------------------+
| 1 | fedora-odl-1 |
| 2 | fedora-odl-2 |
+----+---------------------+</code></pre>

Before we can boot VM instances, there is one more minor configuration difference between the Fed19 and Fed20 VM.

If you are using the Fedora 19 VM,

<pre class="code-sample"><code>~/devstack/addimage.sh
export IMAGE=cirros-0.3.0-i386-disk.img
</code></pre>

If you are using Fedora 20 VM,

<pre class="code-sample"><code>
export IMAGE=cirros-0.3.1-x86_64-uec
</code></pre>

Next lets boot a couple of VMs and verify the network overlay is created by ODL/OVSDB. There are lots of ways to boot a VM but what we tend to use is the following one liner. We are going to boot off the default private network that was setup by Devstack:

<pre class="code-sample"><code>nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep private | awk '{print $2}') admin-private1</code></pre>

Boot a second node:
<pre class="code-sample"><code>nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep private | awk '{print $2}') admin-private2</code></pre>

You can also force a host to boot to a particular hypervisor using the following (note: this requires an admin role which is implicitly granted to the admin user):

<pre class="code-sample"><code>nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep private | awk '{print $2}') demo-private --availability_zone=nova:fedora-odl-1</code></pre>

View the state of the VMs with the following:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ nova list
+--------------------------------------+----------------+--------+------------+-------------+------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+----------------+--------+------------+-------------+------------------+
| 01c30219-255a-4376-867a-45d52e349e87 | admin-private1 | ACTIVE | - | Running | private=10.0.0.2 |
| bdcfd05b-ebaf-452d-b8c8-81f391a0bb75 | admin-private2 | ACTIVE | - | Running | private=10.0.0.4 |
+--------------------------------------+----------------+--------+------------+-------------+------------------+</code></pre>

You can also look directly at Libvirt using Virsh. This is handy for determining where a host is located:
<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ sudo virsh list
Id Name State
----------------------------------------------------
2 instance-00000002 running</code></pre>

From here lets make sure we can ping the endpoints. For this I just use the shell by grabbing a namespace for qdhcp or qrouter. This provides an L3 source to ping the VMs. These will only exist on the controller or wherever you are running those services in your cloud:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ ip netns
qdhcp-3f0cfbd2-f23c-481a-8698-3b2dcb7c2657
qrouter-992e450a-875c-4721-9c82-606c283d4f92
[odl@fedora-odl-1 devstack]$ sudo ip netns exec qdhcp-3f0cfbd2-f23c-481a-8698-3b2dcb7c2657 ping 10.0.0.2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.737 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.578 ms
^C
--- 10.0.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.578/0.657/0.737/0.083 ms
[odl@fedora-odl-1 devstack]$ sudo ip netns exec qdhcp-3f0cfbd2-f23c-481a-8698-3b2dcb7c2657 ping 10.0.0.4
PING 10.0.0.4 (10.0.0.4) 56(84) bytes of data.
64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=2.02 ms
64 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=1.03 ms
^C
--- 10.0.0.4 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.037/1.530/2.023/0.493 ms</code></pre>

Verify the OF13 flowmods short for "flow modifications", or also referred to as "flow rules", "flow tables", "forwarding tables" or whatever you think it should be called.

<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ sudo ovs-ofctl -O OpenFlow13 dump-flows br-int
OFPST_FLOW reply (OF1.3) (xid=0x2):
cookie=0x0, duration=2044.758s, table=0, n_packets=23, n_bytes=2292, send_flow_rem in_port=2,dl_src=fa:16:3e:f5:03:2e actions=set_field:0x1-&gt;tun_id,goto_table:10
cookie=0x0, duration=2051.364s, table=0, n_packets=30, n_bytes=3336, send_flow_rem tun_id=0x1,in_port=1 actions=goto_table:20
cookie=0x0, duration=2049.553s, table=0, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x2,in_port=1 actions=goto_table:20
cookie=0x0, duration=2044.724s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=2 actions=drop
cookie=0x0, duration=2576.478s, table=0, n_packets=410, n_bytes=36490, send_flow_rem dl_type=0x88cc actions=CONTROLLER:56
cookie=0x0, duration=2044.578s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x1 actions=goto_table:20
cookie=0x0, duration=2051.322s, table=10, n_packets=10, n_bytes=1208, send_flow_rem priority=16384,tun_id=0x1,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1,goto_table:20
cookie=0x0, duration=2049.477s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=16384,tun_id=0x2,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1,goto_table:20
cookie=0x0, duration=2050.621s, table=10, n_packets=11, n_bytes=944, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:00:c4:97 actions=output:1,goto_table:20
cookie=0x0, duration=2049.641s, table=10, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x2,dl_dst=fa:16:3e:c6:00:e1 actions=output:1,goto_table:20
cookie=0x0, duration=2051.415s, table=10, n_packets=2, n_bytes=140, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:f7:3d:96 actions=output:1,goto_table:20
cookie=0x0, duration=2048.058s, table=10, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:e1:a7:e1 actions=output:1,goto_table:20
cookie=0x0, duration=2044.517s, table=20, n_packets=13, n_bytes=1084, send_flow_rem priority=8192,tun_id=0x1 actions=drop
cookie=0x0, duration=2044.608s, table=20, n_packets=21, n_bytes=2486, send_flow_rem priority=16384,tun_id=0x1,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:2
cookie=0x0, duration=2044.666s, table=20, n_packets=17, n_bytes=1898, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:f5:03:2e actions=output:2</code></pre>
You can also define new networks with encaps of <a href="http://blog.scottlowe.org/tag/vxlan/" target="_blank">VXLAN</a> or <a href="http://blog.ipspace.net/search?q=gre&x=-987&y=-197" target="_blank">GRE</a> along with specifying the segmentation ID. In this case GRE:

<pre class="code-sample"><code>neutron net-create gre1 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type gre --provider:segmentation_id 1300
neutron subnet-create gre1 10.200.1.0/24 --name gre1</code></pre>

<pre class="code-sample"><code>neutron net-create gre2 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type gre --provider:segmentation_id 1310
neutron subnet-create gre2 10.200.2.0/24 --name gre2</code></pre>

And then boot those instances using those networks:

<pre class="code-sample"><code>nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep 'gre1' | awk '{print $2}') gre1-host
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep 'gre2' | awk '{print $2}') gre2-host</code></pre>
<h2 class="legacy-heading"> Create Multi Network Types, Gre and VXLAN </h2>

Suppose we want to create some hosts in an overlay using the VXLAN encap with specified segmentation IDs (VNIs):

<pre class="code-sample"><code>neutron net-create vxlan-net1 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type vxlan --provider:segmentation_id 1600
neutron subnet-create vxlan-net1 10.100.1.0/24 --name vxlan-net1

neutron net-create vxlan-net2 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type vxlan --provider:segmentation_id 1601
neutron subnet-create vxlan-net2 10.100.2.0/24 --name vxlan-net2

neutron net-create vxlan-net3 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type vxlan --provider:segmentation_id 1603
neutron subnet-create vxlan-net3 10.100.3.0/24 --name vxlan-net3 </code></pre>

Next take a look at the networks which were just created.

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ neutron net-list
+--------------------------------------+------------+-------------------------------------------------------+
| id | name | subnets |
+--------------------------------------+------------+-------------------------------------------------------+
| 03e3f964-8bc8-48fa-b4c9-9b8390f37b93 | private | b06d716b-527f-4da2-adda-5fc362456d34 10.0.0.0/24 |
| 4eaf08d3-2234-4632-b1e7-d11704b1238a | vxlan-net2 | b54c30fd-e157-4935-b9c2-cefa145162a8 10.100.2.0/24 |
| af8aa29d-a302-4ecf-a0b1-e52ff9c10b63 | vxlan-net1 | c44f9bee-adca-4bca-a197-165d545bcef9 10.100.1.0/24 |
| e6f3c605-6c0b-4f7d-a64f-6e593c5e647a | vxlan-net3 | 640cf2d1-b470-41dd-a4d8-193d705ea73e 10.100.3.0/24 |
| f6aede62-67a5-4fe6-ad61-2c1a88b08874 | public | 1e945d93-caeb-4890-8b58-ed00297a7f03 192.168.210.0/24 |
+--------------------------------------+------------+-------------------------------------------------------+ </code></pre>

Now boot the VMS

<pre class="code-sample"><code>nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep vxlan-net1 | awk '{print $2}') vxlan-host1 --availability_zone=nova:fedora-odl-2

nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep vxlan-net2 | awk '{print $2}') vxlan-host2 --availability_zone=nova:fedora-odl-2

nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep vxlan-net2 | awk '{print $2}') vxlan-host3 --availability_zone=nova:fedora-odl-2 </code></pre>

You can pull up the Horizon UI and take a look at the nodes you have spun up by pointing your web browser at the controller IP (port 80).

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2014/02/Horizon-OpenDaylight-e1392513990486.jpg" >}}" alt="GRE/VXLAN Overlays in OpenStack Horizon"></figure>

Now lets ping one of the hosts we just created to verify it is functional:

<pre class="code-sample"><code> [odl@fedora-odl-1 devstack]$ ip netns
qdhcp-4eaf08d3-2234-4632-b1e7-d11704b1238a
qdhcp-af8aa29d-a302-4ecf-a0b1-e52ff9c10b63
qrouter-bed7005f-4c51-4c3a-b23b-3830b5e7663a
[odl@fedora-odl-1 devstack]$ nova list
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+
| f34ed046-5daf-42f5-9b2c-644f5ab6b2bc | vxlan-host1 | ACTIVE | - | Running | vxlan-net1=10.100.1.2 |
| 6b65d0f2-c621-4dc5-87ca-82a2c44734b2 | vxlan-host2 | ACTIVE | - | Running | vxlan-net2=10.100.2.2 |
| f3d5179a-e974-4eb4-984b-399d1858ab76 | vxlan-host3 | ACTIVE | - | Running | vxlan-net2=10.100.2.4 |
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+
[odl@fedora-odl-1 devstack]$ sudo ip netns exec qdhcp-af8aa29d-a302-4ecf-a0b1-e52ff9c10b63 ping 10.100.1.2
PING 10.100.1.2 (10.100.1.2) 56(84) bytes of data.
64 bytes from 10.100.1.2: icmp_seq=1 ttl=64 time=2.63 ms
64 bytes from 10.100.1.2: icmp_seq=2 ttl=64 time=1.15 ms
^C
--- 10.100.1.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.151/1.892/2.633/0.741 ms </code></pre>

Now create three new Neutron networks using the GRE encapsulation. Depending on your VM memory you can always run the risk of blowing up your VM with too many guest VMs.

<pre class="code-sample"><code>### Create the Networks and corresponding Subnets ###
neutron net-create gre-net1 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type gre --provider:segmentation_id 1700
neutron subnet-create gre-net1 10.100.1.0/24 --name gre-net1

neutron net-create gre-net2 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type gre --provider:segmentation_id 1701
neutron subnet-create gre-net2 10.100.2.0/24 --name gre-net2

neutron net-create gre-net3 --tenant_id $(keystone tenant-list | grep '\sadmin' | awk '{print $2}') --provider:network_type gre --provider:segmentation_id 1703
neutron subnet-create gre-net3 10.100.3.0/24 --name gre-net3</code></pre>

<pre class="code-sample"><code>### Boot the VMs ###

nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep gre-net1 | awk '{print $2}') gre-host1 --availability_zone=nova:fedora-odl-2

nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep gre-net2 | awk '{print $2}') gre-host2 --availability_zone=nova:fedora-odl-2

nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep gre-net2 | awk '{print $2}') gre-host3 --availability_zone=nova:fedora-odl-2</code></pre>

Here is what the OVS config looks like. Remember, since the tunnel ID is being set using the OpenFlow OXM metadata field to to set the logical port OFPXMT_OFB_TUNNEL_ID implemented in OpenFlow v1.3.

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ nova list
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+
| 8db56e44-36db-4447-aeb9-e6679ca420b6 | gre-host1 | ACTIVE | - | Running | gre-net1=10.100.1.2 |
| 36fec86d-d9e6-462c-a686-f3c0929a2c21 | gre-host2 | ACTIVE | - | Running | gre-net2=10.100.2.2 |
| 67d97a8e-ecd3-4913-886c-423170ef3635 | gre-host3 | ACTIVE | - | Running | gre-net2=10.100.2.4 |
| f34ed046-5daf-42f5-9b2c-644f5ab6b2bc | vxlan-host1 | ACTIVE | - | Running | vxlan-net1=10.100.1.2 |
| 6b65d0f2-c621-4dc5-87ca-82a2c44734b2 | vxlan-host2 | ACTIVE | - | Running | vxlan-net2=10.100.2.2 |
| f3d5179a-e974-4eb4-984b-399d1858ab76 | vxlan-host3 | ACTIVE | - | Running | vxlan-net2=10.100.2.4 |
+--------------------------------------+-------------+--------+------------+-------------+-----------------------+</code></pre>

Neutron mappings from the Neutron client output:

<pre class="code-sample"><code>[odl@fedora-odl-1 devstack]$ neutron net-list
+--------------------------------------+------------+-------------------------------------------------------+
| id | name | subnets |
+--------------------------------------+------------+-------------------------------------------------------+
| 03e3f964-8bc8-48fa-b4c9-9b8390f37b93 | private | b06d716b-527f-4da2-adda-5fc362456d34 10.0.0.0/24 |
| 4eaf08d3-2234-4632-b1e7-d11704b1238a | vxlan-net2 | b54c30fd-e157-4935-b9c2-cefa145162a8 10.100.2.0/24 |
| a33c5794-3830-4220-8724-95752d8f94bd | gre-net1 | d32c8a70-70c6-4bdc-b741-af718b3ba4cd 10.100.1.0/24 |
| af8aa29d-a302-4ecf-a0b1-e52ff9c10b63 | vxlan-net1 | c44f9bee-adca-4bca-a197-165d545bcef9 10.100.1.0/24 |
| e6f3c605-6c0b-4f7d-a64f-6e593c5e647a | vxlan-net3 | 640cf2d1-b470-41dd-a4d8-193d705ea73e 10.100.3.0/24 |
| f6aede62-67a5-4fe6-ad61-2c1a88b08874 | public | 1e945d93-caeb-4890-8b58-ed00297a7f03 192.168.210.0/24 |
| fa44d171-4935-4fae-9507-0ecf2d521b49 | gre-net2 | f8151c73-cda4-47e4-bf7c-8a73a7b4ef5f 10.100.2.0/24 |
| ffc7da40-8252-4cdf-a9a2-d538f4986215 | gre-net3 | 146931d8-9146-4abf-9957-d6a8a3db43e4 10.100.3.0/24 |
+--------------------------------------+------------+-------------------------------------------------------+</code></pre>

Next take a look at the Open vSwitch configuration. Worthy of note is the tunnel IPv4 src/dest endpoints are defined using OVSDB but the Tunnel ID is set using the flowmod in OpenFlow using key=flow. This tells OVSDB to look for the tunnel ID in the flowmod. There is also a similar concept for IPv4 tunnel source/destination using Nicira extensions with NXM_NX_TUN_IPV4_SRC and NXM_NX_TUN_IPV4_DST that was implemented in OVS 2.0. The NXM code points are referenced in the OF v1.3 specification but it seems pretty nascent wether the ONF is looking to handle tunnel operations with OF-Config or via flowmods such as the NXM references. The NXM code points are defined the ODL openflowjava project that implements the library model for OFv1.3 and would just need to be plumbed through the MD-SAL convertor.

<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ sudo ovs-vsctl show
17074e89-2ac5-4bba-997a-1a5a3527cf56
Manager "tcp:172.16.86.129:6640"
is_connected: true
Bridge br-int
Controller "tcp:172.16.86.129:6633"
is_connected: true
fail_mode: secure
Port "tap8b31df39-d4"
Interface "tap8b31df39-d4"
Port br-int
Interface br-int
Port "gre-172.16.86.129"
Interface "gre-172.16.86.129"
type: gre
options: {key=flow, local_ip="172.16.86.128", remote_ip="172.16.86.129"}
ovs_version: "2.0.0"</code></pre>

And then the OF v1.3 flowmods:

<pre class="code-sample"><code>[odl@fedora-odl-2 devstack]$ sudo ovs-ofctl -O OpenFlow13 dump-flows br-int
OFPST_FLOW reply (OF1.3) (xid=0x2):
cookie=0x0, duration=2415.341s, table=0, n_packets=30, n_bytes=2586, send_flow_rem in_port=4,dl_src=fa:16:3e:1a:49:61 actions=set_field:0x641-&gt;tun_id,goto_table:10
cookie=0x0, duration=2425.095s, table=0, n_packets=39, n_bytes=3300, send_flow_rem in_port=2,dl_src=fa:16:3e:93:20:1e actions=set_field:0x640-&gt;tun_id,goto_table:10
cookie=0x0, duration=2415.981s, table=0, n_packets=37, n_bytes=2880, send_flow_rem in_port=5,dl_src=fa:16:3e:02:28:8d actions=set_field:0x641-&gt;tun_id,goto_table:10
cookie=0x0, duration=877.732s, table=0, n_packets=27, n_bytes=2348, send_flow_rem in_port=6,dl_src=fa:16:3e:20:cd:8e actions=set_field:0x6a4-&gt;tun_id,goto_table:10
cookie=0x0, duration=878.981s, table=0, n_packets=31, n_bytes=2908, send_flow_rem in_port=7,dl_src=fa:16:3e:86:08:5f actions=set_field:0x6a5-&gt;tun_id,goto_table:10
cookie=0x0, duration=882.297s, table=0, n_packets=32, n_bytes=2670, send_flow_rem in_port=8,dl_src=fa:16:3e:68:40:4a actions=set_field:0x6a5-&gt;tun_id,goto_table:10
cookie=0x0, duration=884.983s, table=0, n_packets=16, n_bytes=1888, send_flow_rem tun_id=0x6a4,in_port=3 actions=goto_table:20
cookie=0x0, duration=2429.719s, table=0, n_packets=33, n_bytes=3262, send_flow_rem tun_id=0x640,in_port=1 actions=goto_table:20
cookie=0x0, duration=881.723s, table=0, n_packets=29, n_bytes=3551, send_flow_rem tun_id=0x6a5,in_port=3 actions=goto_table:20
cookie=0x0, duration=2418.434s, table=0, n_packets=33, n_bytes=3866, send_flow_rem tun_id=0x641,in_port=1 actions=goto_table:20
cookie=0x0, duration=2426.048s, table=0, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x2,in_port=3 actions=goto_table:20
cookie=0x0, duration=2428.34s, table=0, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x1,in_port=3 actions=goto_table:20
cookie=0x0, duration=878.961s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=7 actions=drop
cookie=0x0, duration=882.211s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=8 actions=drop
cookie=0x0, duration=877.562s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=6 actions=drop
cookie=0x0, duration=2415.941s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=5 actions=drop
cookie=0x0, duration=2415.249s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=4 actions=drop
cookie=0x0, duration=2425.04s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=8192,in_port=2 actions=drop
cookie=0x0, duration=2711.147s, table=0, n_packets=970, n_bytes=88270, send_flow_rem dl_type=0x88cc actions=CONTROLLER:56
cookie=0x0, duration=873.508s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=1,in_port=3,dl_dst=00:00:00:00:00:00 actions=output:1
cookie=0x0, duration=873.508s, table=0, n_packets=0, n_bytes=0, send_flow_rem priority=1,in_port=1,dl_dst=00:00:00:00:00:00 actions=output:1
cookie=0x0, duration=877.224s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x6a4 actions=goto_table:20
cookie=0x0, duration=2415.783s, table=10, n_packets=7, n_bytes=294, send_flow_rem priority=8192,tun_id=0x641 actions=goto_table:20
cookie=0x0, duration=881.907s, table=10, n_packets=3, n_bytes=169, send_flow_rem priority=8192,tun_id=0x6a5 actions=goto_table:20
cookie=0x0, duration=2424.811s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=8192,tun_id=0x640 actions=goto_table:20
cookie=0x0, duration=881.623s, table=10, n_packets=37, n_bytes=3410, send_flow_rem priority=16384,tun_id=0x6a5,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:3,goto_table:20
cookie=0x0, duration=2429.661s, table=10, n_packets=18, n_bytes=1544, send_flow_rem priority=16384,tun_id=0x640,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1,goto_table:20
cookie=0x0, duration=2418.33s, table=10, n_packets=36, n_bytes=3088, send_flow_rem priority=16384,tun_id=0x641,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:1,goto_table:20
cookie=0x0, duration=2428.227s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=16384,tun_id=0x1,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:3,goto_table:20
cookie=0x0, duration=884.854s, table=10, n_packets=15, n_bytes=1306, send_flow_rem priority=16384,tun_id=0x6a4,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:3,goto_table:20
cookie=0x0, duration=2425.966s, table=10, n_packets=0, n_bytes=0, send_flow_rem priority=16384,tun_id=0x2,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:3,goto_table:20
cookie=0x0, duration=885.097s, table=10, n_packets=12, n_bytes=1042, send_flow_rem tun_id=0x6a4,dl_dst=fa:16:3e:5d:3d:cd actions=output:3,goto_table:20
cookie=0x0, duration=2426.083s, table=10, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x2,dl_dst=fa:16:3e:fa:77:36 actions=output:3,goto_table:20
cookie=0x0, duration=2429.782s, table=10, n_packets=21, n_bytes=1756, send_flow_rem tun_id=0x640,dl_dst=fa:16:3e:f8:d0:96 actions=output:1,goto_table:20
cookie=0x0, duration=873.509s, table=10, n_packets=23, n_bytes=1999, send_flow_rem tun_id=0x6a5,dl_dst=fa:16:3e:21:eb:65 actions=output:3,goto_table:20
cookie=0x0, duration=2418.518s, table=10, n_packets=24, n_bytes=2084, send_flow_rem tun_id=0x641,dl_dst=fa:16:3e:9b:c1:c7 actions=output:1,goto_table:20
cookie=0x0, duration=2428.443s, table=10, n_packets=0, n_bytes=0, send_flow_rem tun_id=0x1,dl_dst=fa:16:3e:ea:1d:9d actions=output:3,goto_table:20
cookie=0x0, duration=877.119s, table=20, n_packets=12, n_bytes=1042, send_flow_rem priority=8192,tun_id=0x6a4 actions=drop
cookie=0x0, duration=2415.73s, table=20, n_packets=31, n_bytes=2378, send_flow_rem priority=8192,tun_id=0x641 actions=drop
cookie=0x0, duration=881.815s, table=20, n_packets=26, n_bytes=2168, send_flow_rem priority=8192,tun_id=0x6a5 actions=drop
cookie=0x0, duration=2424.74s, table=20, n_packets=21, n_bytes=1756, send_flow_rem priority=8192,tun_id=0x640 actions=drop
cookie=0x0, duration=882.005s, table=20, n_packets=37, n_bytes=3410, priority=16384,tun_id=0x6a5,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:8,output:7
cookie=0x0, duration=2424.884s, table=20, n_packets=22, n_bytes=1864, send_flow_rem priority=16384,tun_id=0x640,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:2
cookie=0x0, duration=2415.83s, table=20, n_packets=38, n_bytes=3228, send_flow_rem priority=16384,tun_id=0x641,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:5,output:4
cookie=0x0, duration=877.333s, table=20, n_packets=15, n_bytes=1306, send_flow_rem priority=16384,tun_id=0x6a4,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=output:6
cookie=0x0, duration=878.799s, table=20, n_packets=15, n_bytes=1818, send_flow_rem tun_id=0x6a5,dl_dst=fa:16:3e:86:08:5f actions=output:7
cookie=0x0, duration=2415.884s, table=20, n_packets=15, n_bytes=1818, send_flow_rem tun_id=0x641,dl_dst=fa:16:3e:02:28:8d actions=output:5
cookie=0x0, duration=877.468s, table=20, n_packets=15, n_bytes=1818, send_flow_rem tun_id=0x6a4,dl_dst=fa:16:3e:20:cd:8e actions=output:6
cookie=0x0, duration=882.102s, table=20, n_packets=14, n_bytes=1733, send_flow_rem tun_id=0x6a5,dl_dst=fa:16:3e:68:40:4a actions=output:8
cookie=0x0, duration=2415.171s, table=20, n_packets=15, n_bytes=1818, send_flow_rem tun_id=0x641,dl_dst=fa:16:3e:1a:49:61 actions=output:4
cookie=0x0, duration=2424.998s, table=20, n_packets=24, n_bytes=2532, send_flow_rem tun_id=0x640,dl_dst=fa:16:3e:93:20:1e actions=output:2</code></pre>

For more on TEPs please see a nice document authored by Ben Pfaff who needs no introduction, that can be found <a href="http://benpfaff.org/~blp/ovs-fields.pdf" target="_blank">here</a>.

Next take a look at the flowmods. We simply break the pipeline into three tables, a classifier, egress and ingress. Over the next 6 months we will be adding services into pipeline for a much more complete implementation. We are looking for user contributions in the roadmap and even better, pushing code upstream as the project continues to grow.

Lastly if you want to force availability zones from say the "demo" UID. You can add the admin role to different UIDs using the following Keystone client calls.

<pre class="code-sample"><code>$ keystone user-role-add --user $(keystone user-list | grep '\sdemo' | awk '{print $2}') \
--role $(keystone role-list | grep 'admin' | awk '{print $2}') \
--tenant_id $(keystone tenant-list | grep '\sdemo' | awk '{print $2}')
$ . ./openrc demo demo </code></pre>
<h2 class="legacy-heading"> Unstack and Cleanup DevStack </h2>

Getting used to this setup will take trial and error. Use the following to teardown the stack and reset the state of the VM to pre-stack.

running unstack.sh will kill the stack. It doesn't hurt to look at the OVS config and make sure all bridges have been deleted:
<pre class="code-sample"><code>sudo ovs-vsctl show</code></pre>

A slightly lame cleanup, but handy nonetheless, is to run a few commands to ensure the stack was effectively torn down. Paste the following to create a shell script called ./reallyunstack.sh. Madhu and I always laugh about this one but it can help level set the platform for debugging:

<pre class="code-sample"><code>echo 'sudo killall nova-api nova-conductor nova-cert nova-scheduler nova-consoleauth nova-compute
sudo pkill -9 -f qemu
sudo ovs-vsctl del-manager
sudo ovs-vsctl del-br br-int
sudo ovs-vsctl del-br br-tun
sudo pkill /usr/bin/python
sudo systemctl restart qpidd.service ' &gt; reallyunstack.sh
chmod +x reallyunstack.sh
./reallyunstack.sh</code></pre>

Thats all for now. I am on my way back from the OpenDaylight Summit and have to catch a redeye. My cycles are a wreck at the moment for keeping up with comments so if you have any issues that require attention please shoot them to the ovsdb-dev listserv at OpenDaylight or even better jumping on the irc channel located at #opendaylight-ovsdb on irc.freenode.net. We are driving hard over the next few months for the next release so please be patient with bugs and lack of cycles at times. Cloud infrastructures are complex, troubleshooting is the best way to learn the various frameworks. Hopefully more will get to hacking and join the community to help grow the project and one another. Concrete is what matters now. Plenty of time for talk later.

Thanks much to the relentless work from the key guys on the coding and integration effort:

<ul>
	<li>Madhu Venugopal (Red Hat)<a href="https://twitter.com/MadhuVenugopal" target="_blank">@MadhuVenugopal</a></li>
	<li>Kyle Mestery <a href="https://twitter.com/mestery" target="_blank">@mestery</a> (Cisco)</li>
	<li>(Ryan Moats (IBM) if he would ever get on Twitterz ehem :_)</li>
</ul>


Thanks to all the folks who contributed and certainly give a follow to some of the guys on Twitters that either directly or indirectly (out of time to list them all) in making this happen like (Cisco) <a href="https://twitter.com/kernelcdub" target="_blank">@kernelcdub</a> (Red Hat) <a href="https://twitter.com/dave_tucker" target="_blank">@dave_tucker</a> (HP) <a href="https://twitter.com/edwarnicke" target="_blank">@edwarnicke</a> (Cisco), <a href="https://twitter.com/ArvindSomya" target="_blank">Arvind</a> (Cisco) <a href="https://twitter.com/FlorianOtel" target="_blank">@FlorianOtel</a> (HP) <a href="https://twitter.com/ashw7n" target="_blank">@ashw7n</a> <a href="https://twitter.com/evanzeller" target="_blank"> @evanzeller</a> <a href="https://twitter.com/alagalah" target="_blank">@alagalah</a> (Nexusis), Bachman, Meo, Hague, DMM, Anees, Dixon, phrobb and of course thanks to the creators of OVS <a href="https://twitter.com/martin_casado" target="_blank">@mcasado</a> and <a href="https://twitter.com/Ben_Pfaff" target="_blank">@Ben_Pfaff</a> and the rest of the OVS team which without we would not be able to do a project such as this.

Thanks for stopping by!