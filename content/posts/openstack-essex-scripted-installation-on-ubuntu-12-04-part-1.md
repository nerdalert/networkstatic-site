+++
title = "OpenStack Essex Scripted Installation on Ubuntu 12.04 (Part 1)"
date = "2012-04-23T03:09:36+00:00"
lastmod = "2013-07-30T04:36:44+00:00"
author = "Brent Salisbury"
wp_id = 450
categories = ["In the Lab"]
tags = ["OpenStack", "Tutorials"]
description = ""
url = "/openstack-essex-scripted-installation-on-ubuntu-12-04-part-1/"
image = "/wp-content/uploads/2012/05/openstack-logo-shade.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a8112f4523f652dde44981601ca24f6b35875b60d4c73ebf8f19564b3f163821"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<aside class="legacy-callout">
<ul>
	<li><a href="{{< relurl "/installing-openstack-grizzly-with-devstack/" >}}" target="_blank">Installing OpenStack Grizzly with DevStack</a> : Here is an updated Grizzly DevStack tutorial since Folsom is coming to an end.</li>
</ul>
</aside>

<em><strong>Update:</strong></em> My latest installation document for Folsom can be found <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}">here</a>. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. Thanks!

Here is a two-parter on how to bring up an OpenStack build on VirtualBox. A screencast is accompanying the two sections. I live in networks, so if you see me do so all bad practice in scripting and systems configs it should be expected. Live demos can get squirrely, especially herding Unicorns are never very easy, so whatever is not in the video is written in the steps below (mostly..).

Keep in mind this is just VMs on a laptop. OpenStack Essex is the latest release in the 6-month software lifecycle. It is essentially a software abstraction for orchestrating as a customer, not only your customer prem data center, but also your peak/elastic/hybrid/private/public bursting to the blabbity blah cloud. As a service provider this is the bread and butter of multitenant orchestration, automation provisioning etc. Just as in networking we exchange information over pre-defined sets of protocols to pass rumors to one another, this is the same problems in the rest of the data center today. The use of APIs or gateways to data we can create a single infrastructure abstraction one layer up the stack as opposed to a bunch of components loosely coupled together.

The current trends are collaborative, inclusive, and community driven initiatives, and the overarching economic incentive to the vendors is as much defensive. It is the consumers, collectively demanding inovation, as opposed to the vendors serving stockholders. Granted, many of the "consumers" are also vendors, but it is a much more accountable process than ever witnessed in the infancy of the first century of post microprocessor era. My favorite people are those who are those unwilling to recognize the fundamental paradigm shift we are going through. It is probably very similar to the first 2 quarters of a recession, some people realize what is happening but the majority either cannot or will not be able to accept the trending until their portfolio is in shambles. On to the video and post!
<ul>
	<li>Part 1 is a scripted install and how to spin up a couple of compute nodes.</li>
	<li><a href="{{< relurl "/2012/04/23/openstack-essex-scripted-installation-on-ubuntu-12-04-part-2/" >}}" target="_blank">Part 2</a> is what do I do with it after I have some nodes provisioned. It was pretty late at this point in the recording and I was half asleep. Thats my disclaimer for most things in life :)</li>
</ul>
&nbsp;

<p><a href="http://www.youtube.com/watch?v=K1fgBOXpAkU&hd=1">Watch video on YouTube</a></p>

Part 1 video of the install and provisioning:
<strong>Nova:</strong>
Nova is the guts of the Orchestration. Scheduling, messaging, API, compute, object-store etc are vital. Essex Notes:
• nova-api accepts and responds to end user compute and volume API calls. It supports OpenStack API, Amazon's EC2 API and a special Admin API (for privileged users to perform administrative actions). It also initiates most of the orchestration activities (such as running an instance) as well as enforces some policy (mostly quota checks). In the Essex release, nova-api has been modularized, allowing for implementers to run only specific APIs.
• The nova-compute process is primarily a worker daemon that creates and terminates virtual machine instances via hypervisor's APIs (XenAPI for XenServer/XCP, libvirt for KVM or QEMU, VMwareAPI for VMware, etc.). The process by which it does so is fairly complex but the basics are simple: accept actions from the queue and then perform a series of system commands (like launching a KVM instance) to carry them out while updating state in the database.
• nova-volume manages the creation, attaching and detaching of persistent volumes to compute instances (similar functionality to Amazon’s Elastic Block Storage). It can use volumes from a variety of providers such as iSCSI or Rados Block Device in Ceph.
• The nova-network worker daemon is very similar to nova-compute and nova-volume. It accepts networking tasks from the queue and then performs tasks to manipulate the network (such as setting up bridging interfaces or changing iptables rules).
• The nova-schedule process is conceptually the simplest piece of code in OpenStack Nova: take a virtual machine instance request from the queue and determines where it should run (specifically, which compute server host it should run on).
• The queue provides a central hub for passing messages between daemons. This is usually implemented with RabbitMQ today, but could be any AMPQ message queue (such as Apache Qpid).
• The SQL database stores most of the build-time and run-time state for a cloud infrastructure. This includes the instance types that are available for use, instances in use, networks available and projects. Theoretically, OpenStack Nova can support any database supported by SQL-Alchemy but the only databases currently being widely used are sqlite3 (only appropriate for test and development work), MySQL and PostgreSQL.
<strong>Hypervisor:</strong>
For this demo we are using Qemu a simple hypervisor. Below is a list of the supported hypervisors with links to a relevant web site for configuration and use:
• KVM - Kernel-based Virtual Machine. The virtual disk formats that it supports it inherits from QEMU since it uses a modified QEMU program to launch the virtual machine. The supported formats include raw images, the qcow2, and VMware formats.
• LXC - Linux Containers (through libvirt), use to run Linux-based virtual machines.
• QEMU - Quick EMUlator, generally only used for development purposes.
• UML - User Mode Linux, generally only used for development purposes.
• VMWare ESX/ESXi 4.1 update 1, runs VMWare-based Linux and Windows images through a connection with the ESX server.
• Xen - XenServer 5.5, Xen Cloud Platform (XCP), use to run Linux or Windows virtual machines. You must install the nova-compute service on DomU.
<strong>Images:</strong> The script for this install are Ubuntu Oneiric 11.10 from ubuntu.com. The default repo is:
http://docs.openstack.org/trunk/openstack-compute/admin/content/starting-images.html
The images use the EC2 repository for distributions and it seems to get out of sync. I switch to archive.ubuntu.com and will cover it in the screencast and steps in the post by editing the /etc/repo.
<strong> Storage:</strong> For this demo we are just using the default local filesystem for storage. Swift appears to be lined up to replace this module from the Nova core.
• OpenStack Object Storage - OpenStack Object Storage is the highly-available object storage project in OpenStack.
• Filesystem - The default backend that OpenStack Image Service uses to store virtual machine images is the filesystem backend. This simple backend writes image files to the local filesystem.
• S3 - This backend allows OpenStack Image Service to store virtual machine images in Amazon’s S3 service.
• HTTP - OpenStack Image Service can read virtual machine images that are available via HTTP somewhere on the Internet. This store is readonly.
<strong>Network</strong>- Nova-Network is the current module for networking in the Essex build for Layer2 bridging today. Quantum is the future component, which appears to be getting rolled officially in the Fall 2012, “Folsom” release. The current networking components are probably the least mature of the modules, since it is relying on the bridging kernel module in Linux.
There has been a great deal of code development from many of the vSwitch developers (e.g. Cisco, Nicira, OVS), to have API integration into Quantum. Data Center software switches will be the crux of enabling cloud mobility via OpenStack especially at hyper-scale. Network abstraction allows for programmatic approaches to automation and provisioning. I did not spend much time digging under the hood of Nova-network, since it will likely be replaced by Quantum in the next SW cycle this fall.
Demo interfaces:
• Eth0 – NAT under VirtualBox. Leave it DHCP.
• Eth1 – Setup as a Host only. Needs to be done globally in VirtualBox the first time before you can add it to an instance.
• Eth2 – Compute nodes live here. Vlan100 will be bound to this interface from the install script and it will appear as br100 from ifconfig.

Nova Network commands and default logs:
cat /var/lib/nova/networks/nova-br100.conf – bridging config
/var/log/nova/nova-network.log - logs
cat /etc/init/nova-network.conf - config load
/etc/init.d/nova-network – upstart / startup config

Currently, Nova supports three kinds of networks, implemented in three “Network Manager” types respectively: Flat Network Manager, Flat DHCP Network Manager, and VLAN Network Manager.
<strong>Installation:</strong>
Install VirtualBox. I am doing this on a MacBook. You will have three interfaces as listed above. Eth0 will be left NATing in VirtualBox, Eth1 (virbr0 in Vbox) is host only 172.16.0.0/16 and Eth2 (virbr1 in Vbox) is 10.0.0.0/8.
I did a 15GB drive and used 4 cores and 3GB if memory. I have done it with one core and 1.5Gb of memory and didn’t really notice much of a difference.
I used the beta2 Ubuntu 12.04 LTS (Precise Pangolin) daily build.
Once booted uptionally update your OS and su root passwd. No flack I don’t feel like sudoing every command in dev.
#sudo passwd root
#su
#apt-get update; apt-get upgrade
I also recommend installing the guest addons found in the VirtualBox ‘Devices’ menu. This will optimize perf depending on the box you are doing this on.
I tend to gut networking managers on a fresh install, you could just stop the service if you would rather.
#apt-get purge network-manager
Edit your networking to reflect what is below.
#nano /etc/network/interfaces
(beginning)
#Primary interface NAT interface
auto eth0
iface eth0 inet dhcp

#public interface – The API village
auto eth1
iface eth1 inet static
address 172.16.0.1
netmask 255.255.0.0
network 172.16.0.0
broadcast 172.16.255.255

#Private Vlan Land of Compute Nodes
auto eth2
iface eth2 inet manual
up ifconfig eth2 up
(end)
Restart the networking service.
#/etc/init.d/networking restart
Test Inet connectivity. ping google.com or some Inet host to make sure you have good connectivity.
Pull down the installer script. Uksysadmin did this script and it worked very well. Great thing about a script (especially for a network knucklhead like myself) is its very easy to parse through and change anything you want to customize for yourself yourself. There are a bunch out there at the moment most break quickly. This one works very well and beats compiling each component from scratch just for testing.
More installer links.
http://docs.openstack.org/bexar/openstack-compute/admin/content/ch03s02.html
http://devstack.org/
Install git from the repos:
#apt-get install git
Clone the installer:
#git clone https://github.com/uksysadmin/OpenStackInstaller.git
#cd OpenStackInstaller
#git checkout essex
Run the installer, this will add the network interfaces, DHP and addresses you need automagically:
#./OSinstall.sh -F 172.16.1.0/24 -f 10.1.0.0/16 -s 512 -t demo -v qemu
Edit nova.conf and add the ‘my_ip’ value to the end of nova.conf:
#nano /etc/nova/nova.conf
#--my_ip=172.16.0.1
Wordpress mangles ‘-‘ There are two of the before ‘my’ e.g. “- - my_ip”

You should see the following processes running at this point. If not start scouring logs or respawn with
/etc/init.d/ restart.
# ps -ea | grep glance
1345 ? 00:00:00 glance-api
1346 ? 00:00:00 glance-registry

# ps -ea | grep nova
1340 ? 00:00:21 nova-compute
1341 ? 00:00:16 nova-network
1342 ? 00:00:03 nova-api
1343 ? 00:00:10 nova-scheduler
1344 ? 00:00:00 nova-objectstor
In Ubuntu 12.04, the database tables are under version control, fix it with the following on a new install to prevent the Image service from breaking possible upgrades:
#glance-manage version_control 0
#glance-manage db_sync
Restart Glance just in case, probably not nessecary:
#/etc/init.d/glance-api restart
#/etc/init.d/glance-registry restart
Download the image. This portion, was a bit hit and miss for me. A circuit blew from the pile of gear in my ghettofab lab and clipped the download during one. If you don’t see “saved [197289496/197289496]” and see “saved []” with an empty vaue the image will not show in the Nova dashboard.
#./upload_ubuntu.sh -a admin -p openstack -t demo -C 172.16.0.1
If you need to have a couple of attempts you may need to delete the image download in /tmp/__upload/
# rm /tmp/__upload/* (**only if you get ubuntu 11.10 i386 now available in Glance (empty) or nothing in your images menu in Dashboard later in the install**).
Saving to: `/tmp/__upload/ubuntu-11.10-server-cloudimg-i386.tar.gz'

100%[======================================&gt;] 197,289,496  610K/s   in 5m 31s
2012-04-20 01:49:56 (581 KB/s) - `/tmp/__upload/ubuntu-11.10-server-cloudimg-i386.tar.gz' saved [197289496/197289496]
ubuntu 11.10 i386 now available in Glance (d19924ae-56e7-41bc-9f02-bbc8d7265cdf)
Now time for clickety click time:
Log into the dashboard at http://172.16.0.1
Username: demo
Password: openstack
Make sure you see “ubuntu 11.10 i386 Server” under Project -&gt; Images and Snapshot. If you don’t troubleshoot the image upload and Glance install/config.
Under projects –Demo – Go to Access &amp; Security
And create a keypair and save the key
somewhere you can get to it later.
Edit the default rules with:
IP Protocol From Port To Port Source
TCP 22 22 0.0.0.0/0 (CIDR)
ICMP -1 -1 0.0.0.0/0 (CIDR)
TCP 8080 8080 0.0.0.0/0 (CIDR)
TCP 80 80 0.0.0.0/0 (CIDR)
<a href="{{< relurl "/wp-content/uploads/2012/04/p3-sec1.jpg" >}}"><img class="alignleft size-full wp-image-460" title="p3-sec" src="{{< relurl "/wp-content/uploads/2012/04/p3-sec1.jpg" >}}" alt="" width="459" height="412" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

Time to launch an image!
Under project -&gt; Images &amp; Snapshot -&gt; click launch -&gt;
name the instance, choose the default security policy.
Also, choose the keypair you created from the dropdown.
<a href="{{< relurl "/wp-content/uploads/2012/04/p2-image-ub.jpg" >}}"><img class="alignleft size-full wp-image-461" title="p2-image-ub" src="{{< relurl "/wp-content/uploads/2012/04/p2-image-ub.jpg" >}}" alt="" width="578" height="232" /></a>
After you launch your instances you should see them provisioned and available in Dashboard.
<a href="{{< relurl "/wp-content/uploads/2012/04/p4-running-inst.jpg" >}}"><img class="alignleft size-full wp-image-462" title="P4-running-inst" src="{{< relurl "/wp-content/uploads/2012/04/p4-running-inst.jpg" >}}" alt="" width="564" height="352" /></a>
<p>
If that all looks like above then lets connect to the hosts using the key we saved earlier (get the IP from the dashboard under Instances &amp; Volumes). Use Ubuntu as the login ID. You can get the IP from the Dashboard or dump arp tables from the new node that was spun up.
<p>
cd into the directory with your key.
#ssh -i demo.pem ubuntu@10.1.0.x
<a href="{{< relurl "/wp-content/uploads/2012/04/p1-login-ssh.jpg" >}}"><img class="alignleft size-full wp-image-463" title="P1-login-ssh" src="{{< relurl "/wp-content/uploads/2012/04/p1-login-ssh.jpg" >}}" alt="" width="630" height="343" /></a>
Now we have a self-provisioned abstracted compute node! Soooo what do we do with this thing? I labbed a modified example from the admin guide at OpenStack.org, a Wordpress frontend and backend server. I am breaking this into a two part for anyone who doesn’t like scrolling down. <a href="{{< relurl "/2012/04/23/openstack-essex-scripted-installation-on-ubuntu-12-04-part-2/" >}}" target="_blank">Part 2</a> Is an example of what we can do with the compute nodes once we have them provisioned.