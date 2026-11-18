+++
title = "Install Open vSwitch v2.0 from RPM on RedHat Fedora"
date = "2013-12-05T04:00:02+00:00"
lastmod = "2014-02-18T02:59:21+00:00"
author = "Brent Salisbury"
wp_id = 7121
categories = ["Speculative"]
tags = ["OVSDB", "Open vSwitch", "OpenFlow", "RedHat"]
description = ""
url = "/install-open-vswitch-v2-0-rpm-redhat-fedora/"
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "2c19be85d1f55a683288c7f81fea953828f4ea83265decfcafb95b621f26dc84"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Install Open vSwitch v2.0 from RPM on RedHat Fedora</h2>
This post is for installing OVS from RedHat RPM binaries. If you want to build Open vSwitch from source please see <a href="{{< relurl "/install-open-vswitch-v2-redhat-fedora-19/" >}}" target="_blank">this post</a>. Open vSwitch v2.0 introduces some really important features, at the top of the list is multi-threaded support in vswitchd. This will increase flow instantiation rates significantly into the upstream kernel module. A rough guess would be from less then 10k per/sec to 10x that w/ multithreaded support. I would imagine there will be a single threaded implementation for a single trace, serial hardware switch needs. This release also includes experimental support for OpenFlow v1.1, v1.2 and v1.3 along with some new OVSDB tables that have some cool potential such as <a href="http://networkheresy.com/2013/11/01/of-mice-and-elephants/" target="_blank">IPFIX</a>.

Lastly, is the important support for "remote_ip=flow" and "local_ip=flow" options that are enabling us to push multiple keys/VNIs over a single overlay tunnel in the <a href="https://wiki.opendaylight.org/view/Project_Proposals:OVSDB-Integration" target="_blank">OVSDB OpenDaylight</a> project. This was supported in previous versions but different matching options have been added. An example of a VXLAN tunnel carrying multiple tenants or network IDs or whatever your segmentation strategy is:

<pre class="code-sample"><code> Bridge br-tun
Port br-tun
Interface br-tun
type: internal
Port patch-int
Interface patch-int
type: patch
options: {peer=patch-tun}
Port "vxlan-172.16.58.136"
Interface "vxlan-172.16.58.136"
type: vxlan
options: {in_key=flow, local_ip="172.16.58.139", out_key=flow, remote_ip="172.16.58.136"}</code></pre>

Without the v1.0+ multi-table support you are left with only one key per tunnel like so:

<pre class="code-sample"><code> Bridge br-tun
Controller "tcp:172.16.58.1:6633"
is_connected: true
Port "vxlan-1001-172.16.58.143"
Interface "vxlan-1001-172.16.58.143"
type: vxlan
options: {key="1001", local_ip="172.16.58.136", remote_ip="172.16.58.143"}
Port "vxlan-1002-172.16.58.143" </code></pre>

With OpenFlow v1.1+ multiiple tables are now available. This is great for multi-tenant keys. An example output from 3 OpenStack NetworkID is the following:

<pre class="code-sample"><code> [root@fedora2 devstack]# sudo ovs-ofctl dump-tables br-tun
OFPST_TABLE reply (xid=0x2): 254 tables
0: classifier: wild=0x3fffff, max=1000000, active=3
lookup=244, matched=243
1: table1 : wild=0x3fffff, max=1000000, active=2
lookup=0, matched=0
2: table2 : wild=0x3fffff, max=1000000, active=2
lookup=0, matched=0
3: table3 : wild=0x3fffff, max=1000000, active=1
lookup=0, matched=0
4: table4 : wild=0x3fffff, max=1000000, active=0
lookup=0, matched=0</code></pre>
<h2>Download and Install Open vSwitch 2.0 RPM</h2>
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
Pull down the OVS 2.0 Fedora RPM.
<pre class="code-sample"><code>wget ftp://rpmfind.net/linux/fedora/linux/updates/testing/19/x86_64/openvswitch-controller-2.0.0-1.fc19.x86_64.rpm
wget ftp://rpmfind.net/linux/fedora/linux/updates/testing/19/x86_64/openvswitch-2.0.0-1.fc19.x86_64.rpm
sudo rpm -ivh ./openvswitch-2.0.0-1.fc21.x86_64.rpm
sudo rpm -ivh openvswitch-controller-2.0.0-1.fc21.x86_64.rpm
sudo /usr/share/openvswitch/scripts/ovs-ctl start </code></pre>

OVS installation output:

<pre class="code-sample"><code>sudo rpm -i openvswitch-controller-2.0.0-1.fc21.x86_64.rpm
[brent@fedora2 devstack]$ sudo rpm -ivh openvswitch-2.0.0-1.fc21.x86_64.rpm
Preparing... ################################# [100%]
package openvswitch-2.0.0-1.fc21.x86_64 is already installed
sudo rpm -i openvswitch-controller-2.0.0-1.fc21.x86_64.rpm
[brent@fedora2 devstack]$ sudo rpm -ivh openvswitch-controller-2.0.0-1.fc21.x86_64.rpm
Preparing... ################################# [100%]
package openvswitch-controller-2.0.0-1.fc21.x86_64 is already installed </code></pre>

Verify the OVS version:
<pre class="code-sample"><code>[brent@fedora1 devstack]$ sudo ovs-vsctl show
ad6767c0-f906-485b-bde0-c6805772bff9
Manager "ptcp:6640"
ovs_version: "2.0.0"</code></pre>
<h2>Open vSwitch Troubleshooting Commands</h2>
Troubleshooting on your own is the best way to learn a system, and hey, we have Google.
An easy way to troubleshoot and learn about the Open vSwitch file locations is to merely look at the running processes.

<pre class="code-sample"><code>root 49796 49795 0 21:30 ? 00:00:00 ovsdb-server /etc/openvswitch/conf.db -vconsole:emer -vsyslog:err -vfile:info --remote=punix:/var/run/openvswitch/db.sock --private-key=db:Open_vSwitch,SSL,private_key --certificate=db:Open_vSwitch,SSL,certificate --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert --no-chdir --log-file=/var/log/openvswitch/ovsdb-server.log --pidfile=/var/run/openvswitch/ovsdb-server.pid --detach --monitor
root 49805 49804 0 21:30 ? 00:00:00 ovs-vswitchd unix:/var/run/openvswitch/db.sock -vconsole:emer -vsyslog:err -vfile:info --mlockall --no-chdir --log-file=/var/log/openvswitch/ovs-vswitchd.log --pidfile=/var/run/openvswitch/ovs-vswitchd.pid --detach --monitor</code></pre>

Also take a look at the ovs startup script if you want to adjust any startup values, logs etc.
<pre class="code-sample"><code>vi /usr/share/openvswitch/scripts/ovs-ctl</code></pre>

Another easy place to spot errors is to look at the OVS logs and system logs.
<pre class="code-sample"><code>sudo tail -n 100 /var/log/messages
sudo tail -n 100 /var/log/openvswitch/ovsdb-server.log
sudo tail -n 100 /var/log/openvswitch/ovs-vswitchd.log
# For kernel module troubleshooting, run the command 'dmesg'</code></pre>

Some handy commands that are worth committing to memory or maybe a cheat sheet or two:

<hr>
<ul>
	<li><strong>ovs-dpctl dump-flows </strong><em>Show the current OpenFlow tables entries for a given bridge</em></li>
	<li><strong>ovs-ofctl dump-flows </strong><em>List implemented flows in the OVS kernel module</em></li>
	<li><strong>ovs-ofctl snoop </strong><em>Display all OpenFlow messages (this is very cool):</em></li>
	<li><strong>ovs-appctl fdb/show <bridge></strong><em>List L2 MAC table key/val of Port, VLAN, MAC, entry age</em></li>
	<li><strong> ovsdb-client dump </strong><em>Show the OVSDB tables and any values</em></li>
	<li><strong>ovs-dpctl show </strong><em>Show information on each datapath in the OVS instance</em> </li>
</ul>
<hr>

Finally, the OVS FAQ is very extensive and the guys there do an awesome job keeping it up to date. The listserv goes back a few years and has almost any question you could imagine already asked and answered there so give it a search before asking, I bet you will find your answer.
<hr>
<a href="http://openvswitch.org/faq/" target="_blank" rel="noopener noreferrer">Open vSwitch FAQ</a>
<a href="http://openvswitch.org/mlists/" target="_blank" rel="noopener noreferrer">Open vSwitch LSV</a>

Happy hacking and thanks for stopping by!