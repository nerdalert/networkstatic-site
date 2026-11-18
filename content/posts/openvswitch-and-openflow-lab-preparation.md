+++
title = "OpenvSwitch and OpenFlow Lab Preparation"
date = "2012-09-21T04:51:46+00:00"
lastmod = "2013-04-22T01:12:45+00:00"
author = "Brent Salisbury"
wp_id = 2819
categories = ["In the Lab"]
tags = ["Open vSwitch", "OpenFlow", "Ubuntu", "lab"]
description = ""
url = "/openvswitch-and-openflow-lab-preparation/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "5aa2a665200cf58ba164af48437621552e42652e95bb35df352b9a7da245ddbd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenvSwitch and OpenFlow Lab Preparation</h2>
This post OpenvSwitch and OpenFlow Lab Preparation will serve as a base Linux install using virtual machines in VirtualBox a free hypervisor that you can run on your laptop or desktop. Many do not have access to lab gear but would still like to be able to gets hands on experience in learning new technologies. Another important reason to have access and understanding to how to build virtual machines is for proof of concepts and modeling architectures for validity.

If you have want to get into really digging into KVM and Open vSwitch I highly recommend getting VMFusion since it supports nested hypervisor. Here is a <a href="{{< relurl "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/" >}}" target="_blank">link</a> touching on a use case.

<hr />

<blockquote class="pullquote">About VirtualBox: Multiple guest OSs can be loaded under the host operating system (host OS). Each guest can be started, paused and stopped independently within its own virtual machine. The user can independently configure each VM and run it under a choice of software-based virtualization or hardware assisted virtualization if the underlying host hardware supports this. Oracle Corporation acquired Sun in January 2010 and re-branded the product as "Oracle VM VirtualBox". It was acquired by Oracle under an acquisition of Innotek buy Oracle and had previously been Open Sourced by Innotek and is still subject to the requirements of the GNU General Public License (GPL).<footer><a href="http://virtualbox.org">http://virtualbox.org</a></footer></blockquote>

<hr />

<h2 class="legacy-heading">System Preparation</h2>
<ul>
	<li>Download a Ubuntu desktop or server ISO image located <a href="http://www.ubuntu.com/download" target="_blank">here</a>.</li>
	<li>Download and install VirtualBox for your host operating system <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">here</a>.</li>
</ul>

<hr />

<h2>Install Ubuntu Guest OS on VirtualBox</h2>
The full manual is located <a href="http://dlc.sun.com.edgesuite.net/virtualbox/4.2.0/UserManual.pdf" target="_blank">here</a>. It is pretty self explanatory.

<hr />

I tend to build machines with these settings but it its hard to go wrong with any of it other than a hard disk allocation of less than 5Gb (4.3ish to be accurate) as Ubuntu will not install on less than that. Here are some typical build settings I use:
<hr />

<ul>
	<li>2 CPU and 2 Gb RAM</li>
	<li>Dynamically allocated file will only grow in size when the guest actually stores data on its virtual hard disk. It will therefore initially be small on the host hard drive and only later grow to the size specified as it is filled with data.</li>
	<li>Somewhere around 8-12Gb of Storage or Disk Space. Keep in mind if you allocate the disk dynamically it will only use use physical disk as consumed by the guest VM, not the the total allocation.</li>
	<li>Network - Since most of the stuff I do is infrastructure focused the networking is important. I always change the NIC from its default NAT (Network Address Translation, more accurately PAT Port Address Translation) to "Bridged Adaptor". That puts the VM on the same network as your NIC. You can bind to wireless or wired. VPN connections can be bound to if NATed. So if your physical host like your laptop is on 192.168.1.10 255.255.255.0 a VM in "Bridged Mode" would get 192.168.1.11 255.255.255.0 or whatever your DHCP server assigns to it, the point is it is on the same 192.168.1.x network.</li>
	<li>Snapshots are the other key point I would use heavily. I tend to store a fresh "Snapshot" after I build the OS. This allows me to rollback to a clean install when I break or muck up the image too much.</li>
</ul>

<hr />
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/bridged.snapshot.virtualbox.jpg" >}}"><img class="aligncenter  wp-image-2820" title="bridged.snapshot.virtualbox" alt="virtualbox ubuntu bridged settings" src="{{< relurl "/wp-content/uploads/2012/09/bridged.snapshot.virtualbox.jpg" >}}" width="508" height="565" /></a></p>
<strong>Figure 1.</strong> Network and Snapshot settings in VirtualBox.

<hr />

<h2>Installation of Ubuntu on VirtualBox</h2>
Here is a screencast of an install. Notice the ISO is already downloaded and I choose it for the installation.

<hr />

<p><a href="http://www.youtube.com/watch?v=PXSu8jNa1-4">Watch video on YouTube</a></p>
<h2>Post-Installation of Ubuntu</h2>
I recommend installing the "Guest Additions" located under the "Devices" menu. This provides better guest OS support for various OS specific things like video and input devices. The other notable feature is "Memory Ballooning" which we will discuss next. Optionally you can run "apt-get update" and "apt-get upgrade" after installation to patch the OS to latest releases.

<hr />

At this point I recommend taking a "snapshot" of the host so you can rollback to a fresh installation as you start doing your proofing of technologies and doing labs.
<h2>Virtual Machine Memory Ballooning</h2>

<hr />

While your guest OS is installing take a read to the excerpt below from the VirtualBox docs. Memory ballooning is used very effectively by Hypervisors (VMware, VirtualBox, KVM, XEN) using the Linux OS. It is a key feature if you are running similar images in your Virtual Machine farm to oversubscribe VM tenants for increasing the subscription ratio of VM to Physical host ratio.

The more similar the VMs on a given host are, the more efficiently Page Fusion can reduce the amount of host memory that is in use. It therefore works best if all VMs on a host run identical operating systems (e.g. Windows XP Service Pack)

<hr />

Instead of having a complete copy of each operating system in each VM, Page Fusion identifies the identical memory pages in use by these operating systems and eliminates the duplicates, sharing host memory between several machines ("deduplication"). If a VM tries to modify a page that has been shared with other VMs, a new page is allocated again for that VM with a copy of the shared page ("copy on write"). All this is fully transparent to the virtual machine.
You may be familiar with this kind of memory overcommitment from other hypervisor products, which call this feature "page sharing" or "same page merging". However, Page Fusion differs significantly from those other solutions, whose approaches have several drawbacks

<hr />

Traditional hypervisors scan all guest memory and compute checksums (hashes) for every single memory page. Then, they look for pages with identical hashes and compare the entire content of those pages; if two pages produce the same hash, it is very likely that the pages are identical in content. This, of course, can take rather long, especially if the system is not idling. As a result, the additional memory only becomes available after a significant amount of time (this can be hours or even days!). Even worse, this kind of page sharing algorithm generally consumes significant CPU resources and increases the virtualization overhead by 10-20%.Page Fusion in VirtualBox uses logic in the VirtualBox Guest Additions to quickly identify memory cells that are most likely identical across VMs. It can therefore achieve most of the possible savings of page sharing almost immediately and with almost no overhead.
Page Fusion is also much less likely to be confused by identical memory that it will eliminate just to learn seconds later that the memory will now change and having to perform a highly expensive and often service-disrupting reallocation.

<hr />

I will refer to this post for future labs to help get the base image ready for labs using OpenFlow, OpenvSwitch, OpenStack and more emerging technologies in the future. Stay tuned, feel free to throw any issues you have. Thanks!