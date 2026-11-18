+++
title = "Updated DevStack OpenDaylight VM Image for OpenStack IceHouse"
date = "2014-05-05T19:46:05+00:00"
lastmod = "2015-02-25T07:08:53+00:00"
author = "Brent Salisbury"
wp_id = 7374
categories = ["In the Lab", "Programming"]
tags = ["Java", "Open vSwitch", "OpenDaylight", "OpenStack", "Python"]
description = ""
url = "/updated-devstack-opendaylight-vm-image-for-openstack-icehouse/"
image = "/wp-content/uploads/2012/11/openstack-devstack-crop.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "0566739ad8e7974243afbd0be459818ce86b8573e84dd98523adea8802f8faad"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Updated DevStack OpenDaylight VM Image for OpenStack</h2>

Here is an updated Fedora 20 image for building OpenStack Icehouse and OpenDaylight. ODL is now merged into the upcoming OpenStack Icehouse release so now you can install ODL directly from OpenStack trunk. The updated image comes from Kyle Mestery who was primarily responsible for getting the OpenStack/OpenDaylight merge and navigating the process. Thanks also to Andrew Grimberg from the Linux Foundation with assisting with getting testing setup and all the code contributors from the community.  

We have some cool new stuff that we are working on for the Helium release that leverages more of the killer work from the Open vSwitch community that we are integrating into the ODL (Network Virtualization) OVSDB plugin along with integrating some services into the network pipeline of OVS. We see this as worthwhile in bringing some coherency to the network operations of Neutron by unifying some of the OpenStack services into the application aware, flow forwarding pipeline.

<h2>Download the VM and Follow the Existing Instructions</h2>

Download the latest image from the OpenDaylight Wiki. It is around 2.28GB compressed. It has all OpenStack dependancies taken care of. The only changes required are copying the compute local conf for the compute node and replacing the IP addresses as indicated in the file where we put <COntroller-IP-Goes-Here>. Also some slides we have with further instructions <a href="http://www.slideshare.net/mestery/opendaylight-integration-with-openstack-neutron-a-tutorial">here</a>. Download the Image from below:
<a href="https://wiki.opendaylight.org/images/HostedFiles/Fedora20_ODL_OpenStack.zip" target="_blank" rel="noopener noreferrer">Updated DevStack OpenDaylight VM Image for OpenStack IceHouse</a>

Use the existing instructions from the last post as that has all stayed the same except now the controller is downloaded for you as part of the DevStack build. If you want to use an external controller see Kyle's blog post below. It is simply a flag in the local.conf build pointing to the external API/URI.

There is one error you will hit the first time you ./stack.sh with the volume groups. The work around is to simply ./unstack.sh and ./stack.sh again to resolve them. The error appears as follows:

<pre class="code-sample"><code>
2014-05-26 16:18:57.027 | + sudo vgs stack-volumes
2014-05-26 16:18:57.041 |   Volume group "stack-volumes" not found
2014-05-26 16:18:57.044 |   Skipping volume group stack-volumes
2014-05-26 16:18:57.046 | + sudo vgcreate stack-volumes /dev/loop0
2014-05-26 16:18:57.053 |   A volume group called stack-volumes already exists.
2014-05-26 16:18:57.055 | + exit_trap </code></pre>

The other difference from the original post is that the ML2 update will actually download the ODL virtualization build for you and spin it up on the OpenStack controller instance. If you want to run ODL in a separate VM/instance, you can setup your local.conf to do so. Below is an example OpenStack controller and compute local.conf I use:


Controller local.conf: OpenStack Controller (192.168.1.49) - OpenDaylight Controller (192.168.1.47) 
<pre class="code-sample"><code>
[[local|localrc]]
LOGFILE=stack.sh.log
SCREEN_LOGDIR=/opt/stack/data/log
LOG_COLOR=False
OFFLINE=True
#RECLONE=yes

# Only uncomment the below two lines if you are running on Fedora
disable_service rabbit
enable_service qpid
#disable_service n-cpu
enable_service n-cpu
enable_service n-cond
disable_service n-net
enable_service q-svc
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service quantum
enable_service tempest


Q_HOST=$SERVICE_HOST
HOST_IP=192.168.1.49

Q_PLUGIN=ml2
Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight,logger
# This tells DevStack to look for ODL running on an external host
ODL_MGR_IP=192.168.1.47
ENABLE_TENANT_TUNNELS=True
enable_service odl-server odl-compute
ODL_BOOT_WAIT=20

VNCSERVER_PROXYCLIENT_ADDRESS=192.168.56.135
VNCSERVER_LISTEN=0.0.0.0

HOST_NAME=fedora-odl-1
SERVICE_HOST_NAME=${HOST_NAME}
SERVICE_HOST=192.168.1.49

#FLOATING_RANGE=192.168.210.0/24
#PUBLIC_NETWORK_GATEWAY=192.168.75.254
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
RABBIT_PASSWORD=rabbit
QPID_PASSWORD=rabbit
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin

[[post-config|/etc/neutron/plugins/ml2/ml2_conf.ini]]
[agent]
minimize_polling=True

[ml2_odl]
url=http://192.168.1.47:8080/controller/nb/v2/neutron
username=admin
password=admin
</code></pre>

Controller local.conf: OpenStack Compute (192.168.1.50) - OpenDaylight Controller (192.168.1.47) 
<pre class="code-sample"><code>
[[local|localrc]]
LOGFILE=stack.sh.log
LOG_COLOR=True
SCREEN_LOGDIR=/opt/stack/data/log
OFFLINE=true
#RECLONE=yes

enable_service odl-compute
ODL_MGR_IP=192.168.1.47

disable_all_services
enable_service nova n-cpu quantum n-novnc qpid odl-compute

HOST_NAME=fedora-odl-2
HOST_IP=192.168.1.50
SERVICE_HOST_NAME=fedora-odl-1
SERVICE_HOST=192.168.1.49
VNCSERVER_PROXYCLIENT_ADDRESS=192.168.1.49
VNCSERVER_LISTEN=0.0.0.0

FLOATING_RANGE=192.168.210.0/24

Q_PLUGIN=ml2
Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight,logger
ENABLE_TENANT_TUNNELS=True
Q_HOST=$SERVICE_HOST

MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST

MYSQL_PASSWORD=mysql
RABBIT_PASSWORD=rabbit
QPID_PASSWORD=rabbit
SERVICE_TOKEN=service
SERVICE_PASSWORD=admin
ADMIN_PASSWORD=admin

[[post-config|/etc/neutron/plugins/ml2/ml2_conf.ini]]
[agent]
minimize_polling=True

[ml2_odl]
url=http://192.168.1.47:8080/controller/nb/v2/neutron
username=admin
password=admin</code></pre>


<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}" target="_blank" rel="noopener noreferrer">OpenDaylight OpenStack Integration with DevStack on Fedora</a>

See Kyle's post for details on the local.conf configurations and more SiliconLoon goodness at:

<a href="http://www.siliconloons.com/opendaylight-integration-with-openstack-has-merged-into-icehouse/" target="_blank" rel="noopener noreferrer">OpenDaylight Integration with OpenStack has merged into Icehouse!</a>

<h2>Getting Help with the OpenStack Configuration</h2>
If you have any issues you can get assistance via the OVSDB plugin <a href="https://lists.opendaylight.org/mailman/listinfo/ovsdb-dev" target="_blank">listserv</a> or check the archives <a href="https://lists.opendaylight.org/pipermail/ovsdb-dev/" target="_blank">here</a>. For realtime assistance ping myself in IRC or studs like, Madhu Venugopal, Kyle Mestery, Thomas Bachman, Dave Tucker or any of the other freakishly passionate community in the IRC channel #opendaylight-ovsdb on irc.freenode.net. 

Thanks for stopping by!