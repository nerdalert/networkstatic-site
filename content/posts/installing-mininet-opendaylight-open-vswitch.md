+++
title = "Installing Mininet, OpenDaylight and Open vSwitch"
date = "2013-10-21T18:36:07+00:00"
lastmod = "2015-05-11T00:39:50+00:00"
author = "Brent Salisbury"
wp_id = 7046
categories = ["Speculative"]
tags = ["Open vSwitch", "OpenDaylight", "Software Defined Networking", "Tutorials"]
description = ""
url = "/installing-mininet-opendaylight-open-vswitch/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c7bd7771648c0aee8419998f031493577a1bc2ef976ff4098f75eefd1cc503ba"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Installing Mininet, OpenDaylight and Open vSwitch</h2>
The easiest way to get started with a quick SDN lab image is using the Mininet image that is now managed by the <a href="http://onlab.us" target="_blank">ONLAB</a> which is part of the <a href="http://onrc.stanford.edu" target="_blank">ONRC</a>. They do a nice job keeping the images maintained. Ideally the will incorporate ODL into the image soon since the ODL GUI is great for folks to get started with SDN.
<h2>Download and Bring up Mininet</h2>
You can use your prefered hypervisor of choice to run the image. The Mininet guide has instructions for each. <em>Download Mininet and get the image up and running with the following guide:</em>

<a href="http://mininet.org/download/" target="_blank" rel="noopener noreferrer">Download and Get Started With Mininet</a>

<a href="http://openvswitch.org" target="_blank">Open vSwitch</a> should already be running when you boot mininet. You can stop and start the process with:
<pre class="code-sample"><code>/etc/init.d/openvswitch-switch [start | stop | restart]
/etc/init.d/openvswitch-controller [start | stop | restart]</code></pre>

Stop the controller if you are using ODL for control.
<pre class="code-sample"><code>/etc/init.d/openvswitch-controller stop</code></pre>
<h2>Download and Start OpenDaylight</h2>
Performing the following will get OpenDaylight up and running on your mininet instance or you can run it on the host OS (or any other with IP connectivity). It is a simple two node network. If you run into issues head to the #opendaylight irc channel on irc.freenode.net.
<em>From Mininet run the following</em>:
<pre class="code-sample"><code>
apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk unzip
wget https://jenkins.opendaylight.org/controller/job/controller-merge/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/distribution.opendaylight-osgipackage.zip
unzip distribution.opendaylight-osgipackage.zip
cd opendaylight
##Add to ~/.bashrc for persistence through a reboot##
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64
./run.sh
### Then go to http://:8080 ###
### On Mininet ###
mn --controller=remote,ip= --topo=linear,2 --listenport=6633
### Example ###
mn --controller=remote,ip=192.168.254.128 --topo=linear,2 --listenport=6633</code></pre>

<h2>Upgrade Open vSwitch to v2.0</h2>
If you want to upgrade the Mininet OVS instance to the latest v2.0 you can pull from the following repo.


<pre class="code-sample"><code>sudo apt-get install python-software-properties software-properties-common
sudo add-apt-repository ppa:mighost/ppa
sudo apt-get update
/etc/init.d/openvswitch-switch stop
/etc/init.d/openvswitch-controller stop
sudo apt-get install openvswitch-common  openvswitch-datapath-dkms  openvswitch-switch
/etc/init.d/openvswitch-switch start</code></pre>

For a more advanced tutorial and topologies see the following link:

<a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank" rel="noopener noreferrer">OpenDaylight Controller with Mininet</a>

<hr />

A nice video by James Ahn is at the following:
<a href="http://www.youtube.com/watch?v=Aue5kLSQhew" target="_blank" rel="noopener noreferrer">Youtube Installation Instructions</a>

&nbsp;

<hr />

If you want to ssh to the host and run Wireshark you need to have X enabled in the SSH session. On a MAC until Wireshark fully evacuates QT use <a href="http://xquartz.macosforge.org/landing/" target="_blank">XQuartz</a>.

&nbsp;

<pre class="code-sample"><code>ssh -XY
sudo wireshark
</code></pre>
<h2>Install a Linux GUI</h2>
Install LightDM or Gnomae Desktop if you want a GUI
If you want a GUI either of the following will install a stripped down build (no office etc).
<pre class="code-sample"><code>apt-get no-install-recommends install ubuntu-desktop
### Or Gnome ###
sudo apt-get install gnome-core
</code></pre>

A simple remote remote desktop application is XRDP. For installation instructions see this <a href="{{< relurl "/xrdp-an-easy-remote-desktop-setup-for-your-ubuntu-servers/" >}}" target="_blank">post here</a>.

<h2 class="legacy-heading">ONLab Chat with ODL</h2>

The ONLAB recently presented their work to the Technical Work Stream OpenDaylight call that is open to anyone along with the TSC weekly call. Take a look at the recording if interested. They are doing some interesting stuff with network topologies and also expanding Mininet to a multi-node distribution.

<hr />

<a href="https://wiki.opendaylight.org/view/Tech_Work_Stream:Main" target="_blank" rel="noopener noreferrer">OpenDaylight Tech Work Stream (See the September 30, 2013 meeting Recording at the Bottom)</a>

<em>Update:</em> I ran into a nice, relatively new blog that had a nice post with a clear custom topology explanation and other good hands on posts:

<a href="http://sreeninet.wordpress.com/2013/12/25/tools-used-with-opendaylight/" target="_blank" rel="noopener noreferrer">Tools used with Opendaylight - Sreenivas Makam's Blog</a>

<hr />

Thanks and happy hacking!

&nbsp;