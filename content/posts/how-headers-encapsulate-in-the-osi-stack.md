+++
title = "How Headers Encapsulate in the OSI stack"
date = "2012-04-10T05:51:06+00:00"
lastmod = "2012-12-15T23:06:57+00:00"
author = "Brent Salisbury"
wp_id = 296
categories = ["Study Time", "Tools"]
tags = ["Tutorials"]
description = ""
url = "/how-headers-encapsulate-in-the-osi-stack/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "092fe34768362e35b3a91a65c23286b39c1bf2605057e72d9fb621c72618f5c7"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>How Headers Encapsulate in the OSI stack</h2>
How Headers Encapsulate in the OSI stack: Part 2 of some refreshers. We send application data or payload by encapsulating or framing each layer within the previous layer. We looked at each one individually and now here is how they look when each layer is wrapped inside the previous layer.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/youtube-kitty-osi.jpg" >}}" alt="OSI Model Encapsulation"></figure>
<strong> Figure 1</strong>. Here is how application data gets passed to each protocol in the stack to see a cute cat playing piano.

Each device along the path from source to destination (user to Youtube in this case) strips the header it is concerned with and imposes the new information in another header wrapping the packet back up for its next hop. The payload remains the same along the way outside of fragmentation but these days Path MTU Discovery (PMTUD) has alleviated the need to fragment packets thus reducing overhead on devices in the path. I left out the footer in the Layer 2 Ethernet layer so keep in mind there is one there along with "TCP data" on the tail of the TCP header and payload.

The packaging and re-packaging of pulse of energy and light is fascinating to try and wrap your head around and I am still amazed that the laws of physics allow us to do these things!
<hr>
<a title="Part 1" href="http://networkstatic.wordpress.com/2012/04/08/correlating-ethernet-ip-and-tcp-headers-to-a-wireshark-capture/">Part 1</a> breaks down each header on a previous post.
<hr>