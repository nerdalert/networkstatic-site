+++
title = "SDN Floodlight Controller GUI Topology Video and Install"
date = "2012-07-08T17:55:53+00:00"
lastmod = "2012-11-25T07:53:19+00:00"
author = "Brent Salisbury"
wp_id = 1615
categories = ["Tools"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/floodlight-gui-topology-addition/"
aliases = ["/2012/07/floodlight-gui-topology-addition/"]
image = "/wp-content/uploads/2012/07/network.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cf247fc82d8259fb8a8ee871166fc50ef7703ee1cb141ef63039a04cbebd164f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

SDN Floodlight Controller GUI Topology Video and Install: There is a new topology component to the OpenFlow Controller FloodLight. The page is located in the GUI Web UI under the "Topology" menu and the balls on the screen represent hosts. I haven't checked the listserv to see where they are going with it but it's all in the right direction and actually reminds me of the OpenStack dev history video made with Gource the visualization software. The OpenStack video is the future of computing and network SDN resource visualization if done in realtime and made useful. Replace developer with Tenant and you have some sparkle. Pretty "Minority Report"esque but it wouldn't be the first time Science Fiction predicted the future.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/07/Floodlight-UI.jpg" >}}"><img class="wp-image-1617 aligncenter" title="Floodlight-UI" src="{{< relurl "/wp-content/uploads/2012/07/Floodlight-UI.jpg" >}}" alt="Floodlight-UI" width="554" height="345" /></a></p>
<strong>Figure 1.</strong> Screen Shot of the Web UI Topology Page.

<hr />

http://www.youtube.com/watch?v=kylnrAWx7hM

<strong>Video 1.</strong> FloodLight Topology Web UI Module. Neat first step.

<hr />

http://www.youtube.com/watch?v=l5PrjqezhgI

<hr />

<strong>Video 2.</strong>It would be slick to visualize out networks like this. Useful not sure but certainly slick.

If you have not installed FloodLight before it is super quick and easy. You will not get any visual hosts until you have a switch attached to it. You can do that very easily with a quick lab <a href="{{< relurl "/2012/05/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/" >}}" target="_blank">here</a> or a longer more in depth lab <a href="{{< relurl "/2012/06/openflow-openvswitch-lab/" >}}" target="_blank">here</a>.
<h4>System Preperation</h4>
Install dependencies, apt-get for UB and yum for RH:
<strong>$apt-get install build-essential default-jdk ant python-dev eclipse git</strong>
<hr>
<h2>SDN Floodlight Controller GUI Install</h2>
Clone the Github project and build the jar and start the controller:
<p class="prettyprint">$git clone git://github.com/floodlight/floodlight.git
$cd floodlight
$ant
$java -jar target/floodlight.jar</p>
<p class="prettyprint">Once the service is running you can go to the web GUI and view topologies, flows etc or use curl statements to add remove datapaths.
View the GUI in a web browser http://localhost:8080/ui/index.html</p>
Thanks for stopping by.
<hr>