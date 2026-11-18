+++
title = "Install Open vSwitch v2 from Source on Red Hat Fedora 19"
date = "2013-11-10T06:07:00+00:00"
lastmod = "2014-03-26T04:58:28+00:00"
author = "Brent Salisbury"
wp_id = 7065
categories = ["In the Lab"]
tags = ["Open vSwitch", "RedHat", "Software Defined Networking"]
description = ""
url = "/install-open-vswitch-v2-redhat-fedora-19/"
image = "/wp-content/uploads/2013/11/redhat-ovs-sdn.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "dd2d7a60096c8e25b4c948d8e6b0c45d6e8cf190b5205390bda2ef96bfdcdf5d"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Install Open vSwitch v2 on Red Hat Fedora 19</h2>

This is a walk through for installing Open vSwitch v2.0+ on RedHat Fedora 19 from source.  If you want to build Open vSwitch from RPM binaries please see <a href="{{< relurl "/install-open-vswitch-v2-0-rpm-redhat-fedora/" >}}" target="_blank">this post</a> There are some new OVS tables included in the latest builds that include some <a href="http://networkheresy.com/2013/11/01/of-mice-and-elephants/" target="_blank">neat concepts</a>. OVS is often regarded as the SDN reference data plane implementation in the early SDN space. That is good for the industry and innovation as it reduces R&D risk and thus cost, which leads to less fragmentation and faster adoption of innovative ideas and architectures. Not to mention resides in easily over half of the vendors SDN DP kit in some form, fashion or library. I tend to make a case OVSDB is looking like the reference SDN management protocol based on real world adoption, not slide deckery. For more information on the Open vSwitch database schema, please see the <a href="http://openvswitch.org/ovs-vswitchd.conf.db.5.pdf" target="_blank">ovsdb.conf spec</a>. Fedora is a perennial favorite Linux platform for many and one of the many sponsored community projects by <a href="https://twitter.com/RedHatNews" target="_blank">RedHat</a>. Fedora is often perceived as more bleeding edge with regard to software software packaging then its counterparts, CentOS and the most conservative of the three, RHEL.

<a href="http://fedoraproject.org/get-fedora" target="_blank" rel="noopener noreferrer">Download Fedora Images</a>

<h2>Install a Supported Fedora Kernel Version for Open vSwitch</h2>
Start by downloading the Open vSwitch v2.0 (or any other release found <a href="http://openvswitch.org/releases/" target="_blank">here and install a Fedora Red Hat Distribution </a>)

I ran into a dbus services bug with an error of the following:

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

Next pull the OVS tarball and unzip it:

<pre class="code-sample"><code>sudo yum install wget tar
wget http://openvswitch.org/releases/openvswitch-2.0.0.tar.gz
tar xvzf openvswitch-2.0.0.tar.gz
cd openvswitch-2.0.0</code></pre>

Once you have Fedora up and running, we need to install a kernel version that is 3.10.x or lower. The default kernel in the install was 3.11.7. You can simply install whatever older version is available from the Yum repository. The following will enable you to search for different versions of the same package, in this case the kernel. For example:

<pre class="code-sample"><code>yum search kernel-devel  --showduplicates
=========================== N/S matched: kernel-devel =============================
kernel-devel-3.9.5-301.fc19.x86_64 : Development package for building kernel modules to match the kernel
kernel-devel-3.9.5-301.fc19.x86_64 : Development package for building kernel modules to match the kernel
kernel-devel-3.11.7-200.fc19.x86_64 : Development package for building kernel modules to match the kernel
kernel-devel-3.11.7-200.fc19.x86_64 : Development package for building kernel modules to match the kernel</code></pre>

If you do not install a different kernel version you will receive the following error from v2.0 currently.

<pre class="code-sample"><code> configure: error: Linux kernel in /lib/modules/3.11.7-200.fc19.x86_64/build is version 3.11.7, but version newer than 3.10.x is not supported </code></pre>

The following installed a supported kernel version for OVS. Once complete, reboot your system.

<pre class="code-sample"><code>yum install kernel-3.9.5-301.fc19 kernel-devel-3.9.5-301.fc19</code></pre>

Next install a few more dependencies.

<pre class="code-sample"><code>yum install gcc make python-devel openssl-devel kernel-devel wget</code></pre>

<h2>Install Open vSwitch v2 from Source on Fedora</h2>

Now compile the source and load the kernel module.

<pre class="code-sample"><code> ./configure --with-linux=/lib/modules/`uname -r`/build
 make
make install
make modules_install
/sbin/modprobe openvswitch
/sbin/modprobe gre</code></pre>

If all went well, the OVS kernel module loaded and can be viewed with the following. If there were any problems view the kenel messages in the output of "dmesg".

<pre class="code-sample"><code>[spooney@localhost openvswitch-2.0.0]# lsmod | grep openvswitch
openvswitch            86117  0
gre                    13035  1 openvswitch
libcrc32c              12603  1 openvswitch</code></pre>

At this point, you "should" be able to run a startup script and cover the config initializations with the following:

<pre class="code-sample"><code>
sudo /usr/share/openvswitch/scripts/ovs-ctl start
</code></pre>

From there you can run some tests to verify the build such as:

<pre class="code-sample"><code>
sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-port br0 gre0 -- set Interface gre0 type=gre
sudo ovs-vsctl add-port br0 vx0 -- set Interface vx0 type=vxlan
sudo ovs-vsctl show
e2ce2381-ab5b-4654-9790-4d4320b29c2f
    Bridge "br0"
        Port "br0"
            Interface "br0"
                type: internal
        Port "gre0"
            Interface "gre0"
                type: gre
        Port "vx0"
            Interface "vx0"
                type: vxlan
    ovs_version: "2.1.90"
</code></pre>

<aside class="legacy-callout">If you want to start and initialize the processes by hand continue with the post.</aside>


Next Start Open vSwitch on Fedora with the following to create the OVS initial database for ovsdb-server and start the OVS vswitchd daemon.
<pre class="code-sample"><code>
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema

ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
                     --private-key=db:Open_vSwitch,SSL,private_key \
                     --certificate=db:Open_vSwitch,SSL,certificate \
                     --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
                     --pidfile --detach
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
</code></pre>
Lastly we verify the OVS version and test adding an OVS bridge.
<pre class="code-sample"><code>
@localhost openvswitch-2.0.0]# ovs-vsctl --version
ovs-vsctl (Open vSwitch) 2.0.0
Compiled Nov  9 2013 23:27:47
#############################
@localhost openvswitch-2.0.0]# sudo ovs-vsctl show
b7f46c7f-44ad-4453-99fe-9aeec9ae3364
    Bridge "br0"
        Port "br0"
            Interface "br0"
                type: internal</code></pre>

<h2>Install Open vSwitch on RedHat Fedora from Binary with Yum</h2>

If you just want to get Open vSwitch up and running on your RedHat system you can simply install the binary from the Yum repo manager. 

<pre class="code-sample"><code>sudo yum install openvswitch -y
sudo /usr/share/openvswitch/scripts/ovs-ctl start</code></pre>

Order of operation and dependencies are abstracted under the hood with some of the following service scripts.

<pre class="code-sample"><code>sudo systemctl enable openvswitch.service
sudo systemctl start openvswitch.service
sudo systemctl status openvswitch.service
sudo systemctl status openvswitch-nonetwork
sudo /usr/share/openvswitch/scripts/ovs-ctl start</code></pre>

The Yum version at the time of this post is 1.11.0. If you compiled from source and then installed from package you will need to delete or migrate conf.db.

<pre class="code-sample"><code>sudo ovs-vsctl show
a646c30d-2de1-46cf-a21b-28f7bf5f6c93
    ovs_version: "1.11.0"</code></pre>

For troubleshooting the startup files are located in the systemd directory structure of Fedora. They can be viewed with the following and some additional commands.

<pre class="code-sample"><code>sudo more /usr/lib/systemd/system/openvswitch.service
sudo more /usr/lib/systemd/system/openvswitch-nonetwork.service
grep OPENVSWITCH /boot/config-`uname -r`</code></pre>

For troubleshooting look for the processes and verify the db and pid files exist and not locked.

<pre class="code-sample"><code>ps -ef | grep ovs</code></pre>

<h2>Get to Know Open vSwitch, Fedora and RedHat Projects</h2>


Software companies will and are driving hardware networking companies. Open source software initiatives drive proprietary software platforms and applications. That is not to say hardware or hardware companies are not innovative, but its clear we are heading towards an unbundling of vertical solutions.
<hr>
Community software projects are revolutionizing technology infrastructures as much as ever. Vertical segments get broken down from the bottom up. The projects used in this tutorial were originally developed by visionary companies in Nicira (now Vmware) with Open vSwitch and RedHat with its legacy of Linux kernel development and open source stewardship. 
<hr>
Get involved in any of the awesome OSS infrastructure projects out there. If you are interested in SDN and are not sure where to start, swing by #opendaylight-ovsdb, #openvswitch or #opendaylight on irc.freenode.net and say hello. Community leaders are quickly identified and ready to assist. The ODL folks are a mix of traditional networking professionals and software developers, collaborating and cross-training truly enjoying such a unique time in the industry. More on OVS, OVSDB and OpenDaylight in the next couple of days as my friend <a href="https://twitter.com/MadhuVenugopal" target="_blank">Madhu Venugopal</a> of RedHat and one of the best community conscious developers around. We will be recording some videos this weekend about the OVSDB OpenDaylight project to help folks get started so stop back by!