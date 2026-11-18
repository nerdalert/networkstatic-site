+++
title = "OpenStack Essex Installation and Configuration Screencast from Scratch (Part 1)"
date = "2012-05-12T06:13:51+00:00"
lastmod = "2013-04-05T05:08:44+00:00"
author = "Brent Salisbury"
wp_id = 525
categories = ["In the Lab"]
tags = ["OpenStack", "Python", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openstack-essex-installation-and-configuration-screencast-from-scratch/"
aliases = ["/2012/05/openstack-essex-installation-and-configuration-screencast-from-scratch/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ee5cbc87779f81bbccf33ae0101cd394c7afa76204dd8b145fac8434b3db472e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenStack Essex Install on 12.04</h2>

<aside class="legacy-callout"><strong>Dated Content, Please see the Following</strong><p style="text-align: left;" align="center"><em><strong>Update:</strong></em> My latest installation Tutorial for OpenStack Folsom. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. Thanks!
<a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">OpenStack Folsom Quantum DevStack Installation Tutorial</a> 
</p></aside>



Many hours, days, nights and poor defenseless VMs were destroyed in preparing this how-to. There are some great scripts out there but for most engineers and architects we need to tear it apart look at the guts and put it back together. You are in luck. There are a lot of moving parts on the current OpenStack Essex release, so be prepared to drop MySql tables and rebuild. There is a troubleshooting post following this one to refer to as problems arise.

The OpenStack core components we are installing in this demo are Nova, Glance, Keystone and Dashboard. This will be the standard build for future design scenarios. This is killer software out of the box for data center orchestration built on top of killer modules.

Updated and verified July 12, 2012. Difference from the video is using a database for Keystone.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/2nics-2nets.jpg"><img class="alignleft  wp-image-527" title="2Nics-2nets" src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/2nics-2nets.jpg" alt="" width="406" height="334" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em>Figure 1. Two NICs on a host. Note* If you have one NIC you can use a vNIC i.e. eth0 &amp; eth0:1</em>

http://www.youtube.com/watch?v=S18xVjKndQE&amp;hd=1
<h3>Prerequisites</h3>
The KVM requires an x86 machine with either Intel VT or AMD w/AMD-V support. Anything fairly new will have that support in the processor. There are a few older HW builds that support hardware assisted virtualization by enabling it in the bios. Pretty much Googling your machine for hardware virtualization will let you know. Qemu can be run on non VT HW but the machines will probably get brutalized by a few host VMs. When you are setting up the vSwitch either have an out of band or be on it physically. Be careful when you are adding multiple interfaces to bridges since you can spin up a bridging loop pretty quickly unless you have STP on. I recommend a test/dev network or mom's basement network. If not BPDUguard is your friend :) This is done on a fresh install of 64-bit Ubuntu 12.04 (Precise).

The starting Nic interface config looks like this in /etc/network/interfaces.
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">auto lo
iface lo inet loopback

#Frontend
auto eth0
iface eth0 inet static
	address 192.168.1.6 &lt;--- Your Public interface goes here
	netmask 255.255.255.0
	network 192.168.1.0
	broadcast 192.168.1.255
	dns-nameservers 8.8.8.8
	gateway 192.168.1.1

#Backend
auto eth1
iface eth1 inet manual
	up ifconfig eth1 up</pre>
/*Updates
<strong><em>$apt-get update</em></strong>
<strong>$apt-get dist-upgrade</strong>

/*If not FQDN
<strong><em>$nano /etc/hosts</em></strong>
<p class="textbox">127.0.0.1 localhost
127.0.1.1 openstack1</p>
<strong><em>apt-get install ntp</em></strong>

/*Edit the NTP config to survive an Internet/Network outage:
<strong><em>$nano /etc/ntp.conf</em></strong>
<p class="textbox">server ntp.ubuntu.com iburst
server 127.127.1.0
fudge 127.127.1.0 stratum 10</p>
/*Restart the service
<strong><em>$service ntp restart</em></strong>

/*More packages
<strong>$apt-get install tgt</strong>
<strong> $apt-get install open-iscsi open-iscsi-utils</strong>
<strong> $apt-get install bridge-utils</strong>

/*Restart Networking
<strong>$/etc/init.d/networking restart</strong>

<strong>$apt-get install rabbitmq-server memcached python-memcache</strong>
<strong> $apt-get install kvm libvirt-bin</strong>
<strong> $apt-get install -y mysql-server python-mysqldb</strong>

/* Log into MySQL

<strong>$mysql -u root -p</strong>
/*Create the Nova database with a password ‘openstack’
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">mysql -u root -popenstack -e &#039;CREATE DATABASE nova;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON nova.* TO &#039;nova&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON nova.* TO &#039;nova&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &#039;CREATE DATABASE keystone;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON keystone.* TO &#039;keystone&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON keystone.* TO &#039;keystone&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &#039;CREATE DATABASE glance;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;glance&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;glance&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;</pre>
/*Edit my.cnf
<strong>$nano /etc/mysql/my.cnf</strong>
<p class="textbox">/*from
bind-address = 127.0.0.1
/*to
bind-address = 0.0.0.0</p>
$/etc/init.d/mysql restart
<h2>Keystone Identity Management</h2>
/*More packages
<strong>$apt-get install keystone python-keystone python-keystoneclient</strong>

/*Edit keystone.conf
<strong>$nano /etc/keystone/keystone.conf</strong>
<p class="textbox">/* Change ‘admin_token’ <strong>FROM</strong>
#bind_host = 0.0.0.0
public_port = 5000
admin_port = 35357
admin_token = ADMIN
<strong>/*TO</strong>
#bind_host = 0.0.0.0
public_port = 5000
admin_port = 35357
admin_token = openstack</p>
/*Also in Keystone.conf change the catalog values. If you dont change this you will get endpoint errors.

/*Change the catalog values <strong>FROM</strong>:
<p class="textbox">[catalog]
driver = keystone.catalog.backends.sql.Catalog</p>
<strong>TO</strong>:
<p class="textbox">[catalog]
# driver = keystone.catalog.backends.sql.Catalog
driver = keystone.catalog.backends.templated.TemplatedCatalog
template_file = /etc/keystone/default_catalog.templates</p>
<p class="textbox"><strong>Change from mysqlite to MySQL.</strong></p>
<p class="textbox">#connection = sqlite:////var/lib/keystone/keystone.db</p>
<strong>TO:</strong>
<p class="textbox">[sql]
connection = mysql://keystone:openstack@localhost:3306/keystone</p>
Delete the sqlite db - sudo rm /var/lib/keystone/keystone.db

/*Restart the Keystone service
<strong>$service keystone restart</strong>

/* Download and edit keystone-data.sh to have the proper password and token.
/*Download the script to populate Keystone. It parses out IDs and adds them to the account and role creation (originally Devstack/RackBuilders I beleive so ty to them). <a href="{{< relurl "/wp-content/uploads/2012/08/keystone.sh_.txt" >}}" target="_blank">here </a>
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">ADMIN_PASSWORD=${ADMIN_PASSWORD:-openstack}
SERVICE_PASSWORD=${SERVICE_PASSWORD:-$ADMIN_PASSWORD}
export SERVICE_TOKEN=&quot;openstack&quot;
export SERVICE_ENDPOINT=&quot;http://localhost:35357/v2.0&quot;
SERVICE_TENANT_NAME=${SERVICE_TENANT_NAME:-service}</pre>
/*Save and run the keytone.sh script. Thanks to devstack for the script.
<strong>$chmod +x keystone.sh</strong>
<strong> $./keystone.sh</strong>

<strong>$chmod +x endpoints.sh </strong>

/* Restart and Sync Keystone
<strong> $/etc/init.d/keystone restart</strong>

<strong>$keystone-manage db_synch</strong>

Verify Users the following. If you get any errors make sure you have proper variables from a few steps back with the 'export' command.

<strong>$keystone user-list</strong>
<h3>Installing Glance Image Management</h3>
<p class="textbox"><strong>$apt-get install glance glance-api glance-client glance-common glance-registry python-glance</strong></p>
/* Go ahead and add these to the end of /root/.bashrc or at the least paste into your terminal.
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0</pre>
/*Then refresh the shell. You can also use source novarc but keep it simple to start.
<strong>$bash</strong>

We are going to change the following files
/etc/glance/glance-registry-paste.ini (privileges)
/etc/glance/glance-api-paste.ini (privileges)
/etc/glance/glance-registry.conf (sql connection and flavor)
/etc/glance/glance-api.conf (flavor)

<strong>$rm /var/lib/glance/glance.sqlite</strong>

/*Change the values to match below at the bottom of glance-registry-paste.ini
<strong>$/etc/glance/glance-registry-paste.ini</strong>
<p class="textbox">admin_tenant_name = admin
admin_user = admin
admin_password = openstack</p>
/*Change the values to match below at the bottom of glance-api-paste.ini
<strong>$nano /etc/glance/glance-api-paste.ini</strong>
<p class="textbox">admin_tenant_name = admin
admin_user = admin
admin_password = openstack</p>
/*Adjust mysql with privileges
<strong>$nano /etc/glance/glance-registry.conf</strong>
Replace sql_connection = sqlite:////var/lib/glance/glance.sqlite
<p class="textbox">sql_connection = mysql://glance:openstack@localhost/glance</p>
/*Add this to the bottom of the file
<p class="textbox">[paste_deploy]
flavor = keystone</p>
/*Add flavors to /etc/glance/glance-api.conf at the bottom
<strong>$nano /etc/glance/glance-api.conf</strong>
<p class="textbox">[paste_deploy]
flavor = keystone</p>
/* Restart for funzys
<strong>$/etc/init.d/glance-api restart</strong>
<strong> $/etc/init.d/glance-registry restart</strong>

/* Version control fix for 12.04
<strong>$glance-manage version_control 0</strong>
/*If you get errors on the following db_sync verify your variable by typing ‘export’.

/*Sync Glance with MySQL.
<strong>$glance-manage db_sync</strong>

/* FYI The glance-registry process will complain and abend until you apply version control and synch.
<strong>$/etc/init.d/glance-api restart</strong>
<strong> $/etc/init.d/glance-registry restart</strong>

Continue with <a href="{{< relurl "/2012/05/12/openstack-essex-installation-walkthrough-from-scratch-part2/" >}}">part2</a>