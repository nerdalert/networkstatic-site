+++
title = "Installing Wireshark On Linux for OpenFlow Packet Captures"
date = "2013-02-03T03:35:05+00:00"
lastmod = "2014-03-16T07:13:40+00:00"
author = "Brent Salisbury"
wp_id = 5672
categories = ["Tools"]
tags = ["OpenFlow", "Software Defined Networking", "Wireshark"]
description = ""
url = "/installing-wireshark-on-linux-for-openflow-packet-captures/"
image = "/wp-content/uploads/2013/02/wireshark.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "dec4e50d548dad13c90b834ab1611d52a3c9a182d139b554dd2c216caf0634b5"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Installing Wireshark On Linux for OpenFlow Packet Captures</h2>

<aside class="legacy-callout">Update March 16, 2014:
Fedora 20 has native Wireshark OpenFlow support.
e.g:
yum install wireshark
 </aside>


<aside class="legacy-callout">
<ul>
	<li><strong>Update:</strong> the OpenFlow dissector appears natively included in the nightly Ubuntu dev builds and even better, native in <a href="http://fedoraproject.org/get-fedora" target="_blank">Fedora 19</a>:</li>
<li>### Fedora 19 Wireshark Installation ###
1) sudo yum install wireshark
2) Nothing! Its that easy w/ native OpenFlow support +1
For an X session on Fedora over SSH perform the following.
1) Install the following:
sudo yum install xorg-x11-xauth
sudo yum install xorg-x11-fonts-*
sudo yum install xorg-x11-utils
======================
2) Enable the following in the sshd_config file:
=============================
Change X11Forwarding to yes and uncomment:
X11Forwarding yes
====== sshd_config ==========
#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
#X11Forwarding no
X11Forwarding yes <=== change this
#X11DisplayOffset 10
#X11UseLocalhost yes
#PrintMotd yes
===============
$ export (should contain)
declare -x DISPLAY="localhost:10.0"
=========================
Now you can "ssh -X 192.168.1.100" to your host and run an X Wireshark session using "sudo wireshark".</li>
</ul>
### Mac Installation ###
Wireshark 1.11.0-SVN-52202
<a href="http://www.wireshark.org/download/automated/" target="_blank">http://www.wireshark.org/download/automated/</a>
<ul>
	<li>For a Mac just install quartz and this build and run as su.</li>
	<li>sudo /Applications/Wireshark.app/Contents/MacOS/Wireshark</li>
</ul>
<em>### Installing on Ubuntu using the PPA repo try the following ###</em>
<ul>
	<li> sudo apt-get install python-software-properties</li>
	<li>sudo add-apt-repository ppa:mighost/ppa</li>
<li>sudo apt-get update</li>
<li>### The following was pulled from 1.12.0~201309171613-1ppa1~precise in a dpkg --list. You likely don't need to mess with repo preferences.###</li>
<li>sudo apt-get install wireshark-common libwireshark3 libwireshark-data libwireshark3 libwiretap3 </li>
<li>sudo wireshark</li>
<li>### To run remotely you can connect using X over ssh with 'ssh -XY <ip-address></li>
</ul>
<a href="http://ppa.launchpad.net/mighost/ppa/ubuntu/" target="_blank">Link to the PPA Repo</a>
</aside>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/10/Wireshark-OpenFlow.jpeg" >}}" alt="OpenFlow from Package PPA"></figure>

This tutorial is for those who are learning, troubleshooting and developing using the OpenFlow wire protocol. Packet captures are vital to troubleshooting issues that occur between the switch and OpenFlow controller. The instructions are for installing Wireshark from package or compiling and installing from source. It also walks through installing the OpenFlow v1.0 dissector plugin for Wireshark. Once the plugin is installed you will be able to view OpenFlow messaging in the Wireshark packet captures.
<h2>Installing Wireshark From Repositories</h2>

<ul>
	<li>Ubuntu Wireshark installation from Repository</li>
</ul>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">apt-get update &amp;&amp; apt-get install wireshark-dev wireshark mercurial git</pre>

<ul>
	<li>RedHat (CentOS/RHEL) Wireshark installation from Repository</li>
</ul>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">yum install wireshark-devel wireshark</pre>
<h2>Download and Installing The OpenFlow Wireshark Dissector Option #1 </h2>
This dissector is maintained by Nick Bastin. I am wedging it in here as I missed this one when I initially wrote this post. The other Stanford version is older but works fine for OpenFlow v1.0 but this is much more up to date. The video below is for the original version covered in option #2 below. Start with this one.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">hg clone https://bitbucket.org/barnstorm/of-dissector
cd of-dissector/src
apt-get install scons
scons install
export WIRESHARK=/usr/include/wireshark/
scons install
#This creates a shared object (so) named openflow.so.
#Copy openflow.so to the Wireshark plugin directory.
cp openflow.so /usr/lib/wireshark/libwireshark1/plugins/openflow.so</pre>

<hr />


<ul>
	<li>OpenFlow v1.0 dissector repo <a href="https://bitbucket.org/barnstorm/of-dissector" target="_blank">https://bitbucket.org/barnstorm/of-dissector</a></li>
	<li>OpenFlow v1.1+ dissector repo <a href="https://bitbucket.org/barnstorm/ng-of-dissector" target="_blank">https://bitbucket.org/barnstorm/ng-of-dissector</a></li>
</ul>


<hr />

<h2>Download and Installing The OpenFlow Wireshark Dissector Option #2</h2>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">git clone git://openflow.org/openflow.git
cd openflow
./boot.sh
./configure
make
sudo make install
cd utilities/wireshark_dissectors/openflow</pre>

<hr />

Before you go on you need to edit packet-openflow.c to fix a problem from a change in the Wireshark API.

Open the following C file in a text editor:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">openflow/utilities/wireshark_dissectors/openflow/packet-openflow.c</pre>
Add the following constant somewhere in the file with the other definitions. Look for "#define" and just add wedge it in there.
<pre class="brush: c; gutter: true; first-line: 1; highlight: []; html-script: false">#define NO_STRINGS NULL</pre>
Next change find the function:
Change from:
<pre class="brush: c; gutter: true; first-line: 1; highlight: []; html-script: false">void proto_reg_handoff_openflow()
{
openflow_handle = create_dissector_handle(dissect_openflow, proto_openflow);
dissector_add(TCP_PORT_FILTER, global_openflow_proto, openflow_handle);
}</pre>
To:
<pre class="brush: c; gutter: true; first-line: 1; highlight: []; html-script: false">void proto_reg_handoff_openflow()
{
openflow_handle = create_dissector_handle(dissect_openflow, proto_openflow);
dissector_add_uint(TCP_PORT_FILTER, global_openflow_proto, openflow_handle);
}</pre>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/openflow.so_.jpg" >}}" alt="openflow.so"></figure>
<strong>Figure 1.</strong> The void proto_reg_handoff_openflow() function after edit.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">make
sudo make install</pre>
Copy the dynamic library or shared object (so file) packet-openflow.so into the Wireshark plugins directory.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">cp /var/packet-openflow.so /usr/lib/wireshark/libwireshark1/plugins/</pre>
<h2>Running Wireshark with the OpenFlow Dissector</h2>
If you get the following error, verify you edited acket-openflow.c properly and recompile the dissector again to create another packet-openflow.so object file.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">Couldn&#039;t load module /usr/lib/wireshark/libwireshark1/plugins/packet-openflow.so: /usr/lib/wireshark/libwireshark1/plugins/packet-openflow.so: undefined symbol: dissector_add</pre>
<h2>Verifying OpenFlow Dissector and Wireshark Installation</h2>
In Wireshark go to Help-&gt;About-&gt;Plugins tab. You should see the OpenFlow plugin in the list.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/about-plugin.jpg" >}}" alt="OpenFlow Wireshark Dissector"></figure>

<strong>Figure 2.</strong> The OpenFlow Wireshark plugin

<hr />

You can now view the OpenFlow header and packet type from your Wireshark captures. More information on generating OpenFlow packets can be found in these <a href="{{< relurl "/tag/openflow/" >}}" target="_blank">tutorials</a>.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/02/wireshark-openflow.jpg" >}}" alt="OpenFlow Wireshark Plugin"></figure>

<strong>Figure 3.</strong> Viewing OpenFlow messages in Wireshark.
<h2>Video of Installing and Operating Wireshark with OpenFlow Captures</h2>
[youtube url="http://youtu.be/Uo1TN3nAxCg" width="640" height="360" hd="1"]
<strong>Video 1.</strong> Screemcast of the Wireshark and OpenFlow plugin installation.
<h2>Compiling and Installing Wireshark from Source on Ubuntu and RHEL/CentOS</h2>

<ul>
	<li>Ubuntu</li>
</ul>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">apt-get install libpcap-dev autoconf gtk2.0 flex bison libtool</pre>

<ul>
	<li>RedHat (CentOS/RHEL) I didn't verify the dependencies, but those should cover everything.</li>
</ul>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">yum groupinstall “Development Tools”
yum groupinstall &quot;X Window System&quot;
yum install glib2-devel automake pkgconfig libtool gcc</pre>
Download the source code from <a href="http://wireshark.org" target="_blank">http://wireshark.org</a>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">wget http://wiresharkdownloads.riverbed.com/wireshark/src/wireshark-1.8.5.tar.bz2
bunzip2 wireshark-1.8.5.tar.bz2  
tar -xvf wireshark-1.8.5.tar
./autogen.sh
./configure
make
make install
sudo ldconfig
./wireshark</pre>

<hr />

<h2>Additional Reseources</h2>

<ul>
	<li><a href="http://www.openflow.org/wk/index.php/OpenFlow_Wireshark_Dissector" target="_blank">OpenFlow Wireshark Dissector v1.0</a> - The dissector used in this tutorial.</li>
	<li><a href="https://bitbucket.org/barnstorm/ng-of-dissector" target="_blank">OpenFlow v1.1+ Wireshark</a> Nick Bastin put together a dissector supporting OpenFlow v1.1+. This doesn't support v1.0. So before you pull out your hair wondering why you see the protocol recognized but not dissected, be sure to use a dissector that is supporting your OF version. E.g. learn from my mistakes :*(</li>
	<li>My buddy Murphy McCauley has instructions for installing the dissector on a Mac over at <a href="http://www.noxrepo.org/2012/03/openflow-wireshark-on-mac-os/" target="_blank">Noxrepo.org</a>.</li>
	<li>I would be remiss while on the topic of sharks, if I didn't take the chance to link to a petition against shark hunting, being used as live bait and the horrible practice of "finning" <a href="http://www.thepetitionsite.com/animal-welfare/" target="_blank">The Petition Site</a>.</li>
</ul>


<hr />

Thanks for stopping by.

<hr />