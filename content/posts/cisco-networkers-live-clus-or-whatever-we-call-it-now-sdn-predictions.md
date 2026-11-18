+++
title = "Cisco Networkers Live CLUS or whatever we call it now SDN Predictions"
date = "2012-06-11T01:23:21+00:00"
lastmod = "2012-11-30T04:06:13+00:00"
author = "Brent Salisbury"
wp_id = 1005
categories = ["Speculative"]
tags = ["Cisco", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/cisco-networkers-live-clus-or-whatever-we-call-it-now-sdn-predictions/"
aliases = ["/2012/06/cisco-networkers-live-clus-or-whatever-we-call-it-now-sdn-predictions/"]
image = "/wp-content/uploads/2012/06/open-trap-300x2101.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a0afe54c7eadb421ade902525b56a684fde0833cc85f0026bb1b73edf1518be7"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

I was emailing with my buddy Roy at SDN Central <a title="http://www.sdncentral.com/" href="http://www.sdncentral.com/" target="_blank">http://www.sdncentral.com</a>/ about it would be fun to see a poll for people to guess what Cisco will do with their big SDN announcement. I jotted down four options that are all in the realm of possibility, or at least the same realm of if SDN makes sense and will adopt. Let's say solar-system or galaxy.

<strong>I expect one of these four or some combination to happen:</strong>
<ol>
	<li><strong>Drank the KoolAid</strong> – Announce OpenFlow support in their some of  switches and an OpenFlow Controller in the works that works with any vendor hardware.</li>
	<li><strong>As Open as a Trap</strong> - Announce OpenFlow hardware roadmap support with a controller that is Cisco only with no interoperation.</li>
	<li><strong>Playing Defense</strong> - Announce an OpenFlow roadmap for some of their switch product lines (Trident2 &amp; a couple of others), no controller talk or barely eluding to it.</li>
	<li><strong>Its all Hype</strong> – They announce very little, if anything and give lip service as to watching to hear what their customers want. Change is still bad.</li>
</ol>
Without any NDA information, just based on how Cisco's competitors all seem to be scrambling or downplaying the need for SDN I am fairly bullish on a significant commitment. SDN is not a magic bean but I see really good cases where it makes sense just like wireless controllers make sense in an enterprise. Management is my gripe and need in networking systems today and its the only sound solution I have heard yet.

<strong>Basic OpenFlow Agent Support</strong>

Back to the guess, of the four scenarios, I fully expect Cisco to announce some product roadmap support for the OpenFlow agent (probably v1.2 since most vendors are skipping v1.1, sorry v1.1 we never really got to know you), Broadcom Trident2 chipset, some enterprise core/distribution chassis such as the 6500 (first OpenFlow switch at Stanford til they pulled the plug) and their ASR 9k which use the EzChip chipset with internal TCAM. I really hope to see the campus edge play. That will be vital. Nothing hardware is going in our data centers until it is proofed on our edges. To do that I need just a smidgeon of features like POE. Vendors have missed the boat on this. HP is one of the only vendors who have a POE supported edge switch. Everyone else is sticking to the Trident driven boxes. If a vendor doesn't have the OpenFlow checkbox in an edge switch enterprise RFP they may find themselves losing out solely based on hype or customer making sure they have investment protection. Never even heard back from the Pronto salesy guy when I asked for POE. Sales isn't their strong point anyways lol. Dell/F10 is MIA on the POE play also. IBM is one I will be looking at over the next couple of weeks along with Brocade. Anyways, the answer is yes on OF agent support from Cisco for a fairly wide range range of products. Will they announce most of them? I think my guess is yes.

<strong>One Controller to rule.. Sorry nerd alert there</strong>

The controllers.. Hmm well we have all heard of the rumured Cisco spin-in around SDN. Brad at <a title="NerdTwilight" href="http://nerdtwilight.wordpress.com/2012/03/16/what-ciscos-sdn-spin-in-move-tells-us/" target="_blank">NerdTwilight</a> had an article discussing that. They picked up Dave Ward from Juniper over the winter and have presumably stuffed a black box team full of cash to go develop a strategy. I believe Cisco will come out with a controller and at least announce a roadmap for product to market this week. If they do not, it will in my opinion go down as a mistake. It is easier to get your way when you are leading the charge and they have the resources to do it. They were way too slow to react to the comedy of some of the M&amp;A failures and product lines over the past couple of years, but they have a revamped leadership and cleaned house from the old timers who did not deal with or embrace change well.

Those companies who have been playing the wait and see strategy will obviously be dismayed at this (*cough Dell, HP, Juniper). Ivan P. had a <a href="http://blog.ioshints.info/2012/03/grumpy-monday-hp-and-openflow.html" target="_blank">post</a> a while back thrashing HP for not making a move for the crown jewels which is the controller for the time being. That is where the obnoxiously high software licenses will be. For everyone out there trying to price controllers. Do not price per port if you ever want to do business outside of a data center or carrier. My 75k enterprise ports are a hell of a lot different than 200 carrier ports so price it as such. One of our regional ports could be serving 100k users so dont charge the same for that and the secretary or one of my co-workers cruising Facebook all day. So yes on Controller in at least a mention and timeline.

<strong>Vendor Agnostic Hardware Substrate</strong>

The big gamble in this prediction is the vendor lock, whether a Cisco controller will be agnostic to the network device in the substrate. I.e. can I attach a Dell, IBM, Brocade, HP switch to a Cisco controller and have the full functionality  of that vendors hardware based on the OF spec of the agent. Early SIP protocol and Call Manager come to mind. I think if they stick to the pre-standard value add that we see today (FabricPath/Trill) that will show the added value. Chambers recently commented to Wall Street, that despite the hardware being the same manufacturer at times as the competitor, it is the added value that Cisco brings which prevents commodity and creates overall value. There is some risk to a total SDN embrace in my opinion, if you still cannot admit that most hardware will head in that directions like the x86 market, are you ready to embrace the potential of commoditizing in some fashion your software and beloved IOS? I have no idea on this other than its hard to bet against open. I think the revenue is there from that embrace, and at much better margins in software than hardware.

<strong>My Probably Wrong Guess</strong>
<blockquote>Final answer is #<strong>2</strong>, a roadmap with quite a few products with OpenFlow agent support, some mentioing of a controller but not enough details to determine if it is a open or closed to other vendor controller. That said, I do think when the details get teased out, a controller from Cisco will be open to other vendors minus pre-standard or special magic tricks that you could get with Cisco gear, but I dont see them going that deep this week. Cisco has described themselves as a software company numerous times over the past decade, the proof will be in the pudding this week.</blockquote>
<a href="{{< relurl "/wp-content/uploads/2012/06/open-trap.jpg" >}}"><img class="alignright size-medium wp-image-1030" title="SDN trap cisco clus" src="{{< relurl "/wp-content/uploads/2012/06/open-trap-300x210.jpg" >}}" alt="" width="300" height="210" /></a>

We will be sucked (just like these two dudes and the booth chick) in with promises of great things but it will be the details that make or break the value prop.

I think the much much bigger question is north of the controller that I jotted down some thoughts on in <a href="{{< relurl "/2012/06/the-northbound-api-2/" >}}" target="_blank">"The Northbound API- A Big Little Problem"</a>

**PS  However, if they announce an App Store for networks I may quit. Juniper SDK comes to mind, great idea but no ecosystem. before anyone nerdrages, this is a guess so dont worry about getting upset and type a hate letter. It's fun stuff, lets relax and enjoy the ride and intelectual challenges. Peace and Love.

I expect the Ferro @ <a href="http://etherealmind.com/who-am-i/what-does-ethereal-mind-mean/" target="_blank">http://etherealmind.com</a> and Banks and <a href="http://packetpushers.net" target="_blank">http://packetpushers.net</a> will give those of us who didn't make the plane ride out with some top notch coverage.

Pop in your predictions, I really want to hear if I am being totally naive or not. Dont worry about anyone judging your ideas, no one cares about IT know it all dicks opinions anyways.