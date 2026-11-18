+++
title = "Floodlight OpenFlow Controller GUI Applet"
date = "2012-07-28T19:56:47+00:00"
lastmod = "2013-04-05T05:07:32+00:00"
author = "Brent Salisbury"
wp_id = 1878
categories = ["In the Lab", "Tools"]
tags = ["Java", "OpenFlow"]
description = ""
url = "/floodlight-openflow-controller-gui-applet/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "677bce5141e6da1ddf7779cbd18b501d3aa8ae805eb610b5c90683bbda57c804"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Floodlight OpenFlow Controller GUI Applet</h2>


</a>There is a new FloodLight OpenFlow SDN controller GUI out from a Marist College and IBM research group/internship. I am guessing it is the same IBM researcher that developed the <a href="{{< relurl "/2012/07/floodlight-gui-topology-addition/" >}}" target="_blank">FloodLight web UI</a>. This applet allows one to instantiate a flow from the GUI along with a couple of other bells and whistles. It is great to see the public/private partnership. Kudos to both Marist and IBM for the contribution to the community.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/OF-logo.jpg" >}}" alt="OpenFlow"></figure>
Avior uses the REST API which is one of the best visions <a href="http://www.bigswitch.com/" target="_blank">BigSwitch</a> has brought to the table. It is another tool for learning if one preferred a GUI to instantiate flows. Keep in mind adding individual flows would likely be a rare if ever occurrence, probably even less that using static routes in networks today but very similar in principle. Just as you would typically learn how to add a static layer3 route before dynamic routing protocols the idea is the same only we have many more options in the "Match + [Action|Instruction]" with 10-12 different L2/L3 header fields rather than just focusing on a next hop. Programmatic policy based routing. So take a peak, only takes a second, still some hangs and crashes but its a fun little app.

[youtube url="http://youtu.be/TTlVKPHgoxw" width="610" height="360"]

Video 1. Nice installation and UI walk through from the guys who developed this.
<h2>Installation Preperation</h2>
Install dependencies, apt-get for UB and yum for RH:
<strong>$apt-get install build-essential default-jdk ant python-dev eclipse git</strong>
<h2>Floodlight OpenFlow Controller GUI Applet</h2>
<h4>Start Floodlight</h4>
Clone the Github project and build the jar and start the controller:
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">git clone git://github.com/floodlight/floodlight.git
cd floodlight
ant
java -jar target/floodlight.jar</pre>

<h2>FloodLight GUI</h2>

<p class="prettyprint">Download for your OS http://openflow.marist.edu/avior.html
From the machine you are running the controller on:
$ chmod +x run.sh
Ensure Floodlight is running.
That will start the Jar runtimes and pop open a window to point to your controller. If it is the same machine as where floodlight is running simply enter 127.0.0.1 for it to attach to the running Floodlight instance.</p>
<h2>FloodLight Controller Web Interface<</h2>

<p class="prettyprint">Once the service is running you can go to the web GUI and view topologies, flows etc or use curl statements to add remove datapaths.
View the GUI in a web browser http://localhost:8080/ui/index.html</p>