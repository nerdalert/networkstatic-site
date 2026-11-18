+++
title = "Starting OVSDB and vSwitchd in OpenvSwitch with Debugging Enabled"
date = "2015-04-07T22:24:04+00:00"
lastmod = "2015-06-14T08:25:49+00:00"
author = "Brent Salisbury"
wp_id = 7543
categories = ["In the Lab"]
tags = ["OVSDB", "Open vSwitch"]
description = ""
url = "/starting-ovsdb-and-vswitchd-in-openvswitch-with-debugging-enabled/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "e4c36fb72097b84d778733f0a312d0eb632e439d2919ce46037fb67f596fcfa4"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

</h2><h2 class="legacy-heading">Starting OVSDB and vSwitchd in OpenvSwitch with Debugging Enabled </h2></h2>

Here are some quick notes on how I went about debugging OVSDB (ovsdb-server) and OVS vSwitchd (ovs-vsctl). There are lots of ways to debug OVS these are what I used to get debug logs generated. Those logs are helpful troubleshooting for OVSDB transactions and OpenFlow commands when using the ovs-vctl or OVSDB and OpenFlow APIs.
 
Dont do this unless you are ok w/ trashing the install in case there is something different about your environment then mine :) These are about a year old but I think thats all still the same. 

</h2><h2 class="legacy-heading">Start processes for Debugging OVSDB Transactions</h2></h2>

If you are having OpenFlow API or ovs-vsctl issues and wanted to debug them, you can enable vswitchd syslog debugging with this.

<pre class="lang:sh decode:true " title="Initialization for Debugging vSwitchd" >
# Stop existing OVS processes. kill -9 works too.
/usr/local/share/openvswitch/scripts/ovs-ctl stop
# Start ovsdb-server w/ debugging enabled.
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock  \
  --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
  --private-key=db:Open_vSwitch,SSL,private_key  \
  --certificate=db:Open_vSwitch,SSL,certificate     \
  --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert  \
  --log-file=/var/log/openvswitch/ovs-vswitchd.log \
  -vsyslog:dbg -vfile:dbg  --pidfile --detach

ovs-vswitchd -v --pidfile --detach \
 --log-file=/var/log/openvswitch/ovs-vswitchd.log \
 -vconsole:err -vsyslog:info -vfile:info
ovs-vsctl --no-wait init

tail -f /var/log/ovsdb-*.log
</pre>

</h2><h2 class="legacy-heading">Start processes for Debugging vSwitchd</h2></h2>

If you are having OpenFlow API or ovs-ofctl issues and wanted to debug them, you can enable vswitchd syslog debugging with this:

<pre class="lang:sh decode:true " title="Init for Debuging vSwitchd" >

# Stop existing OVS processes. kill -9 works too.
/usr/local/share/openvswitch/scripts/ovs-ctl stop
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
                     --private-key=db:Open_vSwitch,SSL,private_key \
                     --certificate=db:Open_vSwitch,SSL,certificate \
                     --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
                     --pidfile --detach
ovs-vsctl --no-wait init

# Start ovs-vswitchd w/ debugging enabled.
ovs-vswitchd -v --pidfile --detach \
 --log-file=/var/log/openvswitch/ovs-vswitchd.log -vconsole:dbg -vsyslog:dbg -vfile:dbg

ovs-vswitchd -v --pidfile --detach \ 
 --log-file=/var/log/openvswitch/ovs-vswitchd.log \
 -vconsole:err -vsyslog:dbg -vfile:err
</pre> 

</h2><h2 class="legacy-heading">reset-ovs.sh - resets ovs to default</h2></h2>
Its a hammer appraoch, prolly more elegant ways but this is what I used for reseting OVS to vanilla and then starting OVSDB w/ debugging enabled.

These commands simply delete and reinitialize the OVS schema conf file and restarts the processes. You can always substitute the startup scripts in place of individually starting the procs.
<pre class="lang:sh decode:true " title="Simple ovsdb reset script" >

# Stop existing OVS processes. kill -9 works too.
/usr/local/share/openvswitch/scripts/ovs-ctl stop
sleep 1
cd /home/brent/openvswitch
rm  /usr/local/etc/openvswitch/conf.db
/usr/local/bin/ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema

 ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock  \
  --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
  --private-key=db:Open_vSwitch,SSL,private_key  \
  --certificate=db:Open_vSwitch,SSL,certificate     \
  --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert  \
  --log-file=/var/log/openvswitch/ovs-vswitchd.log \
  -vsyslog:dbg -vfile:dbg  --pidfile --detach
ovs-vswitchd -v --pidfile --detach \
 --log-file=/var/log/openvswitch/ovs-vswitchd.log \
  -vconsole:err -vsyslog:info -vfile:info
ovs-vsctl --no-wait init
sudo ovs-vsctl set-manager ptcp:6640</pre> 

</h2><h2 class="legacy-heading"> debug using the OVS startup scripts</h2></h2>

If you dont want to start the processes manually, you can modify the initialization script and look for -vsyslog, -vfile, etc. You can change those to the syslog level that you want. The script is typically generally located at:

<pre class="lang:sh decode:true " title="Modify the OVS startup script" >
vi /usr/local/share/openvswitch/scripts/ovs-ctl
# Then restart the process once you have the values you want in place
/usr/local/share/openvswitch/scripts/ovs-ctl restart
</pre> 
<hr>
Happy hacking!


