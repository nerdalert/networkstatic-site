+++
title = "OpenStack Essex and Quantum Installation using OpenvSwitch from Scratch"
date = "2012-05-16T07:38:41+00:00"
lastmod = "2013-08-01T00:46:09+00:00"
author = "Brent Salisbury"
wp_id = 617
categories = ["In the Lab"]
tags = ["Neutron", "Open vSwitch", "OpenStack", "Tutorials"]
description = ""
url = "/openstack-essex-and-quantum-installation-using-openvswitch-from-scratch/"
aliases = ["/2012/05/openstack-essex-and-quantum-installation-using-openvswitch-from-scratch/"]
image = "/wp-content/uploads/2012/05/openstack-logo-shade.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "0734ba8f4f23bf0613eb62175aa0092317b9cb478758f125b92a07170230c5a6"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenStack Essex and Quantum Installation using OpenvSwitch from Scratch</h2>
<aside class="legacy-callout"><strong>&lt;em&gt;&lt;strong&gt;Update: This is a very dated post, check out the Grizzly installation&lt;/strong&gt;&lt;/em&gt;</strong> My latest installation document for Folsom can be found at the post <a href="{{< relurl "/installing-openstack-grizzly-with-devstack/" >}}">OpenStack Folsom Quantum Devstack Installation Tutorial and Screencast</a>. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. Thanks!</aside>
<hr>
Here is a walkthrough for the Quantum Network Manager Plugin for OpenStack Essex with a Quantum Installation with OpenvSwitch. It is still in dev so expect weird things and stability issues. For a guy with a networking bread and butter this is the extremely exciting piece of OpenStack for me. I will do a followup and try and breakdown the OpenvSwitch components but the data path is using the same call into the kernel as of 3.2 as Linux bridging is so the performance is in the kernel. It has a control plane component in the way of an OpenFlow controller which executes in user land which has incredible potential. Keystone is clunky still here in that you still have to run random scripts people open source, right your own or what would probably be best is figure out what its doing under the hood, but I don't have time for it and its still arcane for a next gen UI. Here is a nice guide from Stackops I got some of the Quantum configs from <a href="https://github.com/EmilienM/doc-openstack" target="_blank">here.</a>

<ul>
	<li>I recommend getting a working install OpenStack Essex core components as a precursor to this, only because of the added module complexity of mixing in Quantum and OVS @</li>
	<li>OpenStack Essex Installation and Configuration Screencast from Scratch (Part 1)</li>
</ul>

Get to know that conf file. It is the heart of the architecture for today.
To find and replace the address in the file with yours you can get lazy with

sed//g :  $sed -i 's/128.163.188.8/192.168.1.208/g' /etc/nova/nova.conf

Updated and verified July 12, 2012.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/05/2nics-2nets3.jpg" >}}"><img class="wp-image-622 aligncenter" title="2Nics-2nets" src="{{< relurl "/wp-content/uploads/2012/05/2nics-2nets3.jpg" >}}" alt="" width="325" height="267" /></a></p>
<em><strong>Figure 1</strong>. Two NICs on a host. Note* If you have one NIC you can use a vNIC i.e. eth0 &amp; eth0:1</em>
<h3>Prerequisites</h3>
The KVM requires an x86 machine with either Intel VT or AMD w/AMD-V support. Anything fairly new will have that support in the processor. There are a few older HW builds that support hardware assisted virtualization by enabling it in the bios. Pretty much Googling your machine for hardware virtualization will let you know. Qemu can be run on non VT HW but the machines will probably get brutalized by a few host VMs. When you are setting up the vSwitch either have an out of band or be on it physically. Be careful when you are adding multiple interfaces to bridges since you can spin up a bridging loop pretty quickly unless you have STP on. I recommend a test/dev network or mom's basement network. If not BPDUguard is your friend :) This is done on a fresh install of 64-bit Ubuntu 12.04 (Precise).
$apt-get purge network-manager

/*Updates
<strong>$apt-get update</strong>
<strong>$apt-get dist-upgrade</strong>

/*If not FQDN
<strong>$nano /etc/hosts</strong>
127.0.0.1 localhost
127.0.1.1 openstack1
<strong>$apt-get install ntp</strong>

/*Edit the NTP config to survive an Internet/Network outage:
<strong>$nano /etc/ntp.conf</strong>
server ntp.ubuntu.com iburst
server 127.127.1.0
fudge 127.127.1.0 stratum 10
/*Restart the service
<strong>$service ntp restart</strong>

/*More packages please suh
<strong>$apt-get install tgt</strong>
<strong> $apt-get install open-iscsi open-iscsi-utils</strong>

/*Restart Networking
<strong>$/etc/init.d/networking restart</strong>

/*More packages please suh
<strong>$apt-get install rabbitmq-server memcached python-memcache</strong>
<strong> $apt-get install kvm libvirt-bin</strong>
<strong> $apt-get install -y mysql-server python-mysqldb</strong>

/* Log into MySQL
<strong>$mysql -u root -p</strong>
/*Create the Nova database with a password ‘password’,

/****The quote mark is formatted and won't copy and paste. Type the database entries****

Here is a text file you can copy/paste from <a href="{{< relurl "/wp-content/uploads/2012/07/mysql-quantum-paste.txt" >}}" target="_blank">mysql-quatum.txt</a>
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">mysql -u root -popenstack -e &#039;CREATE DATABASE nova;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON nova.* TO &#039;nova&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON nova.* TO &#039;nova&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &#039;CREATE DATABASE keystone;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON keystone.* TO &#039;keystone&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON keystone.* TO &#039;keystone&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &#039;CREATE DATABASE glance;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;glance&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;glance&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &#039;CREATE DATABASE ovs_quantum;&#039;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;ovs_quantum&#039;@&#039;%&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;
mysql -u root -popenstack -e &quot;GRANT ALL ON glance.* TO &#039;ovs_quantum&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;openstack&#039;;&quot;</pre>
/*Edit my.cnf
<strong>$nano /etc/mysql/my.cnf</strong>
<p class="textbox">/*from
bind-address = 127.0.0.1
/*to
bind-address = 0.0.0.0</p>
/*Restart mysql
<strong>$/etc/init.d/mysql restart</strong>
<h2><strong>KeyStone Identity Management</strong></h2>
/*More packages
<strong>$apt-get install keystone python-keystone python-keystoneclient</strong>

<strong>$rm /var/lib/keystone/keystone.db</strong>

/*Edit keystone.conf
<strong>$nano /etc/keystone/keystone.conf</strong>
/*Replace or comment this:
<strong>#connection = sqlite:////var/lib/keystone/keystone.db</strong>
/*With this:
<strong>connection = mysql://keystone:password@localhost:3306/keystone</strong>

/* Change ‘admin_token’ <strong>FROM</strong>
<p class="textbox">#bind_host = 0.0.0.0
public_port = 5000
admin_port = 35357
admin_token = ADMIN</p>
/*<strong>TO</strong>
<p class="textbox">#bind_host = 0.0.0.0
public_port = 5000
admin_port = 35357
admin_token = password</p>
/*Change the catalog values <strong>FROM</strong>:
<p class="textbox">[catalog]
driver = keystone.catalog.backends.sql.Catalog</p>
<strong>TO</strong>:
[catalog]
# driver = keystone.catalog.backends.sql.Catalog
<p class="textbox">driver = keystone.catalog.backends.templated.TemplatedCatalog
template_file = /etc/keystone/default_catalog.templates</p>
/*Restart Keystone
<strong>$service keystone restart</strong>
/*Synch Keystone to MySQL.
<strong>$ keystone-manage db_sync</strong>
/*One more restart to avoid handlers error
<strong>$service keystone restart</strong>
<p class="textbox">/*If you get something like  "Access denied for user keystone" make sure your Admin = is the root MySql user and also double check your formatting of quotes on a paste into MySql and privileges.</p>
/*  This part is rather ridiculous. Hopefully the Folsom release is much more user friendly than this. Either scripting your own or looking for how someone else has kludged together to populate this is a bit silly for the next gen could ecosystem... Anyways here are some people but the time into which at the end of the day you may just want to figure out what its doing and just paste it in. Edit keystone_data.sh to have the proper password and token don't copy and paste the parentheses. Wordpress mangles them. Download the initial Devstack based Keystone <a href="{{< relurl "/wp-content/uploads/2012/08/keystone.sh_.txt" >}}" target="_blank">script here </a>
<p class="textbox">ADMIN_PASSWORD=${ADMIN_PASSWORD:-password}
SERVICE_PASSWORD=${SERVICE_PASSWORD:-$ADMIN_PASSWORD}
export SERVICE_TOKEN="password"
export SERVICE_ENDPOINT="http://localhost:35357/v2.0"
SERVICE_TENANT_NAME=${SERVICE_TENANT_NAME:-service}</p>
/*Save and run the keytone.sh script.
<strong>$chmod +x keystone.sh</strong>
<strong>$./keystone.sh</strong>
<p class="textbox">/* If you get this error "Unable to communicate with identity service: [Errno 111] Connection refused. No handlers could be found for logger "keystoneclient.client"-" make sure you restarted the keystone service after your db sync.</p>
/*This should return a ‘0’ for success.
<strong>$echo $?</strong>

/* Restart Keystone
<strong>$/etc/init.d/keystone restart</strong>

/* Go ahead and add these to the end of /root/.bashrc
<p class="textbox">export SERVICE_TOKEN=password
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0</p>
/*Then refresh the shell. You can also use source novarc but keep it simple to start.
<strong>$bash</strong>
<h2><strong>Glance Image Management</strong></h2>
/*Install Glance packages
<strong>$apt-get install glance glance-api glance-client glance-common glance-registry python-glance</strong>

<strong>$rm /var/lib/glance/glance.sqlite</strong>

Edit the following files. Make sure you touch each with privilege changes and/or flavors as listed.
<p class="textbox">/etc/glance/glance-registry-paste.ini (Password Change)
/etc/glance/glance-api-paste.ini (Password Change)
/etc/glance/glance-registry.conf (sql connection to Mysql and flavor at the bottom)
/etc/glance/glance-api.conf (flavor at the bottom)</p>
/*Change the values to match below at the bottom of glance-registry-paste.ini &amp; glance-api-paste.ini
<strong>$nano /etc/glance/glance-registry-paste.ini</strong>
<strong>$nano $nano /etc/glance/glance-api-paste.ini</strong>
admin_tenant_name = admin
admin_user = admin
admin_password = password

/*Change the values to match below at the bottom of glance-api-paste.ini
$<strong>nano /etc/glance/glance-api-paste.ini &amp; /etc/glance/glance-api-paste.ini</strong>
admin_tenant_name = admin
admin_user = admin
admin_password = password

/*Adjust mysql privileges
<strong>$nano /etc/glance/glance-registry.conf</strong>

<strong></strong>/*Replace or comment the sqlite:
<strong>#connection = sqlite</strong>
<strong>sql_connection = mysql://glance:password@localhost/glance</strong>

/*and add this to the bottom of the file glance-registry.conf file
[paste_deploy]
flavor = keystone
/*Add flavors to /etc/glance/glance-api.conf at the bottom
<strong>$nano /etc/glance/glance-api.conf</strong>
[paste_deploy]
flavor = keystone

/* Restart for funzys
<strong>$/etc/init.d/glance-api restart</strong>
<strong> $/etc/init.d/glance-registry restart</strong>

/* Version control fix for 12.04
<strong>$glance-manage version_control 0</strong>
/*If you get errors on the following db_sync verify your variable by typing ‘export’.
<strong>$glance-manage db_sync</strong>

/* Again for good measure
<strong>$/etc/init.d/glance-api restart</strong>
<strong> $/etc/init.d/glance-registry restart</strong>
<p class="textbox">/* 11.10 image
wget http://uec-images.ubuntu.com/releases/11.10/release/ubuntu-11.10-server-cloudimg-amd64-disk1.img</p>
<p class="textbox">/* 12.04 image
wget https://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img</p>
<strong>$/etc/init.d/glance-api restart</strong>
<strong> $/etc/init.d/glance-registry restart</strong>
or
<strong> $/etc/init.d/glance-registry restart &amp;&amp; /etc/init.d/glance-api restart</strong>

/*List Images
<strong>$glance index (</strong>Should be empty)
/* Add images to Glance
<p class="textbox">$glance add name="Ubuntu 11.10" is_public=true container_format=ovf disk_format=qcow2 &lt; ubuntu-11.10-server-cloudimg-amd64-disk1.img</p>
<p class="textbox">/*Uploading image 'Ubuntu 11.10'
=======================================================================[100%] 167.139407M/s, ETA 0h 0m 0s
Added new image with ID: 3a2404f6-0a4f-44db-b1cd-a81401dd6015</p>
*/
<p class="textbox">$glance add name="Ubuntu 12.04" is_public=true container_format=ovf disk_format=qcow2 &lt; precise-server-cloudimg-amd64-disk1.img</p>
<p class="textbox">Uploading image 'Ubuntu 12.04'
=======================================================================[100%] 143.583705M/s, ETA 0h 0m 0s
Added new image with ID: 92ca562e-bb18-425a-94ac-eb292fbcabec
*/
/* If your image is well above 220Mb you have the wrong image not a Ostack compatible one</p>
<strong>$glance index</strong>
<h2><strong>Nova Installation</strong></h2>
<p class="textbox">$apt-get install nova-api nova-cert nova-common nova-compute nova-compute-kvm nova-doc nova-network nova-objectstore nova-scheduler nova-vncproxy nova-volume
$apt-get install nova-consoleauth novnc python-nova python-novaclient novnc</p>
/*Add to /etc/libvirt/qemu.conf at the top.
/*If you copy/paste make sure the quotes are not formatted from browser
<p class="textbox">clear_emulator_capabilities = 0
user = "root"
group = "root"
cgroup_device_acl = [
"/dev/null", "/dev/full", "/dev/zero",
"/dev/random", "/dev/urandom",
"/dev/ptmx", "/dev/kvm", "/dev/kqemu",
"/dev/rtc", "/dev/hpet", "/dev/net/tun",
]</p>
/* Next edit /etc/nova/api-paste.ini and change the password
<p class="textbox">admin_tenant_name = admin
admin_user = admin
admin_password = password</p>
/* Fix Permissions (if still needed in your release)
<strong>chown -R nova:nova /etc/nova</strong>

/*sync with mysql
<strong>$nova-manage db sync</strong>

/* UP/Down Startup Script
<p class="textbox">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" stop; done
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" start; done</p>
<strong>$chmod +x &lt;ex. restart-nova (filename)&gt;</strong>
/* Edit /etc/nano.conf Pull files from comments below or file at the top of post and replace.
<h2><strong>Install Quantum Network Plugin</strong></h2>
More details here <a href="http://openvswitch.org/openstack/documentation/" target="_blank">http://openvswitch.org/openstack/documentation/</a>

<strong>$apt-get install -y quantum-server quantum-plugin-openvswitch</strong>
<strong> $apt-get install -y openvswitch-datapath-source</strong>
<strong> $apt-get install module-assistant</strong>

/*Add OVS DP module
<strong>$module-assistant auto-install openvswitch-datapath</strong>

/*Change the default plugin for Quantum in /etc/quantum/plugins.ini
<p class="textbox">[PLUGIN]
provider = quantum.plugins.openvswitch.ovs_quantum_plugin.OVSQuantumPlugin</p>

<h2><strong>Install OpenvSwitch</strong></h2>
<strong>$apt-get install -y openvswitch-switch quantum-plugin-openvswitch-agent</strong>

/*Load the ovs module:
<strong>$modprobe openvswitch_mod</strong>

/*Add to the module startup file:
<strong>$echo "openvswitch_mod"&gt;&gt;/etc/modules</strong>

/*Edit /etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini and change the SQL
connection <strong>FROM</strong>:
sql_connection = sqlite://
<strong>TO</strong>
sql_connection = mysql://ovs_quantum:password@128.163.188.8:3306/ovs_quantum

Create “quantum-agent.sh” to the startup directory /etc/init.d./
<strong>$nano /etc/init.d/quantum-agent.sh</strong>
/*Agent Script quantum-agent.sh paste the following into the file you created in init.d
<p class="textbox">#!/bin/bash
quantum-openvswitch-agent /etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini</p>
/*Make executable
<strong>$chmod +x /etc/init.d/quantum-agent.sh</strong>

/*Add to startup directories:
<strong>$update-rc.d quantum-agent.sh defaults</strong>

/*Restart
<strong>$/etc/init.d/quantum-server start</strong>

/* Create an OVS “integration” bridge, to which all VMs will connect:
<strong>$ovs-vsctl add-br br-int</strong>

/*If you want to tie your machine to a physical interface which I am in this.
/*That adds our connector bridge to an interface.
/*Warning- do not add two physical interfaces unless they are bonded or you may be explaining a bridging loops to your VP the next morning. I highly recommend something like BPDUguard on your interfaces connecting you OpenStack nodes to protect the network and cranky network guys.
<strong>$ ovs-vsctl add-port br-int eth0</strong>

/*Start with the ‘&amp;’ to run in bg.
<strong>$/etc/init.d/quantum-agent.sh &amp;</strong>

/*One more restart for good measure
<p class="textbox">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" stop; done
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" start; done</p>
/*Check Services
<strong>$nova-manage service list</strong>
<strong>4nova-manage network list</strong><strong>
</strong>

/*If you have problems the rabbit-qm scheduler seems to die at some points on me. Resolve with:

<strong>$/etc/init.d/rabbitmq-server restart</strong>

Then check services again <strong>$nova-manage service list</strong>

/*Should see something along these lines:
<p class="textbox">$ ps -ea | grep nov
11176 ? 00:00:03 nova-cert
14282 ? 00:00:00 nova-network
14293 ? 00:00:00 nova-compute
14303 ? 00:00:01 nova-api
14313 ? 00:00:00 nova-objectstor
14323 ? 00:00:00 nova-scheduler
14353 ? 00:00:00 nova-xvpvncprox</p>
$ps –ea | grep libvirt
pre&gt;2665 ? 00:00:00 libvirtd

/*Good
<p class="textbox">$nova-manage service list
Binary Host Zone Status State Updated_At
nova-scheduler openstack-dev nova enabled :-) 2012-05-10 06:39:29
nova-compute openstack-dev nova enabled :-) 2012-05-10 06:39:09
nova-network openstack-dev nova enabled :-) 2012-05-10 06:39:29</p>
/*Bad most of the time. Compute can come in and out of that state and recover.
/*I have never seen network recover, it is normally down hard and time to start scouring the logs.
<p class="textbox">$nova-manage service list
Binary Host Zone Status State Updated_At
nova-scheduler openstack-dev nova enabled :-) 2012-05-10 07:26:29
nova-compute openstack-dev nova enabled XXX 2012-05-10 07:19:20
nova-network openstack-dev nova enabled XXX 2012-05-10 07:21:06</p>
/*Add your vNIC “Flat Network” as defined in nova.conf Here is an <a href="{{< relurl "/wp-content/uploads/2012/07/nova-quantum-update.txt" >}}" target="_blank">example config.</a>

/*Ensure your hostname is resolvable to the value in nova.conf for ‘--quantum_connection_host=’

/* TRACE nova QuantumIOException: Unable to connect to server. Got error: [Errno -2] Name or service not known (Indicates a bad hostname in nova.conf for ‘--quantum_connection_host=’

/*Note the difference from the nova-network creation with Quantum Manager. Dont try and copy and paste this or else you get unicode errors "TRACE nova UnicodeEncodeError: 'decimal' codec can't encode character"
<strong>$ nova-manage network create --label=public --fixed_range_v4=172.31.252.0/24</strong>

/*To delete files you need to use the ID found in 'nova-manage network list'
<strong>$nova-manage network delete --uuid</strong> 6ec716d0-1b22-497e-be6c-2017b268af1d &lt;--ID

/*(Optional) Create a floating pool. Can be any address you want to assign. Essentially NAT.
/*Quantum Manager uses the same ‘nova-manage floating’ command.
<strong>$nova-manage floating create --ip_range=128.163.188.240/28</strong>

/*Floating Commands (Optional)
<strong>$nova-manage floating list</strong>
<strong>$nova-manage floating create 128.163.188.248/29</strong>

/*Virtual Machines from CLI-Skip if only interested in dashboard.
/*Make sure your nova db has been synced if you skip:

/*If not synced or sure if synced, sync.
<strong>$nova-manage db sync</strong>

/*Iptables is e.g. ‘ nova secgroup-add-rule ‘ is not supported in OpenvSwitch v1.4

/*Create security keys
<strong>$ nova keypair-add ssh_key &gt; ssh_key.pem</strong>

/*Set Permissions
<strong>$chmod 0600 ssh_key.pem</strong>
<strong> $ssh -i ssh_key.pem ubuntu@172.31.248.2</strong>
/*e.g.
<strong>$ssh -i ssh_key.pem ubuntu@</strong>

/*One more reboot for good measure
<p class="textbox">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" stop; done
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" start; done</p>
/*List your images
<strong>$glance index</strong>
/*List or edit your flavors
<strong>$nova flavor-list</strong>

<strong>/*If things get squirrely on you restart everything.</strong>
<strong>/etc/init.d/quantum-server restart</strong>
<strong>./restart-nova.sh</strong> &lt;scripted&gt;

/*Boot a VM from CLI or skip to the Dashboard frontend. Hyphens get mangled here so copy paste won't work.
<p class="textbox">/*Ubuntu 11.10
$nova boot - -flavor 1 - -image 3a2404f6-0a4f-44db-b1cd-a81401dd6015 - -key_name ssh_key dem11.10
/* Ubuntu 12.04
$nova boot - -flavor 1 - -image 92ca562e-bb18-425a-94ac-eb292fbcabec - -key_name ssh_key demo12.04</p>
/*Windows 2008 R2
<strong>$nova boot - -flavor 1 - -image 13fdbdb7-0800-4c70-9b6a-73656ca62432 - -key_name ssh_key demoWin2k8</strong>
<p class="textbox">Quicky on building a windows image
/*Create the raw logical disk
kvm-img create -f raw windowsserver.img 20G
/*Boot windows iso along with
kvm -m 1024 -cdrom win2k8_dvd.iso -drive file=windowsserver.img,if=virtio,boot=on -fda virtio-win-1.1.16.vfd -boot d -nographic -vnc :0</p>
<p class="textbox">/*Here is the command used for this image using the virtio iso.
kvm -smp 2 -m 2048 -no-reboot -boot order=d -drive file=win2k8r2_dc.img,if=virtio,boot=off -drive file=windows2k8_dvd.iso,media=cdrom,boot=on -drive file=virtio-win-0.1-22.iso,media=cdrom,boot=off -net nic,model=virtio -nographic -vnc :1</p>
/*Watch your machine boot or error ☺
<strong>$nova show demo1</strong>

/*View all VMs in your Project (Project you have creds in ENV for only)
<strong>$nova list</strong>
<h2><strong>Dashboard</strong></h2>
/*Install packages
<strong>$apt-get install libapache2-mod-wsgi openstack-dashboard</strong>

/*Restart Apache
<strong>$restart apache</strong>
<strong> $service apache2 restart</strong>

/*Connect to the Dashboard web page.
http://localhost or http://x.x.x.x
<h2><strong>Getting to know OVS</strong></h2>
<p class="textbox">Some quick commands to start leveraging a true vSwitch as opposed to Linux bridging. OpenvSwitch is good stuff.
ovs-vsctl list sflow
ovs-ofctl dump-flows
ovs-dpctl dump-flows br0
ovs-vsctl list-br
ovs-vsctl list-ports
ovs-vsctl show
ovs-dpctl show
ovs-ofctl dump-tables br-int
ovs-appctl fdb/show br-int</p>
<a href="{{< relurl "/wp-content/uploads/2012/05/dp-ctl-flows.jpg" >}}"><img class="alignleft  wp-image-620" title="dp-ctl-flows" src="{{< relurl "/wp-content/uploads/2012/05/dp-ctl-flows.jpg" >}}" alt="" width="448" height="202" /></a>
<em></em>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

<em>Figure 2. Example of the Data Path flow dump from 'ovs-dpctl show br-int'.</em>
<h3>Networking command outputs.</h3>
/*Notice there are not any bridges defined in /etc/network/interfaces. I was guessing the brcompat_mod.ko kernel was building that but that module isn't loaded. Must either be loaded into openvswitch_mod.ko or calling brctl. You used to need to unload bridge.ko but I had not used OpenvSwitch since v1.2.
<p class="textbox">~# brctl show
bridge name bridge id STP enabled interfaces
br-int 0000.5c260a5ac8b2 no eth0
gw-0393c785-7f
tap0d144643-96
tapb8d11bf7-94
tape2d5bcc1-9c
virbr0 8000.000000000000 yes</p>
/*View the OpenFlow Controller and classifier tables.
<p class="textbox">ovs-ofctl dump-tables br-int
OFPST_TABLE reply (xid=0x1): 255 tables
0: classifier: wild=0x3fffff, max=1000000, active=10
lookup=764491, matched=757280
1: table1 : wild=0x3fffff, max=1000000, active=0
lookup=0, matched=0
2: table2 : wild=0x3fffff, max=1000000, active=0
lookup=0, matched=0</p>
/Show the forwarding tables
<p class="textbox">$ovs-appctl fdb/show br-int
port VLAN MAC Age
9 2 fa:16:3e:33:4f:e8 37
3 2 fa:16:3e:6f:c0:8b 37
1 0 00:1d:09:aa:71:16 28
1 0 00:e0:1e:5d:86:6f 23
1 0 00:9c:02:b1:ff:c0 19
1 0 00:23:69:62:26:09 18
1 0 00:9c:02:b2:76:c0 17
10 2 fa:16:3e:5f:22:22 15
11 2 fa:16:3e:48:21:4f 4
1 0 00:9c:02:b2:76:e8 3
0 0 5c:26:0a:5a:c8:b2 2
1 0 10:40:f3:94:e0:82 2
1 0 00:26:b9:c0:c8:b0 1</p>