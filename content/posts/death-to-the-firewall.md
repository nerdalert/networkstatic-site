+++
title = "Death to the Firewall"
date = "2011-06-06T20:00:11+00:00"
lastmod = "2013-07-30T05:10:45+00:00"
author = "Brent Salisbury"
wp_id = 24
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/death-to-the-firewall/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a6ecc579abe3d60eb11c5b5b230a33d310cae51b0fd50ad72c977df75ddd3ebb"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Death to the Firewall</h2>
The Firewall will die soon. Blackbox hardware just doesn't make sense anymore. CPU is king when it comes to processing payload and that is commodity. SDN will put a nail in the custom hardware closed system soon enough. Until then, some musings on a project to collapse some functions into a router. Ironically, I can only collapse application processing into a router because the Quantum Flow RE is merely a bunch of Intel cores.
<hr>
<ol class="legacy-numbers">

<ol>
	<li>10gbps throughput with MPLS/VPN support to act as a PE node with MVPN support.</li>
	<li>Traffic shaping and reduction of traffic.</li>
	<li>Blacklisting of offenders who violate policy, DMCA/RIAA etc.</li>
</ol>
</ol>
Traditionally that would be a huge traffic shaping box that is through the roof if available at 10G speeds.

For route/switch, either a chassis based lan switch with MPLS support (overkill possibly). Other than the ME3600 (which we have some of but thats another long story) it is big chassis or ISR/ASR routers from each vendor. Juniper 4500 is sketchy on the documentation of whether it is just MPLS on the northbound uplinks.
<hr>
The firewalling could be done at 10GE with expensive ASA/ESX solutions but also very pricey.

All three of those boxes are expensive to life-cycle on a 5 year to top it up. 500K+.

In comes NBAR-2. Before you flame it looks like there is a really cool manner inwhich it is done on the ESP in the ASR from what I can see. Typically NBAR for classifications on the 6ks wrecked shop but the nice thing about the ASR 1k is the 40 cores on it. Instead of just forking the header up for a forward it inspects payload in the ESP it appears.

For firewalling/blacklisting I will give a go with the IOS FW onboard also due to the loads of cores to deal with that. I need to dig deeper on impact there but it still beats a 5585-ssp60.

10GE route switch should still be available if the proper ESP is selected and still maintain the speeds. After digging in with a TME it seems there are some cool classification features roadmaped but I cannot remember what was NDA and not.
<h2>Custom Hardware Will Not See Another Decade</h2>
Mainframes as network systems are done. Open systems will become prevalent as SDN evolves. Until then, I will blog about boring bullshit that I have to deal with in networking today and hope there is change sooner rather then later. I think we need a good recession to drive change.


Death to firewalls. What self respecting network engineer like em anyways :)