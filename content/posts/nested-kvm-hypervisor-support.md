+++
title = "Nested KVM Hypervisor Support"
date = "2012-08-25T05:50:01+00:00"
lastmod = "2013-06-07T03:12:24+00:00"
author = "Brent Salisbury"
wp_id = 2371
categories = ["In the Lab"]
tags = ["KVM", "hypervisor"]
description = ""
url = "/nested-kvm-hypervisor-support/"
image = "/wp-content/uploads/2012/08/tux-copy.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c8b89569f120fc11a066117c664b1501790277b9966de6269b22fb82e7f83a77"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Nested KVM Hypervisor Support</h2>

Adding Hardware Virtualization Support to a VM in KVM with Nested Hypervisor support is pretty important for folks wanting to do proofs for VMs, IaaS, OpenStack etc. It is fairly well supported now under both KVM and Xen. Not to mention, who wants to lab up bare metal when they can use their laptop for modeling. The major driver for nested virtualization is the ability to run nested Hypervisors in IaaS and/or Public Cloud services. It will be attractive for some to run VM farm as a service instances. This provides added flexibility to the customer to maximize their subscription of leased cloud instances.

<a href="{{< relurl "/openstack-quantum-devstack-on-a-laptop-with-vmware-fusion/" >}}" target="_blank" rel="noopener noreferrer">Nested hypervisor Support On Laptops</a>

<h2>Add Nested Hypervisor support in the KVM-Intel or KVM-AMD KO Module</h2>
<hr>
<pre class="code-sample"><code>#Unload and reload kvm-intel kernel module with nested support.
modprobe -r kvm-intel
modprobe kvm-intel nested=1
cat /sys/module/kvm_intel/parameters/nested
Y (Y for yes)</code></pre>
Boot the ISO with Nested Hardware Virtualization support. If you get
This is slightly different from the Rackspace guide. The difference is in the form of that loads the VMX HW virt support for the VM.
<pre class="code-sample"><code>-enable-kvm -cpu qemu64,+vmx</code></pre>
The ability to run nested KVM hypervisors is extremely important for lab environments for test/dev. For some reason KVM pulled support a while back but this is a work around for now written by IBM. More on it in a Sigg <a href="http://static.usenix.org/events/osdi10/tech/full_papers/Ben-Yehuda.pdf" target="_blank">here </a> and the code review from the legend himself Torvalds <a href="https://github.com/torvalds/linux/blob/master/Documentation/virtual/kvm/nested-vmx.txt" target="_blank">Github.</a>
<h2>Booting a KVM Nested Instance</h2>
An example booting the RackSpace OpenStack ISO installer.
<pre class="code-sample"><code>/usr/local/bin/qemu-system-x86_64 \
-enable-kvm -cpu qemu64,+vmx \
-uuid $CONTROLLER_UUID -drive file=rackspacecloud_controller.qcow2,if=virtio \
-cdrom alamo-v1.0.0.iso -boot d -m 8192 -net nic,macaddr=$CONTROLLER_MAC,model=virtio,vlan=1 \
-net tap,vlan=1 -net vde,sock=/tmp/vde_tap0.sock,vlan=1 \
-vnc :1 &amp;</code></pre>
If you get errors when you try and run the qemu-system-x86_64 command they are likely missing the VMX support.

Booting a with an iso to build an image with an OVS tap:
<pre class="code-sample"><code>qemu-system-x86_64 -enable-kvm -cpu qemu64,+vmx \
-m 1024 -hda /media/Storage/imgs/centos.img \
-net nic,macaddr=00:11:22:CC:CC:C5 \
-net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown \
-cdrom /media/Storage/vm-images/CentOS-6.2-x86_64-LiveCD.iso</code></pre>
Booting a built image with an OVS tap:
<pre class="code-sample"><code>qemu-system-x86_64 -enable-kvm -cpu qemu64,+vmx \
-m 1024 -hda /media/Storage/imgs/centos.img \
-net nic,macaddr=00:11:22:CC:CC:C5 \
-net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown</code></pre>
If you get errors when you try and run the qemu-system-x86_64 command they are likely missing the VMX support.
<h2>Para-Virtualization and Full Virtualization</h2>
<hr>
Some hypervisors support Para-virtualizing and Full Virtualization in hypervisors and . Most hypervisors support paravirtualization through the addition of guest tools. Guest tools are often available to install on the VM host OS to optimize memory I/O such as Guest Ballooning, Hypervisor Swapping. The debate gets into the realm of <a href="http://serverfault.com/questions/222010/difference-between-xen-pv-xen-kvm-and-hvm" target="_blank">religion</a>. The gap between these two options is shrinking and likely supported in both manners by future releases. Fundamentally KVM is upstreamed into the Kernel while Xen is run in userland. Both of those have strengths and weaknesses. Here is a nice article describing <a href="http://deinoscloud.wordpress.com/2010/09/30/ballooning-and-hypervisor-swapping-common-misunderstandings/" target="_blank">Swapping and Ballooning.</a> Another nice article from IBM can be read <a href="http://www.ibm.com/developerworks/cloud/library/cl-nestedvirtualization/index.html" target="_blank">here.</a>

Thanks for stopping by.
<hr>