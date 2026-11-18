+++
title = "SDN Dominates NFD#5"
date = "2013-03-30T06:09:43+00:00"
lastmod = "2013-07-07T22:46:48+00:00"
author = "Brent Salisbury"
wp_id = 6136
categories = ["Speculative"]
tags = ["Brocade", "Cisco", "Juniper", "Network Field Day"]
description = ""
url = "/sdn-dominates-nfd5/"
image = "/wp-content/uploads/2013/03/Network-Field-Day-5.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "84653fca3cee879feb5ed326125aec95250b1ee4313f7b6d93b4f0febdc82c77"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>SDN Dominates NFD#5</h2>
SDN was the soup dajoure at <a href="http://techfieldday.com/event/nfd5/" target="_blank">Networking Field Day #5</a> and rightfully so. My friends are not only talented bloggers, but also some of the best architects, engineers and operators in the networking field. The networking industry has gone without significant innovation since at least MPLS and arguably Ethernet. Our network architectures are snapshots of the cold war. Every device must maintain a full consistent state in case Reagan or Gorbachev hit the red button.

Every vendor out there is hedging their bets on a combination of the following. There are a few more arguable points but to keep things manageable I am sticking to the following:

<ol class="legacy-numbers">
<ol>
	<li><strong>Management Protocols</strong> - APIs are SDN and existing protocols are good enough.</li>
	<li><strong>OpenFlow</strong> - Differentiate in software. Control and policy are complimentary creating an open control loop. This could be another abstraction, but I tend to land in the good enough camp on OF.</li>
	<li><strong>Proprietary SDN</strong> - I consider proprietary SDN as decoupled control from the data plane using proprietary southbound messaging protocols. Closed systems need to differentiate in hardware and software to remain closed.</li>
</ol>
</ol>
<h2>Cisco ONE Controller and A Fun Debate</h2>
<p><a href="http://vimeo.com/61490502">Watch video on Vimeo</a></p>

<hr />

<p><a href="http://vimeo.com/61490419">Watch video on Vimeo</a></p>
<h2>Juniper Zeroing in on their SDN Strategy</h2>
<p><a href="http://vimeo.com/61490395">Watch video on Vimeo</a></p>

<hr />

<p><a href="http://vimeo.com/61490396">Watch video on Vimeo</a></p>
<h2>Plexxi Optical or SDN</h2>
<p><a href="http://vimeo.com/61490399">Watch video on Vimeo</a></p>

<hr />

<p><a href="http://vimeo.com/61490515">Watch video on Vimeo</a></p>
<h2>Brocade Continues Delivering SDN</h2>
<p><a href="http://vimeo.com/61490406">Watch video on Vimeo</a></p>

<hr />

<p><a href="http://vimeo.com/61490501">Watch video on Vimeo</a></p>

<hr />

<h2>My Take Aways</h2>

<ul>
	<li><strong>Cisco</strong></li>
</ul>


There are some folks at Cisco who believe the future is software differentiation and not vertically integrated products. There are also those who think they can replicate what Apple did. I think IBM is a bit closer, which is not so shabby, considering their value is at an all time high. It is no surprise to silicon hugging. Cisco is the market share incumbent in switching, routing and a handful of other categories. Business has been good.

Cisco can be fairly Dr. Jekyll and Mr. Hyde on SDN. On one hand there are introductory <a href="http://tools.cisco.com/gems/cust/customerSite.do?METHOD=E&LANGUAGE_ID=E&SEMINAR_CODE=S17515&PRIORITY_CODE=000105096" target="_blank">OpenFlow 101</a> webinars and the next telling us, no one is asking for SDN, followed up with the old "hand you a loaded gun". I can think of a handful of mousetrap solutions that scare me much more then running OpenFlow in a production environments.

That said, I think Cisco is heading in the right direction, they are developing a really nice controller. onePK is there to be leveraged by the controller. Anyone excited about onePK for anything other than the <a href="http://www.networkcomputing.com/virtualization/ciscos-one-controller-debuts-targets-sdn/240147798" target="_blank">Cisco ONE controller</a> are probably intending on building their own control apps using Cisco's proprietary APIs. I don't know any of those people. Fortune 50s drive product at Cisco.

Hats off to Cisco for having an honest debate in public with us. I thoroughly enjoyed it. It's the sort of thing most won't get near. It comes across as passion for networking, genuine interest in hearing from the customer and stimulating debate. Also, meeting Jan Medved was fantastic, brilliant and nice guy along with a pro, Phil Cassini as the ONE controller product manager. And of course we had <a href="https://twitter.com/omarsultan" target="_blank">Omar Sultan</a> there who is top notch.

Now, lets see if we ever get OpenFlow HW support for the <a href="http://newsroom.cisco.com/press-release-content?articleId=892363" target="_blank">Catalyst 3750-X</a>. If someone at a Fortune 20 could request that, it would be appreciated :)

<hr />


<ul>
	<li><strong>Juniper</strong></li>
</ul>

Juniper unveiled their newest programmable chip they are calling "ONE" that was an excellent deep dive. They also had a presentation on Puppet that I enjoyed. They went into quite a bit of detail on Contrail, the recent SDN acquisition that is arguably most interesting for a niche early carrier cloud Vmware alternative market. I was surprised not to hear anything other than Puppet and MPLS on SDN because I had a great call with Juniper the week before regarding OpenFlow/SDN.

While the Contrail solution is interesting, I will be curious to see if it goes anywhere other than service providers. As someone who beleives in <a href="http://packetpushers.net/uses-of-mpls-in-the-enterprise-and-data-center/" target="_blank">MPLS in the enterprise</a> for path isolation and operational ease, the fact is most vendors dont support it because it tends to compete with SP BUs or it just isn't an "enterprise technology". Juniper has not been very bullish on the enterprise lately either. Much like Cisco, there is much debate involved with SDN and it will take a little while to get consensus internally. Keeping the ears open is the key, and my interactions on that front have been good. Of course thanks to the social media master <a href="https://twitter.com/abothman" target="_blank">Bothman</a> and Juniper for accommodating us and our friend <a href="https://twitter.com/abnerg" target="_blank">Abner Germanow</a> for always being friendly even when we ask annoying questions :)

<hr />


<ul>
	<li><strong>Plexxi</strong></li>
</ul>


I wrote a bit on <a href="{{< relurl "/plexxi-capacity-planning-done-right/" >}}" target="_blank">Plexxi</a> not too long ago. I like the unique WDM optical concept. They are looking to differentiate in hardware. While I am generally not too interested in that, having an optical component gives them a better story. I like WDM integration for one main reason, operators can provision bandwidth without needing to hope a fiber circuit gets put in place before remaining bandwidth is exhausted. I will be interested to see what their next bandwidth capacity increase is when they go from 2-degree to 4-degree and how this compares with 100Gb pricing in coming months with the Broadcom TridentII chip. That said, still no product announcements from anyone on that chip.
One thing I am very interested in with Plexxi is their analytics. I believe someday we will trust algorithms enough to provision based on predictive analysis. Also good to see NFD friends <a href="https://twitter.com/cloudtoad" target="_blank">Winkworth</a> and <a href="https://twitter.com/mbushong" target="_blank">Bushong</a>. Quick note, the Plexxi fellas have increased the blogging on their site. Defininently worth adding to the reader at <a href="http://www.plexxi.com/blog/" target="_blank" rel="noopener noreferrer">Plexxi Blog</a>

<hr />


<ul>
	<li><strong>Brocade</strong></li>
</ul>


I thoroughly enjoyed Brocade's presentations. It was great to see them talk about the Internet2 SDN deployment. Brocade is staying true to their commitment to seeing SDN and OpenFlow through. Meyer's hinted at integrating Vyatta into an open operating system. I believe Ethan was going to do a followup with David since we ran out of time with him. We also got an update from <a href="http://packetpushers.net/pq-show-20-open-network-foundation-fawg-update/">Curt Beckmann</a> that was great to hear as always. Last but not least was the puppet master and frighteningly smart <a href="https://twitter.com/RealLisaC" target="_blank">Lisa Caywood.</a>

Brocade sells really cheap 100Gb. While light on the FIB size, I like their commitment to supporting customers looking to do early OpenFlow production deployments. Of all of the aforementioned vendors, Brocade is the only one with GA OpenFlow shipping product today. 

<hr />

As we embark on these exciting times, it's people like <a href="http://techfieldday.com/event/nfd5/" target="_blank">NFD delegates</a> I salute for taking the time to filter substance from noise for the community.

<hr>
<aside class="legacy-callout"><strong>Packet Pushers White Paper on Nuage Networks SDN Solution VSP</strong>Check out this sponsored Packet Pushers white paper that Greg and Ethan recently did. MP-BGP and OpenFlow southbound, controller to forwarding element protocols. <a href="http://packetpushers.net/nuage-networks-sdn-arrives-launch-vsp-white-paper-sponsored/">Nuage Networks VSP at PacketPushers.net</a>
</aside>
<hr>
Thanks for stopping by.