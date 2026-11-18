+++
title = "Network Management System NMS - Statseeker"
date = "2012-10-14T18:51:03+00:00"
lastmod = "2012-11-25T10:25:41+00:00"
author = "Brent Salisbury"
wp_id = 3012
categories = ["Tools"]
tags = ["Network Management", "tech field day"]
description = ""
url = "/network-management-system-nms-statseeker/"
image = "/wp-content/uploads/2012/10/Power-lines_729-620x349.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "40a28bacf9f940230bd0a654c001f8906ece9c5c8abdfeb48bc5aa9cf7c1f63f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

Network Management NMS - Statseeker<em> Not a Swiss Army Knife, but a Sharp Blade:
</em>

At <a href="http://techfieldday.com/event/nfd4/" target="_blank">Network Field Day #4</a> we had a a company named Statseeker who is in the Network Management business. Stewart Reed from <a href="http://www.statseeker.com" target="_blank">Statseeker</a>, an Australian presented and demoed the product.  We were almost outnumbered something friends, <a href="http://thenetworksherpa.com" target="_blank">John Harrington</a> an Irishman, <a href="http://blog.ciscoinferno.net" target="_blank">Anythony Burke</a> an Australian and me a native Kentuckian with a funny accent had some fun with (*cough 3xC*). Network Management (NMS) has been a fairly major pain point in the networking industry. The history of NMS is paved with failed products and product deployments.

Network Engineers are guilty until proven innocent. If you cant pull data as close as possible to an event and prove it was not the network then it was the network. Network architects must be able to do or set capacity planning policy, that is impossible to do efficiently without long term trends and realtime data. While Staseeker is not the proverbial swiss army knife approach to network management systems. It doesn't have a crappy set of tweezers and a lame magnifying glass but it is a pretty sharp knife that "appears" to do link capacity monitoring quite well.

Statseeker also has NetFlow and Sflow capabilities. NetFlow organizational policy is a mess in most shops. Security wants it for security things, network wants it for capacity planning, all human problems working with very large data sets and terse technologies. Very few solutions open or proprietary out there that focus solely on NetFlow and correlation unfortunately. Until I hear how that works under the hood, I am maintaining healthy skepticism that on very little hardware tens of thousands of physical ports flows now 500k-1mil+ can be ingested and stored. I also thought that going into the demo on SNMP polling data but what Statseekers bread and butter is only pulling specific SNMP data rather than send it all to store and process even if you do not need it.

On the backend is their DB that is optimized for these particular data sets to produce very fast results instead of the normal hourglass waiting time for database queries other products can have. Well defined set of functions in order to optimize their efficiency is the market separator here. To get straight to the video on the Tech Field Day site check <a href="http://techfieldday.com/appearance/statseeker-presents-at-networking-field-day-4/" target="_blank">here</a>.
<h4> Things to Look for in Network Management in Products</h4>
<!--?xml version="1.0" encoding="UTF-8" standalone="no"?-->
<div><strong><em>1. Ease of use. If someone can't operate it, I can't use it:</em></strong></div>
<blockquote>
<div>Most shops an amazing tendency to take NMS and give it to anyone willing to do it. The IQ needs to be high in order to effectively operate and extract network state and performance from our extremely complicated and distributed networks. Statseeker has a very fixed set of functions and focuses on those. Statseeker could likely be maintained by entry level tiered operations and more importantly operated properly.</div></blockquote>
<div><strong><em>2. Features.</em></strong></div>
<div>
<blockquote>
<div> If this product falls short anywhere it is in the feature category. They are very upfront this is what it is and this is what it isn't. Example, this is not a configuration management NMS. I Tweeted on ze Twitterz" <a href="https://twitter.com/networkstatic" data-user-id="38229327"><s>@</s><strong>networkstatic</strong></a><strong> </strong><a dir="ltr" href="https://twitter.com/search?q=%23NFD4&src=hash" data-query-source="hashtag_click"><s>#</s><strong>NFD4</strong></a> <a dir="ltr" href="https://twitter.com/statseeker"><s>@</s><strong>statseeker</strong></a> presentation. I am always a fan of a product that does a handful of well defined functions well then all of them poorly".</div></blockquote>
</div>
<div><strong><em>3. Clearly defined scale:</em></strong></div>
<blockquote>
<div>Statseeker polls every 1 minute. That was pretty outrageous and I like it. I have had to back other NMS over the years as low as 10-15 minute polling intervals. Those gaps in visibility are pretty huge when it comes down to events not being captured.</div></blockquote>
<div><strong><em>4</em>. Delivering on what it claims to do.</strong></div>
<blockquote>
<div>Having never used the product in production I can't comment here. If someone asked me a list of what NMS products to evaluate Statseeker would be on it.</div></blockquote>
<h4>ROI Required</h4>
<div>In today's economic climate, we know as many business acronyms as technical anymore. A feature in Statseeker that scrapes port counters and looks for unused ports in whatever time range you defined is handy. The average medium to large 50,000+ port network has a lot more unused ports than you might realize. Often capacity planning means someone goes into a closet sees 4 open (ports without cables patched in) and says its time to buy a new $2,000-$12,000 48-port switch. What many do not do is check port counters to see what ports are down and if that port is down do the counters show any traffic. I liked that feature so much I will do two things in the next couple of weeks, see if the NMS I currently use for capacity planning in my job has this feature and if it doesn't program something to pull those stats. My problem rolling it myself is I can either capture the port counters and correlate to the uptime of the switch or push into a backend to trend those numbers which gets out of the time allocation reality. That makes this product a business tool and the ability to hit your return on investment (ROI) and likelihood of receiving funding much more realistic.</div>
<div><a href="{{< relurl "/wp-content/uploads/2012/10/access-idf-port-audit.jpg" >}}"><img class="size-full wp-image-3013 aligncenter" title="access-idf-port-audit" src="{{< relurl "/wp-content/uploads/2012/10/access-idf-port-audit.jpg" >}}" alt="access-idf-port-audit" width="531" height="225" /></a></div>
<div><strong><em>Figure 1.</em></strong> Empty ports in the IDF means you bought more gear than the business needed and wasted money. Even if it was See the Amazon AWS capacity vs. consumption needle wide gap for perfect just in time IT about halfway down the page in this <a href="{{< relurl "/does-the-cost-of-cloud-iaas-intersect-the-local-vm/" >}}" target="_blank">post</a>.</div>
<div></div>
<div>As we see <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">exponential</a> growth in wireless and more migrations from the wired to <a href="{{< relurl "/the-death-of-the-wired-enterprise-network/" >}}" target="_blank">wireless</a> networks this will become increasingly important.</div>
<h4>In Summary</h4>
<div>There is some pretty cool optimization under the hood that separates Statseeker from it's peers. It is an engineers tool. From all NMS vendors I would like to see more focus on executive reporting. Drop some pretty graphs and charts into an executive summary of a solution or a root cause analysis and it's like spike the vein of middle managers all the way to C-level. We live in the land of complexity, abstracting that to pretty pictures works 90% of the time. The buck stops at the network engineer, who does he blame? The power company? We have to use and provide proper tools to even come close to managing today's networks. Those tools need to work quickly and properly, what I saw from Statseekers demo looked good on the surface.If currently shopping for an NMS, I would take a look at this <a href="http://techfieldday.com/appearance/statseeker-presents-at-networking-field-day-4/" target="_blank">video</a> from NFD to get a baseline and check out there site <a href="http://www.statseeker.com" target="_blank">statseeker.com</a>.</div>
<div></div>
<h4>Other Network Field Day #4 Delegates Thoughts</h4>
<div>
<ul>
	<li>My good friend and fellow native Kentuckian Paul Stewart <a href="https://twitter.com/packetu" target="_blank">@packetu</a> CCIE #26009 (works a few blocks away, bizarre, never knew him before NFD, thanks for that NFD team) had a nice writeup on his thoughts of the presentation on his site <a href="http://www.packetu.com/2012/10/11/statseeker-does-it-fit-your-organization/" target="_blank">packetu.com</a>.</li>
	<li>From the man himself, John Herbert CCIE#<em>6727 </em><a href="https://twitter.com/mrtugs" target="_blank">@mrtugs</a> Pretty sure he has forgotten more than I know at <a href="http://lamejournal.com/2012/10/14/statseeker-keeping-an-eye-on-the-little-things/" target="_blank">lamejournal.com</a> shares his thoughts from the network field day presentation.</li>
	<li>The gentleman that was about a decade younger than all of us and still teaching us not too mention a fantastic presenter/storyteller, Anthony Burke <a title="@pandom_" href="http://twitter.com/pandom_" target="_blank">@pandom_</a> . Brilliant each and every one.</li>
</ul>
</div>
<div></div>
<div></div>
<div>As a Tech Field Day Delegate Statseeker was a sponsor but anyone that has ever watched the videos or even funnier the Twitter feeds during an event will realize this is furthest from softball shills ever. If your product has problems you hear about it really quickly and even viciously at times depending on receptiveness of the vendor to critical feedback. Thanks to my fellow <a href="http://techfieldday.com/event/nfd4/" target="_blank">delegates</a> and lifelong friends and the original folks organizing network field day like  <a href="http://blog.fosketts.net" target="_blank">Steven Foskett</a>, <a href="http://packetpushers.net" target="_blank">Greg Ferro</a>, <a href="http://networkingnerd.net" target="_blank">Tom Hollingsworth</a> and <a href="http://techfieldday.com/delegate/claire-chaplais/" target="_blank">Claire Chaplais</a> for the overwhelming opportunity. Over the next couple of weeks there will be some more posts on the other sponsors. Some are requiring more research than others due to breadth of product lines. More information at <a href="http://techfieldday.com" target="_blank">http://techfieldday.com</a> Thanks for stopping by!</div>
<div></div>