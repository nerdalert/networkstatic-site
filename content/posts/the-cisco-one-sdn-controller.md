+++
title = "The Cisco ONE SDN Controller"
date = "2013-04-12T05:11:13+00:00"
lastmod = "2014-02-18T02:52:11+00:00"
author = "Brent Salisbury"
wp_id = 6266
categories = ["Speculative"]
tags = ["Cisco", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/the-cisco-one-sdn-controller/"
image = "/wp-content/uploads/2013/04/Cisco-ONE-Controller-Login.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "693fc3359071633f1c653b57a956810db4edccb7b115c998e534a9d5262c5665"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The Cisco ONE SDN Controller GUI</h2>
Cisco announced the ONE controller at Cisco Live last summer. The ONE has been in Beta for a few months now. There is still plenty of fragmentation around what SDN is and what it should solve. One generally accepted concept is the way we operate networks today, is showing signs of age. The announcement of OpenDaylight this week, pretty much sealed the SDN deal. Right, wrong or stupid, the old way of doing things will change. One generally agreed upon outcome is the way we operate networks, hand coding APIs calls into VTY sessions may be subject to change. So what is it going to look like, a GUI or an API using web services calls to operate the network? Yes.
<h2>Cisco ONE SDN/OpenFlow Controller GUI</h2>
It's good to see a functional GUI on a controller, that will be available soon. While some of us love to roll up our sleeves and hack away on code, many engineers aren't nerds like you and me. Even more often, network professionals would like to, but don't have the time. When people start learning OpenFlow, the rawness can be a bit daunting for those not used to OSS, which is many engineers/operators today. The key will be to see if OpenDaylight is a stall tactic for Insieme. OSS will ideally prevent this from being a misdirection.

The idea that you will have to write code to operate networks of the future, is not what I am seeing in my neck of the woods (as much as I would like to). Most of those I know need commercial products because of lack of time, lack of resources and risk avoidance. For those who are indifferent or just don't have the time to learn scripting, Python, JS, Java, Linux, etc there will be functional GUIs to operate, just like wireless and VoIP controllers today.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/Static-Flow.png" >}}" alt="Cisco ONE Static Flows"></figure>
<h2>SDN and Network Management</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/Cisco-ONE1.png" >}}" alt="Cisco ONE SDN"></figure>

<hr />

Troubleshooting the wired network today is fairly tragic. Green lights mean something is functional enough to send an ICMP echo reply. It is not indicative that all is well for the user getting ready to toss their laptop out the window. That is not a slight against network management companies. They come up with slick products with an incredibly limited toolkit. I am looking forward to see what companies like <a href="http://www.ixiacom.com/solutions/sdn-openflow/index.php" target="_blank">Ixia</a>, <a href="http://techfieldday.com/appearance/solarwinds-presents-at-networking-field-day-5/" target="_blank">Solarwinds</a>, <a href="http://techfieldday.com/appearance/spirent-presents-at-networking-field-day-4/" target="_blank">Spirent</a>, <a href="http://techfieldday.com/appearance/statseeker-presents-at-networking-field-day-4/" target="_blank">Stat Seeker</a> and others will be able to do with new primitives and frameworks.
<h2>SDN and Network Management</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/Cisco-ONE-OpenFlow.png" >}}" alt="Cisco ONE Static Flows"></figure>

<hr />

A couple of things get me really excited, plugging a switch into the network and watching it pop up in a controller, ready to be configured is one of those. Wired switch deployments, just got about %80 more operationally efficient. Today operators either have, A) remote hands with out of band TTY connections, B) roll experienced techs to the field to program a switch or C) live in web 2.0 and twist the vendors arm to get some custom boot strapping for homegrown scripts. This is what <a href="{{< relurl "/the-good-and-bad-of-wireless/" >}}" target="_blank">wireless</a> and VoIP has had for a long time.

<a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">Managing wireless</a> networks an IP telephony networks is constantly improving. Why is that? They are centralized or logically centralized rather then distributed. Decentralization within an ASN is the goal, not distributed. Decentralization can be presented as centralized via abstraction and state distribution with consistency either using SPFs or whatever else fits your environment.

Pushing policy by hand to central points scales or pushing policy by hand to 10,000 points. We are far from the magical greatness of predictive analysis from data analytics programming the functions of our network, so until then, we still need to craft policy. That all said, there isn't one answer, its more options to fit your organization, use case and applications.

<hr />

Back to the controller, its a pretty sexy UI.
<h2>Cisco ONE Topology Independent Forwarding</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/TIF-Forwarding.png" >}}" alt="Cisco ONE Controller"></figure>

<hr />

There is a custom forwarding application for classifying and stitching a path A to Z rather then A -&gt; B -&gt; C ... -&gt; Z. The constraints are flexible, greater then, less then, bandwidth, latency, regex etc. Some constraints such as latency, imply control on the switch. Latency in OpenFlow is measured from the controller to the switch rather then switch to switch. Without having the onePK beta software, I can only speculate. The value of being able to key off of any attribute for path selection transcends the DC, SP and enterprise.

There is plenty of maturity to go with OpenFlow, mostly around having actual hardware support and products to beta such as the ONE. such as some OAM functionality that is missing from OpenFlow. While fast failover is addressed with group-tables, something requiring CP functionality like BFD is just not doable with OpenFlow. Controller logic and placement can address much of that in my opinion. That said, skeptics of OpenFlow, go grab a junior engineer, give him a packet capture of OpenFlow flowmods and along with a capture of RSVP signaled MPLS/TE extensions with OSPF link updates and MPLS LSA (then add L4 somewhere) and ask what is going on in each one. My money is on OpenFlow mainly because edge program logic is just easier. Macro or native for the aggregation is fine with me either way. If it missed the edge, it makes less sense at aggregation.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/OpenFlow-Packet-Flowmod.png" >}}" alt="OpenFlow Flowmod"></figure>

<hr />

Its not a far stretch to assume that those are proprietary features from onePK. onePK does much more for the ONE controller then it does for me. The last thing I am looking to do is roll a control plane. That said, onePK adding pre-standards to the OpenFlow spec doesn't bother me. Its FabricPath before TRILL, ISL before 802.1q, if a vendor adds differentiating functionality that the OpenFlow specification cannot offer, then go nuts. Personally my litmus test will simply be, can I jack another vendor into the controller and achieve functionality? If yes, the controller or application stays on the list, if no, the vertical solution needs to differentiate in hardware to justify.
<h2>Cisco ONE at Network Field Day #5</h2>
<p><a href="http://vimeo.com/61490502">Watch video on Vimeo</a></p>

<hr />

<h2>My Thoughts and a Little OpenDaylight</h2>
This was a busy week, the long awaited OpenDaylight announced. Networking hit a milestone, this milestone more then any is, it learned from the rest of computing. Rather then an extracted controller war, we may move straight to where it counts, the application. When Microsoft is now developing Office apps for Apple IOS, you know the operating system is only as good as the apps running on it, not solitaire. We may have stack wars,<a href="http://www.gartner.com/technology/reprints.do?id=1-1C3IGID&ct=120919&st=sb" target="_blank"> CloudStack vs. OpenStack </a>played out last year. Dell is taking the Citrix route with <a href="http://searchsdn.techtarget.com/news/2240179932/Dell-and-Object-Management-Group-launch-an-SDN-standards-body" target="_blank">OMG</a> as compared to CloudStack, maybe it will work. One thing tends to stay constant in open source, <a href="{{< relurl "/installing-openstack-grizzly-with-devstack/" >}}" target="_blank">more and better code wins</a>.

The other win was the embrace of open source. I am less skeptical then some of my friends, mainly because irregardless of the OpenDaylight outcome, we are destined to have open source alternatives along with commercial products. I am also much less critical of Cisco in this, they led an initiative to open source an SDN framework.

What still blows me away is that everyone (outside of the startups) who had a chance to take the lead on the disruption, with nothing to lose and marketshare to take, sat around hedging their bets on what Cisco would do. Unbelievable. Secondly, that people inside of Cisco were able to convince the C-levels to make such a move is impressive. Daylight board members have one vote at the table, contribute upstream and thats your influence. Thats a lot of control to let go so kudos.

That said, they are still dragging their feet in the enterprise waiting on Furtune 100 to demand OpenFlow. Apparently it doesn't matter because no other incumbents will do anything until Cisco makes the first move. Joking, sort of. Not really. HP is in the game in the enterprise with the only GA PoE OpenFlow enabled gear you can buy today, period.

Wether its the ONE, Big Switch or anyone else's most of us don't have a stake and would probably like to see a blending of best components (. On the OpenDaylight controller(s). Both are Java, more then likely forked from David Erickson's Beacon. Who by the way, is a nice guy who constantly monitors the Beacon forum and is looking for <a href="https://openflow.stanford.edu/forums/forum/4-beacon-general/" target="_blank">beta testers</a> so throw him an intern if you have a couple. The difference is OSGI v. Netty. Both are great, maybe there can be some agreement, or a cagematch, either one is fun.

<blockquote class="pullquote">Many people mistakenly think a new technology cancels out an old one.<footer>Judith Martin</footer></blockquote>

We need products, transparency and open dialogues. We are missing some of that. I stay fairly uncritical of that because it is still early. There isn't much room for ivory towers and black holes in open source. NDAs are also getting a bit old, it's not launch codes and its not exactly a secret who has a controller, who has OpenFlow switch code and who doesn't have anything and is playing catchup. Let us see products like this or don't talk about it. The community is needing to define how SDN is getting integrated, especially outside of the data center (yes that exists:-).

My skepticism around OpenDaylight is politics and the value still placed on edge hardware. The SDN core is the edge, OpenStack has been unbelievably successful, but no one there is saying their Intel chips are better then the next OEMs Intel chips (well maybe ARM soon).

On the topic of hardware, it needs to get better. L2 rewrites in hardware is going to reinvent the L2 domain. Intel and the <a href="http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/ethernet-switch-fm6000-sdn-paper.pdf" target="_blank">FM6000</a> Seacliff Trail switch is going to eat everyones lunch (including Broadcom) if they don't start shipping OpenFlow/SDN kit soon. Look at the Intel partners. Along with better OF support in hardware, we also need investment protection for existing hardware. If you buy kit today, might be worth thinking about making sure it supports OpenFlow.

IBM stock is at an all time high. Disruptive technologies are manageable.
<h2>Additional Links</h2>



<ul>
<li><a href="http://packetpushers.net/programming-101-for-network-engineers-why-bother/" target="_blank">Programming 101 for Network Engineers – Why Bother?</a></li>
	<li><a href="http://www.networkcomputing.com/data-networking-management/how-to-set-up-floodlight-and-test-openfl/240152558?token=5711907302e5cbc6ea756fe2a243d893" target="_blank">How To Set Up Floodlight and Test OpenFlow Rules</a></li>
	<li><a href="http://www.networkcomputing.com/data-networking-management/openflow-test-deployment-options/240152428" target="_blank">OpenFlow Test Deployment Options</a></li>
</ul>


<hr />

So don't be shy to get out there and throw your hat in the ring. The community is respectful of others ideas. Get a blog for free over at wordpress or go blog at <a href="http://packetpushers.net" target="_blank">PacketPushers</a>. Or even better both! Tell your vendors what you want to see moving forward, even if its nothing. Vendor field sales teams will be hit and miss, bypass them if they blow you off.