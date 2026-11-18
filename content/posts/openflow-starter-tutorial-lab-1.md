+++
title = "OpenFlow Starter Tutorial Lab #1"
date = "2012-06-15T05:44:57+00:00"
lastmod = "2014-02-15T07:13:02+00:00"
author = "Brent Salisbury"
wp_id = 1081
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/openflow-starter-tutorial-lab-1/"
image = "/wp-content/uploads/2012/09/openflow-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cbe73bee4297195ce86bd34a519e64123d147253afe04d0f4ec0812d0b19dc0d"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenFlow Starter Tutorial Lab #1</h2>
<ol class="legacy-numbers">

<aside class="legacy-callout">For a more up to date tutorial as anything more then 6 months old is outdated in the world of SDN Please see:
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}">OpenDaylight OpenStack Integration with DevStack on Fedora 20</a></aside>

<ol>
	<li>Lab 1: Add static destination MAC addresses to each node. Match: DstMac: , Action:DstPortX</li>
	<li>Lab 2: Add static flow with src mac address match with the associated action to an output port e.g. Match:SrcMac Action:DstPortY.</li>
	<li>Lab 3: Add a bad static flow for one of the hosts and watch ICMP replies from the gateway on the board port come back through tcpdump. Match:DstMac, Action:PortZ</li>
</ol>
</ol>
<hr>
<a href="{{< relurl "/wp-content/uploads/2012/06/Topology-overview.jpg" >}}"><img class="wp-image-1087 aligncenter" title="Openflow lab tutorial openvswitch" alt="" src="{{< relurl "/wp-content/uploads/2012/06/Topology-overview.jpg" >}}" width="482" height="265" /></a>
<strong>Figure 1.</strong> The topology for the lab simulates in software the same capabilities you can get in hardware thanks to OpenvSwitch.
This setup allows you to add and remove as many matches into the API calls and tinker with them to get a feel once you nail down the basics. Then you can write the next "killer app" get rich and make it rain, but first lets figure out what is going on here.
<h2>RESTful/JSON API</h2>
The API is documented very well (that is huge and differentiating IMO) @
<pre class="code-sample"><code><a href="http://www.openflowhub.org/display/floodlightcontroller/Proposed+New+API">http://www.openflowhub.org/display/floodlightcontroller/Proposed+New+API</a></code></pre>
RESTful APIs are very important in my opinion if there is to be a transition of any kind to make it human readable for at the least troubleshooting or easy field parsing programmaticlaly for those of us who are only willing to muck our way through interpreted languages. Huge fan of what they have done here with their API and I expect the industry to follow this.
<h2>Forwarding Table in OpenvSwitch</h2>
Based on 'ovs-appctl fdb/show br-int' build your cheat sheet so see what port your host VMs are on inside of OpenvSwitch. If you do not see your entry it has like timed out ~300 seconds or so, refresh the entry by simply pinging the host VM from the vSwitch. These tables are the same as your CAM tables doing key/value exact matches for L2 mac address lookups and LPM (Longest Prefix Match) in todays network systems only in software.
<pre class="code-sample"><code>$ovs-appctl fdb/show br-int
port  VLAN  MAC                Age
1     0  00:23:69:62:26:09   58
6     0  00:11:22:cc:cc:10    7
5     0  00:00:00:00:cc:10    4
0     0  5c:26:0a:5a:c8:b2    3
7     0  22:22:22:00:cc:10    3</code></pre>
MAC tables for this lab are as follows. Yours will likely be different based on the assignment by the vSwitch. The mac addresses are specifed by the KVM boot but anything can be used as long they are unique.

The DPID datapath ID is required to send the API calls. You need to find the one on your vSwitch. Lots of ways to find it either through the Floodlight console or APIs or from the ovs-ofctl show &lt;bridge name&gt; listed below. It is basically a few bytes prepended on your Nics MAC address).
<pre class="code-sample"><code>$ ovs-ofctl show br-int
OFPT_FEATURES_REPLY (xid=0x1): ver:0x1, dpid:00005c260a5ac8b2  (that is your DPID)</code></pre>
Replace the curl commands with your DPID curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2",  (that longer than usual mac looking ID)

"ovs-dpctl dump-flows br-int" will display the datapaths being instantiated into the OpenvSwitch and handy for debugging and tshooting.
<a href="{{< relurl "/wp-content/uploads/2012/06/Addresses.jpg" >}}"><img class="size-full wp-image-1084 aligncenter" title="Openvswitch FIB entries" alt="Openvswitch FIB entries" src="{{< relurl "/wp-content/uploads/2012/06/Addresses.jpg" >}}" width="472" height="300" /></a><strong>Figure2.</strong> MAC to Port mapping or forwarding table for the labs. Build this from  <strong>"ovs-appctl fdb/show br-int"</strong> output.
Throughout the lab I have my VM hosts pinging the gateway so I can watch what happens as I instantiate static flows into the OpenvSwitch (OVS) flow table.
<h2>OpenFlow WebUI GUI</h2>
Through the lab for starters it might be easier for some to watch the web page. This is a nice Django front end put together by Wes Felter and some of his guys at IBM. There are some bugs which I'm sure the Floodlight guys would like anyone to clean up. If you leave the page open it continues to refresh until it consumes the planet as it polls the controller. Just close and reopen every now and then.

The WebUI loads be default with the jar binary:
<pre class="code-sample"><code>java -jar floodlight.jar</code></pre>
<pre class="code-sample"><code>http://&lt;yourIP&gt;:8080/ui/index.html</code></pre>
<a href="{{< relurl "/wp-content/uploads/2012/06/WebUI-Flows.jpg" >}}"><img class="wp-image-1085 aligncenter" title="Openflow GUI web interface" alt="" src="{{< relurl "/wp-content/uploads/2012/06/WebUI-Flows.jpg" >}}" width="586" height="552" /></a>
<strong>Figure 3.</strong> WebUI starts automatically and binds to port 8080

It might be more comfortable for some to use the WebUI / GUI. It is a nice clean web front at that!

http://www.youtube.com/watch?v=8vHZN-Mb518

All three labs are in this screencast.

<h2>Lab 1 Static MAC entries for our 3 hosts</h2>
<a href="{{< relurl "/wp-content/uploads/2012/06/Lab11.jpg" >}}"><img class="size-full wp-image-1083 aligncenter" title="Openflow tutorial lab opevswitch" alt="" src="{{< relurl "/wp-content/uploads/2012/06/Lab11.jpg" >}}" width="505" height="312" /></a><strong>Figure 3.</strong> Three hosts with static mac entries for each port.
<h2>Static Flow Push into the OpenFlow Pipeline</h2>
Before we run we crawl, before we dynamically forward we statically forward! It seems natural that most of the time we start with static entries when teaching the mechanics of routing with network IGPs. Here we are defining static data paths. We match (or don't) a rule and have an associated action to it that will eventually kick off a fairly complex sets of flow tables in a pipeline in v1.1 and up.

The fairly close command for a data path  in a tradiational instruction set on today's switches would be this '"mac-address-table static 0000.0000.cc10 vlan 100 interface GigabitEthernet0/1". We are not setting a vlan id but would be as easy as adding "dataLayerVirtualLan":x to the flow push. That is obviously not scalable but I think it is important to understand how datapaths get pushed to the OF enabled switch. Normally even in the SDN world those mac address are learned through flooding to all ports FFFF.FFFF.FFFF on the broadcast domain. The controller than learns of it starts a mac address timer to begin to age it out if no more traffic is received so as not to exhaust the it's tables but cache it if it continues talking by restarting the timer each time a frame is received from the MAC source.

Push static flows for each destination mac address in the switch to an assigned port. We have a match and action explicitly defined. All we are doing is adding static mac address entries instead of them being defined dynamically through flooding. Not each name is unique. If copying and pasting make sure to strip formatting.

As you add the flows keep in mind each curl you do will overwrite the previous one their with the same name in the table. Notice each flow pushed has a unique name. It's almost ACLs but not quite.
<ul>
	<li>Install curl</li>
</ul>
<pre class="code-sample"><code>$apt-get install curl</code></pre>
With OVS and the OF controller run each of these from your command line.
Remember to replace the DPID "switch": "00:00:5c:26:0a:5a:c8:b2" &amp; the IP addr 192.168.1.208 with your lab addresses. Each curl command is one line.

<h2>Instantiate The OpenFlow Forwarding Rules</h2>

<ul>
	<li>Host 1</li>
</ul>
<pre class="code-sample"><code>$ curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow1", "cookie":"0", "priority":"32768", "dst-mac":"00:00:00:00:cc:10","active":"true", "actions":"output=5"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<ul>
	<li>Host 2</li>
</ul>
<pre class="code-sample"><code>$ curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow2", "cookie":"0", "priority":"32768", "dst-mac":"00:11:22:cc:cc:10","active":"true", "actions":"output=6"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<ul>
	<li>Host 3</li>
</ul>
<pre class="code-sample"><code>$ curl -d '{"switch": "00:00:5c:26:0a:5a:c8:b2", "name":"static-flow3", "cookie":"0", "priority":"32768", "dst-mac":"22:22:22:00:cc:10","active":"true", "actions":"output=7"}' http://192.168.1.208:8080/wm/staticflowentrypusher/json</code></pre>
<h2>List the Flows</h2>
Now through the API we can pull all static flows that have been pushed with this API call. Notice all of the Tuples (header fields e.g. SrcMac, Dest,IP etc) being listed. Look for the "match" and "action" you pushed.
<pre class="code-sample"><code>$ curl http://192.168.1.208:8080/wm/staticflowentrypusher /list/00:00:5c:26:0a:5a:c8:b2/json</code></pre>
<h2>Clear or Delete the Static Flows</h2>
To clear all of the static flows the API call looks like this. Clear all flows the API also has a delete function documented:
<pre class="code-sample"><code>$ curl http://192.168.1.208:8080/wm/staticflowentrypusher /clear/00:00:5c:26:0a:5a:c8:b2/json</code></pre>

<hr />



<ul>
	<li><a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank">Getting Started OpenFlow OpenvSwitch Tutorial Lab – Setup</a></li>
	<li><a href="{{< relurl "/openflow-starter-tutorial-lab-1/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #1</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-2/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #2</a></li>
	<li><a href="{{< relurl "/openflow-tutorial-lab-3/" >}}" target="_blank">OpenFlow Starter Tutorial Lab #3</a></li>
</ul>

Thanks for stopping by.

