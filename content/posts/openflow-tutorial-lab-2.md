+++
title = "OpenFlow Starter Tutorial Lab #2"
date = "2012-06-15T05:47:04+00:00"
lastmod = "2014-02-15T07:13:28+00:00"
author = "Brent Salisbury"
wp_id = 1089
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openflow-tutorial-lab-2/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "4d1c028c3bab6cd1da6e6208139c266326c6a27809d7460be0d10ded23ad8ddf"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow Starter Tutorial Lab #2</h2>

<aside class="legacy-callout">For a more up to date tutorial as anything more then 6 months old is outdated in the world of SDN Please see:
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}">OpenDaylight OpenStack Integration with DevStack on Fedora 20</a></aside>

OpenFlow Starter Tutorial Lab #2 :This lab is to restrict two hosts to only talk to each other with source based forwarding using the static flow pusher RESTful API. You can add any field you want to make the forwarding decisions on. Remember to name the flows with unique names or else you will overwrite previously instantiated flows. Previous posts in the series have setup included. Links to those at the bottom of this post.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/Lab24.jpg" >}}" alt="OpenFlow Tutorial Lab"></figure>
<em>Figure 1.</em> OpenFlow Starter Tutorial Lab #2 Topology

Based on source MAC address we can lock two ports into only talking to each other. This is used for security reasons today in sensitive areas. This allows for very granular port to port mapping. We are adding two flows, just as a host needs a flow setup to talk to another host it also needs a return flow to put established.

Delete old static Flows from Lab 1.
<pre class="code-sample"><code>curl http://192.168.1.208:8080/wm/staticflowentrypusher/clear/00:00:5c:26:0a:5a:c8:b2/json</code></pre>
<h2>Push the two static OpenFlow RESTful API Calls to Create Your FlowMod</h2>
<pre class="code-sample"><code>#To ping from port 1 to 6
$curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow1", "cookie":"0", "priority":"32768", "src-mac":"00:11:22:cc:cc:10","active":"true", "actions":"output=6"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json
#To ping from port 6 to 1
$curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow2", "cookie":"0", "priority":"32768", "src-mac":"22:22:22:00:cc:10","active":"true", "actions":"output=1"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
Ping the hosts from those two ports. They should only be able to ping each other not your gateway or anything else since the closets match is the static one pushed.

Once I add these may gateway no longer pings becuase the only place those to source mac addresses explicitly match on are eachothers ports. So while they can talk to each other they can not talk anywhere else.

While this is clearly not managable at scale, it should get the your wheels going on the possiblities this opens when you start thinking about how powerful this granularity can become in the security world if done programmatically from policy.

<hr />

Check out the rest of the tutorials in this series:


<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank">Getting Started OpenFlow OpenvSwitch Tutorial Lab – Setup</a></li>
	<li><a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #1</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-2/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #2</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-3/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #3</a></li>
</ul>

<hr>
Thanks for stopping by.

