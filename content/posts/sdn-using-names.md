+++
title = "SDN Using Names"
date = "2012-10-09T10:05:41+00:00"
lastmod = "2012-11-27T07:34:20+00:00"
author = "Brent Salisbury"
wp_id = 2990
categories = ["Programming"]
tags = ["Software Defined Networking", "dns"]
description = ""
url = "/sdn-using-names/"
image = "/wp-content/uploads/2012/10/SDN-DNS-DC.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d3008bc567b2e54c989ff2a6a8d0da757ea6394f9474a2a7a51b601ffaf8d950"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> SDN Using Names</h3>
SDN Using Names as an approach to simplifying policy application and ease operations barrier: For anyone who is visiting for the first time, first thank you for visiting. By day I design networks with completely traditional means, the handful of scalable architectures with a slight amount of flexibility, BGP/VPNs thats it. I am a one trick pony as the saying goes, because nothing else is the right combination of stability, scalability and lowest possible operational TCO (obviously generalized). Needless to say, it isn't working in an R&amp;D lab solving next-gen network problems during the day. I say that because there are obvious performance limitations in what I am proposing but I feel silicon innovation will solve much of those problems just as merchant silicon has opened a new world up to the x86 industry almost two decades ago with the microprocessor and much more recently starting to bring the hope of horizontalization to the networking industry. By night, I think of ways to fix the ever growing frustrating list of problems we in the networking industry face. Our answers are to create more problems with more protocols/encapsulation/shims/duck tape rather than as Scott Shanker puts it "The ability to master complexity is not the same as the ability to extract simplicity".
<h3>SDN Abstraction Refresher</h3>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/SDN-Abstraction-Layers.jpg" >}}"><img class="size-full wp-image-2993 aligncenter" title="SDN-Abstraction-Layers" src="{{< relurl "/wp-content/uploads/2012/10/SDN-Abstraction-Layers.jpg" >}}" alt="SDN-Abstraction-Layers" width="537" height="424" /></a><em><strong>Figure 1.</strong> </em>Some quick concepts on abstraction layers as compared to x86 concepts.</p>
I volunteered to pick up a scholarship program that was in jeopardy, because keeping pace with operating networks that grow at <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">exponential</a> rates on tight and shrinking budgets is a monumental task that my amazing colleagues perform every minute of the year. Instead of going through 50 some odd IGPs, EGPs and encapsulations I thought we should go a different path. The tragic history of networking over the past 15 years since the train came of the rails after really smart folks stabilized BGP and the Internet was born did not seem appropriate to ready these two really smart CS interns. I was listening to Nick Mckeon (master evangelist for disruption) in a recorded talk last weekend and he described the network router today as conforming to 6,000 RFCs. No wonder we lost our way.

So the past couple of weeks the three of us at night have started writing a module to plug into the <a href="http://floodlight.openflowhub.org" target="_blank">FloodLight</a> open source OpenFlow Controller written in Java that has a very nicely evolving community around it with some great contributions.

I am particularly interested in relieving operational burden of provisioning and de-provisioning of network resources. The other problem that I and everyone else that has ever stepped foot in a data center with a serial cable in the past 15 years is stretching Layer2 domains for live workload migration. My friend <a href="http://blog.ioshints.info" target="_blank">Ivan Pepelnjak</a> is much more effective in describing and bashing people over the head with why bridging domains do not scale. One of the few ways to deliver high availability to broken applications that have no layer3 HA mechanism to where a VM can be shutdown, readdressed and migrated is through DNS load balancing. That topic was beat to death <a href="http://www.tenereillo.com/GSLBPageOfShame.htm" target="_blank">10 years ago</a>, not looking to open that can of worms, just using the concept as an example.
<h3>DNS Names are Decoupled from Infrastructure and Much More Flexible</h3>
There is a research project out there today that is looking at replacing IP with names someday that I heard Scott Shanker discuss in a recording recently that sounded very logical. That would be an incredibly long funnel, considering we can't seem to efficiently migrate from IPv4 to IPv6. The fundamentals are spot on, but I may be retired or stroked out well before. For now I think there are some use cases that the me and the intern night crew will be chasing.

There are some operational constraints of IPv4/6 addressing could alleviate some provisioning challenges and policy application by using IP to DNS name mappings for flow instantiation. I will be posting more thoughts on problems this could help solve particularly in the realm of edge classification that is not as tightly coupled to inflexible methods. There is a movement to enable networks to be self provisioned but so far it is strictly in the hypervisor or adding more complexity rather than less.

I like the extreme simplicity of leveraging naming as every systems administrator out there already does it today. Dynamic DNS for the enterprise is also quite prevalent and could see the use cases for mapping tenancies to a DNS name provisioned from a typical single sign on today. NAC products today are a tangled mess that try and flip data paths or wedge a spinning disk inline of high speed links, no thanks. DNS consistency is also easily federated between autonomous systems which I think could be attractive in a regional scenario for providers.

Throwing some ideas out there and when we get enough night midnight hours burned we will get the code out there and submit it for a good bashing. The concepts are why we are interested in this more than anything but if a packet-in event is piping to a controller for a flow lookup a simple IP to name lookup is completely negligible at small scale. Scale being the keyword so once we finish the modules we will do some comparisons. There will be some really smart interns needing jobs next year which by the way, I will have links to their sites as soon as the get them put up for job inquiries as they are both very sharp and motivated. I have mostly conceptual drawings to kickstart the ideas along with what I am guessing will be somewhere in the ballpark of the lookup algorithm below.
<h3>Self Provisioned Policy via DNS name mappings algorithm:</h3>
<ul>
	<li>Ends host receives a traditional DNS mapping either statically assigned by the Systems Administrator or Dynamically via Directory Services. This is used today to classify services e.g - erp.company.com</li>
</ul>
<div></div>
<ul>
	<li>The DNS records are updated and notify the distributed DNS caching servers running on the SDN controllers there has been an update and acknowledge receipt and consistency.</li>
</ul>
<div></div>
<ul>
	<li>The caching server then processes the FQDN, hostname, suffix, prefix or any combination or even portion (RegEx) of a field thereof and creates a data structure that maps the name to policy. That could be in the form of simple associative arrays with the key being the name and the value being the action or a more robust data structure such as hash tables or binary search trees. This would be very similar to address prefix matching algorithms. The name to instruction preprocessing could be offloaded to a policy engine that could collect policy from a number of plug-gable applications that are operating in the ecosystem such as Load Balancing, Traffic Engineering, Network Access Control (NAC), QOS policy or any other number of services that are being done with little to no understand of the holistic policy. Beyond just forwarding policy those same mapping could and someday will take into account analytics of compute, storage, economics, and other business objectives.</li>
</ul>
<div></div>
<ul>
	<li>OpenFlow example: A flow is initiated from a new flow triggering a packet-in event from the physical or virtual switch for a forwarding decision from the SDN controller(s).</li>
</ul>
<div></div>
<ul>
	<li> The SDN controller resolves the IPv4 or IPv6 address extracted from the IP header and queries its local DNS cache to resolve the IP to name dictionary.</li>
</ul>
<div></div>
<ul>
	<li> After the controller resolves the names which could be broken into as many n-tuple(s) as desired depending on how coarse or fine the policy being matched is it either matches or it does not. Matched policy would construct the action set and send it back to the virtual or physical switch with its forwarding instructions to be instantiated into the forwarding tables of the switch. The switch then retrieves any buffered packets collected from the delta of the instruction lookup and executes the instruction as defined by the SDN controller policy. If there is no match the controller can either drop the flow or perform a default instruction as defined in the controller policy.</li>
</ul>
<div></div>
<ul>
	<li>Increment/decrement counters, write to disk or send analytics north, rinse and repeat.</li>
</ul>
<div><a href="{{< relurl "/wp-content/uploads/2012/10/SDN-SIMPLE-DNS.jpg" >}}"><img class="size-full wp-image-2994 aligncenter" title="SDN-SIMPLE-DNS" src="{{< relurl "/wp-content/uploads/2012/10/SDN-SIMPLE-DNS.jpg" >}}" alt="SDN-SIMPLE-DNS-te" width="340" height="290" /></a></div>
<strong><em>Figure 2.</em></strong> Simple example scenario: Classify traffic based on DNS values and select the path based on policy proactively or reactively residing on the SDN Controller. It does not have to be just the path. There are many powerful headers between Layer2-4 that can be hashed into policy.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/SDN-DNS-DC.jpg" >}}"><img class="size-full wp-image-2995 aligncenter" title="SDN-DNS-DC" src="{{< relurl "/wp-content/uploads/2012/10/SDN-DNS-DC.jpg" >}}" alt="SDN-DNS-DC-tenancy" width="584" height="306" /></a></p>
<p style="text-align: left;"><strong><em>Figure 3</em>.</strong> Multi-Tenancy could be mapped with authorized with Naming in an easy manner for operators. If I were a systems administrator I think I would prefer getting all networking by requesting a subdomain than getting put in the 10 step process of current cumbersome network provisioning process as it stands in all organizations big and small today.</p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/SDN-SP.jpg" >}}"><img class="size-full wp-image-2996 aligncenter" title="SDN-SP" src="{{< relurl "/wp-content/uploads/2012/10/SDN-SP.jpg" >}}" alt="SDN-SP" width="420" height="438" /></a></p>
 <strong><em>Figure 4.</em> </strong>Coloring, Provisioning and Operating Traffic Engineered Paths today is Pretty Close to the Definition of Insanity. The option to only select a particular tenant and leave the rest of the pipeline to the default path will bring new tools and scale. What is the alternative PBR or overly complex Tunnels.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/SDN-Policy.jpg" >}}"><img class="size-full wp-image-2997 aligncenter" title="SDN-Policy" src="{{< relurl "/wp-content/uploads/2012/10/SDN-Policy.jpg" >}}" alt="SDN-Policy" width="446" height="401" /></a></p>
<strong>Figure 5.</strong> DNS Names are Being Allocated by Systems Engineers today w/ Classifications such as Role, Tenancy and Security Zoning. This Delivers a Network that Actually Supports the Policy Dynamically through Existing Classifications Already being Used Universally Today.

Thanks for taking a look at this little idea, we will have some code ready in four or five weekends and maybe some benchmarks too. Worst case is my Java Programming gets better but probably not tidier.