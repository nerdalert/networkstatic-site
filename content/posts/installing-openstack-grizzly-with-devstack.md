+++
title = "Installing OpenStack Grizzly with DevStack"
date = "2013-04-08T06:53:22+00:00"
lastmod = "2014-02-18T02:57:11+00:00"
author = "Brent Salisbury"
wp_id = 6212
categories = ["Speculative"]
tags = ["DevStack", "Open vSwitch", "OpenStack"]
description = ""
url = "/installing-openstack-grizzly-with-devstack/"
image = "/wp-content/uploads/2013/04/unicorn-accountant.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "baa1e89132687ee8587df6b35dd634a97d3b117b61f6882756fc69ed852fd989"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenStack Multi-Node DevStack Nova Network Tutorial</h2>

DevStack is a scripted OpenStack installer  maintained for developers to prototype and debug. It is also handy for operators to proof concepts and test new services and configurations. This is a good starter for folks new to OpenStack to help understand how to install and operate OpenStack. Some folks have been asking about multi-node DevStack deployment using nova network, so I thought this tutorial might help.

Another difference in this tutorial. is using nova-network instead of the Quantum network plugin. The Quantum plugin is very flexible and offers much richer networking feature, by implementing vSwitches, rather then Linux bridging. With flexibility, comes complexity.The reality if most people looking to do test deployments, proof of concepts or richer KVM/XEN hypervisor management do not really need the added complexity. Nova-network is slated for depreciation at some point, but I am not sure that is the best plan of action for typical until the installation becomes easier for folks in my humble opinion. Most enterprises don't have "DevOps" programmers, and I think OpenStack brings some good value and expenditure savings to the enterprise. The complexity of the advanced networking may turn some folks off to the project in smaller organizations. Then again smaller organizations aren't the ones running OpenStack and that may be attractive to vendors looking to find revenue from service offerings. Anywho, thats my two cents, let's get on to the tutorial.
<h2>OpenStack Flat Network Manager Topology</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/OpenStack-Flat-Network-Manager.jpg" >}}" alt="OpenStack Flat Network Manager Topology"></figure>

<strong>Figure 1.</strong> Flat Network Manager Topology
<h2>Configuring DevStack Installation</h2>
DevStack is not a persistent installation, meaning it will be erased when you run ./unstack.sh. This works fine on a single machine running in VMfusion since it supports nested virtualization.
<pre class="code-sample"><code> % git clone https://github.com/openstack-dev/devstack.git
% cd devstack</code></pre> 
Create a file called localrc for the controller and compute node and fill it in with the localrc configurations below. Change the IP addresses to match your addressing. Put the localrc file in the root of the DevStack folder.
<pre class="code-sample"><code>  % ./stack.sh</code></pre> 
After that is complete, if you do not have any errors you should have a functioning controller and working compute node(s). The compute nodes run the guest VMs. The compute node also does the NAT and security functionality. That can be configuring in the web GUI or from CLI. Your Floating Range will be your publicly reachable network. The fixed range is for the guest VM to talk to the compute node for resources. Since we are using one NIC in each machine, all of the addresses on the compute node are bound to the br100 bridge that is in turn bound to eth0 as secondary addresses. Everything is sharing the same broadcast domain on br100. It is fairly confusing for many without a strong networking background, albeit much simpler than Quantum services. The more you dig in and explore, the clearer it will inevitably become.

When installing note the path of the logs. This is helpful for reverse engineering the installation and troubleshooting services while stack.sh is running. Logs are not dumped to /var/log/nova* like a regular installation.
<h2>OpenStack Controller localrc</h2>
Place this in a file named localrc in the root of the devstack directory you clone. That installs into the /opt/ directory be default.
<pre class="code-sample"><code> ## Controller Host ##
 HOST_IP=192.168.1.10
 MULTI_HOST=1
## Network nova-network ##
 FLAT_INTERFACE=eth0
 FIXED_RANGE=172.24.17.0/24
 FIXED_NETWORK_SIZE=254
 FLOATING_RANGE=192.168.1.128/25
## Leaving Default Services Enabled ##
 DISABLED_SERVICES=quantum
## Logs ##
 LOGFILE=/opt/stack/logs/stack.sh.log
 VERBOSE=True
 LOG_COLOR=False
 SCREEN_LOGDIR=/opt/stack/logs</code></pre> 
<h2>OpenStack Controller Node nova.conf</h2>
nova.conf is located in /etc/nova/nova.conf
<pre class="code-sample"><code> [DEFAULT]
 verbose=True
 auth_strategy=keystone
 allow_resize_to_same_host=True
 api_paste_config=/etc/nova/api-paste.ini
 rootwrap_config=/etc/nova/rootwrap.conf
 compute_scheduler_driver=nova.scheduler.filter_scheduler.FilterScheduler
 dhcpbridge_flagfile=/etc/nova/nova.conf
 force_dhcp_release=True
 fixed_range=172.24.17.0/24
 default_floating_pool=nova
 s3_host=192.168.1.10
 s3_port=3333
 osapi_compute_extension=nova.api.openstack.compute.contrib.standard_extensions
 my_ip=192.168.1.11
 sql_connection=mysql://root:password@192.168.1.10/nova?charset=utf8
 libvirt_type=kvm
 libvirt_cpu_mode=none
 instance_name_template=instance-%08x
 enabled_apis=ec2,osapi_compute,metadata
 state_path=/opt/stack/data/nova
 lock_path=/opt/stack/data/nova
 instances_path=/opt/stack/data/nova/instances
 multi_host=True
 send_arp_for_ha=True
 logging_context_format_string=%(asctime)s %(levelname)s %(name)s [%(request_id)s %(user_name)s %(project_name)s] %(instance)s%(message)s
 network_manager=nova.network.manager.FlatDHCPManager
 public_interface=br100
 vlan_interface=eth0
 flat_network_bridge=br100
 flat_interface=eth0
 novncproxy_base_url=http://192.168.1.10:6080/vnc_auto.html
 xvpvncproxy_base_url=http://192.168.1.10:6081/console
 vncserver_listen=127.0.0.1
 vncserver_proxyclient_address=127.0.0.1
 ec2_dmz_host=192.168.1.10
 rabbit_host=192.168.1.10
 rabbit_password=password
 glance_api_servers=192.168.1.10:9292
 compute_driver=libvirt.LibvirtDriver
 firewall_driver=nova.virt.libvirt.firewall.IptablesFirewallDriver</code></pre> 
<h2>OpenStack Compute localrc</h2>
Place this in a file named localrc in the root of the devstack directory you clone. That installs into the /opt/ directory be default.
<pre class="code-sample"><code> ## Compute Host ##
 #SERVICE_HOST_NAME=controller
 SERVICE_HOST=192.168.1.10
 HOST_IP=192.168.1.11
 MULTI_HOST=1
## Network nova-network ##
 FLAT_INTERFACE=eth0
 FIXED_RANGE=172.24.17.0/24
 FIXED_NETWORK_SIZE=254
 FLOATING_RANGE=192.168.1.128/25
## Compute Node Services ##
 ENABLED_SERVICES=n-cpu,n-net,n-api,n-vol
## API URIs ##
 Q_HOST=$SERVICE_HOST
 MYSQL_HOST=$SERVICE_HOST
 RABBIT_HOST=$SERVICE_HOST
 GLANCE_HOSTPORT=$SERVICE_HOST:9292
 KEYSTONE_AUTH_HOST=$SERVICE_HOST
 KEYSTONE_SERVICE_HOST=$SERVICE_HOST
## Auth ##
 ADMIN_PASSWORD=password
 MYSQL_PASSWORD=password
 RABBIT_PASSWORD=password
 SERVICE_PASSWORD=password
 SERVICE_TOKEN=password
## Logs ##
 LOGFILE=/opt/stack/logs/stack.sh.log
 VERBOSE=True
 LOG_COLOR=False
 SCREEN_LOGDIR=/opt/stack/logs</code></pre> 
<h2>OpenStack Compute Node nova.conf</h2>
nova.conf is located in /etc/nova/nova.conf
<pre class="code-sample"><code> [DEFAULT]
 verbose=True
 auth_strategy=keystone
 allow_resize_to_same_host=True
 api_paste_config=/etc/nova/api-paste.ini
 rootwrap_config=/etc/nova/rootwrap.conf
 compute_scheduler_driver=nova.scheduler.filter_scheduler.FilterScheduler
 dhcpbridge_flagfile=/etc/nova/nova.conf
 force_dhcp_release=True
 fixed_range=172.24.17.0/24
 default_floating_pool=nova
 s3_host=192.168.1.10
 s3_port=3333
 osapi_compute_extension=nova.api.openstack.compute.contrib.standard_extensions
 my_ip=192.168.1.11
 sql_connection=mysql://root:password@192.168.1.10/nova?charset=utf8
 libvirt_type=kvm
 libvirt_cpu_mode=none
 instance_name_template=instance-%08x
 enabled_apis=ec2,osapi_compute,metadata
 state_path=/opt/stack/data/nova
 lock_path=/opt/stack/data/nova
 instances_path=/opt/stack/data/nova/instances
 multi_host=True
 send_arp_for_ha=True
 logging_context_format_string=%(asctime)s %(levelname)s %(name)s [%(request_id)s %(user_name)s %(project_name)s] %(instance)s%(message)s
 network_manager=nova.network.manager.FlatDHCPManager
 public_interface=br100
 vlan_interface=eth0
 flat_network_bridge=br100
 flat_interface=eth0
 novncproxy_base_url=http://192.168.1.10:6080/vnc_auto.html
 xvpvncproxy_base_url=http://192.168.1.10:6081/console
 vncserver_listen=127.0.0.1
 vncserver_proxyclient_address=127.0.0.1
 ec2_dmz_host=192.168.1.10
 rabbit_host=192.168.1.10
 rabbit_password=password
 glance_api_servers=192.168.1.10:9292
 compute_driver=libvirt.LibvirtDriver
 firewall_driver=nova.virt.libvirt.firewall.IptablesFirewallDriver</code></pre> 
<h2>SSH Keys and Booting a Guest VM</h2>
<pre class="code-sample"><code> nova keypair-add ssh_key &gt; ssh_key.pem &gt; ~/ssh_key.pem
chmod 0600 ~/ssh_key.pem</code></pre> 
<h2>OpenStack Glance Guest VM Images</h2>
DevStack will download CirrOS but in case it doesn't or you want to install another image like the Ubuntu Cloud image you can do the follwing.

<em>Download a pre-built OpenStack ready image:</em>
<pre class="code-sample"><code> #Download Ubuntu 12.04 (The default login for this image is &quot;ubuntu&quot;)
 % wget https://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img
 #or:
 #Download CirrOS 0.3 (The default login is &quot;cirros&quot;)
 % wget https://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img</code></pre> 
Import the downloaded image into Glance
<pre class="code-sample"><code> % glance add name=Ubuntu-12.04 is_public=true container_format=ovf \
 disk_format=qcow2 &lt; precise-server-cloudimg-amd64-disk1.img
% glance add name=CirrOS-0.3.0 is_public=true container_format=ovf \
 disk_format=qcow2 &lt; cirros-0.3.0-x86_64-disk.img
#Verify image imports with % glance index</code></pre> 

<h2>Verifying OpenStack Services</h2>
If you get errors stating you are not authorized or don't have permsissions to use the client tools, verify your environmental variables are set by typing export. Manually add ENVs with the following.

<pre class="code-sample"><code> export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0</code></pre> 

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/nova-manage-OpenStack.jpg" >}}" alt="OpenStack nova-manage"></figure>

<strong>Figure 2.</strong> Viewing processes running in DevStack with 'nova-manage service list' ': -)' means the process is functioning. 'XXX' means the process has died.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/OpenStack-PS.jpg" >}}" alt="OpenStack Processes"></figure>
<strong> Figure 3</strong>. View running procs in Linux with 'ps auxw'.
<h2>Nova-Network Configuration</h2>
DevStack will build your network as specified in the localrc. The manual operations of that are as follows:
<pre class="code-sample"><code> #Create the private address space where guest VMs will reside.
 % nova-manage network create private 172.24.17.0/24 1 254
#Create the floating address pool and associate it to an object named Nova for something meaningful to tenants.
 % nova-manage floating create 192.168.1.128/25 --pool=nova</code></pre> 
Since we are only using one NIC in this interface, we will have both the Flat Interface (Public) and the Fixed Range (Privates for VMs) bound to br0100.
<pre class="code-sample"><code> % ip addr show
br100: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc noqueue state UP
 link/ether 00:0c:29:65:fd:82 brd ff:ff:ff:ff:ff:ff
 inet 172.24.17.3/24 brd 172.24.17.255 scope global br100
 inet 192.168.1.11/24 brd 192.168.1.255 scope global br100
 inet 192.168.1.129/32 scope global br100
 inet6 fe80::d4ee:3cff:fef2:556d/64 scope link
 valid_lft forever preferred_lft forever</code></pre> 
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/OpenStack-Nova-Network-Topology.jpg" >}}" alt="OpenStack Processes"></figure>
<strong>Figure 4.</strong> View the Linux routing tables 'route -n'.

To view the Linux bridge configuration use the brctl command. If for some reason DevStack doesn't create the bridge br100, you can define it yourself with 'brctl add-br br100' and 'brctl addif br100 eth0'. Remember, eth0 is nested in br100. That becomes your Layer3 interface.
<pre class="code-sample"><code> % brctl show
 bridge   name         bridge id STP enabled interfaces
 br100 8000.000c2965fd82 no eth0
 vnet0</code></pre> 
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/01/brctl-show-openstack.jpg" >}}" alt="OpenStack Brctl"></figure>
<p style="text-align: left;"><strong>Figure 5.</strong> Linux bridge output from 'brctl'</p>

<h2>10 Quick OpenStack Operational Notes</h2>
<ol class="legacy-numbers">
<ol>
	<li>At anytime you can check to make sure the services show smiley faces :-) and not XXX with 'nova-manage service list'.</li>
	<li>To manually boot an image, running 'glance index' and copy the ID of the image that was loaded in the script.</li>
	<li>nova boot --flavor 1 --image &lt;insert image ID here&gt; --key_name ssh_key demohost</li>
	<li>Run 'nova list' to check the progress and look for any errors.</li>
	<li>After a couple of minutes the instance will be booted, make sure you can ping it.</li>
	<li>SSH to the ubuntu instance by running "ssh -i ~/ssh-key.pem ubuntu@&lt;ip in nova list&gt;" The key was created by the script.</li>
	<li>Check out the web page with http://localhost or http://&lt;public address used&gt;</li>
	<li>Under the "Admin" project in Dashboard (the webpage) go to security and access and allocate a floating address to your project.</li>
	<li>Once allocated to the project, allocate the address to your VM you started.</li>
	<li>Running ./unstack will unload DevStack. Running ./stack.sh will rebuild the stack.</li>
</ol>
</ol>
<h2>Additional DevStack Resources</h2>
<aside class="legacy-callout">
<ul>
	<li><a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}" target="_blank">OpenStack Folsom Quantum Devstack Installation</a>: For a how-to and screencast using DevStack and Quantum.</li>
	<li><a href="http://www.slideshare.net/mestery/openstack-development-using-devstack" target="_blank">OpenStack Development Using DevStack</a>: For a nice presentation on DevStack from <a href="http://www.siliconloons.com" target="_blank">Kyle Mestery</a> <a href="https://twitter.com/mestery" target="_blank">@mestery</a>.</li>
	<li><a href="http://devstack.org/stack.sh.html" target="_blank">DevStack Code</a>: Reviewing the code is a really great way to get to understanding the script. DevStack Website</li>
	<li><a href="http://docs.openstack.org" target="_blank">OpenStack Documentation</a>: This has remarkably improved.</li>
</ul>
</aside>

<hr />

Thanks for stopping by.

<hr />