+++
title = "Enterprise 802.11 Wireless Growth (Part 3)"
date = "2012-09-07T05:51:33+00:00"
lastmod = "2013-01-26T01:46:30+00:00"
author = "Brent Salisbury"
wp_id = 2499
categories = ["Speculative"]
tags = ["Cisco", "Software Defined Networking", "Wireless"]
description = ""
url = "/enterprise-802-11-wireless-growth-part-3/"
image = "/wp-content/uploads/2012/08/Enterprise.Wireless.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "0e04f156f8f635ab5326b730bd3b086a305f4b83a2488bf3a1d315eaa793d20f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Enterprise 802.11 Wireless Growth (Part 3)</h2>
In <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">part 1</a> of the three parter we looked at the ability to manage 802.11 wireless networks and the benefits of analytics that is provided out of the box. In <a href="{{< relurl "/2012/09/enterprise-wireless-and-wired-traffic-part2" >}}" target="_blank">part 2</a> we compared traffic rates (unscientifically) between an average wireless controller distribution and wired distribution. In the conclusion we will look at the growth of three points over two years. We have those numbers because out of the box central controllers retain this information. While we capture similar information from wired networks, it is a totally separate process, cost and operational task requiring significant engineering people hours to operate the management plane independently in the enterprise. This is very close to what many are explaining software defined networking as today. Missing key ingredients are open standards and integration into the rest of the computing ecosystem but it is certainly a much more coherent architecture than thousands of distributed devices individually maintaining state within a single administrative boundary.

<h2>Exponential Enterprise 802.11 Wireless Growth</h2>
The numbers are doubling annually with no signs of letting up. The <a href="http://www.cisco.com/en/US/solutions/collateral/ns341/ns525/ns537/ns705/ns827/white_paper_c11-520862.html" target="_blank">Cisco Networking Index</a> is always fun to read, if you have not before I recommend admiring the data. I whole heartedly believe the reason we can deliver really good wireless (enterprise, certainly not giving kudos to my cell service) networks is because of the of the centralized nature of the current predominate frameworks. 
<h2>Centralized Wireless Today is SDN</h2>
The need to manage edge RF, was enough of a technical reason to drive centralization. Interesting product stories on who was first and who followed when wireless controller architectures emerged a few years back if anyone has never poked around on that. These numbers are from September of 2012, while <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">part 1</a> were from August of 2012. The delta is students returning for Fall semester and it is a 14-day aggregate. These are 802.11 vendor OUI are burned into wireless NICs and captured centrally from the controller. I wrote a hacked up Perl script years ago to crawl neighbor discoveries for that years ago, then Cisco Works fixed that 0_O, thats right Cisco works. 

The difference in today's centralized wireless solutions to the current SDN debate is only different in adding  the ability to distribute forwarding to the edge. In most centralized wireless controllers, the data plane is an overlay tunnel back to a headend control plane for policy and forwarding. Sound familiar? It should, that is  the same logic as most of the emerging SDN data center overlay solutions. Companies like Aruba are beginning to sell products that address this for remote sites and more theoretical distributed scale. That is flow based forwarding. Knowing nothing about the technology, if you were to match up Aruba distributed wireless, Juniper's Q-Fabric, Cisco's SW firewall and OpenFlow, there would be very similar logic in the lineup. The main difference would be proprietary vs. open wire protocols.


<h2>Two Year 802.11 Wireless Growth</h2>
Here are the new sets of data from September of 2012. Pretty fun data so have fun!
<a href="{{< relurl "/wp-content/uploads/2012/09/802.11-Growth-Linear.jpg" >}}"><img class="aligncenter size-full wp-image-2500" title="802.11-Growth-Linear" alt="wireless peak and averages" src="{{< relurl "/wp-content/uploads/2012/09/802.11-Growth-Linear.jpg" >}}" width="562" height="339" /></a>

<em>Figure 1. </em>Overall client growth at a typical state University. X=count Y=time
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Client-Summary-by-Vendor.jpg" >}}"><img class="aligncenter  wp-image-2503" title="Client-Summary-by-Vendor" alt="802.11 clients by vendor" src="{{< relurl "/wp-content/uploads/2012/09/Client-Summary-by-Vendor.jpg" >}}" width="591" height="422" /></a></p>
<em>Figure 2. </em>Apple up ~%3 from August.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Session-Time-by-Vendor.jpg" >}}"><img class="aligncenter  wp-image-2504" title="Session-Time-by-Vendor" alt="usage hours by vendor 802.11 apple dominating" src="{{< relurl "/wp-content/uploads/2012/09/Session-Time-by-Vendor.jpg" >}}" width="539" height="423" /></a></p>
<em>Figure 3.</em> Session time by vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Sessions-by-vendors.jpg" >}}"><img class="aligncenter  wp-image-2505" title="Sessions-by-vendors" alt="802.11 Sessions by vendors" src="{{< relurl "/wp-content/uploads/2012/09/Sessions-by-vendors.jpg" >}}" width="553" height="416" /></a></p>
<em>Figure 4</em>. Sessions by Vendor
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Traffic-bt-Vendor1.jpg" >}}"><img class="aligncenter  wp-image-2506" title="Traffic-bt-Vendor" alt="802.11 traffic by vendor" src="{{< relurl "/wp-content/uploads/2012/09/Traffic-bt-Vendor1.jpg" >}}" width="553" height="411" /></a></p>
<em>Figure 5.</em> Traffic by Vendor.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Client-by-Vendor21.jpg" >}}"><img class="aligncenter  wp-image-2508" title="Client-by-Vendor2" alt="802.11 client by vendor" src="{{< relurl "/wp-content/uploads/2012/09/Client-by-Vendor21.jpg" >}}" width="549" height="423" /></a></p>
<em>Figure 6</em>. Clients by Vendor
<h2>Are the Wired Enterprise Days Numbered to be replaced by Wireless?</h2>
Does anyone think that we aren't going to need wired enterprise campuses anymore? I look at traffic rates and its nothing from the client. I think poor cellular networks have forced content providers to be very conscience of page loads anymore, so, thanks, I guess, wtf? I used to stress over wireless replacing wired. Looking at these numbers, I realize its probably inevitable in many places. I cant think of the last time I actually hardwired my laptop, it was probably a serial cable into a USB converter to attach to a console. I used to think video or some massive holographic Stars Wars stuff would drive a physical medium. Certainly still a toss of the coin, the everyday bandwidth intensive app will determine that for us. That said, I would always prefer my IV pump and heart monitor to be on wired, so someone popping popcorn in the microwave doesn't cut my drip would be nice, but even medical devices are all heading wireless to drive down cost and be portable in patient care environments. 

Wireless still has to backhaul so we will still have gear but we are already seeing some new construction reducing capital in wiring infrastructure on new builds. It will take an app to drive bandwidth needs to justify traditional cable plant to the cubicle over the next 10 years if I were to speculate. Apps are being optimized to run on terrible cellular networks. The lackluster user experience on cellular networks has significantly lowered the bar for enterprise and residential voice and data delivery, people are used to piss poor networks now.

<h2 class="legacy-heading">Change is Normally Good, Well Unless it's the Bad Kind or Total Destruction</h2>

If it wasn't for change we wouldn't have the Internet and my life would be foosball and D&amp;D, now that would suck. We have a major problem of shortage of optimism in IT. Not sure why that is, but is sucks the life out of me being around the perennial pessimist. I think it's the hero mentality that many in IT need to be the smartest in the room, so if its not their idea it's not a good one. Newsflash, nothing is original and if it is you should get back to your private island. Bet against technology go ahead, but more often than not you will lose. VM farms didn't replace systems administrators when x86 started getting virtualized, nor will SDN curtail the huge demand for network engineers and architects, it is after all the umbilical chord of the future. I fully expect someone to step out with a controller product for the wired network just as someone did a few years back to solve an edge problem sooner rather than later. Sooner is still not in weeks or months (hedging bets :) After all what technology ever really simplified anything, abstracted yes, simplified never.

<h2>Summary</h2>

We (the royal we) need tools, vendor agnostic tools, and not the tools the scripts we have been cobbling together with a few minutes of free time at night for two decades, but software. Do we just settle for management is the question? My chips are on no, because it doesn't solve policy application at the edge. Flipping Vlans via SNMP for a kludged together NAC solution, a duct taped BYOD strategy or even more comical, a QOS policy that requires no care and feeding when adding more bandwidth would be a fraction of the OpEx.

Thanks for stopping by, oh one other thing, I almost forgot. A ginger riding a unicorn. I wanna work for that kid someday.


<aside class="legacy-callout">
<ul>
	<li>Part 1 - <a href="{{< relurl "/2012/08/why-enterprise-wireless-networks-got-it-right/" >}}" target="_blank">Why Enterprise Wireless Got it Right</a></li>
	<li>Part 2 - <a href="{{< relurl "/2012/09/enterprise-wireless-and-wired-traffic-part2/" >}}" target="_blank">A Byte is a Byte</a></li>
	<li>Part 3 - <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank">Enterprise 802.11 Wireless Growth</a></li>
</ul>
</aside>
Thanks for stopping by!
<hr>