+++
title = "Installing Openvswitch and KVM on CentOS 6.2"
date = "2012-01-26T09:22:02+00:00"
lastmod = "2013-11-09T06:08:01+00:00"
author = "Brent Salisbury"
wp_id = 111
categories = ["In the Lab"]
tags = ["KVM", "Software Defined Networking", "Tutorials"]
description = ""
url = "/installing-openvswitch-and-kvm-on-centos-6-2/"
image = "/wp-content/uploads/2012/06/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d2a18367c899f129615cd2f43ad97211309f91cad669cdde63bd3ad496207c46"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>  Installing Openvswitch and KVM on CentOS 6.2 </h2>

<aside class="legacy-callout">Please see the updated how-to on <a href="{{< relurl "/open-vswitch-red-hat-installation/" >}}" target="_blank">Installing OpenvSwitch on CentOS</a>.</aside>



This is all (mostly) covered in the INSTALL.Linux inside the tar. This might help folks with some of the

graph
<h2> Download and Install Open vSwitch</h2>
<pre class="code-sample"><code>
$ wget http://openvswitch.org/releases/openvswitch-1.3.0.tar.gz
wget http://download.fedoraproject.org/pub/fedora/linux/releases/16/Everything/source/SRPMS/autoconf-2.68-2.fc15.src.rpm
$rpm -ivh webdot-2.26-1.el6.noarch.rpm
$yum -y install graphviz-tcl
$yum -y install python-zope-filesystem
$yum -y install python-zope-interface
$yum -y install automake
$yum -y install autoconf
</code></pre>

add yum -y install openssl-devel this package is necessary if you use SSL with OpenVSWitch. (Thanks for input Marcos)

<pre class="code-sample"><code>
$yum –y install gcc
</code></pre>

The Open vSwitch datapath requires bridging support (CONFIG_BRIDGE) to be built as a kernel module.  (This is common in kernels provided by Linux distributions.)  The bridge module must not be loaded or in use. If the bridge module is running (check with "lsmod | grep bridge"), you must remove it ("rmmod bridge") before starting the datapath.

To build the Linux kernel module, so that you can run the kernel-based switch, pass the location of the kernel build directory on --with-linux.  For example, to build for a running instance of Linux:

<pre class="code-sample"><code>
./configure --with-linux=/lib/modules/`uname -r`/build
$make
$make install
insmod datapath/linux/openvswitch_mod.ko
</code></pre>
Verify the kernel mod loaded
<pre class="code-sample"><code>
[root@localhost openvswitch-1.3.0]# lsmod
openvswitch_mod        82086  0
</code></pre>
If everything compiles and install create the sockets and db.
<pre class="code-sample"><code>
$mkdir -p /usr/local/etc/openvswitch
$ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db
--remote=punix:/usr/local/var/run/openvswitch/db.sock
--remote=db:Open_vSwitch,manager_options
--private-key=db:SSL,private_key
--certificate=db:SSL,certificate
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file
$ovs-vsctl --no-wait init
$ovs-vswitchd --pidfile --detach
$sudo ovs-vswitchd --pidfile --log-file --detach -v
$ovs-vswitchd --pidfile –detach
</code></pre>
Setup the networking component by moving the IP off the physical interface to the new bridge interface
<pre class="code-sample"><code>
$ifconfig eth0 0
$ifconfig br0 192.168.1.25 netmask 255.255.255.0 up
$ifconfig eth0 up
$ifconfig eth0 0.0.0.0
$sudo ovs-vsctl add-br br0
$sudo ovs-vsctl add-port br0 eth0
$route add default gw 192.168.1.1 br0
$route add default gw 192.168.1.1 br0
</code></pre>

<h2> Installing and Integrating KVM into Open vSwitch </h2>

 

*Note* KVM is no longer supported on 32-bit HW.
<pre class="code-sample"><code>
x86_64 <a href="http://packages.sw.be/rpmforge-release/rpmforge-release-0.5.2-2.el5.rf.x86_64.rpm">http://packages.sw.be/rpmforge-release/rpmforge-release-0.5.2-2.el5.rf.x86_64.rpm</a>
$wget rpmforge-release-0.5.2-2.el6.rf.i686.rpm
$rpm -ivh rpmforge-release-0.5.2-2.el6.rf.i686.rpm
$rpm --import <a href="http://apt.sw.be/RPM-GPG-KEY.dag.txt">http://apt.sw.be/RPM-GPG-KEY.dag.txt</a>
$yum -y install qemu-kvm qemu-kvm-tools libvert
</code></pre>
<h2> KVM GUI management tool </h2>

<pre class="code-sample"><code>
$yum –y install virt-manager
$yum install dejavu-lgc-sans-fonts
</code></pre>

Start the libvert daemon or reboot the system.
<pre class="code-sample"><code>
$ Service libvertd start
</code></pre>
Start the KVM GUI


<pre class="code-sample"><code>
$ ./virt-manager
</code></pre>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/01/virt-manager.png" >}}" alt="KVM Virt-Manager"></figure>



<hr>
See the updated Install at the top for accurate information!