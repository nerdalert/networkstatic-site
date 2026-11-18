+++
title = "Installing OpenStack ML2 Neutron Plugin with DevStack on Fedora"
date = "2013-11-26T09:27:02+00:00"
lastmod = "2014-02-18T03:00:24+00:00"
author = "Brent Salisbury"
wp_id = 7090
categories = ["In the Lab"]
tags = ["OpenDaylight", "OpenStack", "RedHat", "Software Defined Network"]
description = ""
url = "/installing-openstack-ml2-neutron-plugin-devstack-fedora/"
image = "/wp-content/uploads/2013/11/openstack-logo.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c09845f5f0d4746aeb7bab44f73fb95af7445a03ee44e4ef22fb67b69f27221e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Installing OpenStack ML2 Neutron Plugin with DevStack on Fedora </h2>
OpenStack networking is tricky. This is primarily because programmable distributed systems are relatively new beyond the rigid L2/L3 control protocols we have used for the past 20 years. What I am consistently impressed with about OpenStack networking is the innovative network services that systems programmers are developing using APIs and virtual switching. Of course most vendors have a plugin for their hardware but service instantiation in the hypervisor endpoint is relatively easy since these are open systems with compute scale.

My comrades and I that are working on the OVSDB implementation in the OpenDaylight project have needed to get up to speed on the OpenStack Neutron ML2 (Modular Layer 2) plugin to begin integration. OVSDB in OpenDaylight enables us to implement an agent-less/driver-less OpenStack/OpenDaylight integration using OVSDB for topology provisioning and OpenFlow for forwarding control and service insertion. We are fortunate to have our friend and OVSDB committer <a href="http://www.siliconloons.com" target="_blank">Kyle Mestery</a> who is also on the core Neutron team to assist on the ML2 integration front.
<h2>Brief ML2 Neutron Overview </h2>
The ML2 GRE overlay implementation proactively provisions tenant tunnels with ini files on the compute nodes that provides each OVS a list of VTEPs. The OVS instances build TEPs to each compute hosts along with endpoint(s) with an external bridge (br-ex) to drain traffic into the native underlay. From a control perspective <a href="{{< relurl "/openflow-proactive-vs-reactive-flows/" >}}" target="_blank">proactive flow rules</a> are pushed for each segmentation ID into an OVS table. For more information on Open vSwitch check the FAQ. <a href="https://twitter.com/Ben_Pfaff" target="_blank">Ben Pfaff</a> and team do an awesome job documenting and the <a href="http://openvswitch.org/mlists/" target="_blank">listserv</a> has about every answer you need archived.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/11/under-the-hood-scenario-1-ovs-compute.jpeg" >}}" alt=""></figure>

When Nova requests a compute node, Libvirt will provision the post by calling OVS using the ovs-vsctl client and Neutron requests the provider network and allocates a provider segmentation ID which is used for a GRE key or VXLAN VNI for tenant isolation. The provider network type is simply the overlay encapsulation in this case (GRE). It also provides the tenants device_id, network_id, tenant_id, IP addr, MAC addr to name a few important fields. Neutron ML2 API calls to a plugin are currently unidirectional currently, but I think this can improve over time.
<h2>Git Devstack</h2>
For first time DevStackers, this is very doable but is not quite easy mode and may require some Googling to troubleshoot (best way to learn, break and rebuild). Also, this is all subject to change as projects are architectures do so also.

<aside class="legacy-callout">
<ul>
	<li>FYI, there appears to be a packaging bug when installing the Fedora using the LiveCD with Open vSwitch 1.11. The symptom is that the OVS_GRE</li>
</ul>
[brent@fedora1 devstack]$ lsmod | grep openvswitch
openvswitch 66519 0
<strong>gre </strong> <strong>18216 1 openvswitch</strong>

[brent@fedora1 devstack]$ modinfo gre
filename: /lib/modules/3.11.7-200.fc19.x86_64.debug/kernel/net/ipv4/gre.ko
<ul>
	<li>The easiest workaround is to install Fedora using the Net-Install Fedora image (317 MB) found here: <a href="http://dl.fedoraproject.org/pub/fedora/linux/releases/19/Fedora/x86_64/iso/" target="_blank">Download Fedora-19-x86_64-netinst.iso</a></li>
	<li>Thats it, just make sure you use the net install disk. I didn't see a bug so will file one shortly. If you have had success with an image maybe save someone else the problems and pop your success below if you have a moment to share.</aside></li>
</ul>
There is no warranty with this post and guaranteed to have an exceedingly short half-life. There are far too many moving parts to not require some troubleshooting. I tend to do a snapshot of the vanilla OS due to my ability to ruin a machine from time to time and it saves the OS rebuild time.

I ran into a dbus services <a href="https://bugzilla.redhat.com/show_bug.cgi?id=974811">bug</a> with an error of the following:

<pre class="code-sample"><code> Activation via systemd failed for unit 'dbus-org.freedesktop.nm-dispatcher.service': Unit dbus-org.freedesktop.nm-dispatcher.service failed to load: No such file or directory. See system logs and 'systemctl status dbus-org.freedesktop.nm-dispatcher.service' for details.
Dec  4 03:33:52 fedora1 NetworkManager[7498]: <warn> Dispatcher failed: (32) Unit dbus-org.freedesktop.nm-dispatcher.service failed to load: No such file or directory. See system logs and 'systemctl status dbus-org.freedesktop.nm-dispatcher.service' for details. </code></pre>

 A symlink will workaround the bug so you may want verify you have the latest NetworkManager patches:

<pre class="code-sample"><code>sudo yum -y upgrade NetworkManager
systemctl enable NetworkManager-dispatcher.service
sudo systemctl status NetworkManager-dispatcher.service</code></pre>
If you have an existing installation from package, you can query and remove it with the following:

<pre class="code-sample"><code>rpm -qa | grep openvswitch</code></pre>
Then remove the existing. You can always upgrade but the extra step may avoid potential issues removing the kernel module:
<pre class="code-sample"><code>rpm -e openvswitch-1.11.0-1.fc19.x86_64</code></pre>

In the example local.conf configs the hosts are as follows:

<ul>
	<li>Controller : 172.16.58.139 [Fedora2] (SERVICE_HOST)</li>
	<li>Compute: 172.16.58.136 [Fedora1]</li>
</ul>

Edit the hostnames and make them resolvable via hostname to one another with vi /etc/hosts.

<pre class="code-sample"><code>git clone https://github.com/openstack-dev/devstack.git
cd devstack
vi local.conf  (Add a compute or controller local.conf config from below)
./stack.sh</code></pre>
<h2>local.conf files for DevStack on Fedora </h2>
This local.conf works on Fedora 19 for the controller host. For Fedora builds use QPID not RABBIT. I left Rabbit as there was a bug a while back but I haven't noticed issues disabling it for Fedora. There are a few unnecessary fields in the config files below. I recommend reading the script and getting to know it especially if looking to do dev or integrating other projects into OpenStack as the DevStack script greatly simplifies exchanging development environment amongst a team.

<em>DevStack local.conf Compute Node (Fedora2 - 172.16.58.139)</em>

<pre class="code-sample"><code>[[local|localrc]]
LOGFILE=stack.sh.log
SCREEN_LOGDIR=/opt/stack/data/log
LOG_COLOR=False
#OFFLINE=True
RECLONE=yes

disable_service rabbit
enable_service qpid

enable_service n-cond
disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service neutron

Q_HOST=$SERVICE_HOST
HOST_IP=172.16.58.139

Q_PLUGIN=ml2
Q_AGENT=openvswitch
Q_ML2_PLUGIN_MECHANISM_DRIVERS=openvswitch,linuxbridge,l2population
Q_ML2_TENANT_NETWORK_TYPE=gre
Q_USE_SECGROUP=True
Q_AGENT_EXTRA_AGENT_OPTS=(tunnel_types=gre)
Q_AGENT_EXTRA_SRV_OPTS=(local_ip=$HOST_IP)

VNCSERVER_PROXYCLIENT_ADDRESS=192.168.64.193
VNCSERVER_LISTEN=0.0.0.0

SERVICE_HOST_NAME=${HOST_NAME}
SERVICE_HOST=172.16.58.139

FLOATING_RANGE=192.168.100.0/24
#PUBLIC_NETWORK_GATEWAY=192.168.75.254
MYSQL_HOST=$SERVICE_HOST
#RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
QPID_PASSWORD=qpid
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin</code></pre>

<hr />

<em>DevStack local.conf Compute Node (Fedora1 - 172.16.58.136)</em>

This local.conf foes on the compute node:

<pre class="code-sample"><code>[[local|localrc]]
LOGFILE=stack.sh.log
SCREEN_LOGDIR=/opt/stack/data/log
LOG_COLOR=False
#OFFLINE=true
RECLONE=yes
disable_all_services
enable_service n-cpu quantum q-agt n-novnc qpid

HOST_IP=172.16.58.136
SERVICE_HOST_NAME=fedora2
SERVICE_HOST=172.16.58.139

FLOATING_RANGE=192.168.100.0/24

Q_PLUGIN=ml2
Q_AGENT=openvswitch
Q_ML2_PLUGIN_MECHANISM_DRIVERS=openvswitch,linuxbridge,l2population
Q_ML2_TENANT_NETWORK_TYPE=gre

Q_AGENT_EXTRA_AGENT_OPTS=(tunnel_types=gre)
Q_AGENT_EXTRA_SRV_OPTS=(local_ip=$HOST_IP)

Q_HOST=$SERVICE_HOST
MYSQL_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
QPID_PASSWORD=qpid
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin</code></pre>
<h2>Post Installation</h2>
<em>The following will get you started getting hosts booted:</em>

<pre class="code-sample"><code>### Set ENV Credentials ###
[brent@fedora1 devstack]$ . ./openrc admin admin
### Verify Nodes ###
[brent@fedora2 devstack]$ nova hypervisor-list
+----+---------------------+
| ID | Hypervisor hostname |
+----+---------------------+
| 1 | fedora1 |
| 2 | fedora2 |
+----+---------------------+
### Get the Image ID for cirros-0.3.1-x86_64-uec ###
[brent@fedora1 devstack]$ nova image-list
+--------------------------------------+---------------------------------+--------+--------+
| ID | Name | Status | Server |
+--------------------------------------+---------------------------------+--------+--------+
| 166de3dd-b52e-4d04-9237-92d063b9482a | cirros-0.3.1-x86_64-uec | ACTIVE | |
| 8a93dc1d-dcac-4ace-b2ac-9dc0038243d2 | cirros-0.3.1-x86_64-uec-kernel | ACTIVE | |
| 41d9c73a-d177-4333-8b47-dbb4209e5999 | cirros-0.3.1-x86_64-uec-ramdisk | ACTIVE | |
+--------------------------------------+---------------------------------+--------+--------+
### Get the Network ID ###
[brent@fedora1 devstack]$ nova network-list
+--------------------------------------+---------+------+
| ID | Label | Cidr |
+--------------------------------------+---------+------+
| 8f8370fe-bb5c-4fd7-b541-ec513e63e922 | public | None |
| fa56cd9f-22b2-4117-899b-85bdff4161a3 | private | None |
+--------------------------------------+---------+------+
### Boot a guest host. If you want to force the VM to the compute node to verify the overlay tunnel use --availability_zone with the admin crendentials. You need to modify the UID Demo role using Keystone if you wish to do the same with that tenant.
nova boot --flavor m1.nano --image 166de3dd-b52e-4d04-9237-92d063b9482a --nic net-id=8f8370fe-bb5c-4fd7-b541-ec513e63e922 turtles1 --availability_zone=nova:fedora1
### View the guest host ###
[brent@fedora1 devstack]$ nova list
+--------------------------------------+-----------+--------+------------+-------------+------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+-----------+--------+------------+-------------+------------------+
| 62c26e76-1d20-424c-a82d-242d85b45d42 | turtles1 | ACTIVE | None | Running | private=10.0.0.8 |
| e3fe70b7-5516-464c-96f3-923062e05173 | r2vm1 | ACTIVE | None | Running | private=10.0.0.3 |
+--------------------------------------+-----------+--------+------------+-------------+------------------+</code></pre>

I will post VXLAN/VNI configurations for just vanilla DevStack and even cooler, ODL support in the next week or so hopefully (dependency is getting OF v1.3 atm).
<h2>Additional Content: OpenStack ML2 Videos from the OpenStack Summit</h2>
Check out this great panel with some friends and rockstar leaders from the OpenDaylight project speaking at the ODL mini-summit in Hong Kong. The speakers are Chris Wright (RedHat), Anees Shaikh (IBM), Kyle Mestery (Cisco) and Stephan Baucke (Ericsson).
<h2>OpenDaylight: An Open Source SDN for Your OpenStack Cloud</h2>
<p><a href="http://www.youtube.com/watch?v=Y0P_h6INi_o">Watch video on YouTube</a></p>
<h2>A Deep Dive into the ML2 Plugin</h2>
Bob Kukura (RedHat) and Kyle Mestery (Cisco) give a great overview and dig into the critical details.

<p><a href="http://www.youtube.com/watch?v=whmcQ-vHams">Watch video on YouTube</a></p>
<h2>What Next?</h2>
Scott Shenker of UC-Berkeley and a co-founder of Nicira said network virtualization is the "killer application". If this is the case, the first application of the killer application is supporting OpenStack at scale. Nicira earned this right with the huge investment it made into the SDN reference data plane implementation of OVS. If you have not whatched Shenker's latest revision of his always impressive SDN vision be sure to make time for it.

<a href="http://www.youtube.com/watch?v=WabdXYzCAOU" target="_blank" rel="noopener noreferrer">Software-Defined Networking at the Crossroads -</a>

<figure class="legacy-figure"><a href="{{< relurl "/wp-content/uploads/2013/11/slide-cat-shark-duck1.jpeg" >}}"><img class="alignright size-full wp-image-7113" alt="slide-cat-shark-duck" src="{{< relurl "/wp-content/uploads/2013/11/slide-cat-shark-duck1.jpeg" >}}" width="300" height="225" /></a></figure>
I could go on for days but time is unfortunately not on my side with day job in a couple of hours. Not to mention the all-star <a href="https://twitter.com/MadhuVenugopal" target="_blank">Madhu's</a> Roomba just went off on the Hangout we are on which is the 4AM nightly alarm and always hilarious sounding. We will demo and post instructions for ODL/Neutron plugin in the next few days. We are waiting on OF v1.3 to finish so we can get multi-table support *cough* *hint* *hint* Ed :-) OFv1.3 will avoid a full mesh tunnel overlay per tenant/network. In the meantime, take a look ML2 using DevStack. I am really impressed at the thought that went into putting it together. It has limitations obviously but I think in the near term, SDN controllers and hardware w/vTEP capabilities will alleviate a lot of the OpenStack networking pain and abstract the overlay complex state of hacking networks today.