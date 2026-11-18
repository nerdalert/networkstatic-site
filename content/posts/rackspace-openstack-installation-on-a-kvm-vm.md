+++
title = "Rackspace OpenStack Installation on a KVM VM"
date = "2012-08-16T04:09:33+00:00"
lastmod = "2012-12-10T06:18:54+00:00"
author = "Brent Salisbury"
wp_id = 2112
categories = ["In the Lab"]
tags = ["OpenStack", "Public Cloud"]
description = ""
url = "/rackspace-openstack-installation-on-a-kvm-vm/"
image = "/wp-content/uploads/2012/08/openstack-logo1.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "91f253099daa1bfbdd1b598cccf31b410c48c572c10232a2dadf201c438dfc11"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<a href="{{< relurl "/wp-content/uploads/2012/08/Cloud-Uni3.jpg" >}}"><img class="alignright  wp-image-2289" title="Cloud Unicorn" src="{{< relurl "/wp-content/uploads/2012/08/Cloud-Uni3-350x304.jpg" >}}" alt="" width="270" height="234" /></a>

Rackspace OpenStack Installation on a KVM VM: Big day in the OpenStack world, Rackspace announced it was releasing its Openstack installer image named Alamo v1.0. running on top of KVM, along with Opscode Chef and Rackspace OpenStack cookbooks. This may be the Open Source renaissance we have been needing and forced into by exorbitant profit taking, M&amp;A, takeovers, buyouts, spin-ins, spin-offs, spin-outs, IPOs and greedy margins during times of economic uncertainty. Never fear my young republican, there is profits to be made here on by monetizing open source software, but they will be earned with value, partnerships with customers and risk.

We are entering a new era of choices thanks to the decoupling of the virtual from the physical. Rackspace and the entire community has released a very straightforward, yet flexible packaged install. The open source community has done a very nice job of simplifying the installation in what 12 months ago only the strong of heart would attempt. Open Source will win because it isn't about how much money you have or how much you talk, it's about contributing code and doing rather than talking.
<h4>False Alarm</h4>
I must admit when I saw the Twitter buzz this morning after a 3 hour nap and it was, Rackspace offering free access to their cloud resources. I was excited to think they were nailing up tunnels on their public cloud with a client integration peice. We would finally see some real hybrid cloud computing not just handwaving we are accustomed to from, well most. For years we have been hearing it all the while knowing how unrealistic it is without tunnels, orchestration and most importantly disruptive leadership from outside the traditional infrastructure vendors namely the consumers. We are not quite there yet, but getting very close.
<h4>Crunch Time</h4>
In just the past couple of weeks <a href="http://www.theregister.co.uk/2012/08/13/red_hat_openstack_distro/" target="_blank">RedHat</a>, IBM, likely <a href="http://ostatic.com/blog/dell-expands-openstack-cloud-efforts-and-other-open-source-programs" target="_blank">Dell</a> (were very strong initially then keeping options open) and <a href="http://www.networkworld.com/news/2012/060812-microsoft-hyperv-openstack-259983.html" target="_blank">Microsoft</a> have all thrown in their hats (again). CloudStack may be on the verge of getting consumed but alternatives are nice.

After I realized I was getting a free VM instantiated in the cloud quite yet I went ahead and pulled down the package and chose to do the install on a box running KVM. I was going to install the <a href="http://www.rackspace.com/knowledge_center/getting-started/rackspace-private-cloud" target="_blank">Rackspace Openstack</a> all in one on a VM. They had very nice instructions up until I hit the KVM nested hypervisor support. Not sure if their documentation got a little squirrely because  out of the box on Ubuntu 12.04 QEMU/KVM doesn't support Virtual Distributed Ethernet (VDE) nor nested Hypervisors (A Hypervisor inside a Hypervisor). Not a problem we can work around those things! Disclaimer this isn't a knock on the documentation from Rackspace, just how I got things up and running it is certainly possible I missed something all together. Overall their docs were very nice.
<h4>Network Preparation</h4>
I used the same IP scheme the <a href="http://www.rackspace.com/knowledge_center/article/installing-rackspace-private-cloud-kvm" target="_blank">how-to</a> did in the how-to.
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">IP Address: 10.80.1.1
Network: 10.80.1.0
Broadcast: 10.80.1.255
Netmask: 255.255.255.0
DNS1: 8.8.8.8</pre>
This next part ids line from line from their docs, I recommend using those for it <a href="http://www.rackspace.com/knowledge_center/article/installing-rackspace-private-cloud-kvm" target="_blank">here</a>.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">apt-get install uml-utilities
tunctl -t tap0
ifconfig tap0 up
ifconfig tap0 10.80.1.1 netmask 255.255.255.0
apt-get install vde2 libvde-dev libvdeplug2-dev
vde_switch --sock /tmp/vde_tap0.sock -d --tap tap0
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -I INPUT 1 -i tap0 -j ACCEPT
iptables -A FORWARD -i tap0 -s 10.80.1.0/255.255.255.0 -j ACCEPT
qemu-img create -f qcow2 rackspacecloud_controller.qcow2 30G</pre>
When I went to spin up the VM that part failed because of two reasons for me. QEMU/KVM does not by default build in Ubuntu 12.04 have VDE compiled nor nested hardware virtualization support.
<h4>Re-compile QEMU with VDE support.</h4>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">#Download QEMU v1.1.1 (or any version that supports VDE)
wget http://qa.debian.org/watch/sf.php/kvm/qemu-kvm-1.1.1.tar.gz
#Unpack
tar -xvf qemu-kvm-1.1.1.tar.gz
cd qemu-kvm-1.1.1
#prepare with VDE support and the output to /usr/local/bin
./configure --enable-vde --prefix=/usr/local/bin
#make/install
make &amp;&amp; make install
#Check version if no errors.
/usr/local/bin/qemu-system-x86_64 --version
#QEMU emulator version 1.1.1 (qemu-kvm-1.1.1), Copyright (c) 2003-2008 Fabrice Bellard
#That will not replace the old v1.0 QEMU btw.</pre>
If later you get an error about QEMU "expects a network client type" you either didn't get VDE compiled in or you are running the default Ubuntu QEMU v1.0
<h4>Adding Hardware Virtualization Support to a VM in KVM - Nested Hypervisor</h4>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">#Unload and reload kvm-intel kernel module with nested support.
modprobe -r kvm-intel
modprobe kvm-intel nested=1
cat /sys/module/kvm_intel/parameters/nested
Y (Y for yes, may already be supported in the KO)</pre>
Boot the ISO with Nested Hardware Virtualization support. If you get
This is slightly different from the Rackspace guide. The difference is in the form of that loads the VMX HW virt support for the VM.
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">-enable-kvm -cpu qemu64,+vmx</pre>
The ability to run nested KVM hypervisors is extremely important for lab environments for test/dev. For some reason KVM pulled support a while back but this is a work around for now written by IBM. More on it in a Sigg <a href="http://static.usenix.org/events/osdi10/tech/full_papers/Ben-Yehuda.pdf" target="_blank">here </a> and the code review from the legend himself Torvalds <a href="https://github.com/torvalds/linux/blob/master/Documentation/virtual/kvm/nested-vmx.txt" target="_blank">Github.</a>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">export CONTROLLER_UUID=`uuidgen`
export CONTROLLER_MAC=`printf &#039;52:54:BE:EF:%02X:%02X\n&#039; $((RANDOM%256)) $((RANDOM%256))`
/usr/local/bin/qemu-system-x86_64 -enable-kvm -cpu qemu64,+vmx -uuid $CONTROLLER_UUID -drive file=rackspacecloud_controller.qcow2,if=virtio -cdrom alamo-v1.0.0.iso -boot d -m 8192 -net nic,macaddr=$CONTROLLER_MAC,model=virtio,vlan=1 -net tap,vlan=1 -net vde,sock=/tmp/vde_tap0.sock,vlan=1 -vnc :1 &amp;</pre>
If you get errors when you try and run the qemu-system-x86_64 command they are likely missing the VMX support. If no errors, open vnc and attach to your public interface ip on your physical hardware followed by a colon 1 eg. 'into vncviewer ex"172.31.249.5:1".

GUI installation
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/role.jpg" >}}"><img class="wp-image-2115 aligncenter" title="role" src="{{< relurl "/wp-content/uploads/2012/08/role.jpg" >}}" alt="" width="503" height="139" /></a>
<em>Figure 1.</em> Install Options. All in one or multiple nodes.</p>
Choose Controller "All-in-One" if you only want to mess with one node or else mix a controller and compute nodes. That is an alternative in the install. The only mildly unclear thing if new to OpenStack would be the fixed-range. Fixed range is your backend network. That would be a seperate network than the one your ip is on with the TAP into the physical host. The tap0 you made in the beginning and adding the IP masquerading allows you to share that address with your physical and VM hosts.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/IP-add1.jpg" >}}"><img class="wp-image-2116 aligncenter" title="IP-add" src="{{< relurl "/wp-content/uploads/2012/08/IP-add1.jpg" >}}" alt="" width="520" height="266" /></a>
<em>Figure 2.</em> Add an IP on the same IP range as the VDE tap0 you made earlier.</p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/main-menu.jpg" >}}"><img class="size-full wp-image-2117 aligncenter" title="main-menu" src="{{< relurl "/wp-content/uploads/2012/08/main-menu.jpg" >}}" alt="" width="474" height="550" /></a>
<em>Figure 3.</em> At anytime hitting escape will get you to here and you can bounce the image and start over.</p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Chef1.jpg" >}}"><img class="wp-image-2123 aligncenter" title="Chef" src="{{< relurl "/wp-content/uploads/2012/08/Chef1.jpg" >}}" alt="" width="488" height="376" /></a>
<em>Figure 4</em>. Installing Chef</p>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/08/post-config.jpg" >}}"><img class="alignleft  wp-image-2120" title="post-config" src="{{< relurl "/wp-content/uploads/2012/08/post-config.jpg" >}}" alt="" width="548" height="415" /></a>
<em>Figure 5.</em> Post Install</p>
After it is complete if you can figure out how to send control+function+alt+F2 on a mac over a terrible VNC viewer build you beat me. I just sshed to the box from there.

ssh to the VM controller node using the user name you entered during the install to the IP you entered (10.80.1.2).
ssh @10.80.1.2
You can also get to Horizon/Dashboard Web UI now.
http://10.80.1.2

The rest is documented very well here -&gt; <a href="http://c421178.r78.cf1.rackcdn.com/rackspace-private-cloud-gettingstarted.pdf" target="_blank">http://c421178.r78.cf1.rackcdn.com/rackspace-private-cloud-gettingstarted.pdf</a>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/exports.jpg" >}}"><img class="size-full wp-image-2121 aligncenter" title="exports" src="{{< relurl "/wp-content/uploads/2012/08/exports.jpg" >}}" alt="" width="438" height="199" /></a>
<em>Figure 6.</em> When you type 'export' it should look something like this if you add source .novarc.
After you ssh make sure you do these two things to get your ENVs right.</p>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">sudo -i
source .novarc</pre>
<a href="{{< relurl "/wp-content/uploads/2012/08/glance.jpg" >}}"><img class="alignleft  wp-image-2122" title="glance" src="{{< relurl "/wp-content/uploads/2012/08/glance.jpg" >}}" alt="" width="565" height="78" /></a>
Figure 7. 'glance index' show the images loaded.

The rest is getting familiar with the <a href="{{< relurl "/2012/05/openstack-essex-operational-demo/" >}}" target="_blank">operational</a> components of OpenStack.
More than just to the cloud it has the potential of pooling compute, storage and network resources across partnerships, business units, government entities etc to further find cost savings and efficiency vis a vi consolidation. Amazing stuff, easy way to blow out lots of different mixes and matches of your own private cloud that someday soon will be able to elastically burst to an Openstack cloud provider. Which will be nice and nasty, full of tunnels and MTU problems over incompetent LEC networks and we may very well <a href="http://packetpushers.net/show-72-how-we-are-killing-the-internet/" target="_blank">kill</a> the Internet. See more jobs, not less :)