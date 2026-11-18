+++
title = "It's OK to Like OpenFlow"
date = "2012-06-19T04:59:25+00:00"
lastmod = "2012-09-09T02:33:48+00:00"
author = "Brent Salisbury"
wp_id = 1405
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/its-ok-to-like-openflow/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "6783008c2819c0a2126e344834585cda792910bbd9eb04278d3428a5db5b1ce0"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

&nbsp;

A trend is happening, seems like a recurring theme from vendors or pundits the past year has been to point out SDN is much larger than just OpenFlow. My question is, who thinks that SDN is exclusively OpenFlow? I am looking for the person who thinks this so I can understand the fuss. What is SDN? We already have SDN management for automation from HP with HP Network Node Manager (NNM), from via Dell Advanced Infrastructure Manager (AIM) and Cisco's slew of Cloud Automation packs and so on. We now have proprietary extensibility from Juniper, Cisco, Arista etc. So whats all the fuss? Clearly we already have everything we need.

Sorry thats all tongue in cheek and I am clearly oversimplifying things. The small but incredibly important piece of SDN is the Southbound API. That is the communications from a decoupled control plane to the networking firmware/hardware. In my opinion it is fundamentally a debate around how do we commoditize networking hardware, similar to what has been done in the x86 market. If it is instantiating data paths into exposed forwarding tables of networking devices then whats missing? That is why the premise of OpenFlow is attractive. A standard framework that can instantiate flows and be vendor agnostic to the underlying substrate. On paper it sounds great, latency and other factors will be problematic but I think an island approach today has some legs. So my question is are we ever going to find the perfect decoupling of the control plan and NOS? Probably not but a "good enough" approach for now in exploration is probably just as good as the "good enough" approach in today's networks and especially management of those networks (OpEx reduction is my favorite potential of SDN).

<strong>Even the Creators Agree</strong>
<blockquote>
<p class="textbox">I borrowed this from Brad Casemore's <a href="https://nerdtwilight.wordpress.com">blog</a> “OpenFlow is one possible solution (as a configuration mechanism); it’s clearly not the right solution. I mean, it’s a very good solution for now, but there’s nothing that says this is fundamentally the right answer. Think of OpenFlow as x86 instruction set. Is the x86 instruction set correct? Is it the right answer? No, It’s good enough for what we use it for. So why bother changing it? That’s what OpenFlow is. It’s the instruction set we happen to use, but let’s not get hung up on it.” -Scott Shenker</p>
</blockquote>
We need something to get started for our <a href="{{< relurl "/2012/06/the-northbound-api-2/" >}}" target="_blank">Northbound</a> travels. If not OpenFlow than what is my question? Proprietary APIs are not going to cut the need for ubiquity between platforms. That would bring us back to where we are screen scraping CLI or worse, navigating complicated development kits. I am pretty optimistic we will get the flexibility sprinkled with a little change to bring networks up to a proper layered abstraction over the next decade.

<a href="{{< relurl "/wp-content/uploads/2012/06/hates-nerds1.jpg" >}}"><img class="alignright size-full wp-image-1439" title="hates-nerds" src="{{< relurl "/wp-content/uploads/2012/06/hates-nerds1.jpg" >}}" alt="" width="353" height="200" /></a>
<p class="textbox"><strong>The SDN Wiki defines it as the Following:</strong>
The firmware of network switches and routers (control plane) has traditionally remained proprietary, locked and under the control of the companies that manufactured the equipment. Software defined networking (SDN) seeks to change this disposition, and to make the control plane remotely accessible and remotely modifiable via third-party software clients, using open protocols such as OpenFlow.
Thus SDN allows for
1. Quick experimenting and optimization of switching/routing policies.
2. External access to the innards of switches and routers that formerly were closed and proprietary.</p>
I thought that was actually pretty well stated in the Wiki. Hats off to whoever wrote it. Anytime someone works "innards" into a technical definition well thats winning. I am just looking forward to this layer firming up so we can see the glorious problems SDN will solve. Link me the control plane alternatives that are something we can use to test with for research networks on multi-vendor hardware (not FPGAs) if there is one I missed. Net is don't let the fear of being perceived as buying into hype, discourage us from taking a new approach to our networks and until something better comes along I think it is the wheels on the car of SDN.

Its Jerry vs. Seinfeld,  Xbox vs. Playstation, Homer vs. Ned Flanders. Nerdrage for years to come, should be fun!

<strong>Footnote:</strong> the picture I Photoshopped had "nerds" underneath it. Those ding dongs at some crazy midwest church actually picketed ComicCon lol. <a href="http://techland.time.com/2010/07/16/god-hates-nerds-your-friendly-salvation-reminder/" target="_blank">Link</a>
Orignal Pic Lolz.
<a href="{{< relurl "/wp-content/uploads/2012/06/586_god_hates_nerds_12-25-2002-copy.jpg" >}}"><img class="alignleft size-thumbnail wp-image-1410" title="586_god_hates_nerds_12-25-2002-copy" src="{{< relurl "/wp-content/uploads/2012/06/586_god_hates_nerds_12-25-2002-copy-150x150.jpg" >}}" alt="" width="150" height="150" /></a>