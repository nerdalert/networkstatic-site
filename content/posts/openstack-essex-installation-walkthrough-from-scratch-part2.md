+++
title = "OpenStack Essex Installation Walkthrough from Scratch (Part2)"
date = "2012-05-12T06:18:10+00:00"
lastmod = "2013-04-05T05:08:23+00:00"
author = "Brent Salisbury"
wp_id = 537
categories = ["In the Lab"]
tags = ["OpenStack", "Python", "Tutorials"]
description = ""
url = "/openstack-essex-installation-walkthrough-from-scratch-part2/"
aliases = ["/2012/05/12/openstack-essex-installation-walkthrough-from-scratch-part2/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cf80af57b6db3ea93d348a461fb5320da18d78544a2d89c4752b24d06efe2437"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<em><strong>Update:</strong></em> My latest installation document for Folsom can be found <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}">here</a>. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. Thanks!

http://www.youtube.com/watch?v=fnxWSTuV4FU&amp;hd=1
<h3>Populate Glance Host VM OS Images</h3>
<p class="textbox">/*Upload Images
/* 11.10 image
wget http://uec-images.ubuntu.com/releases/11.10/release/ubuntu-11.10-server-cloudimg-amd64-disk1.img
/* 12.04 image
wget https://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img</p>
$/etc/init.d/glance-api restart
$/etc/init.d/glance-registry restart

/*List Images
$glance index (Should be empty)
<h3>Add Images</h3>
/*If you copy and paste below retype the (") parentheses since the formatting isn't plaint text.
<p class="textbox">/* Add images to Glance
$glance add name="Ubuntu 11.10" is_public=true container_format=ovf disk_format=qcow2 &lt; ubuntu-11.10-server-cloudimg-amd64-disk1.img
/*Uploading image 'Ubuntu 11.10'
============================================[100%] 167.139407M/s, ETA 0h 0m 0s
Added new image with ID: 3a2404f6-0a4f-44db-b1cd-a81401dd6015</p>
<p class="textbox">$glance add name="Ubuntu 12.04" is_public=true container_format=ovf disk_format=qcow2 &lt; precise-server-cloudimg-amd64-disk1.img
Uploading image 'Ubuntu 12.04'
=============================================[100%] 143.583705M/s, ETA 0h 0m 0s
Added new image with ID: 92ca562e-bb18-425a-94ac-eb292fbcabec*/</p>
/* If the image over  ~220Mb you have the wrong image and not Ostack compatible one.
$glance index
<h3>Nova Installation</h3>
<p class="textbox">apt-get install nova-api nova-cert nova-common nova-compute nova-compute-kvm nova-doc nova-network nova-objectstore nova-scheduler nova-vncproxy nova-volume python-nova python-novaclient</p>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; stop; done 
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; start; done</pre>
Manually adding the bridge is typically only necessary if you are trying to use only one NIC. I added it as a reference if anyone ever needed it. Probably not necessary as nova will build your bridge dynamically with an interface config starting that looks like this.
auto lo
<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">iface lo inet loopback
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
$chmod +x &lt;script&gt;
<p class="textbox">/*Add this to /etc/network/interfaces
#Bridged Interfaces
auto br100
iface br100 inet static
bridge_ports eth1
bridge_stp off
bridge_maxwait 0
bridge_fd 0
address 172.31.252.7
netmask 255.255.254.0</p>
/*Add Bridge br100
$brctl addbr br100

/*bring br100 up
$ifconfig br100 up
<p class="textbox">/* Edit /etc/nova/api-paste.ini and add
admin_tenant_name = admin
admin_user = admin
admin_password = openstack</p>
/* Fix Permissions
$chown -R nova:nova /etc/nova

/* Edit /etc/nano.conf <a href="{{< relurl "/wp-content/uploads/2012/08/nova-conf1.txt" >}}" target="_blank">Example-File.</a>
#sync with mysql
$nova-manage db sync

/*Restart Script
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; stop; done 
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; start; done</pre>
<p class="textbox">/*Add your vNIC “Flat Network” as defined in nova.conf. **Below each argument is passed with to dashes "- -". The formatting mangles it. e.g. - - fixed_reange_v4=prefix
$nova-manage network create private --fixed_range_v4=172.31.252.0/23 --num_networks=1 --bridge=br100 --bridge_interface=eth0 --network_size=500</p>
<p class="textbox">/*(Optional) Create a floating pool. Can be any address you want to assign. Essentially NAT.
$nova-manage floating create --ip_range=128.163.188.240/28</p>
/*Check Services
/*Should see something along these lines:
<p class="textbox">$ ps -ea | grep nov
11176 ? 00:00:03 nova-cert
14282 ? 00:00:00 nova-network
14293 ? 00:00:00 nova-compute
14303 ? 00:00:01 nova-api
14313 ? 00:00:00 nova-objectstor
14323 ? 00:00:00 nova-scheduler
14353 ? 00:00:00 nova-xvpvncprox</p>
<p class="textbox">$nova-manage service list
Binary Host Zone Status State Updated_At
nova-scheduler openstack-dev nova enabled :-) 2012-05-10 06:39:29
nova-compute openstack-dev nova enabled :-) 2012-05-10 06:39:09
nova-network openstack-dev nova enabled :-) 2012-05-10 06:39:29</p>
<p class="textbox">/*Bad most of the time. Compute can come in and out of that state and recover.
/*I have never seen network recover, it is normally bad or overburdened and time
to start scouring the logs.
$nova-manage service list
Binary Host Zone Status State Updated_At
nova-scheduler openstack-dev nova enabled :-) 2012-05-10 07:26:29
nova-compute openstack-dev nova enabled XXX 2012-05-10 07:19:20
nova-network openstack-dev nova enabled XXX 2012-05-10 07:21:06</p>
/*Virtual Machines from CLI. Skip if only interested in dashboard.
/*Make sure your nova db has been synced if you skip:

/*If not synced or sure if synced, sync.
$nova-manage db sync
<p class="textbox">/*Create rules for the project
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0</p>
<p class="textbox">nova secgroup-add-rule default tcp 22 22 0.0.0.0/0</p>
/*Windows image
nova secgroup-add-rule default tcp 3389 0.0.0.0/0
<p class="textbox">/*Create security keys
$ nova keypair-add ssh_key &gt; ssh_key.pem</p>
/*Set Permissions
$chmod 0600 ssh_key.pem
<p class="textbox">/*One more restart for good measure</p>

<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; stop; done 
for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service &quot;$a&quot; start; done
/etc/init.d/rabbitmq-server restart</pre>
/*List your images
$glance index

/*List or edit your flavors
$nova flavor-list
<p class="textbox">/*Boot a VM from CLI or skip to the Dashboard frontend.
/*Ubuntu 11.10
$nova boot --flavor 1 --image 3a2404f6-0a4f-44db-b1cd-a81401dd6015 --key_name ssh_key demo
/* Ubuntu 12.04
$nova boot --flavor 1 --image 92ca562e-bb18-425a-94ac-eb292fbcabec --key_name ssh_key demo1</p>
/*Watch your machine boot or error ☺
$nova show demo1

/*View all VMs in your Project (Project you have creds in ENV for only)
$nova list
<p class="textbox">SSH to your new host. If you get public key errors you didn't set your permissions on the key a few steps back.
$ssh -i ssh_key.pem ubuntu@172.31.248.2
or
&gt;$ssh -i ssh_key.pem ubuntu@&lt;your IP&gt;</p>
The final part 3 is <a href="{{< relurl "/2012/05/12/openstack-essex-installation-walkthrough-from-scratch-part3/" >}}">here</a>.