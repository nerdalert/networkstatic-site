+++
title = "Floodlight OpenFlow Controller Screencast with HP Switches"
date = "2012-05-01T04:50:33+00:00"
lastmod = "2013-07-30T04:47:18+00:00"
author = "Brent Salisbury"
wp_id = 509
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/floodlight-openflow-controller-screencast-with-hp-switches/"
image = "/wp-content/uploads/2012/05/openflow2.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "fc8d1bea8d05e1bcdd1cbd2ffe546d96c1976a22c76c641118e51461f36f9a41"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Floodlight OpenFlow Controller Screencast with HP Switches</h2>

<hr>
There is an updated post with the newest HP OpenFlow firmware that can be found at: <a href="{{< relurl "/configure-an-hp-openflow-switch-for-floodlight/" >}}">Configure an HP OpenFlow Switch for Floodlight</a>
<hr>

Quick how-to on installing the Floodlight OpenFlow controller and a slick http UI fronted someone put up on GutHub. Floodlight is probably the easiest of all controllers to setup. It is built in Java and based on the Beacon controller project. It is a great way to get your feet wet in SDN. I will work on a post showing some of the capabilities in the next few days.
<p style="text-align: left;">The switches in the post are a couple HP3500yl running the OpenFlow v1.0 agent. I think the TCAM on that box allows for maybe a 5-tuple in HW. None of the HP switches I am aware of support any layer 2 header rewrites due to TCAM size limitations. Just not enough rows, but maybe the bigger 5400 but I havent dug in. That limits manipulation of the ethertype, L2 src address and L2 dst address.  Thanks to the gentleman who shared his code on GitHub with the nifty web UI. It was needed. It looks very much like the Beacon web UI.
<a href="{{< relurl "/wp-content/uploads/2012/05/topo1.jpg" >}}"><img class="size-full wp-image-511 aligncenter" title="topo" src="{{< relurl "/wp-content/uploads/2012/05/topo1.jpg" >}}" alt="" width="344" height="267" /></a></p>
 <strong>Figure 1.</strong> Here is the topology.

Kick the tires on a very simple controller install and see what you think. No C compiler errors in this project which can be nice depending on how much you like or dislike Java :)
http://www.youtube.com/watch?v=pAOzHYm7Yhc
<h4>System Preperation</h4>
Install dependencies, apt-get for UB and yum for RH:
<strong>$apt-get install build-essential default-jdk ant python-dev eclipse git</strong>
<h4>Start Floodlight</h4>
Clone the Github project and build the jar and start the controller:
<pre class="code-sample"><code>$git clone git://github.com/floodlight/floodlight.git
$cd floodlight
$ant
$java -jar target/floodlight.jar</code></pre>
<p class="prettyprint">Once the service is running you can go to the web GUI and view topologies, flows etc or use curl statements to add remove datapaths.
View the GUI in a web browser http://localhost:8080/ui/index.html</p>

<h4>Attach the HP Switch to the OpenFlow Controller</h4>
<pre class="code-sample"><code>vlan 1 openflow controller tcp:192.168.1.171 enable
Here is what the HP config looks like.
#Non-OpenFlow Vlan. Out of Band for Control Comm.
vlan 1
name "Native Path to Controller"
ip address 192.168.1.211 255.255.255.0
tagged 1-3,5
#OpenFlow enabled Vlan
vlan 3
name "OF Controlled Vlan"
untagged 48
ip address 10.1.1.3 255.255.255.0
tagged 2-3
exit
#Enable OF on the Vlan. Needs to enabled per Vlan.
vlan 3
enable
controller "tcp:192.168.1.171:6633"
exit</code></pre>
Later this week I will breakdown some of the datapaths and flows and we can see what they look like in action.