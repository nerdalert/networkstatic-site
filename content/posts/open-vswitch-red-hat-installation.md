+++
title = "Open vSwitch Red Hat Installation"
date = "2012-12-01T06:57:57+00:00"
lastmod = "2013-11-09T10:41:13+00:00"
author = "Brent Salisbury"
wp_id = 4867
categories = ["In the Lab"]
tags = ["Open vSwitch", "RedHat"]
description = ""
url = "/open-vswitch-red-hat-installation/"
image = "/wp-content/uploads/2012/05/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "57487ecdac549fca0ccc19881c72c2491e841c5fa727131fef45bb8d9e14194f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Open vSwitch Red Hat Installation</h2>
This is an updated tutorial for an Open vSwitch Red Hat Installation. It is a little tricky at the moment from a kernel-devel bug that has a broken symbolic link. I did a screencast also in case anyone gets stuck. Just let me know if I mistyped anything and I will update it.
<h2>Install Open vSwitch Pre-Reqs for Red Hat</h2>

<hr />

The OS details are here.
<pre class="code-sample"><code>[root@localhost]# uname -a
Linux localhost.localdomain 2.6.32-279.el6.x86_64 #1 SMP Fri Jun 22 12:19:21 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux
[root@localhost]# cat /etc/redhat-release
CentOS release 6.3 (Final)</code></pre>
Next using Yum, install some dependencies.
<pre class="code-sample"><code>yum install gcc make python-devel openssl-devel kernel-devel kernel-debug-devel
wget http://openvswitch.org/releases/openvswitch-1.7.1.tar.gz
tar xvfz openvswitch-1.7.1.tar.gz
cd openvswitch-1.7.1</code></pre>
<h2>Open vSwitch Red Hat Installation</h2>
No need to run -&gt; ./boot.sh from the tarball.
Next fix a bug from kernel-devel before you run ./configure.
<pre class="code-sample"><code>cd /lib/modules/2.6.32-279.el6.x86_64/</code></pre>
rm build Add the new symlink based on the output of:
<pre class="code-sample"><code>ls /usr/src/kernels/
rm build
ln -s /usr/src/kernels/2.6.32-279.14.1.el6.x86_64/ build</code></pre>
<a href="{{< relurl "/wp-content/uploads/2012/12/build-ovs.jpg" >}}"><img class="aligncenter size-large wp-image-4873" title="build-ovs" alt="build-ovs" src="{{< relurl "/wp-content/uploads/2012/12/build-ovs-650x200.jpg" >}}" width="650" height="200" /></a>
<em>Figure 1</em>. It will look something like this. Notice the symbolic link is linked to a bad target. you will simply re-link that.

Once you fix the symlink your configure will run clean so cd back into the openvswitch dir.
<pre class="code-sample"><code>cd ~/openvswitch-1.7.1</code></pre>
Now ./configure will go clean.
<pre class="code-sample"><code>./configure --with-linux=/lib/modules/`uname -r`/build</code></pre>
If you leave the bad symlink you will get this error:
<pre class="code-sample"><code>configure: error: source dir /lib/modules/2.6.32-279.el6.x86_64/build doesn't exist</code></pre>
Next we need to edit a kernel file and comment something out.
<pre class="code-sample"><code>vi openvswitch-1.7.1/datapath/linux/compat/include/linux/skbuff.h</code></pre>

Open skbuff.h and head to line 242 or there about. Find the following code and comment it out.

<a href="{{< relurl "/wp-content/uploads/2012/12/skbuff.h.pre_.jpg" >}}"><img class="aligncenter size-full wp-image-4871" title="Openvswitch skbuff before edit" alt="Openvswitch skbuff before edit" src="{{< relurl "/wp-content/uploads/2012/12/skbuff.h.pre_.jpg" >}}" width="578" height="284" /></a>
<em>Figure 2</em>. Edit skbuff.h around line 242.

Change it to reflect the next screenshot by commenting out the following method and next three lines after it.
<pre class="code-sample"><code>static inline struct page *skb_frag_page(const skb_frag_t *frag)</code></pre>
<a href="{{< relurl "/wp-content/uploads/2012/12/skbuff-post-comment.jpg" >}}"><img class="aligncenter size-full wp-image-4869" title="skbuff-post-comment" alt="skbuff-post-comment-openvswitch" src="{{< relurl "/wp-content/uploads/2012/12/skbuff-post-comment.jpg" >}}" width="604" height="169" /></a>
<em>Figure 3.</em> Here is what it should look like after the edit.

Now finish the build.
<pre class="code-sample"><code>make &amp;&amp; make install</code></pre>
If you do not comment out the file properly you will get and error like the following:
<pre class="code-sample"><code>make -C /lib/modules/2.6.32-279.el6.x86_64/build M=/home/brent/openvswitch-1.7.1/datapath/linux modules
make[4]: Entering directory `/usr/src/kernels/2.6.32-279.14.1.el6.x86_64'
CC [M] /home/brent/openvswitch-1.7.1/datapath/linux/genetlink-brcompat.o
In file included from /home/brent/openvswitch-1.7.1/datapath/linux/compat/include/linux/netlink.h:4,
from /home/brent/openvswitch-1.7.1/datapath/linux/compat/include/net/genetlink.h:5,
from /home/brent/openvswitch-1.7.1/datapath/linux/compat/genetlink.inc:3,
from /home/brent/openvswitch-1.7.1/datapath/linux/genetlink-brcompat.c:10:
/home/brent/openvswitch-1.7.1/datapath/linux/compat/include/linux/skbuff.h:242: error: redefinition of ‘skb_frag_page’
include/linux/skbuff.h:1612: note: previous definition of ‘skb_frag_page’ was here
make[5]: *** [/home/brent/openvswitch-1.7.1/datapath/linux/genetlink-brcompat.o] Error 1
make[4]: *** [_module_/home/brent/openvswitch-1.7.1/datapath/linux] Error 2
make[4]: Leaving directory `/usr/src/kernels/2.6.32-279.14.1.el6.x86_64'
make[3]: *** [default] Error 2
make[3]: Leaving directory `/home/brent/openvswitch-1.7.1/datapath/linux'
make[2]: *** [all-recursive] Error 1
make[2]: Leaving directory `/home/brent/openvswitch-1.7.1/datapath'
make[1]: *** [all-recursive] Error 1
make[1]: Leaving directory `/home/brent/openvswitch-1.7.1'
make: *** [all] Error 2</code></pre>
Now that you got it to build cleanly you need to make sure the linux bridge kernel module is not loaded.
<pre class="code-sample"><code>lsmod | grep bridge
bridge 79950 0
/sbin/rmmod bridge</code></pre>
Then insert the openvswitch.ko kernel module. Fastpath good, slow path bad. This is executed from within the untarred Open vSwitch directory where you compiled the code so the full path would be /home//openvswitch/datapath/linux/openvswitch.ko.
<pre class="code-sample"><code>insmod datapath/linux/openvswitch.ko</code></pre>
If you do not remove the Linux bridge module you will get ths follwoing error.
<pre class="code-sample"><code>$ insmod datapath/linux/openvswitch.ko
insmod: error inserting 'datapath/linux/openvswitch.ko': -1 Invalid module format
$ dmesg | tail
openvswitch: exports duplicate symbol br_should_route_hook (owned by bridge)</code></pre>
The rest is just copy and paste.
<pre class="code-sample"><code>insmod datapath/linux/openvswitch.ko
touch /usr/local/etc/ovs-vswitchd.conf
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db \
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,manager_options \
--private-key=db:SSL,private_key \
--certificate=db:SSL,certificate \
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
ovs-vsctl show</code></pre>
Configure the Open vSwitch Bridge and Network
<pre class="code-sample"><code> ovs-vsctl add-br br0
sudo ifconfig eth0 0
sudo ovs-vsctl add-port br0 eth0
sudo ifconfig br0 192.168.1.20 netmask 255.255.255.0
route add default gw 192.168.1.1 br0</code></pre>
<h2>Open vSwitch Red Hat Installation Screencast</h2>
<p><a href="http://www.youtube.com/watch?v=x_3HFfdHTQA&hd=1">Watch video on YouTube</a></p>

<hr />

Thanks for stopping by, feel free to post any issues, apologies for any delays in response.