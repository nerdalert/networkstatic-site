+++
title = "The HP Public Cloud and OpenStack"
date = "2012-08-21T04:48:34+00:00"
lastmod = "2012-12-09T06:41:27+00:00"
author = "Brent Salisbury"
wp_id = 2300
categories = ["Speculative"]
tags = ["OpenStack", "Public Cloud"]
description = ""
url = "/the-hp-public-cloud-and-openstack/"
aliases = ["/2012/08/the-hp-public-cloud-and-openstack/"]
image = "/wp-content/uploads/2012/08/unicorn-accountant.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "83940777290af7ef15e76f705cb18837419e3ecddc157dff0329898338332e7c"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The HP Public Cloud and OpenStack</h2>
We have listened to people ramble on about the promise of the cloud and the impact on infrastructure for a few years now, but very rarely has anyone articulated a reasonable blueprint on ramp into this public cloud. SaaS is everywhere, the application was and will continue to be the low hanging fruit, the rest is a bit more difficult. Even the United States Government has a cloud first policy, too bad its not a broadband first policy. To say the public cloud is remotely close to the end game is irresponsible if you gloss over a weak National Internet infrastructure that is strangle-held by the incumbent local exchanges carriers (ILEC) and cable companies only interested in serving what serves themselves. You can't blame them, they answer to stockholders not tax payers. This isn't a rant on the FCC or the horrendous <a href="http://www.broadband.gov/plan/" target="_blank">lack</a> of an actionable national broadband roadmap but if we are serious about public cloud we had better get serious about the public (not stakeholder but tax payer owned) infrastructures. Later in the post we will provision an HP OpenStack public cloud instance and in the next post setup what today may qualify as network as a service alpha v0.9 and actually build a hybrid private/public cloud. Sorry about the unicorn addiction, I cant get enough, that one does my taxes, cute little fella.
<h2>Transport to the "public cloud" today</h2>
<ol class="legacy-numbers">
<ol>
	<li>Leased lines from your local premise to a cloud provider. At the point you are picking up this sort of cost you are much closer to a colocation arrangement or on a scale that can absorb the cost that would wreck most business cases.</li>
	<li>Through the Internets. Also lots of problems, but one of those is not necessarily economic. The cost of commodity Internet services in the US has gone from $60-$100 per/1mb to well under $1 per/1mb from some of the more aggressive providers (obviously not AT&amp;T). By leveraging existing infrastructure and  tunneling encapsulations we begin to roadmap what it might mean to deliver networking as a service (NaaS).</li>
</ol>
</ol>
Let's choose path #2 since the cost prohibitive nature of leased lines is less likely and hey I don't need a leased line to Google to check my email.
<h2>Public Cloud Brokerage</h2>

We have gone from Amazon Web Services and a couple other fledging to a whole hell of a lot more cloud providers in the past year. Part of the allure to the public cloud should be the commoditized nature of the services. Instead of the IT guy worrying about types of storage, compute and network he needs to purchase, negotiating the best rate with the manufacturer and putting together an even remotely accurate TCO, he instead throws a number at the business unit and they cut the check. So we all know that is mostly fairy tale today but at some point it will be more reasonable a scenario. The cost of IaaS in the public cloud is going to most of the time be significantly more than local. If you can manage to pull of an elastic environment to offload peak compute to the cloud it becomes very attractive in todays standards. The classic example is doing payroll at the end of the month, why buy 200% hardware that sits at 50% usage except for one day of the month. Buy half the hardware and burst the peak to a (partner, public, private) cloud rather than buy capacity that is not maximized.

The importance of your public cloud provider in appearing commodity to you the consumer is that forces competition and allows you to maximize savings by leveraging competition. You are now the broker on any resource you need to consume and how to get it there whether storage, compute or network. 1/4 of hardware is virtualized today in a projected 75 billion dollar public cloud industry we have some growing ahead, with plenty of pain no doubt. Decoupling and abstracting the logical OS from physical hardware in both compute and network will accelerate the indifference to where the workload resides.
<h2>Cloud Resource Orchestration</h2>
I am bullish on OpenStack as an orchestration mechanism for public cloud, but at the end of the day it doesn't matter as long as what is getting presented is a ubiquitous set of APIs that your compute and business logic can adhere to. Like anything else we talk about in computing we can decompose it to layers all the way down to a chip and find parallels. A functional API like <a href="{{< relurl "/2012/07/sdn-apis-this-all-feels-pretty-familair/" >}}" target="_blank">POSIX</a>, has for years, allowed for proper abstraction into operating systems for application developers to focus on higher level abstraction and efficiency.

That all said lets get our compute node up and running. For that piece I am using an instance on the <a href="https://www.hpcloud.com" target="_blank">HP Public Cloud</a> because they have a free offering as part of their launch, though you do have to put a credit card on file, hopefully I wont be raging at a $1,000 at the end of the month. It says you have $20 credit but doesn't tell you what that means or give you usage information so needless to say after I ran some benchmarks I deleted the instance. More on that later.
<h2>HP Public Cloud</h2>
I love the interface HP has with this. It is a polished up OpenStack interface. It would be great if they released the components of that like Rackspace has done with their private cloud OpenStack <a href="http://www.rackspace.com/cloud/private/openstack_software/" target="_blank">package</a> to the public. If you have used the OpenStack <a href="http://www.openstack.org/software/essex/" target="_blank">Horizon/Dashboard</a> Web UI you will be right at home. If not it is still pretty intuitive and the documentation is more than adequate. Pro/Con later in the post.
<h2>Building a VM IaaS Instance<</h2>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/1-Geo-Location1.jpg" >}}"><img class="aligncenter  wp-image-2305" title="1-Geo-Location" src="{{< relurl "/wp-content/uploads/2012/08/1-Geo-Location1.jpg" >}}" alt="" width="537" height="475" /></a></p>
<em>Figure 1. </em>HP Availability Zones.
<p style="text-align: center;"> <a href="{{< relurl "/wp-content/uploads/2012/08/Flavor.jpg" >}}"><img class="aligncenter  wp-image-2346" title="Flavor" src="{{< relurl "/wp-content/uploads/2012/08/Flavor.jpg" >}}" alt="" width="515" height="349" /></a> </p>
Figure 2. Listed flavors of OS builds. <a href="{{< relurl "/2012/08/building-a-windows-image-for-openstack/" >}}" target="_blank">Windoze 2008 R2 image</a> is road mapped according to the forum.<span style="text-align: center;"> </span>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/2key.jpg" >}}"><img class="aligncenter  wp-image-2338" title="ssl openstack keys" src="{{< relurl "/wp-content/uploads/2012/08/2key.jpg" >}}" alt="" width="552" height="376" /></a></p>
<em>Figure 3. </em>One of the more confusing parts for beginners is creating a private key. Simply generate the private key under the OpenStack "generate private keys", then copy that RSA key into a file i.e. ssh-key.pem give it proper permission chmod 0400 ssh-key.pem. Then 'ssh -i ssh-key.pem ubuntu@&lt;publicHP-IP&gt;. More directions there from HP is likely needed. (As I sit here and do free analysis &lt;--dummy).
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/Sec-Group.jpg" >}}"><img class="aligncenter  wp-image-2339" title="Sec-Group" src="{{< relurl "/wp-content/uploads/2012/08/Sec-Group.jpg" >}}" alt="" width="512" height="470" /></a></p>
<em>Figure 4. </em>Self-Provision your own security. This is big, something centrally audit-able (&lt;--Spelling?) unlikes most host based security.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/CapWap.jpg" >}}"><img class="aligncenter  wp-image-2340" title="CapWap" src="{{< relurl "/wp-content/uploads/2012/08/CapWap.jpg" >}}" alt="" width="614" height="281" /></a></p>
<em>Figure 5. </em>Add ports for tunneling technologies such as CapWap above.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/08/merge-instance1.jpg" >}}"><img class="aligncenter  wp-image-2344" title="merge-instance" src="{{< relurl "/wp-content/uploads/2012/08/merge-instance1.jpg" >}}" alt="" width="576" height="349" /></a></p>
<em>Figure 6. </em>Pick the instance count and create your instance and you are up and running. Thats a before and after btw.

<a href="{{< relurl "/wp-content/uploads/2012/08/API-Keys.jpg" >}}"><img class="aligncenter size-full wp-image-2343" title="API-Keys" src="{{< relurl "/wp-content/uploads/2012/08/API-Keys.jpg" >}}" alt="" width="576" height="587" /></a>

<em>Figure 7. </em>This is pretty important here. It is the guts of the ecosystem, the all mighty orchestration APIs that haters of change get frumpy over.
<h2>Pro and Cons of My Beta Experience</h2>

Starting with Cons becuase I am impressed with all public cloud providers that have seen the value and are taking the risk to be all in with a community developed ecosystem.

<strong>Cons:</strong>

<ul>
	<li>Billing and usage. I don't see anywhere that tells me what I have consumed and what I would be charged. I signed up and it said the first $20 was free but it also says compute nodes after May 10th are half price. My wife will kick my ass if I have a $500 cloud bill. (On roadmap per message boards) The trial promotion ambiguity leaves the it off the pros list since I am not sure what it means yet, hopefully I'm not pestering <a href="https://twitter.com/FlorianOtel" target="_blank">@FlorianOtel</a> to help me out with a bill at the end of the month.</li>
	<li>Working with Public and Private SSL keys. Folks familiar with ECS or OpenStack like services will be right at home but to a new user it will need more explanation.</li>
	<li>No pausing or suspending of instances. This could come across like they are trying to trick the customer into leaving a node running and soaking CPU cycles and thus a large bill. The option today is to leave the instance up 24x7 or terminate the instance thus losing your data with it. (On roadmap per message boards)</li>
</ul>

<strong>Pros:</strong>

<ul>
	<li>Its OpenStack and with that implicitly provides common APIs and frameworks to operate and integrate with.</li>
	<li>OpenStack Public Cloud Providers allows the customer to move seemlessly between providers based on what metrics are important to them eg. performance, location, availability, economics etc.</li>
	<li>Very nice styling wrapper to the Horizon/Dashboard that I hope will be released to the community at some point.</li>
	<li>Good documentation from HP to augment the existing OpenStack documentation. Also a community board that I have not spent much time in but appears to have potential.</li>
	<li>This has similar roots as something like Linux. Unlike Linux a sexy UI to the user isn't important. It needs functionality and robustness. Does a user care what hypervisor he/she is running on or what object store they are using? The value of anything other than free hypervisors should be <a href="http://www.colinmcnamara.com/vmwares-acquisition-of-nicira-vmware-confirming-the-hypervisor-is-dead/" target="_blank">dead</a> within two years, long live the hypervisor. The next abstraction efficiency in consumption.</li>
	<li>Consolidation of Public Cloud offerings is a big win for the consumer, commoditized competitive markets drive down cost.</li>
</ul>

<div><a href="{{< relurl "/2012/08/public-cloud-network-as-a-service/" >}}">Part 2</a> will visit the networking as a service</div>
&nbsp;