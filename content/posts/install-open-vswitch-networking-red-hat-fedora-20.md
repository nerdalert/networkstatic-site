+++
title = "Install Open vSwitch Networking on Red Hat Fedora 20"
date = "2014-01-23T02:28:08+00:00"
lastmod = "2015-05-11T00:40:59+00:00"
author = "Brent Salisbury"
wp_id = 7157
categories = ["In the Lab"]
tags = ["Open Source", "Open vSwitch", "RedHat"]
description = ""
url = "/install-open-vswitch-networking-red-hat-fedora-20/"
image = "/wp-content/uploads/2012/06/open-vswitch-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "85aeb135c981bb6497e9e796c475f6e148c953aa75c4a5c1f16198bbe1b7308f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Install Open vSwitch Networking on Red Hat Fedora 20 </h2>

The following tutorial will bootstrap you in installing and configuring Open vSwitch on Red Hat Fedora 20. It also has some extras that are just general Fedora configuration tasks such as setting up networking along with Wireshark over an X11 ssh session. This is the first of lots of integration posts over the next year as we develop network virtualization in Open Daylight and continue to integrate further into OpenStack. The "we" is a royal "we". It is the awesome team I am on at Red Hat, but much broader, the OpenDaylight and OpenStack communities and the thousands of contributors around the world that truly mak the difference. The OVSDB ODL team is hyper-focused on simplifying and automating the deployment and integration of cloud infrastructures. Complexity is in my opinion, typically a hurdle for consumers of open source projects and cloud/scale in general.

<h2> General Fedora Configuration </h2>

First some general configurations of Fedora 20 that I tend to use in a fresh image to be sued for development. Turn down some security services for initial development. These being on are obviously important for production services.

<pre class="code-sample"><code>
sudo systemctl stop firewalld.service
/usr/sbin/getenforce
/usr/sbin/setenforce 0
/usr/sbin/getenforce
</code></pre>

To disable Selinux persistently modify the following and reboot:
<pre class="code-sample"><code>
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
</code></pre>

Install Wireshark with:
<pre class="code-sample"><code>
sudo yum install wireshark
</code></pre>

Optionally enable X11 forwarding for Wireshark pcaps. If you have a desktop manager installed, yum install wireshark with do it. If a windows manager (such as Gnome) is not isntalled, add the following dependencies:
<pre class="code-sample"><code>
sudo yum install wireshark xorg-x11-xauth xorg-x11-fonts-* xorg-x11-utils wireshark-gnome 
sudo yum install wireshark
</code></pre>

The OpenFlow disector is bundled into the Wireshark RPM by default which is excellent for those of us that have spent many hours patching disectors to get them to compile in the past. If on a Mac download XQuartz for X11 at <a href="http://xquartz.macosforge.org" target="_blank">http://xquartz.macosforge.org</a>.


<pre class="code-sample"><code>
sudo sed -i 's/#X11Forwarding\ no/X11Forwarding\ yes/'  /etc/ssh/sshd_config 
sudo systemctl restart sshd.service 
</code></pre>

Now you can ssh to the guest OS w/ "ssh -X <Insert_IP>" and run "sudo wireshark &" and wireshark will get tunneled over an ssl channel and show up as an application running on your local machine.

<h2> Setup Fedora Networking </h2>

Edit the following configuration file for  IPv(x) and netmask configs -  "/etc/sysconfig/network-scripts/ifcfg-en*" (*=some unique number) using the following example:

<pre class="code-sample"><code>
/etc/sysconfig/network-scripts/ifcfg-en*
----------------------------------------
TYPE=Ethernet
BOOTPROTO=static
IPADDR=172.16.58.180
NETMASK=255.255.255.0
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=no
IPV6_AUTOCONF=no
IPV6_DEFROUTE=no
IPV6_FAILURE_FATAL=no
NAME=eth0
UUID=d61f1687-9bcb-4f35-bac1-ddf27c777526
ONBOOT=yes
HWADDR=00:0C:29:91:09:95
PEERDNS=yes
PEERROUTES=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
</code></pre>

Edit the following configuration file for  IPv(x) and netmask configs -  "/etc/sysconfig/network":

<pre class="code-sample"><code>
/etc/sysconfig/network
----------------------
NETWORKING=yes
HOSTNAME=fedora2
GATEWAY=172.16.58.1
</code></pre>


<h2> General Fedora Configuration </h

Next install Open vSwitch. Fedora 20 is packaged with OVS version 2.0.0. This is an important release with multithreading and solid support for the fashionable encapsulations.

Check out the version prior to install with the following:

<pre class="code-sample"><code>
$ sudo yum info openvswitch
Available Packages
Name        : openvswitch
Arch        : x86_64
Version     : 2.0.0
Release     : 1.fc20
Size        : 1.5 M
Repo        : fedora/20/x86_64
Summary     : Open vSwitch daemon/database/utilities
URL         : http://openvswitch.org
License     : ASL 2.0 and LGPLv2+ and SISSL
Description : Open vSwitch provides standard network bridging functions and
            : support for the OpenFlow protocol for remote per-flow control of
            : traffic.
</code></pre>

The Open vSwitch install is the easiest part. The Fedora folks did an exceptional job with this. I am seriosuly ecstatic how well this was done. Mileage has varied with OVS package support from all Linux distros in the past but this was a bangup job with kernel mod support and so important.

<pre class="code-sample"><code>
sudo yum install openvswitch
sudo /sbin/service openvswitch start
</code></pre>

Verify kernel modules loaded with the following:
<pre class="code-sample"><code>
$ lsmod | grep openv
openvswitch            66772  0 
vxlan                  37238  1 openvswitch
gre                    13888  1 openvswitch
libcrc32c              12603  1 openvswitch
</code></pre>

The following is a verbose output of the install:

<pre class="code-sample"><code>
$ sudo yum install openvswitch
Resolving Dependencies
--> Running transaction check
---> Package openvswitch.x86_64 0:2.0.0-1.fc20 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
==================================================================================================
 Package                  Arch                Version                   Repository           Size
==================================================================================================
Installing:
 openvswitch              x86_64              2.0.0-1.fc20              fedora              1.5 M
Transaction Summary
==================================================================================================
Install  1 Package
Total download size: 1.5 M
Installed size: 6.3 M
Is this ok [y/d/N]: y
Downloading packages:
openvswitch-2.0.0-1.fc20.x86_64.rpm                                        | 1.5 MB  00:00:08     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : openvswitch-2.0.0-1.fc20.x86_64                                                1/1 
  Verifying  : openvswitch-2.0.0-1.fc20.x86_64                                                1/1 
Installed:
  openvswitch.x86_64 0:2.0.0-1.fc20                                                               
Complete!
[brent@wtf1 ~]$ sudo /sbin/modprobe openvswitch
[brent@wtf1 ~]$ sudo lsmod | grep open
openvswitch            66772  0 
vxlan                  37238  1 openvswitch
gre                    13888  1 openvswitch
libcrc32c              12603  1 openvswitch
$ sudo ovs-vsctl --version
ovs-vsctl (Open vSwitch) 2.0.0
Compiled Oct 28 2013 23:38:30</code></pre>

View the startup script for various runtime options:
<pre class="code-sample"><code>
 /usr/share/openvswitch/scripts/ovs-ctl start
</code></pre>
<h2> Open vSwitch Commands </h2>

Finally are some random commands that I keep in my ~/.bashrc for lazyness, I mean efficiency.

<pre class="code-sample"><code>
###########################################
###### Fedora ~/.bashrc lazy aliases ######
###########################################
alias ovs='sudo ovs-vsctl show'
alias ovsd='sudo ovsdb-client dump'
alias ovsp='sudo ovs-dpctl show'
alias ovsf='sudo ovs-ofctl '
alias logs="sudo journalctl -n 300"
alias ologs="tail -n 300 /var/log/openvswitch/ovs-vswitchd.log"
alias vsh="sudo virsh list"
alias ovtun="sudo ovs-ofctl dump-flows br-tun"
alias ovint="sudo ovs-ofctl dump-flows br-int"
alias ovap="sudo ovs-appctl fdb/show "
alias ovapd="sudo ovs-appctl bridge/dump-flows "
alias ovl="sudo ovs-ofctl dump-flows br-int"
alias dfl="ovs-ofctl -O OpenFlow13 del-flows "
alias ovls="ovs-ofctl -O OpenFlow13  dump-flows br-int"
alias dpfl="ovs-dpctl dump-flows "
alias ovsdbl="ovsdb-client dump -f list"
alias ofport="ovs-ofctl -O OpenFlow13 dump-ports br-int"
alias del="ovs-ofctl -O OpenFlow13 del-flows "
alias delman="ovs-vsctl del-manager"
alias addman="ovs-vsctl set-manager tcp:172.16.58.1:6640"
alias prof="vi ~/.bash_profile"
alias nmap="nmap -sT "
alias code="cd ~/code/"
alias hex='printf "%d\n"'
alias ma='mvn clean install -DskipTests  -Dmaven.compile.fork=true'
alias mansu='mvn clean install -DskipTests  -Dmaven.compile.fork=true -nsu'
alias lsoff='lsof -P -iTCP -sTCP:LISTEN'
alias pkil='killall java'
alias src="source ~/.bashrc"
alias vsh="sudo virsh list"
alias ns="sudo ip netns exec " 
</code></pre>

<h2> Get Involved In Something </h2>

Thanks to all of those that work so hard to deliver all of these amazing projects and changing industry through <a href="http://www.siliconloons.com/?p=523" target="_blank">collaboration</a> and commitment. Its a great time for those seeking to <a href="http://packetpushers.net/show-176-intro-to-python-automation-for-network-engineers/" target="_blank">evolve</a>. Pop into #opendaylight-ovsdb on irc.freenode.net and get to know some great folks if interested in an up and coming project. You can even meet Madhu's Roomba.
<hr>
Thanks for stopping by!
