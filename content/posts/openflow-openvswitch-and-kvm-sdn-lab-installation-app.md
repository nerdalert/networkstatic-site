+++
title = "OpenFlow, OpenvSwitch and KVM SDN Lab Installation App"
date = "2012-09-24T23:15:47+00:00"
lastmod = "2013-06-07T03:19:51+00:00"
author = "Brent Salisbury"
wp_id = 2823
categories = ["In the Lab", "Programming"]
tags = ["KVM", "Open vSwitch", "OpenFlow", "Python", "Software Defined Networking"]
description = ""
url = "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/"
image = "/wp-content/uploads/2012/09/bunker-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b58e461b15280769f2861fbdd9c0b98e3c06dfa0d1dd92ce1bca498d39befcc4"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow, OpenvSwitch and KVM SDN Lab Installation App</h2>
This OpenFlow, Open vSwitch and KVM SDN Lab Installation App is a python app that will install a few different options at an SDN lab. There are some really nice SDN applications that are coming along that have been open sourced from vendors or the community. Lots of people are really getting interested in understanding what SDN and getting to know new technologies but can quickly hit a wall wether its time to figure out the often tricky installs, lack of experience in Unix and for all of us just time to dedicate to getting a lab framework built.I tried to keep the Python program very linear to make it as readable and reusable as I could. I think I wrote about five pages worth of comments in it.
<hr>
<a href="{{< relurl "/wp-content/uploads/2012/09/term21.jpg" >}}"><img class="alignright size-full wp-image-2873" title="term2" alt="terminal sdn" src="{{< relurl "/wp-content/uploads/2012/09/term21.jpg" >}}" width="200" height="200" /></a>
It can be difficult either remembering how to install some of this stuff after a while so I have gotten to the point just to automate everything if possible. The nice thing is you can easily fire up QEMU/KVM within VM Fusion and VirtualBox  without having to have a server. I will refer to QEMU/KVM interchangeably, it just depends on hardware virtualization. The app will script install for OpenFlow controllers like FloodLight and POX along with OpenvSwitch v1.8.9 with and without VXLan (Cisco contribution) support all on top of the KVM hypervisor. That installation can be used as an SDN lab or just in general to start understanding hypervisor switching with Open vSwitch and forget about the control plan OpenFlow part.
<hr>
There is a screencast below in case anyone gets stuck and needs a reference. I did a post for the pre-requisite Ubuntu <a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}" target="_blank">install</a> in case anyone is unfamiliar with that. VM Fusion networking seemed to work the best for me with OpenvSwitch when it came to being able to talk all the way from the nested VM out, I touch on that later before the installation.

<h2>Open vSwitch KVM and OpenFlow Build Options</h2>

There are four installation builds to choose from. I didn't want to muck up the code too much with too many nested options so I kept it simple. If you were to want for example FloodLight with the OpenvSwitch VXlan build you would just stop the openvswitch-controller service and install Floodlight as explained in these <a href="{{< relurl "/floodlight-openflow-controller-screencast-with-hp-switches/" >}}" target="_blank">directions</a>. I also compile everything from source to have the latest development releases with latest features and also to avoid too much package break. I install generic things from package for simplicity, for example, Git, JRE and linux-headers.

<hr />

The four options are:
<ol class="legacy-numbers">
<ol>
	<li>Base install* KVM &amp; OpenvSwitch, Git(hub), Test Kernel image.</li>
	<li>Base + FloodLight OpenFlow Controller (Java -Open Source).</li>
	<li>Base + POX OpenFlow Controller (Python -Open Source).</li>
	<li>Base + OpenvSwitch v1.8.90 w/ VXlan encapsulation support.</li>
</ol>
</ol>

I did the dev testing for this using a MAC Book Pro and only a wireless NIC. It is likely the reason that VirtualBox struggles with bridging the instantiated VMs from VirtualBox to the wired network over home wireless. It is not a big deal since most lab stuff would be working on the inter "nested" VM communication using the small Linux kernel  or building a VXlan or GRE tunnel between two hypervisors which would be two instances of Ubuntu 12.04 running VMware or VirtualBox. Have not tried Parallels out yet, but suspect it would work fine at least internal to your lab machine.
<hr>
<a href="{{< relurl "/wp-content/uploads/2012/09/SDN.LAB_.Openflow2.jpg" >}}"><img class="aligncenter size-full wp-image-2871" title="SDN.LAB.Openflow" alt="openvswitch openflow sdn tutorial" src="{{< relurl "/wp-content/uploads/2012/09/SDN.LAB_.Openflow2.jpg" >}}" width="519" height="359" /></a>

<em>Figure 1.</em> Some topology ideas. 
<hr>
Use multiple VMs if you want on one physical host and build GRE and VXLan tunnels between them. That is proofing data center overlays right there.

You can basically proof hypervisor to hypervisor tunneling with the lightweight Linux kernel image Linux-0.2.img instance. That image allows for you to boot up lots of nested VMs to test networking even in a non-virtualized environment like a laptop running those instances nested. VirtualBox does not support hardware virtualization "<em>enough</em>" to run KVM it will drop back to Qemu which runs the image without HW virtualization extensions. VM Fusion/Workstation now supports hardware virtualization.

<a href="{{< relurl "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/?shared=email&replytocom=10558" >}}" target="_blank" rel="noopener noreferrer">More On Nested Hardware Virtualization</a>

<hr>

Here is why I suspect VirtualBox can't seem to get it together in this but it doesn't stop you from doing anything you want even tunneling between two VBox instances on the same host with say VXLan for example. Lots of scenarios you can do with these options and hey, its free.
<blockquote class="pullquote">Bridging to a wireless interface is done differently from bridging to a wired interface, because most wireless adapters do not support promiscuous mode. All traffic has to use the MAC address of the host's wireless adapter, and therefore VirtualBox needs to replace the source MAC address in the Ethernet header of an outgoing packet to make sure the reply will be sent to the host interface. When VirtualBox sees an incoming packet with a destination IP address that belongs to one of the virtual machine adapters it replaces the destination MAC address in the Ethernet header with the VM adapter's MAC address and passes it on. VirtualBox examines ARP and DHCP packets in order to learn the IP addresses of virtual machines.</blockquote>

To run the App install a vanilla Ubuntu 12.04 or 12.10 instance into VMware Fusion (preferred) or VirtualBox. The main difference again being VirtualBox doesn't like wireless NICs. If you are hardwired it may work fine, not sure have not tested that. I probably recommend install the guest OS tools for Ubuntu/Linux. On VMware Fusion they are called "VMware Tools" and on VirtualBox they are called Guest utilities. They also do things like ballooning memory and what not.
<h2>OpenFlow, OpenvSwitch and KVM SDN Lab Installation App</h2>
<p><a href="http://www.youtube.com/watch?v=13F1gWjsRPE&hd=1">Watch video on YouTube</a></p>

<hr />

Video: The first Installation is installing OpenvSwitch and KVM on both boxes one being VirtualBox and one VM Fusion. One Open vSwitch install had OpenvSwitch with VXLan and the other was the regular dev build from their Git. The second install is OpenvSwitch, KVM, Openflow Floodlight to complete an SDN lab.

<hr />

I tried to automate every bit of the setup. Requirements:

<ul>
	<li>Before running the script run "apt-get update" to refresh your repo sources.</li>
	<li>Ubuntu 12.04 or greater is installed. Would probably work fine on 11.10 but I have not tested.</li>
	<li>You can ping google.com from the Ubuntu VM or your physical machine.</li>
	<li>Your IP address is on eth0. If you aren't sure type 'ifconfig eth0'.</li>
</ul>

Optional Delete Network-Manager:
Delete "Network-Manager" hey we are network and systems jockeys we don't need GUI IP managers. Below will do it for you, plug in your IP and gateway. Again its pretty optional.
<pre class="code-sample"><code>apt-get purge network-manager
$ ifconfig  eth0 &lt;insert IP&gt; netmask 255.255.255.0 up &lt;- This sets your IP on eth0
$ route add default gw &lt;your gateway such as 192.168.1.1&gt;
$ echo nameservers 8.8.8.8 &gt;&gt; /etc/resolv.conf
$ ping google.com
#Set root account passwd and &#039;su&#039; into it.
$ sudo passwd root
#Enter passwords
$ su</code></pre>
If on a VM take a "snapshot" of your image before you start in case something goes wrong. If on a physical machine, well I didn't test it on one but I "think" it will build fine :)
That said, this is for lab enviroments to get your feet wet with some different SDN projects so I disavow all responsibility. Take a look at the code, I kept it very linear without any classes to avoid any confusion in reading it (hopefully).

<hr />
<h2>Download and Run the Python SDN Lab Installation App</h2>

Make sure you run this as root and use a directory on the local hardrive. Also run this from the GUI of the Ubuntu machine in a console. The IP address bound to eth0 will be moved to a new bridge interface created on OpenvSwitch call "br-int". br-int is arbitrary and could be named anything like br0 for example. Your default route will also be changed from using eth0 to br-int on the Ubuntu host only. <strong>Nothing</strong> on the machine hosting VirtualBox or VM Fusion gets touched and code couldn't even if it tried for that matter. The glory of virtualization and the hypervisor. Pull from wget, git or download the script.
<hr>
<a href="https://github.com/nerdalert/SDN-OpenFlow-Lab/blob/master/sdn.lab.install.v1.2.py" target="_blank" rel="noopener noreferrer">SDN Lab Installer</a>


<h2>Quick Install Instructions for the Impatient Like Myself


<pre class="code-sample"><code>wget http://dl.dropbox.com/u/43333687/sdn.lab.install.v1.2.py
#Or
git clone https://github.com/nerdalert/SDN-OpenFlow-Lab.git
python sdn.lab.install.v1.2.py </code></pre>
Choose 1 of the 4 installation options and press enter. If using VM fusion pay attention to the install as when OpenvSwitch starts digging into the networking it will prompt you for the host machine password.

<h2 class="legacy-heading">Post SDN Lab Install</h2>

You should see one VM in a QEMU window. Assign that an address. If you are using VM Fusion you should be able to ping your gateway and if on VirtualBox you can only ping your host and more VMs we will spin up in a second. Give the first VM in the QEMU window an IP address. Example using the 192.168.1.0 255.255.255.0 or 192.168.1.0/24 network.
<pre class="code-sample"><code> ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up promisc
#Optional gateway, if on VM Fusion or a physical box its always nice to ping 8.8.8.8 :)
 route add default gw 192.168.1.1</code></pre>

<h2>Start more KVM/QEMU VM Instances</h2>

If you are using a nested hypervisor like Vbox or Fusion you will get a complaint about KVM not available. That is only becuase you don't have HW virtualization. Ignore it as the image is so lightweight it runs in software for testing networks perfectly.
<hr>
Examples to copy and paste (Notice unique MAC addresses on each VM 01, 02, 03). The NIC needs to be unique to each host. You can copy and paste this into your Ubuntu console to spin up more machines after the install. Each KVM command will launch a new nested VM.
<pre class="code-sample"><code>kvm -m 128 -net nic,macaddr=22:22:22:00:cc:01 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -hda linux-0.2.img &amp;
kvm -m 128 -net nic,macaddr=22:22:22:00:cc:02 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -hda linux-0.2.img &amp;
kvm -m 128 -net nic,macaddr=22:22:22:00:cc:03 -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown -hda linux-0.2.img </code></pre>
If you ever get a message about not being able to start a VM becasue a "tap0" is in use, it means there is an orphaned VNIC/VIF. You just delete it with "ovs-vsctl del-port tap0" or tap3 etc. Another thing, this build isn't setup to hold the setting after a reboot. Pretty much just as easy to restore a snapshot. If anyone needs it to be a permanent configuration persistent after a reboot, just hit me up and I can add a few functions if you need a hand to adjust it.
<hr>
Thanks to <a href="http://openvswitch.org" target="_blank">Pfaff</a>, <a href="http://networkheresy.com" target="_blank">Casado</a> <a href="http://www.noxrepo.org" target="_blank">McCauley</a>, <a href="http://www.siliconloons.com" target="_blank">Mestery</a> for shepherding these projects into the Open Source community. It is a very small one with regard to networking for now, but will continue to expand as we hurdle (or crawl) towards horizontalization and abstraction with the promise of simplification. Write stuff and share it, code, thoughts, Tweets anything that leaves your mark for the betterment of the community.
<hr>
I will try and help were I can if anyone has issues. I am pretty bad at replying quickly but I try. The real world gets in the way too often so apologies up front. I spent most of last weekend debugging. Just make sure you have Internets, Bridged mode like in the video and it should install painlessly. If it doesn't revert to your snapshot or look in the code at the commands and tshoot.
<hr>
Here are a few starter labs that you can use with this Topology much easier than what I had before in a VM since the images used in this are much smaller. <a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}">OpenFlow SDN Tutorials</a> Will be posting some new ones over the next couple weeks as nights and weekend permit.