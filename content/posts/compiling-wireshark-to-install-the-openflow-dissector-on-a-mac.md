+++
title = "Compiling Wireshark to Install the OpenFlow Dissector on a MAC"
date = "2013-05-20T02:25:36+00:00"
lastmod = "2014-02-18T02:52:57+00:00"
author = "Brent Salisbury"
wp_id = 6582
categories = ["In the Lab", "Tools"]
tags = ["OpenFlow", "Software Defined Networking", "Wireshark"]
description = ""
url = "/compiling-wireshark-to-install-the-openflow-dissector-on-a-mac/"
image = "/wp-content/uploads/2013/05/openflow2.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "1fe593f9ee99274d3992863106aab2b99f270a8b6a212d8b60d3f21d4811e4af"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Compiling Wireshark to Install the OpenFlow Dissector on a MAC</h2>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/10/Wireshark-OpenFlow.jpeg" >}}" alt="OpenFlow from Package PPA"></figure>


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

For those looking to learn or begin some development work with OpenFlow your trusty friend is the OpenFlow Wireshark dissector. Unfortunately it is still not available as a built in plugin packaged with the Wireshark binary yet. So in the meantime it requires compiling wireshark to get the C header files to generate the shared object file to drop into the Wireshark plugin directory. First install MacPorts, then compile Wireshark with MacPorts and lastly compiling the OpenFlow Dissector.


<h2>For the impatient, quick install: Wireshark OpenFlow on a MAC</h2>

<hr>
<pre class="code-sample"><code>#Install MacPorts
sudo port install wireshark-devel
sudo port install scons
sudo port install mercurial
hg clone https://bitbucket.org/barnstorm/ng-of-dissector
export WIRESHARK=/opt/local/include/wireshark/
cd of-dissector/src
apt-get install scons
alias sudo='sudo env WIRESHARK=/usr/include/wireshark/'
sudo scons install
#This creates a shared object (so) named openflow.so.
#Move openflow.so to the Wireshark plugin directory.
sudo mv ~/.wireshark/plugins/openflow.so /usr/lib/wireshark/libwireshark1/plugins/</code></pre>
<hr>

<h2>Download and Install MacPorts</h2>



First download and install MacPorts. My buddy Murphy McCauley has a tutorial using HomeBrew <a href="http://www.noxrepo.org/2012/03/openflow-wireshark-on-mac-os/" target="_blank">here</a>. I had some dependency issues particularly around GTK+ 2.12 since Wireshark needs &gt;= GTK+ 2.40.

<hr />

First download MacPorts. I am using MacPorts becuase they have Wireshark in their repository.
<a href="http://www.macports.org/install.php" target="_blank" rel="noopener noreferrer">Download and Install MAC Ports </a>
<hr>
<h2>Compile Wireshark using MACPorts</h2>
Once ports is installed, build the following packages.
<hr>
MacPorts will download and do most of the heavy lifting for you. Compiling from source is fairly painful to get the right combination of deps.
<pre class="code-sample"><code>sudo port install wireshark
sudo port install scons
sudo port install mercurial</code></pre>
<h2>Download and Install the Wireshark Dissector</h2>
Next pull down the of-dissector that Nick Bastin forked from the original Stanford one. <a href="https://github.com/CPqD" target="_blank">CPqD</a> also has some from v1.0-v1.3. Keep in mind that to capture OpenFlow v1.0 you need an OpenFlow v1.0 dissector and so on. The specs are pretty different with regard to error codes, messages and data structures so one size fits all is not a small task.

<hr />

Using mercurial (hg) pull the dissector. Next you need to export the wireshark directory that contains the C header files that MacPorts installs to /opt/local/include/wireshark/. If the scons build complains, try searching for packet.h in a Wireshark directory.

<pre class="code-sample"><code>hg clone https://bitbucket.org/barnstorm/ng-of-dissector
export WIRESHARK=/opt/local/include/wireshark/
alias sudo='sudo env WIRESHARK=/opt/local/include/wireshark/'
cd ng-of-dissector/src/
sudo scons install
#This creates a shared object (so) named openflow.so.
#Move openflow.so to the Wireshark plugin directory.
sudo mv ~/.wireshark/plugins/openflow.so /usr/lib/wireshark/libwireshark1/plugins/
</code></pre>

If you have never installed Wireshark the libwireshark1 above will just be libwireshark. Scons will drop a file named openflow.so into your home directory. You just need to move openflow.so to your Wireshark plugin directory.

I had to hack around for a while to get this working so I cant guarantee these are all of the exact steps and there isn't another dependency needed but Im pretty sure it pretty close.
<h2>Running Wireshark With The OpenFlow Dissector</h2>
<hr>
Next run the application w/sudo.
<pre class="code-sample"><code>sudo /opt/local/bin/wireshark</code></pre>

Then in the filter box type "of" and hit enter or apply. Fire up your controller and point a network element at it and off you go.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/05/OpenFlow-Dissector1.jpg" >}}" alt="OpenFlow Packet Capture Wireshark"></figure>

You can then drill down into the OF encapsulated packet, to view the OpenFlow messages.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/05/OpenFlow-Packet-Flowmod.png" >}}" alt="OpenFlow Wireshark Dissector Mac"></figure>

<hr />

Thanks for stopping by. I can try and assist anyone having issues but keep in mind don't have another Mac that I could replicate any issues on so its may be tricky. Thanks to Murphy and Nick for putting up docs and code for this. Cheers.