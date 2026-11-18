+++
title = "Quantum OpenStack Scripted Python Install"
date = "2012-08-14T05:18:48+00:00"
lastmod = "2013-03-27T02:05:21+00:00"
author = "Brent Salisbury"
wp_id = 2071
categories = ["In the Lab"]
tags = ["Neutron", "OpenStack", "Programming"]
description = ""
url = "/quantum-openstack-python-installer/"
image = "/wp-content/uploads/2012/08/python2.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "99e2df515d25fa5c043a7cbb0799e322b45ba15012fe0f03cfd774b0e2141a3b"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<em><strong>Update:</strong></em> My latest installation document for Folsom can be found <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}">here</a>. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. This will not work with OpenStack apt-get repos anymore since the packages have changed to Folsom. Thanks!

Quantum OpenStack Python Installer Installation: Here is a cobbled together Openstack Essex scripted installation including the Quantum networking component. It is still baking in development so expect issues and what not. There is a lot going on to get it working so getting it scripted out for a lab environment is helpful since I tend to break everything. Devstack has fantastic install scripts, I just wanted something nice and simple tailored to a box with two NICs so I put this together.

It only takes a couple minutes to install depending on your connection. Granted this was on a 10G connection but at home on my horrible SPs DSL its still only around 10 minutes mainly to download the EC2 Ubuntu image. The install uses <a href="http://openvswitch.org/openstack/documentation/" target="_blank">OpenvSwtich</a> as the software switch, which integrates into KVM and OpenStack via the Quantum plugin. I will fix things as I run into them in the lab. For an installer just using Linux bridging that is probably more stable/baked this may work for you <a href="{{< relurl "/2012/08/openstack-essex-installer-script/" >}}" target="_blank">here</a>. The <a href="http://wiki.openstack.org" target="_blank">OpenStack Wiki</a> has lots of information to help. This is for lab testing only.
<h2>Quantum OpenStack Python Installer Installation</h2>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/quantum-py1.jpg" >}}"><img class="size-full wp-image-2406 aligncenter" title="quantum-python" src="{{< relurl "/wp-content/uploads/2012/08/quantum-py1.jpg" >}}" alt="" width="330" height="303" /></a></p>
<strong>Figure 1</strong>. Topology looks as follows. A public NIC on Eth0 and a Private/backend NIC on Eth1.
<h4>System Preperation</h4>
Paste the following before running the installer to setup proper environmentals.
<pre class="brush: bash; gutter: true">export OS_PASSWORD=openstack
export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export SERVICE_ENDPOINT=&quot;http://localhost:35357/v2.0&quot;
export OS_AUTH_URL=&quot;http://localhost:5000/v2.0/&quot;

echo declare -x OS_PASSWORD=openstack &gt;&gt; /root/.bashrc
echo declare -x SERVICE_TOKEN=openstack &gt;&gt; /root/.bashrc
echo declare -x OS_TENANT_NAME=admin &gt;&gt; /root/.bashrc
echo declare -x OS_USERNAME=admin &gt;&gt; /root/.bashrc
echo declare -x SERVICE_ENDPOINT=&quot;http://localhost:35357/v2.0&quot; &gt;&gt; /root/.bashrc
echo declare -x OS_AUTH_URL=&quot;http://localhost:5000/v2.0/&quot; &gt;&gt; /root/.bashrc
source /root/.bashrc
export
#Verify in the export you see what you just pasted. If you use a differnt password than &#039;openstack&#039; you need to adjust what you put above to reflect that. The script defaults to openstack</pre>
The /etc/network/interfaces should look roughly like this.
<pre class="brush: text; gutter: true">auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
	address 192.168.1.6
	netmask 255.255.255.0
	network 192.168.1.0
	broadcast 192.168.1.255
	dns-nameservers 8.8.8.8
	gateway 192.168.1.1

auto eth1
iface eth1 inet manual
	up ifconfig eth1 up</pre>
You can throw a persistent static route at the bottom of /etc/network/interfaces in case you add the wrong interface in OVS.
up route add default gw &lt;gateway IP&gt;
<h4>Installer Script</h4>
<a href="{{< relurl "/wp-content/uploads/2012/08/py-quantum.py_.txt" >}}" target="_blank">Download the Python script</a> and then execute it.

Name the downloaded file to something.py. Python is installed by default and you just type $python (scriptname) to run it. Make sure when you type export your ENVs are in there. If ENVs and your NICs are good it should run.
<pre class="brush: text; gutter: false">python oStackEssex.py</pre>
<h4>Removal Script</h4>
To remove the install (or most of the files) You can use this <a href="{{< relurl "/wp-content/uploads/2012/08/remove-quantum.sh_.txt" >}}" target="_blank">remove sh script</a> or just paste it in your bash console. Might not hurt to run it twice back to back. ./remove.sh &amp;&amp; ./remove.sh

To build a Windows image here is one way to do it <a href="{{< relurl "/2012/08/building-a-windows-image-for-openstack/" >}}" target="_blank">here.</a>
http://www.youtube.com/watch?v=eoebCKHeG1A

Video. Quick screencast of an install.
<h4>A Cool Unicorn</h4>
Spread the good open word! Thats one pretty Uni straight off the Uni ranch down here.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Unicorn-code.jpg" >}}"><img class="aligncenter size-full wp-image-2395" title="Unicorn-code" src="{{< relurl "/wp-content/uploads/2012/08/Unicorn-code.jpg" >}}" alt="" width="482" height="667" /></a></p>
I believe before we simplify things are going to get more complicated for a while. Or we just stack and abstract complexity like we always have. Layers mostly work though :-)

Some good how-tos for quantum

<a href="http://docs.openstack.org/trunk/openstack-network/admin/content/index.html" target="_blank">http://docs.openstack.org/trunk/openstack-network/admin/content/index.html</a>
<a href="http://devstack.org/exercises/quantum.sh.html">http://devstack.org/exercises/quantum.sh.html</a>
<a href="http://wiki.openstack.org/QuantumDevstack">http://wiki.openstack.org/QuantumDevstack</a>
<a href="http://docs.openstack.org/essex/openstack-compute/install/openstack-install-guide-essex.pdf" target="_blank">http://docs.openstack.org/essex/openstack-compute/install/openstack-install-guide-essex.pdf</a>
<a href="http://wiki.openstack.org/QuantumDevstack" target="_blank">https://github.com/EmilienM/doc-openstack</a>
<a href="http://openstackgd.wordpress.com/2012/04/25/rhel-and-centos-rpm-packages-for-openstack-essex-2012-1-release-is-out/" target="_blank">http://openstackgd.wordpress.com/2012/04/25/rhel-and-centos-rpm-packages-for-openstack-essex-2012-1-release-is-out/</a>