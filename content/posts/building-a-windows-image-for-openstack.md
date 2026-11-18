+++
title = "Building a Windows Image for OpenStack"
date = "2012-08-10T03:36:20+00:00"
lastmod = "2012-12-21T01:07:43+00:00"
author = "Brent Salisbury"
wp_id = 2007
categories = ["In the Lab"]
tags = ["OpenStack", "Tutorials", "windows"]
description = ""
url = "/building-a-windows-image-for-openstack/"
aliases = ["/2012/08/building-a-windows-image-for-openstack/"]
image = "/wp-content/uploads/2012/05/openstack-logo-shade.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "fe0548c60ec7a3f4e5220f0886b7f925f3c34aee24e261262345a6a0eabeb23b"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Building a Windows Image for OpenStack</h2>
Building a Windows Image for OpenStack :  Here is a how-to for building a Windows image to import into OpenStack or a KVM Hypervisor. We need to sysprep the image before we can import it into Glance.

<aside class="legacy-callout">For a tutorial on getting OpenStack Folsom up and running have a look at <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">OpenStack Folsom Installation with Devstack Guide</a> </aside>


<!--?xml version="1.0" encoding="UTF-8" standalone="no"?-->
<div>Download the Virtio-win binary driver
<a href="http://alt.fedoraproject.org/pub/alt/virtio-win/latest/images/" target="_blank">http://alt.fedoraproject.org/pub/alt/virtio-win/latest/images/</a></div>
<h4>System Prep</h4>
<div>Have the windows install ISO and the VirtIO iso in the same directory that you execute the commands below.</div>
<div></div>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">apt-get install vncviewer kvm qemu-kvm
kvm-img create -f raw windowsr2.img 20G (Create the image file)
kvm -m 2048 -no-reboot -boot order=d -drive file=windowsr2.img,if=virtio,boot=off -drive file=windows-2008r2.iso,media=cdrom,boot=on -drive file=virtio-win-0.1-30.iso,media=cdrom,boot=off -net nic,model=virtio -nographic -vnc :1
vncviewer</pre>
<div></div>
<div>***Note if you add index=x in the command as listed in the OpenStack admin <a href="http://docs.openstack.org/trunk/openstack-compute/admin/content/creating-a-windows-image.html" target="_blank">guide</a> it may throw an error like this:</div>
<div><!--?xml version="1.0" encoding="UTF-8" standalone="no"?-->root@openstack1:/home/brent# kvm -m 2048 -cdrom windows-2008r2.iso -drive file=windowsr2.img ,if=virtio,boot=on -boot d drive file=virtio-win-0.1-30.iso,index=3,media=cdrom -net nic,model=virtio -net user -nographic -vnc :0</div>
<div>kvm: -drive file=windowsr2.img: drive with bus=0, unit=0 (index=0) exists***</div>

<hr />

<h2>Build the Windows Image for OpenStack</h2>
Enter 127.0.0.1:1 into the window. :1 = is the screen number after you put in the KVM command. This will spawn a VNC window in which you will install windows.
<div><a href="{{< relurl "/wp-content/uploads/2012/08/Windows-VM2.jpg" >}}"><img class="wp-image-2012 aligncenter" title="Windows Openstack VM" alt="" src="{{< relurl "/wp-content/uploads/2012/08/Windows-VM2.jpg" >}}" width="513" height="383" /></a></div>
<div><strong>Figure 1. </strong>Next.</div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/08/select-driver1.jpg" >}}"><img class="aligncenter  wp-image-2020" title="select-driver" alt="" src="{{< relurl "/wp-content/uploads/2012/08/select-driver1.jpg" >}}" width="542" height="399" /></a></div>
<div><strong>Figure 2. </strong>I used the WLH-&gt;AMD folder to locate the driver.</div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/08/SCSI4.jpg" >}}"><img class="aligncenter  wp-image-2024" title="SCSI" alt="" src="{{< relurl "/wp-content/uploads/2012/08/SCSI4.jpg" >}}" width="561" height="440" /></a></div>
<div><strong>Figure 3. </strong>Choose the VirtIO SCSI driver which will be the only one listed.</div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/08/20G-img2.jpg" >}}"><img class="aligncenter  wp-image-2025" title="20G-img" alt="" src="{{< relurl "/wp-content/uploads/2012/08/20G-img2.jpg" >}}" width="557" height="443" /></a></div>
<div><strong>Figure 4. </strong>Choose the 20GB image you created with the kvm-img command from the CLI earlier.</div>
&nbsp;
<div><a href="{{< relurl "/wp-content/uploads/2012/08/Installing.jpg" >}}"><img class="aligncenter  wp-image-2017" title="windows openstack image" alt="" src="{{< relurl "/wp-content/uploads/2012/08/Installing.jpg" >}}" width="570" height="446" /></a></div>
<div><strong>Figure 5. </strong>Windows will install.</div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/08/nic-driver.jpg" >}}"><img class="aligncenter  wp-image-2018" title="windows openstack image" alt="" src="{{< relurl "/wp-content/uploads/2012/08/nic-driver.jpg" >}}" width="574" height="401" /></a></div>
<div><strong>Figure 6. </strong>Under Computer Management -&gt; Device Manager update the drivers to the RedHat Ethernet Adaptor on the virtio ISO mounted.</div>
&nbsp;
<div></div>
<div><a href="{{< relurl "/wp-content/uploads/2012/08/windows-FW.jpg" >}}"><img class="aligncenter  wp-image-2019" title="windows openstack image" alt="" src="{{< relurl "/wp-content/uploads/2012/08/windows-FW.jpg" >}}" width="593" height="512" /></a></div>
<div><strong>Figure 7.</strong> Either disable the firewalls or open TCP 3389 and allow ICMP to test your image. RDC is the only way to reach the host for initial setup.</div>
<h2>Import the Image into Glance</h2>
<div>Shutdown the windows machine and import it into Glance.</div>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">glance add name=Ubuntu-12.04 is_public=true container_format=ovf disk_format=qcow2 &lt; windowsr2.img
#Open TCP 3389 and ICMP in Nova Security
nova secgroup-add-rule default tcp 3389 3389 0.0.0.0/0
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0</pre>
<div></div>
<div>After the Windows host boots you should be able to ping it. Depending on your build you may need to add a floating IP to the instance and the RDC into the host.</div>
<div></div>
<div>Finis!</div>