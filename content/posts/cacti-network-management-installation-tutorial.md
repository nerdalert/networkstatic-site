+++
title = "Cacti Network Management Installation Tutorial"
date = "2012-12-03T05:29:07+00:00"
lastmod = "2013-06-14T14:29:47+00:00"
author = "Brent Salisbury"
wp_id = 4938
categories = ["In the Lab", "Tools"]
tags = ["Network Management", "Programming"]
description = ""
url = "/cacti-network-management-installation-tutorial/"
image = "/wp-content/uploads/2012/12/cacti-nms.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b506ca98a199c7c94cc8bb593be4716f6ef5027b962259758721ce534aadf06d"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Cacti Network Management Installation Tutorial</h2>
Network management has to be, one of the most neglected pieces of networking. I am sure we all have our hypotheses as to why but that is for another day. This tutorial is for installing the latest stable release 0.8.8a, released on 04/29/12. I needed to proof Cacti and get a scripted installation together. Cacti has been around a long time and has a nice ecosystem of plugins. Like any open source there is much more code then documentation. That said, the <a href="http://forums.cacti.net/viewforum.php?f=25" target="_blank">Cacti community forum</a> is fantastic and full of community contributions. I tested the installation on both current CentOS and RHEL. It could be easily ported to Ubuntu s/yum/apt-get/g.

<h2 class="legacy-heading">Cacti Network Management Plugins</h2>

Here are some supported and user built <a href="http://docs.cacti.net/plugins" target="_blank">plugins</a> part of this install.


<ul>
	<li>Discovery - Auto Host Discovery</li>
	<li>Mactrack - End Device Port Tracker and General Network Toolkit</li>
	<li>Monitor - Monitoring for Cacti</li>
	<li>Realtime - Realtime Graph Viewer</li>
	<li>Routerconfigs - Router Config Backup</li>
	<li>Syslog - Sylog Viewer for Cacti</li>
	<li>Weathermap - Generate maps and diagrams using data collected by Cacti or other sources</li>
</ul>

<h2>Examples of Cacti</h2>
A couple of my friends in have some public examples of similar Cacti network management deployments using the Weathermap plugin for Cacti.


<ul>
	<li>A GigaPop in Illinois from <a href="http://www.forwardingplane.net" target="_blank">Nick Buraglio</a> found <a href="http://iccn.illinois.edu/status/weather-maps/" target="_blank">here</a>.</li>
	<li>Here is another one from <a href="http://lonesysadmin.net" target="_blank">Bob Plankers</a> found <a href="https://stats.net.wisc.edu" target="_blank">here</a>.</li>
</ul>

<h2>Cacti Installation ScreenCast</h2>
<p><a href="http://www.youtube.com/watch?v=R2OB5eFjeNw&hd=1">Watch video on YouTube</a></p>
<h2>Cacti Network Management Installation Script</h2>
I started writing my own script from the doc and realized I needed better documentation. Poking around on the forum I found a nice script that had already done most of the work on the forums. I modified it for the latest releases, modified a couple of PHP configs and updated a couple of plugins.
<pre class="code-sample"><code>#!/bin/sh
# Testing script for install cacti 0.8.7i and spine 0.8.7i on Centos Linux Release 6.x
# Version : 1.0.4
# Make by Patrick.Ru @ China
# E-Mail : patrick.ru@hotmail.com
# Date : 28-Dec-2011
# Thanks to Patrick Ru of China for posting this script.
# I modified the script add the latest version 0.8.8a, released 04/29/12.
# Along with updating a couple plugins and 
# changing the php config at the end s//g -Brent Salisbury
chkconfig iptables off
service iptables stop
sed -i &#039;s/SELINUX=enforcing/SELINUX=disabled/g&#039; /etc/selinux/config
/usr/sbin/setenforce 0
yum update -y
yum install -y wget
mkdir -p /usr/src/cacti
cd /usr/src/cacti
yum install -y httpd
chkconfig httpd on
service httpd start
yum install -y mysql-server
chkconfig mysqld on
service mysqld start
mysqladmin -u root password dbadmin
yum install -y php php-gd php-mysql php-cli php-ldap php-snmp php-mbstring php-mcrypt
service httpd restart
yum install -y rrdtool
yum install -y net-snmp-utils
yum install -y tftp-server
chkconfig xinetd on
service xinetd start
wget http://www.cacti.net/downloads/cacti-0.8.7i-PIA-3.1.tar.gz
tar zxvf cacti-0.8.7i-PIA-3.1.tar.gz
wget http://www.cacti.net/downloads/patches/0.8.7i/settings_checkbox.patch
cd cacti-0.8.7i-PIA-3.1
yum install -y patch
patch -p1 -N &lt; ../settings_checkbox.patch
cd ..
mv -f cacti-0.8.7i-PIA-3.1/* /var/www/html/
rm -rf cacti-0.8.7i-PIA-3.1
chown -R apache:apache /var/www/html/
service httpd restart
mysql -u root -pdbadmin -e &#039;CREATE DATABASE `cacti` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;&#039;
mysql -u root -pdbadmin -e &quot;CREATE USER &#039;cactiuser&#039;@&#039;localhost&#039; IDENTIFIED BY &#039;cactiuser&#039;;&quot;
mysql -u root -pdbadmin -e &#039;GRANT ALL PRIVILEGES ON `cacti` . * TO &#039;cactiuser&#039;@&#039;localhost&#039;;&#039;
mysql -u cactiuser -pcactiuser cacti &lt; /var/www/html/cacti.sql
cat &gt; /etc/cron.d/cacti &lt;&lt;EOF
*/5 * * * * apache /usr/bin/php /var/www/html/poller.php &gt; /dev/null 2&gt;&amp;1
EOF
yum install -y gcc gcc-c++ make automake patch libtool net-snmp-devel openssl-devel mysql mysql-devel
wget http://www.cacti.net/downloads/spine/cacti-spine-0.8.7i.tar.gz
tar zxvf cacti-spine-0.8.7i.tar.gz
cd cacti-spine-0.8.7i
./configure
make &amp;&amp; make install
cp /usr/local/spine/etc/spine.conf.dist /usr/local/spine/etc/spine.conf
cd /usr/src/cacti
wget http://docs.cacti.net/_media/plugin:settings-v0.71-1.tgz -O settings.tgz
tar zxvf settings*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/settings
wget http://docs.cacti.net/_media/plugin:clog-v1.7-1.tgz -O clog.tgz
tar zxvf clog*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/clog
wget http://docs.cacti.net/_media/plugin:thold-v0.4.9-3.tgz -O thold.tgz
tar zxvf thold*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/thold
wget http://docs.cacti.net/_media/plugin:monitor-v1.3-1.tgz -O monitor.tgz
tar zxvf monitor*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/monitor
wget http://docs.cacti.net/_media/plugin:realtime-v0.5-1.tgz -O realtime.tgz
tar zxvf realtime*.tgz -C /var/www/html/plugins
mkdir -p /var/www/html/plugins/realtime/cache
chown -R apache:apache /var/www/html/plugins/realtime
yum install -y unzip
wget http://www.network-weathermap.com/files/php-weathermap-0.97a.zip
unzip php-weathermap-0.97a.zip -d /var/www/html/plugins/
chown -R apache:apache /var/www/html/plugins/weathermap
wget http://docs.cacti.net/_media/plugin:mactrack-v2.9-1.tgz -O mactrack.tgz
tar zxvf mactrack*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/mactrack
wget http://docs.cacti.net/_media/plugin:syslog-v1.22-2.tgz -O syslog.tgz
tar zxvf syslog*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/syslog
wget http://docs.cacti.net/_media/plugin:routerconfigs-v0.3-1.tgz -O routerconfigs.tgz
tar zxvf routerconfigs*.tgz -C /var/www/html/plugins
mkdir -p /var/www/html/plugins/routerconfigs/backups
chown -R apache:apache /var/www/html/plugins/routerconfigs
wget http://docs.cacti.net/_media/plugin:docs-v0.4-1.tgz -O docs.tgz
tar zxvf docs*.tgz -C /var/www/html/plugins
mv -f /var/www/html/plugins/docs* /var/www/html/plugins/docs
chown -R apache:apache /var/www/html/plugins/docs
wget http://nchc.dl.sourceforge.net/project/cacti-reportit/cacti-reportit/reportit_v073/reportit_v073.tar.gz -O reportit.tar.gz
tar zxvf reportit*.tar.gz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/reportit
wget http://docs.cacti.net/_media/plugin:rrdclean-v0.41.tgz -O rrdclean.tgz
tar zxvf rrdclean*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/rrdclean
wget http://docs.cacti.net/_media/plugin:discovery-v1.5-1.tgz -O discovery.tgz
tar zxvf discovery*.tgz -C /var/www/html/plugins
chown -R apache:apache /var/www/html/plugins/discovery
if [ &quot;$HOSTTYPE&quot; == &quot;x86_64&quot; ]; then
wget http://www6.atomicorp.com/channels/atomic/centos/6/x86_64/RPMS/wmi-1.3.14-2.el6.art.x86_64.rpm
rpm -Uvh wmi-1.3.14-2.el6.art.x86_64.rpm
elif [ &quot;$HOSTTYPE&quot; == &quot;i386&quot; ]; then
wget http://www6.atomicorp.com/channels/atomic/centos/6/i386/RPMS/wmi-1.3.14-2.el6.art.i686.rpm
rpm -Uvh wmi-1.3.14-2.el6.art.i686.rpm
fi
wget http://svn.parkingdenied.com/CactiWMI/trunk/wmi.php -O /var/www/html/scripts/wmi.php
chown -R apache:apache /var/www/html/scripts/wmi.php
service httpd restart</code></pre>
The Cisco Catalyst 6500 template I used for the screencast can be downloaded <a href="{{< relurl "/wp-content/uploads/2012/12/cacti_host_template_cisco_6500.xml_.txt" >}}" target="_blank">here</a>. Simply copy and paste it into the templates section and then associate it to the 6500 you populate. Check the forums for more <a href="http://forums.cacti.net/viewforum.php?f=12" target="_blank">templates</a>.
<h2>Post Installation and Plugins</h2>
If you have issues with RHEL you may need to run the following.
<pre class="brush: bash; gutter: true">php -q /var/www/html/cli/rebuild_poller_cache.php</pre>
Enable plugins under settings -&gt; Management as shown in the following screen capture. Just click the blue down arrow to add it into the console as tab.
<hr />
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/cacti-plugins.jpg" >}}" alt="Cacti Plugins"></figure>
<hr />

So checkout the forums if interested and see if any of the project can help your operations, maybe even contribute what you do back.
Thanks for stopping by.

<hr />