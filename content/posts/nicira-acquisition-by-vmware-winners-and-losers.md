+++
title = "Nicira Acquisition by VMWare Winners and Losers"
date = "2012-07-24T03:10:29+00:00"
lastmod = "2012-09-09T00:04:14+00:00"
author = "Brent Salisbury"
wp_id = 1837
categories = ["Speculative"]
tags = ["Vmware", "nicira"]
description = ""
url = "/nicira-acquisition-by-vmware-winners-and-losers/"
image = "/wp-content/uploads/2012/07/Ghetto-Lisa.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "bbebfe2c9225360e06f71cf316331752d7f8cf226ef6136d505ea1fcfe5d21a8"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<a href="{{< relurl "/wp-content/uploads/2012/07/Ghetto-Lisa.jpg" >}}" rel="attachment wp-att-1862"><img class="alignright size-full wp-image-1862" title="Ghetto-Lisa" src="{{< relurl "/wp-content/uploads/2012/07/Ghetto-Lisa.jpg" >}}" alt="" width="190" height="190" /></a> VMware acquired Nacira today. They were one of the two (not including Embrane) venture cap groups that came out of the of Stanford group that developed among other things the OpenFlow and much larger the concepts around making Software Defined Networks (SDN) a potential reality. They open sourced and upstreamed Open vSwitch, two big contributions. I hope this frees up some millionaires now to focus all of their time on OVS and community :)

I think this acquisition will drive Cisco in a direction to embrace KVM and OpenStack in earnest. That I am looking forward to. The acquisition was an excellent move by VMWare since hypervisors alone is not a long term strategy as KVM and XEN continue to improve. The talk by the VMWare CTO regarding embracing OpenStack and CloudStack is one of the more insane things I have ever heard someone tell people and expect them to believe. Who knows maybe they are getting into a market that doesn't deal with data center and cloud orchestration, oh never mind.
<p class="prettyprint">VMware CTO Steve Herrod goes out of his way to talk about openness:
&nbsp;
They [Nicira] are major contributors to the networking capabilities of other hypervisors (via the Open vSwitch community) as well as to the “Quantum Project”, one of the key subsystems of OpenStack.
&nbsp;
I can imagine skepticism as to whether we will continue this substantial embrace of non-VMware hypervisors and clouds. Let me be clear in this blog… we are absolutely committed to maintaining Nicira’s openness and bringing additional value and choices to the OpenStack, CloudStack, and other cloud-related communities.</p>

All that said, if I was a do it yourself shop looking to make profit on open source margins today didn't change much. The OpenStack Quantum pieces is a little sketchy to me since Nicira is still very involved there but the guys on the OVS IRC channel are all about community so I think we are in good shape there. Folks are counting on that vSwitch around cloud startups and I imagine vSwitch forks from other competitors as a base build.

Some folks today thought this is bad for BigSwitch, personally I would be pretty happy to see the competition sell for 1.2 billion. Not to mention there is a lot of talent there. They have adjusted their strategies to be both hypervisor and top of rack hardware SDN integrators. I still think there is room for one dark horse from a VC to be a popular network OS, there is always two of everything.
<h4>Winners:</h4>
<ul>
	<li>Open vSwitch is open source and upstream in the Linux Kernel. That ship was put in the water.</li>
	<li>SDN - SDN is real if you can take $50 million in VC and turn 1.2 billion in 4 years.</li>
	<li>VMWare - Brilliant acquisition. This should force Microsoft Hyper-V (MS Hypervisor) to come up with a similar software approaches and Cisco to embrace open source Hypervisors.</li>
	<li>Cisco - IF they fill the void of being a vSwitch that is hypervisor agnostic with a support model. As alternative hypervisors continue to mature the value of that abstraction becomes increasingly commoditized. It's not an iPhone its a totally abstracted layer from the user and DC orchestrations should begin abstracting it from an administrative UI also. Open Source hypervisors and MS Hyper-V should be high on the list now.</li>
</ul>
<h4>Losers:</h4>
<ul>
	<li>Open vSwitch - The loss of some really smart, and not to mention nice guys like Ben Pfaff to VMWare (assumption) away from OVS. Maybe they will be so rich now they can just maintain OVS for fun from the yacht or private jet? :) It sounds like OVS is obviously still the core of the vSwitch product. The question will be can they keep VMWare from closing it? I would think to keep the data path in the kernel it will need to stay fairly pure so I am optimistic and should have this in the wait and see column but Im too lazy to make a new one and the loser column has to have something in it or that ruins the whole title.</li>
	<li>Consumer - One less competitor. Competition is good for the consumer. What happens to the person who was betting the farm on a Nicira/KVM solution? VMWare licensing just took a big one on that persons TCO.</li>
	<li>Open Source Cloud Orchestration - Short term only I think. A robust network stack is being counted on coming out of the Fulsom release along with a refined simpler experience.</li>
	<li>Cisco - IF they try to sell a VMWare/Nexus 1000v combination and differentiate against a full blown VMWare network product. Since Cisco has a fairly large stake in VMWare shares it sure does send a pretty clear signal that the marriage is coming to an end.</li>
</ul>
<strong>SDN Startup Capitals guesses and published.</strong>
BigSwitch - ~$13 million or so published but likely closer to $20-$25.
Insieme - $100 million Cisco spin-in
Nicira - $50 million

This was a quick rambling post as I have RL work to do this evening and I am officially burned out on talking about this. Apologies if reading it contributed to your Nicira/VMWare burnout. The train is still heading down the tracks and will smash those who want us to purchase and operate distributed firmware (OS if you insist) on proprietary hardware, software and APIs for the rest of our careers. The vSwitch is just a piece of the ecosystem that will evolve irregardless of any single vendor because shrinking budgets and ever increasing growth and reliance of networks will force it to happen. Three cheers to hyper scale cloud and content providers. Google NWO FTW.

&nbsp;

&nbsp;