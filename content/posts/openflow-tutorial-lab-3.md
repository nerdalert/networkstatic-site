+++
title = "OpenFlow Starter Tutorial Lab #3"
date = "2012-06-15T05:47:44+00:00"
lastmod = "2014-02-15T07:13:50+00:00"
author = "Brent Salisbury"
wp_id = 1096
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openflow-tutorial-lab-3/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "7fd998c2f60402244461f320d30bc9da30ecee4d2bd6758bfae13204b4f656c6"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow Starter Tutorial Lab #3</h2>

<aside class="legacy-callout">For a more up to date tutorial as anything more then 6 months old is outdated in the world of SDN Please see:
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}">OpenDaylight OpenStack Integration with DevStack on Fedora 20</a></aside>

OpenFlow Starter Tutorial Lab #3 : Move individual flows
<aside class="legacy-callout">Pre-requisites install and the beginning of the lab can be found <a href="{{< relurl "/2012/06/openflow-openvswitch-lab/" >}}">here.</a></aside>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/Lab31.jpg" >}}" alt="OpenFlow Lab #3 Topology"></figure>
<em>Figure 1.</em> OpenFlow starter tutorial Lab #3 topology. Add an entry to the wrong port and watch it break.

Let's clear all of our flows and get everything pinging the gateway again.
<pre class="code-sample"><code>$curl http://192.168.1.208:8080/wm/staticflowentrypusher /clear/00:00:5c:26:0a:5a:c8:b2/json</code></pre>
Add our three earlier entries from Lab1
<pre class="code-sample"><code>$curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow1", "cookie":"0", "priority":"32768", "dst-mac":"00:00:00:00:cc:10","active":"true", "actions":"output=5"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<pre class="code-sample"><code>curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow2", "cookie":"0", "priority":"32768", "dst-mac":"00:11:22:cc:cc:10","active":"true", "actions":"output=6"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<pre class="code-sample"><code>$curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow3", "cookie":"0", "priority":"32768", "dst-mac":"22:22:22:00:cc:10","active":"true", "actions":"output=7"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<h2>TCPdump Analysis</h2>
Start tcpdump on the host you will send Host3's traffic to. In my case I am starting tcpdump on Host1 where I am going to send Host3's traffic to.
<pre class="code-sample"><code>$ sudo tcpdump -i eth0 host &lt;IP of host 3&gt;</code></pre>
The filter "host &lt;ip&gt;"says only capture traffic to or from that host. We should never see unicast traffic from one host to another under proper condictions on a packet switched network.
<h2>Instantiate Bad Flows</h2>
Now lets push a mac to a bad port and watch it break. This will overwrite 'static-flow3'. This will break Host 3.
<pre class="code-sample"><code>$curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"wrong-port", "cookie":"0", "priority":"32768", "dst-mac":"22:22:22:00:cc:10","active":"true", "actions":"output=5"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/tcp-dump-ping2.jpg" >}}" alt="OpenFlow Lab #3 TCPDump"></figure>
<em>Figure 2.</em> TCPdump output when I push host 3's forwarding datapath to host 1.

As soon as you added the "wrong-port" static flow you began getting ICMP replies from the gateway until that times out. This has many more security type implications. Why not have your action be forward to two ports instead of just one. The 2nd port could be an IDS monitoring traffic and instead of trying to process the firehose of traffic in a typical port mirror you can get as granular you want and watch only particular matching traffic as defined by the tuple matching in the header fields  (src_mac,dst_ip,VID etc.). No you can use a fraction of the hardware and only process what is important to your use case. Load balancing is another obvious one. Policy routing that may be scalable if managed programmatically by northbound API's.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/06/SDN-API2.jpg" >}}" alt="OpenFlow Lab #3 Abstractions"></figure>
<em>Figure 3</em>. The API is the end game IMO
<h2>Conclusion</h2>
Thats it hope this maybe demystifies a bit of OpenFlow for you. I still have lots to learn as it is never-ending cycle, but going through a couple of labs seems to help nail some of this down and show that with complexity or more accuraltely abstraction, will bring more simplicity to the operators(some day so very very very far away theoretically). This lab setup can scale out to a wide range of different scenarios then just the couple little guys here. Would love to hear what others are doing.

From an end user perspective, it is the same ideas we have had in best matching of prefixes all along but we are adding more ways to match and fields to match upon. The API is what is going to be very important in my opinion and will open up the value over the next coulple of years as the northbound apps begin to surface. Sorry there is not any commentary on the videos, swamped but I think its fairly straightforward. I only added the video in case someone gets stuck. Feel free to contact with assistance or jump on irc.freenode.net on #openflow.

<h2 class="legacy-heading">Miscellaneous API Calls</h2>


Find all flows
<pre class="code-sample"><code>$curl http://192.168.1.208:8080/wm/core/switch/ 00:00:5c:26:0a:5a:c8:b2/flow/json</code></pre>
List all static
<pre class="code-sample"><code>$curl http://192.168.1.208:8080/wm/staticflowentrypusher/list/00:00:5c:26:0a:5a:c8:b2/json</code></pre>
Clear all flows
<pre class="code-sample"><code>$curl http://192.168.1.208:8080/wm/staticflowentrypusher/clear/00:00:5c:26:0a:5a:c8:b2/json</code></pre>

<hr />

<h2>Additional OpenFlow and SDN Links and Resources</h2>
<a href="http://openvswitch.org/" target="_blank">http://openvswitch.org/</a> Martin Casado's group have put an amazing vSwitch out there. I doubt there will be many vSwitches that are not munging his work in some form or fashion over the next few years.

<a href="http://floodlight.openflowhub.org/" target="_blank">http://floodlight.openflowhub.org/</a> Thanks to Nick Bastin for answering my question on the #openflow channel. He is a great asset to the community.

<a href="http://www.noxrepo.org/" target="_blank">http://www.noxrepo.org/</a> Another nice OpenFlow Controller is POX a Python based platform agnostic project the Murphy McCauley is doing a great job with. As soon as I dig into the API I am going to do a similar tutorial with that. I need the API docs if anyone has them hook me up.

I am typically always /nick networkstatic on irc.freenode.net in #openvswitch #openflow #openstack and #packetpushers if anyone has any questions.

<hr />

Check out the rest of the tutorials in this series:


<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank">Getting Started OpenFlow OpenvSwitch Tutorial Lab – Setup</a></li>
	<li><a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #1</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-2/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #2</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-3/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #3</a></li>
</ul>

<hr />

Thanks for stopping by.