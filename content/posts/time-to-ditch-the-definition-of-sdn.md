+++
title = "Time to Ditch the Definition of SDN"
date = "2015-08-16T21:44:35+00:00"
lastmod = "2016-03-29T07:36:57+00:00"
author = "Brent Salisbury"
wp_id = 7820
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/time-to-ditch-the-definition-of-sdn/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "da2fdc455a82bd93256b2147e273fbf059db34af5248fef0ab0b631080cfafdd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Time to Ditch the Definition of SDN</h2>
While at a stoplight looking at the random news feeds on Linkedin I ran across a post of a recent <a href="https://www.opennetworking.org/?p=1830&option=com_wordpress&Itemid=316" target="_blank">blog post</a> by the ONF and the subsequent conversation where my friend <a href="http://blog.ipspace.net" target="_blank">Ivan Pepenlnjak</a> commented. So I threw in my two cents and quickly regretted it because Linkedin has an amazing ability to frustrate me as it updated the comment counter but ate my post and then disappeared. Awesome. So I'm going to post what I remember of it here. Let me also disclaim this isn't a response to a response and so on, the blog post simply mustered up enough energy in me to write a disappearing comment on LinkedIn. I really like Dan Pitt, few have made such a difference in networking by promoting new ways to think about networking like Dan has. He is merely pointing out the accepted definition of SDN, not defining it. My disagreement of the opinionated definition of SDN is simply where my thinking has landed after being involved in both ops/dev on both sides of the approach. We have centralized with one or two protocols vs whatever makes sense to the use case.

Quick review, OpenFlow is not a framework, architecture or philosophy, but a wire protocol that can be used to program a local or remote forwarding tables of an IP endpoint (presumably dwdm lambdas now too last I read the draft). SDN is where things get squirrely. There is this long running assumption that SDN is only SDN if it uses a centralized controller and programs remote endpoints/datapaths. I'm as guilty as the rest, before trying to guess the state of remote endpoints from a controller to deal with the nearly infinite number of states an endpoint can be in. I have also used that definition where it was convenient being one controller with lots of remote endpoints. If that works for you go nuts. Im not saying its bad in some cases, the traffic alignment of wireless controllers often make a lot of sense to have a central cluster to insert into the datapath since it needs to traverse that path anyways etc. Of course even here good opposing arguments can be made. 

My only criticisms of OpenFlow is it punts on state and it doesn't have simple to use defaults. That said I haven't had time to follow the drafts like I once did. Linux networking has become more and more interesting as time goes on. The appeal for me is it abstracts much of the irrelevant complexities. I really like <a href="https://www.kernel.org/doc/Documentation/networking/ipvlan.txt">IPVlan</a>. Offering both a low level and higher order abstraction, in the case of Linux IPRoute2 and Netlink makes it useful to a wider set of developers and users with a lower technical barrier to entry. Regarding state, introducing latency to network state is pretty insurmountable if performance is relevant in any way. The races conditions abound and eventually will cascade into failure. Dealing with state locally is hard enough, shipping it north is race condition central.

<h2>Too Many Contradictions</h2>
To say, SDN is only SDN if it programs remote datapaths hasn't made much sense for a while.




<ul>
	<li>If I use a local controller or process and program OVS using OF is that not SDN?</li>
	<li>If I use a local controller or process and program the configuration using NetConf is that not SDN?</li>
	<li>If I use a de-centralized controller or process and program the configuration using OpenFlow is that not SDN?</li>
	<li>If I use a logically-centralized controller or process and program the configuration using OpenFlow is that not SDN?</li>
	<li>If I use a local controller or process and program the datapath using Netlink is that not SDN?</li>
	<li>If I use a local controller or process and program the datapath configuration using NetConf is that not SDN?</li>
	<li>If I use a local controller or process and program the datapath using IPRoute2 is that not SDN?</li>
	<li>If I use a local controller or process and program packet forwarding policy using Ip Tables or HA Proxy is that not SDN?</li>
	<li>If I use a local or remote route server and program a custom next hop of a prefix is that not SDN?</li>
	<li>If I use a local controller or process and program the network using open source software and standardized APIs is that not SDN?</li>
</ul>



You get my point. What is SDN? Well, software programming networks? Haven't we always had that? Yes, but this time its different :) or I am just old, or both.

<ol class="legacy-numbers">

<ol>
	<li>SDN shouldn't be one particular architecture, protocol or definition and if we really want to be honest with the conversation, the true adoption of "SDN" has been provisioning and de-provisioning mostly ports but some paths in conjunction with compute orchestration.</li>
	<li>Let's ditch definitions for emerging nascent disruptions. Its obvious the ingredients of SDN include being open and programmatic. Open could be argued but I personally wouldn't attempt to defend anything beyond those two because there are too many holes in those ships and it starts to sound like religion.</li>
</ol>
</ol>

Discounting an innovation because it doesn't fit an academic definition will always lose.

<a href="{{< relurl "/wp-content/uploads/2015/08/angry_panda_vs_chef.gif" >}}"><img class="aligncenter size-full wp-image-7822" src="{{< relurl "/wp-content/uploads/2015/08/angry_panda_vs_chef.gif" >}}" alt="angry_panda_vs_chef" width="323" height="235" /></a>

How we deal with configuration and packet forwarding in networks needs to be flexible enough to capture the rapidly changing converged infra models. Interestingly, you have projects like P4 (and the startup to make money from it Barefoot) from some of the same folks that brought you OpenFlow. Rather then trying to get ODM/OEMs to conform to a specification, its seems to be looking to redefine networking hardware. I haven't looked much but I assume that rather then fixed length fields everything is essentially a TLV. We could use more of that thought in <a href="https://tools.ietf.org/html/draft-lapukhov-bgp-opaque-signaling-00" target="_blank">routing protocols</a> too if the technical debt can stay lower then previous attempts. The density and time scales of compute have and will continue to change exponentially. Devops has been the answer for systems engineers and will likely continue to be for converged infra as networking evolves towards that model. 

So lets keep it simple and inclusive, changing configurations line by line by hand like many of us did for a long time vs. programmatically changing the state the network. The new edge is the server, those will be managed in some form or fashion much more like compute. I also think containers on switches will have a significant impact for the vendor packaging apps and the user consuming or writing their own just like they would any other system. Aligning solutions to that only makes sense. Through all of this the emerging x-factor is packaging and simplicity in the user experience. Gone are the days of the week long OpenStack install, or Devstack dependency hell. What will ultimately decide what adopts and what doesn't is the people, not the technology.