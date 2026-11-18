+++
title = "Troubleshooting Common OpenStack Errors"
date = "2012-05-12T22:56:15+00:00"
lastmod = "2012-12-01T08:13:01+00:00"
author = "Brent Salisbury"
wp_id = 545
categories = ["In the Lab"]
tags = ["OpenStack", "Tutorials"]
description = ""
url = "/troubleshooting-common-openstack-errors/"
aliases = ["/2012/05/12/troubleshooting-common-openstack-errors/"]
image = "/wp-content/uploads/2012/05/openstack-logo-shade.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "efbbf3ed7d06055b3ab9e321d8bf304f2eb008821084a667213cadd7701b683f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Troubleshooting Common OpenStack Errors</h2>
These are some notes from troubleshooting common OpenStack Errors that I have run into in the past year. These were mostly from Diablo and Essex but some are applicable to future releases especially surrounding Nova.

/*Check all services
$nova-manage service list (check for XXX or smiley face)
Binary Host Zone Status State Updated_At
nova-scheduler openstack1 nova enabled : - ) 2012-05-12 22:42:14
nova-compute openstack1 nova enabled : - ) 2012-05-12 22:42:12
nova-network openstack1 nova enabled : - ) 2012-05-12 22:42:14

$ ps -ea | grep nova
11448 ? 00:02:54 nova-cert
12072 ? 00:02:57 nova-network
12083 ? 00:10:31 nova-compute
12093 ? 00:06:40 nova-api
12117 ? 00:02:26 nova-scheduler
12154 ? 00:00:00 nova-xvpvncprox
55746 ? 00:00:00 nova-objectstor

If you are missing services or an XXX check the logs and look for errors i.e.
nova-compute openstack1 nova enabled XXX 2012-05-12 22:42:12
$tail –n 400 /var/log/nova-compute
<h4><strong>Common Errors</strong></h4>
Errors:
thon2.7/dist-packages/nova/virt/libvirt/connection.py", line 338, in _connect
2012-05-09 17:05:42 TRACE nova return libvirt.openAuth(uri, auth, 0)
2012-05-09 17:05:42 TRACE nova File "/usr/lib/python2.7/dist-packages/libvirt.py", line 102, in openAuth
2012-05-09 17:05:42 TRACE nova if ret is None:raise libvirtError('virConnectOpenAuth() failed')
2012-05-09 17:05:42 TRACE nova libvirtError: Failed to connect socket to '/var/run/libvirt/libvirt-sock': No such file or directory
012-05-09 22:05:41.909+0000: 12466: info : libvirt version: 0.9.8
2012-05-09 22:05:41.909+0000: 12466: error : virNetServerMDNSStart:460 : internal error Failed to create mDNS client: Daemon not running
Look in:
root@:/home/brent/openstack# cat /var/log/libvirt/libvirtd.log

Solution:
libvirt-bin service will not start without dbus installed.

Make sure dbus is running ps –ea |grep dbus
And
sudo apt-get install lxc

https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/918343
<h4><strong>Failed to Add Image</strong></h4>
Error
Failed to add image. Got error: The request returned 500 Internal Server Error

Solution:
Fix the OS ENV variables (insert your values from your API configs.)
e.g.
declare -x OS_AUTH_KEY="openstack"
declare -x OS_AUTH_URL="http://localhost:5000/v2.0/"
declare -x OS_PASSWORD="openstack"
declare -x OS_TENANT_NAME="admin"
declare -x OS_USERNAME="admin"
<h4><strong>Nova Instance Not Found</strong></h4>
Local file storage of the image files.

Error:
2012-05-09 17:58:08 TRACE nova raise exception.InstanceNotFound(instance_id=instance_name)
2012-05-09 17:58:08 TRACE nova InstanceNotFound: Instance instance-00000002 could not be found.
2012-05-09 17:58:08 TRACE nova

Solution:
Logs are at
cat /var/log/libvirt/libvirtd.log

either delete the instance in MySQL or drop the database and start a new one. Here is dropping the DB for testing.
$mysql –u root –p
DROP DATABASE nova;

Recreate the DB:
CREATE DATABASE nova; (strip formatting if you copy and paste any of this)
GRANT ALL PRIVILEGES ON nova.* TO 'novadbadmin'@'%' IDENTIFIED BY '&lt;password&gt;';
Quit

Resync DB
$nova-manage db sync
Restart Nova
$for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" stop; done
$for a in libvirt-bin nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-vncproxy; do service "$a" start; done

Regen keys
$nova keypair-add ssh_key &gt; ssh_key.pem

re-apply security policy.
$nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0
$nova secgroup-add-rule default tcp 22 22 0.0.0.0/0

$Add network back. nova-manage add etc.

Gut libvirt for any remnants of the machine. There are ways to recover a VM I have seen in the oStack channel if someone needs a hand. I just dont have the notes on me.

$rm -rf /etc/libvirt/qemu/instance-00000043.xml
$rm -rf/var/lib/libvirt/qemu/instance-00000043.monitor
$rm -rf/var/lib/nova/instances/instance-00000043
$rm -rf/var/lib/nova/instances/instance-00000043/console.log
$rm -rf/var/lib/nova/instances/instance-00000043/disk
$rm -rf/var/lib/nova/instances/instance-00000043/libvirt.xml
$rm -rf/var/log/libvirt/qemu/instance-00000043.log

Restart (maybe not nessecary)
/etc/init.d/libvirt-bin

Check libvirt logs for errors after restart:
tail -n 200 cat /var/log/libvirt/libvirtd.log
<h4><strong>KeyStone NoHandlers</strong></h4>
Error
root@openstack-dev-r910:/home/brent/openstack# ./keystone_data.sh
No handlers could be found for logger "keystoneclient.client"
Unable to authorize user
No handlers could be found for logger "keystoneclient.client"
Unable to authorize user
No handlers could be found for logger "keystoneclient.client"
Unable to authorize user

Fix:
Adjust the admin token to be the same as your script and your /etc/keystone/keystone.conf

Also make sure keystone.conf has the following.

driver = keystone.catalog.backends.templated.TemplatedCatalog
template_file = /etc/keystone/default_catalog.templates

Someone say pain in the ass?
<h4>ERROR: string indices must be integers, not str</h4>
Fix
/etc/nova/nova-api.con
Add acocunts at bottom
<h4>Rebuilding Nova</h4>
Deleting Nova and re-installing along with some of the file locations.
apt-get purge nova-api nova-cert nova-common nova-compute nova-compute-kvm nova-doc nova-network nova-objectstore nova-scheduler nova-vncproxy nova-volume python-nova python-novaclient

nova-manage project scrub nova (or) drop database nova

mysqlshow --count glance

$rm -rf /root/.novaclient/
$rm -rf /var/lib/nova
$rm -rf /var/lib/mysql/nova
$rm -rf /etc/libvirt/nwfilter/nova*

MySQL –u name -r
Drop database nova;
CREATE DATABASE nova;
GRANT ALL PRIVILEGES ON nova.* TO 'novadbadmin'@'%'
IDENTIFIED BY 'openstack';

killall dnsmasq
service nova-network restart

ps -ea | grep key
ps -ea | grep nova
ps -ea | grep gl root@openstack1:/home/brent/openstack# apt-get install -y mysql-server python-mysqldb mysql-common

ance
ps -ea | grep libv

/var/log/nova/nova-api.log
/var/log/nova/nova-cert.log
/var/log/nova/nova-compute.log
/var/log/nova/nova-dhcpbridge.log
/var/log/nova/nova-manage.log
/var/log/nova/nova-network.log
/var/log/nova/nova-objectstore.log
/var/log/nova/nova-scheduler.log
/var/log/nova/nova-volume.log
/var/log/nova/nova-xvpvncproxy.log
/var/log/upstart/nova-api.log
/var/log/upstart/nova-cert.log
/var/log/upstart/nova-compute.log
/var/log/upstart/nova-network.log
/var/log/upstart/nova-objectstore.log
/var/log/upstart/nova-scheduler.log
/var/log/upstart/nova-vncproxy.log
/var/log/upstart/nova-volume.log
/var/crash/_usr_bin_nova-api.114.crash
/var/crash/_usr_bin_nova-compute.114.crash
/var/crash/_usr_bin_nova-network.114.crash
/var/crash/_usr_bin_nova-objectstore.114.crash
/var/crash/_usr_bin_nova-scheduler.114.crash
/var/crash/_usr_bin_nova-xvpvncproxy.114.crash
<h4>Clean Up Scripted Prior to Re-Install</h4>
#!/bin/bash
mysql -uroot -popenstack -e "drop database nova;"
mysql -uroot -popenstack -e "drop database glance;"
mysql -uroot -popenstack -e "drop database keystone;"
apt-get purge nova-api nova-cert nova-common nova-compute
nova-compute-kvm nova-doc nova-network nova-objectstore
nova-scheduler nova-vncproxy nova-volume python-nova python-novaclient
apt-get autoremove
rm -rf /var/lib/glance
rm -rf /var/lib/keystone/
rm -rf /var/lib/nova/
rm -rf /var/lib/mysql
<h4>Instance not found (duplicate)</h4>
Sometimes things go screwy as you are testing things and compute can crash leaving a headless instance out there. Track down the instance files and delete them and drop the database and rebuild it.

Errors:
Invalid: Instance has already been created
InstanceNotFound: Instance instance-00000001 could not be found.

/var/lib/nova/instances/instance-000000ed/libvirt.xml
/var/lib/nova/instances/instance-000000f5/console.log
/var/lib/nova/instances/instance-000000f5/disk
/var/lib/nova/instances/instance-000000f5/libvirt.xml
/var/log/libvirt/qemu/instance-00000001.log
/var/log/libvirt/qemu/instance-00000002.log
/var/log/libvirt/qemu/instance-00000003.log
/var/log/libvirt/qemu/instance-00000004.log
/etc/libvirt/nwfilter/nova-instance-instance-000000bd-fa163e668ec9.xml
/etc/libvirt/nwfilter/nova-instance-instance-000000c3-fa163e5b0541.xml
/etc/libvirt/nwfilter/nova-instance-instance-000000c9-fa163e77d2c5.xml

$rm –f /var/log/libvirt/qemu/instance*
$rm –f /etc/libvirt/nwfilter/nova*
$rm –f /var/lib/nova/instances/instance-*
$rm –f /var/log/libvirt/qemu/inst*
$rm -f /etc/libvirt/nwfilter/nova-*

$mysql -u root -p
drop database nova;

Then recreate the DB.
/*Re-create the Nova database
CREATE DATABASE nova;
GRANT ALL PRIVILEGES ON nova.* TO 'novadbadmin'@'%' IDENTIFIED BY 'password';

Maybe restart for good measure before a resync.

$nova-manage db sync
<h4>Keystone: ValueError: you need to pass either an existing engine or a database uri</h4>
Problem:~# keystone-manage db_sync

File "/usr/lib/python2.7/dist-packages/migrate/versioning/util/__init__.py", line 116, in construct_engine
raise ValueError("you need to pass either an existing engine or a database uri")
ValueError: you need to pass either an existing engine or a database uri

Resolution:

Check Keystone.conf

Make sure it looks like this: connection = mysql://keystone:openstack@localhost:3306/keystone

Not that is for glance.registry :/  mysql_connection = mysql://keystone:openstack@localhost:3306/keystone
<h4>No handlers could be found for logger "keystoneclient.client"</h4>
Problem: No handlers could be found for logger "keystoneclient.client"
Authorization Failed: Unable to communicate with identity service: '\xe2\x80\x9dhttp'. (HTTP 400)

Resolution: Make sure you have the following variables:

root@openstack1:~# export SERVICE_TOKEN=openstack
root@openstack1:~# export OS_TENANT_NAME=admin
root@openstack1:~# export OS_USERNAME=admin
root@openstack1:~# export OS_PASSWORD=openstack
root@openstack1:~# export OS_AUTH_URL=”http://localhost:5000/v2.0/”
root@openstack1:~# export SERVICE_ENDPOINT=http://localhost:35357/v2.0
root@openstack1:~# keystone user-list
+----------------------------------+---------+--------------------+---------+
| id | enabled | email | name |
+----------------------------------+---------+--------------------+---------+
| 149136826c504aaf896645ee169aec7b | True | glance@domain.com | glance |
| 6ba91505d57a44b3abff9c957d10b463 | True | nova@domain.com | nova |
| bba82931db1a4236a6af9e377ab1aebb | True | admin@domain.com | admin |
| bd36f79a3708445593200b50a32b4127 | True | quantum@domain.com | quantum |
| d49d9dda0b95496594f0d142c5f25d22 | True | demo@domain.com | demo |
| f0c159e20b244477b02ae448b8029051 | True | swift@domain.com | swift |
+----------------------------------+---------+--------------------+---------+

&nbsp;
<h4>Access denied for user 'keystone'@'openstack1' (using password: YES)")</h4>
Problem:# keystone-manage db_sync

File "/usr/lib/python2.7/dist-packages/MySQLdb/connections.py", line 187, in __init__
super(Connection, self).__init__(*args, **kwargs2)
sqlalchemy.exc.OperationalError: (OperationalError) (1045, "Access denied for user 'keystone'@'openstack1' (using password: YES)") None None

Make sure you keystone.conf looks like this.

[sql]
connection = mysql://keystone:openstack@localhost:3306/keystone
<h4>Connect error/bad request to Auth service at URL %(url)s.</h4>
Problem $ glance index
Failed to show index. Got error:
Connect error/bad request to Auth service at URL %(url)s.

Resolution: Make sure you have "SERVICE_ENDPOINT" and "OS_AUTH_URL" exported.

export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0

Thanks for stopping by.