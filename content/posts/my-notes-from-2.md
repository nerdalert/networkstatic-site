+++
title = "OpenStack on Ubuntu 11.10 Installation"
date = "2012-02-01T16:43:46+00:00"
lastmod = "2013-01-01T08:29:20+00:00"
author = "Brent Salisbury"
wp_id = 132
categories = ["In the Lab"]
tags = ["KVM", "OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/my-notes-from-2/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "f72acb24b2e10482c3690d0e8b365b1b3db2700e329876096eb4caa9b6b7561e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<aside class="legacy-callout"><strong>&lt;em&gt;&lt;strong&gt;Update:&lt;/strong&gt;&lt;/em&gt;</strong> My latest installation document for Folsom can be found at the post <a href="{{< relurl "/openstack-folsom-quantum-devstack-installation-tutorial/" >}}">OpenStack Folsom Quantum Devstack Installation Tutorial and Screencast</a>. It's too tough to try and keep up with debugging installers myself so I am just using DevStack in that tutorial. Thanks!</aside>

My notes from an OpenStack &amp; Ubuntu 11.10. These are only my notes. Lots of errors. It was a fairly painless install. I didnt have the lab gear setup with two Nics so I got a bit kludgy at the end. I think the interesting component will be to replace the Openstack bridging with OpenVswitch.

sudo apt-get install rabbitmq-server

sudo apt-get install python-software-properties

sudo add-apt-repository ppa:nova-core/trunk

sudo apt-get update

or

apt-get install python-software-properties

sudo apt-get install python-nova

add-apt-repository ppa:openstack-release/2011.3

apt-get update

apt-get upgrade

sudo apt-get install python-nova

sudo apt-get install nova-common nova-doc nova-api nova-network nova-objectstore nova-scheduler nova-compute euca2ools unzip

apt-get install bridge-utils

apt-get install -y ntp

sudo visudu

nii ALL=(ALL) NOPASSWD:ALL

nova ALL=(ALL) NOPASSWD:ALL

sudo nova-manage network create novanetwork 192.168.1.0/24 1 64

apt-get install -y python-greenlet python-mysqldb

apt-get install -y mysql-server

passwd=spam99

sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf

mysql -u root -p(passwd) -e 'CREATE DATABASE nova;'

mysql -u root -pspam99 -e "GRANT ALL PRIVILEGES ON nova.* TO 'novadbadmin'@'%' ;"

mysql -u root -pspam99 -e "SET PASSWORD FOR 'novadbadmin'@'%' = PASSWORD('0815');"

mysql -u root -pspam99 -e "SET PASSWORD FOR 'novadbadmin'@'%' = PASSWORD('spam99');"

Test connection

mysql -u novadbadmin -pspam99 nova

mysql -u root -pspam99 -e 'CREATE DATABASE glance';

mysql -u root -pspam99 -e 'CREATE USER glancedbadmin';

mysql -u root -pspam99 -e "GRANT ALL PRIVILEGES ON glance.* TO 'glancedbadmin'@'%';"

mysql -u root -pspam99 -e "SET PASSWORD FOR 'glancedbadmin'@'%' = PASSWORD('spam99');"

Install Glance image manager

Install Nova-Core

apt-get install nova-volume nova-vncproxy nova-api nova-ajax-console-proxy

apt-get install nova-doc nova-scheduler

apt-get install nova-network nova-compute

Euca Tools rather than Opstack cli

apt-get install -y euca2ools unzip

/home/brent/openflow# cat /etc/nova/nova.conf

--dhcpbridge_flagfile=/etc/nova/nova.conf

--dhcpbridge=/usr/bin/nova-dhcpbridge

--logdir=/var/log/nova

--state_path=/var/lib/nova

--lock_path=/var/lock/nova

--use_deprecated_auth

--force_dhcp_release

--libvirt_use_virtio_for_bridges

--connection_type=libvirt

--root_helper=sudo nova-rootwrap

#Block of IP addresses that are fixed IPs

--fixed_range=192.168.0.0/16

# Set network type: FlatDHCPManager

--network_manager=nova.network.manager.FlatDHCPManager

# Sets whether to user IPV6 Addresses

--use_ipv6=false

# Network Configuration

--dhcpbridge_flagfile=/etc/nova/nova.conf

--dhcpbridge=/usr/bin/nova-dhcpbridge

--flat_network_bridge=br100

#Backend Interface

--flat_interface=wlan0

--flat_injected=False

--public_interface=eth0

# Outgoing IP for Instances with fixed IP Range

--routing_source_ip=192.168.1.80

# Top-Level Directory for Maintaining nova's state

--state_path=/var/lib/nova

# These indicates where nova-api services are installed

--rabbit_host=192.168.1.80

--glance_api_servers=192.168.1.80:9292

--s3_host=192.168.1.80

--ec2_host=192.168.1.80

--osapi_host=192.168.1.80

--network_host=192.168.1.80

#Debug out

--verbose

#MySql conn

--sql_connection=mysql://novadbadmin:spam99@192.168.1.80/nova

# Imageservice: Glance default

--image_service=nova.image.glance.GlanceImageService

# Other

--logdir=/var/log/nova

--lock_path=/var/lock/nova

--force_dhcp_release=True

--use_deprecated_auth

--verbose #ISCSI

--iscsi_helper=ietadm

--iscsi_ip_prefix=192.168.1.80

apt-get install lvm2 iscsitarget

Add iSCSI DKMS support

apt-get install iscsitarget-dkms

create but dont mount

pvcreate /dev/sda4

make 10G container

dd if=/dev/null of=diskfile bs=1G count=10

grab a loop

losetup -f

losetup /dev/loop0 diskfile

enable iSCSI target

ISCSITARGET_ENABLE=true

service iscsitarget start

Check for a socket

/home/brent/openflow# lsof -i -a | grep 3260

ietd      11777     root    7u  IPv4 406342      0t0  TCP *:3260 (LISTEN)

ietd      11777     root    8u  IPv6 406343      0t0  TCP *:3260 (LISTEN)

service nova-volume start

service nova-vncproxy restart

service nova-api restart

service nova-ajax-console-proxy restart

service nova-scheduler restart

service nova-network start

service nova-compute restart

sudo lsof -i

sudo netstat -lptu

Installing the OpenStack Dashboard

Here are the overall steps for creating the OpenStack dashboard.

Install the OpenStack Dashboard framework including Apache and related modules.

Configure the Dashboard.

Restart and run the Apache server.

Install the OpenStack Dashboard.

sudo apt-get install openstack-dashboard openstackx python-sqlite

Enable the rewrite module for apache: sudo a2enmod rewrite

sudo a2enmod rewrite

Next, create a symbolic link to "dash" with the Apache2 Enable site utility (a2ensite).

sudo a2ensite dash

Disable the "default" site so that the Dashboard can come up as the Apache site's default.

sudo a2dissite default