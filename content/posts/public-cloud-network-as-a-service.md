+++
title = "Public Cloud and Network as a Service"
date = "2012-08-21T04:59:44+00:00"
lastmod = "2013-09-05T21:54:09+00:00"
author = "Brent Salisbury"
wp_id = 2307
categories = ["Speculative"]
tags = ["OpenStack", "Public Cloud"]
description = ""
url = "/public-cloud-network-as-a-service/"
aliases = ["/2012/08/public-cloud-network-as-a-service/"]
image = "/wp-content/uploads/2012/08/cabling-bad.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "08d913724310ac82230d8615759f99961484ae11fdaba894bf00c228f1b8083f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Public Cloud and Network as a Service</h2>
The first part of the post was building the <a href="{{< relurl "/2012/08/the-hp-public-cloud-and-openstack/" >}}">Public Cloud</a> node. The second part of this post is going to be a primitive blue print for how to build a hybrid private/public network and what network as a service could mean. Without reliable national broadband and backbone networks both provider and customer will be taking serious risks. I will ask one question and move on, what incentive does a carrier have to improve their infrastructure if they are the incumbent with no competition? Puzzling we get so enthralled in the minute details of technology yet something as broken as the very backbone substrate right before our eyes. It isn't waiting on any technological breakthroughs, only vision and leadership.



<aside class="legacy-callout"><strong>So WtF is Hybrid Cloud Networking? </strong>It is a fancy name for GRE and VXLAN tunnels getting pinned from a local cloud stack to a public cloud stack. Voila!</aside>

<h2>Grandpas Network, What has Changed?</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/fail-cabling.jpg" >}}" alt="Cloud Internet Fail"></figure>
There has been a growing swell in the networking industry coined Software Defined Networking (SDN) that has culminated into a full fledged evolution. One primary drivers of change in the networking industry has come from commodity hardware. Researchers at Stanford began working to decouple the network operating system and control plane. As soon as <a href="http://blog.ioshints.info/2012/05/openflow-google-brilliant-but-not.html" target="_blank">Google</a> bought in things got serious. As a result, <a href="http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/" target="_blank">merchant silicon</a> manufacturers have supposedly begun to alter their "off the shelf silicon" to facilitate this exploration. Still today, the topic of decoupling the control and management plane into some form of centralization is enough to start a nerd rage brawl. 

The second driver, is the need for much more abstraction and scale in the hyper-scale data centers. Public cloud providers need to better align the network with automation and orchestration eco's in the data center. Folks like Amazon, have made it clear they expect vendors to pursue this support or risk some fairly large accounts. Data center orchestration is merely a subset of <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">network management</a> and operational efficiency which has but nothing but a total joke in the networking industry to date. So here is a rough cut at what one option and some research someone could use if their CEO walked in tomorrow and said he was all in for the public cloud and you had to deliver something other than laughter or even sarcasm, well maybe both.
</h2><h2 class="legacy-heading">Tunnels in the Data Center</h2></h2>
The early productization that has came from the same Stanford folks like Mckeown (Nicira), Shanker (Nicira), Casado (Nicira), Ericson (Beacon/origon of Floodlight) and Appenzeller (BigSwitch) all rely heeavily on tunnuling encapsulations/overlays. What there seems to be a demand for is the need to unglue the compute and storage from the physical networking limitations. Unfortunately this means sprawling layer2 adjacencies everywhere to facilitate things like live workload migrations and then of course don't forget poorly written applications that communicate through broadcasts. Spanning-tree cant hack it and hasn't been able to for the last decade. I plugged a random vendor switch into a data center the other day and probably triple checked myself, to make sure these two vendors were actually speaking the same language and a bridging loop wasn't going to melt down that data center.

These new ideas are all grounded in traditional networking, which makes adoption much more realistic. Our bread and butter today are <a href="http://packetpushers.net/show-102-a-layer-of-indirection-is-mpls-tunneling/" target="_blank">overlays and tunnels</a> vis a vis MPLS or lesser scalable technologies. MPLS is a prime example of trying to solve the problem of the edge and on my top 3 list of most important technologies in the history of networks. That said, I think we can deliver better virtualization via software abstraction. That debate is for another day.
<h2>Tunnels to Cloud Providers</h2>

Is someone going to try and do a live workload migration (vMotion) to a cloud provider? They may try, but the weak speeds of our carrier networks are no where near being able to replicate memory across the Internet reliably. What would be important to many people I think is to provision or extend their network into a cloud providers network and VM. We have been doing this for many years at a huge price tag in leased lines, local and remote networking hardware and exorbitant collocation prices.

Early adoption will no doubt freak many people especially those in the practice of security so one way to maintain those policy controls will be to extend the particular security zone into the cloud through a tunnel. While there are still security problems with this it is a significantly lower price tag to get into the cloud from the cost avoidance of not duplicating services like IDS/Firewall/Flow analysis and all of the other weird appliances we have come to rely on and break out of networking boxes for purpose built operations which is pretty much just x86 processors on a board anymore anyways.
<h2>A Dash of Fear</h2>
The OpenStack framework is significantly more flexible than the unyielding rigors of the network architecture of Amazon AWS/ECS, this can also present security challenges. You are on a broadcast domain with other tenants. I have never been one to get overly concerned with security since there are hordes of security folks for that already but there is quite a bit of personal responsibility in giving the freedom and mixed tenancy like that. It will be interesting to see what tricks the providers will use until more mature DC ~SDN products start becoming mainstream to deal with virtualizing flat networks. Vlans would not even come close to solving that problem due to ID limitations. For all I know they may be doing some of that today but ICMP is allowed on the flat backend network to other hosts from what I observed.

<h2>Still Waiting for New Silicon</h2>
Silicon is developed in foundries. Fab and Fabless engineered chips take years. Q1-Q2 of 2013 will bring announcements and more flexibility than what can be done on today's hardware optimized for distribution. We will start seeing a combination of Hypervisor tunneling over any L2/L3 unbundled network from the likes of <a href="http://www.thecloudcast.net/2012/07/the-cloudcast-eps47-sdn-openflow-and.html" target="_blank">BigSwitch</a>, <a href="http://www.ethernetsummit.com/English/Collaterals/Proceedings/2012/20120222_2-103_Recio.pdf" target="_blank">IBM DOVE</a> and the one who started it all VMWare(Nicira). By the way, we already do overlay/encaps today. The future are encaps, for simplicity and packet preservation. Tunneled networks depend on the native network. One drawback is the lack of operational visibility from the substrate. I would expect to start seeing ASIC/Chipset manufacturers begin to added support for these overlay encapsulations in their data center gear in the next few cycles. Usable networking hardware is too far off to even fathom at this point. The vSwitch is the early and only foreseeable SDN win to really change networking. Hardware cycles will get there but I think it will take an Intel to change it. They are the only ones I see really disrupting hardware other then margin deflation.

It is just the beginning of seeing who can embrace change and who isn't willing to work themselves out of one opportunity and into a greater opportunity. Don't let vendors explain to you why your needs as a customer is not reasonable, they don't do that to Google, Facebook, Amazon etc. When was the last field engineer you meet more up to speed on the industry than you? Not likely often, the feedback loops of what these product managers get themselves into by convincing everyone their way is the only way is painful to witness. There is way to much complexity in anything related to technology to walk around sporting arrogance ego. If you are that smart you should be working on a much longer <a href="http://www.popsci.com/technology/article/2012-08/researchers-test-router-thats-step-toward-quantum-computing-internet" target="_blank">term problem.</a>
<h2>Network as a Service (NaaS)</h2>
Is this Network as a Service? Not interested in the semantics, but I guess this would be my closest stab at it today, with the primitive tools we have to work with for even basic management . The provider today can provision some but very little networking service. We can get some public IP addresses out of a dynamic pool and we get self-provisioned security policy. The services will mature and become much more robust as the APIs mature and more flexibility is demanded from large scale customers.
</h2><h2 class="legacy-heading">The Testbed in Mom's Basement</h2></h2>

There are three nodes in the Private Cloud and one node in the HP Cloud. The transport between the Private and Public Cloud is the Internet. There are two 1Gb connections and a 10Gb Internet connections out of the private cloud site into the Internet. The AS-Path to the HP Cloud node was Asymmetric to what appears to be a site in Las Vegas  (az-3.region-a.geo-1) sourcing from Level 3. Each node has two tunnels, one is VXLan encapsulated and one is GRE encapsulated. Each tunnel endpoint terminates only to the node in the center that acts as a Hub w/spokes. That is enough to get end to end connectivity of all spokes. Compiled on each node is <a href="http://openvswitch.org" target="_blank">Open vSwitch</a> using a Cisco fork that supports VXLan encap. Detailed instructions for that build can be found <a href="{{< relurl "/2012/07/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank">here</a>.

For a quick build and install of Open vSwitch this will work for an Ubuntu 12.04 install.
<pre class="brush: bash; gutter: false">apt-get install -y git python-simplejson python-qt4 python-twisted-conch automake autoconf gcc uml-utilities libtool build-essential git pkg-config linux-headers-`uname -r`
git clone https://github.com/mestery/ovs-vxlan.git
cd ovs-vxlan
git checkout vxlan
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make &amp;&amp; make install
insmod datapath/linux/openvswitch.ko
insmod datapath/linux/brcompat.ko
touch /usr/local/etc/ovs-vswitchd.conf
mkdir -p /usr/local/etc/openvswitch
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
ovsdb-server /usr/local/etc/openvswitch/conf.db \
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,manager_options \
--private-key=db:SSL,private_key \
--certificate=db:SSL,certificate \
--bootstrap-ca-cert=db:SSL,ca_cert --pidfile --detach --log-file
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
ovs-vsctl show</pre>
<h2>Baseline Bandwidth</h2>

Here is output from the Private Cloud site of bandwidth pulling an image from Argonne National Labs. The HP pull was much less than 20MBytes/sec but I didn't think that a fair comparison since I was picking up Argonne over 10Gb on <a href="http://www.internet2.edu/network/" target="_blank">Internet2</a>.
<pre class="brush: bash; gutter: false; first-line: 1; highlight: []; html-script: false">wget http://mirror.anl.gov/pub/ubuntu-iso/CDs-Ubuntu/12.04/ubuntu-12.04-server-amd64.iso--2012-08-20 03:21:03--  http://mirror.anl.gov/pub/ubuntu-iso/CDs-Ubuntu/12.04/ubuntu-12.04-server-amd64.iso
Resolving mirror.anl.gov (mirror.anl.gov)... 146.137.96.7, 2620:0:dc0:1800:214:4fff:fe7d:1b9
Connecting to mirror.anl.gov (mirror.anl.gov)|146.137.96.7|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 717533184 (684M) [application/octet-stream]
Saving to: `ubuntu-12.04-server-amd64.iso&#039;
100%[================================================&gt;] 717,533,184 35.7M/s   in 26s    
2012-08-20 03:21:29 (26.5 MB/s) - `ubuntu-12.04-server-amd64.iso&#039; saved [717533184/717533184]</pre>
&nbsp;
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Topology-demo2.jpg" >}}"><img class="aligncenter  wp-image-2359" title="Topology-demo" src="{{< relurl "/wp-content/uploads/2012/08/Topology-demo2.jpg" >}}" alt="" width="524" height="343" /></a></p>
<em>Figure 1</em>. Three OpenStack local nodes as part of the Private Cloud build a tunnel through one box to the HP Cloud instance. Isn't it great, we use cloud to denote the unknown yet we speculate on a big unknown cloud as the future. Im ok with that though. Much easier to be an optimist and get disappointed then hate everything.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Big-pic.jpg" >}}"><img class="aligncenter  wp-image-2312" title="Big-pic overlay" src="{{< relurl "/wp-content/uploads/2012/08/Big-pic.jpg" >}}" alt="" width="488" height="331" /></a></p>
<em>Figure 2</em>. This can scale up and out if properly orchestrated.<span style="text-align: center;"> </span>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/VXLan.jpg" >}}"><img class="aligncenter  wp-image-2317" title="VXLan" src="{{< relurl "/wp-content/uploads/2012/08/VXLan.jpg" >}}" alt="" width="491" height="307" /></a></p>
<em>Figure 3</em>. In the OpenStack Dashboards on both the Private and Public Clouds open UDP 8472 to allow for the VXLan packet traversal which is carrying the encapsulated payload of source destination MAC/IP/Transport headers from one VM to another.

<a href="{{< relurl "/wp-content/uploads/2012/08/ove-hub-show.jpg" >}}"><img class="aligncenter size-full wp-image-2319" title="ove-hub-show" src="{{< relurl "/wp-content/uploads/2012/08/ove-hub-show.jpg" >}}" alt="" width="552" height="560" /></a>

<em>Figure 4</em>.The Hub Open vSwitch configuration. Each tunnel endpoint is associated to a bridge with its own unique Data Path ID (DPID)
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/no-tunel.jpg" >}}"><img class="aligncenter  wp-image-2318" title="no-tunel" src="{{< relurl "/wp-content/uploads/2012/08/no-tunel.jpg" >}}" alt="" width="581" height="266" /></a></p>
<em>Figure 5</em>. Baseline Bandwidth from the Private to Public Cloud over the Internet un-encapsulated. Average 29Mbytes/sec.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/gre-spoke-to-hp.jpg" >}}"><img class="aligncenter  wp-image-2321" title="gre-spoke-to-hp-cloud" src="{{< relurl "/wp-content/uploads/2012/08/gre-spoke-to-hp.jpg" >}}" alt="" width="530" height="258" /></a></p>
<em>Figure 6</em>. Iperf output of a spoke to the Public Cloud instance. Average bandwidth of 18Mbytes/sec.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/spoke-to-hub.jpg" >}}"><img class="aligncenter  wp-image-2322" title="spoke-to-hub" src="{{< relurl "/wp-content/uploads/2012/08/spoke-to-hub.jpg" >}}" alt="" width="485" height="144" /></a></p>
<em>Figure 7</em>. Baseline bandwidth from spoke to spoke un-encapsulated internal to the Private Cloud and traversing a 10Gb top of rack switch w/ an MTU of 9000.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/spoke-to-spoke-gre.jpg" >}}"><img class="aligncenter  wp-image-2325" title="spoke-to-spoke-gre" src="{{< relurl "/wp-content/uploads/2012/08/spoke-to-spoke-gre.jpg" >}}" alt="" width="545" height="162" /></a></p>
<em>Figure 8</em>. Baseline bandwidth from spoke to spoke with a GRE encapsulated tunnel internal to the Private Cloud and traversing a 10Gb top of rack switch w/ an MTU of 9000.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/spoke-to-spoke-vxlan.jpg" >}}"><img class="aligncenter  wp-image-2324" title="spoke-to-spoke-vxlan" src="{{< relurl "/wp-content/uploads/2012/08/spoke-to-spoke-vxlan.jpg" >}}" alt="" width="537" height="161" /></a></p>
<em>Figure 8</em>. Baseline bandwidth from spoke to spoke with a VXLan encapsulated tunnel internal to the Private Cloud and traversing a 10Gb top of rack switch w/ an MTU of 9000.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/gre-spoke-to-hp2.jpg" >}}"><img class="aligncenter  wp-image-2326" title="gre-spoke-to-hp" src="{{< relurl "/wp-content/uploads/2012/08/gre-spoke-to-hp2.jpg" >}}" alt="" width="478" height="232" /></a></p>
<em>Figure 9. </em>Private Spoke to Cloud Spoke w/GRE encapsulation.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/vxlan-spoke-to-hp.jpg" >}}"><img class="aligncenter  wp-image-2327" title="vxlan-spoke-to-hp" src="{{< relurl "/wp-content/uploads/2012/08/vxlan-spoke-to-hp.jpg" >}}" alt="" width="532" height="261" /></a></p>
<em>Figure 10. </em>Private Spoke to Cloud Spoke w/VXLan encapsulation.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/all-hosts-gre.jpg" >}}"><img class="aligncenter  wp-image-2328" title="all-hosts-gre" src="{{< relurl "/wp-content/uploads/2012/08/all-hosts-gre.jpg" >}}" alt="" width="534" height="404" /></a></p>
<em>Figure 11. All </em>Private Spokes to Cloud Spoke simultaneously w/GRE encapsulation.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/all-hosts-vxlan.jpg" >}}"><img class="aligncenter  wp-image-2329" title="all-hosts-vxlan" src="{{< relurl "/wp-content/uploads/2012/08/all-hosts-vxlan.jpg" >}}" alt="" width="531" height="258" /></a></p>
<em>Figure 12. All<em> </em>Private Spokes to Cloud Spoke simultaneously w/GRE encapsulation.</em>
<hr>
Thats all for now. I need to proof these posts but time is lacking and have day job work to get done before bed at 4am. The research data is more interesting than my blathering anyways. Thanks for stopping by.