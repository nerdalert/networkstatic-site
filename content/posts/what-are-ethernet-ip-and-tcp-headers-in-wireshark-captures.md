+++
title = "What are Ethernet, IP and TCP Headers in Wireshark Captures"
date = "2012-04-08T04:58:49+00:00"
lastmod = "2013-07-30T04:53:27+00:00"
author = "Brent Salisbury"
wp_id = 274
categories = ["Study Time", "Tools"]
tags = ["Tutorials"]
description = ""
url = "/what-are-ethernet-ip-and-tcp-headers-in-wireshark-captures/"
image = "/wp-content/uploads/2012/04/1-slide11.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3e63cbdcbe69c655253df7518c5a16bcd0368c79171c5f992ed54f1c583cd0fc"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>What are Ethernet, IP and TCP Headers in Wireshark Captures</h2>
If I could go back in time when I was a n00b kid wanting to go from zero to a million in networking, the one thing I would change would be spending about 6 months on the fundamentals of networking headers and framing before ever touching a single peice of vendor gear. Ethernet, IP and Transport headers (L2-L4) are the past present and future of networking. Protocols will come and go, Ethernet and IP will undoubtedly be with us for the rest of our careers. I know a lot of good engineers, Ops and architects that have learned and forgotten fundamental details five times over, me included as we fill our heads with timers of IGPs and framing encapsulations of data center interconnects.

I tend to try and go back and refresh the basics on the wikis as much as possible. Example, 802.1Q encapsulation is not actually encapsulating the original frame but inserting a 32-bit field with the TPID, VID etc.

Layered architectures are great (in theory :-) but it requires understanding how they interact with one another. I think the encapsulation of the layers can be tough to wrap ones head around as they are entering the field. Once they do they become rock stars, as the beauty of decoupling the layers allow for comprehension of enormous scale.

When working with interns at work we tend to start by breaking out Wireshark capture. This doesn't necessarily always help, as that can be even more confusing than looking at abstracted theoretical layers for a greenhorn. I tend to break a Wireshark capture down and try to correlate that to the three most relevant layers and their headers L2-L4.
<ol class="legacy-numbers">
<ol>
	<li>Ethernet II - Layer 2</li>
	<li>IP Header - Layer 3</li>
	<li>TCP Header -Layer 4. I left out UDP since connectionless headers are quite simpler, e.g. Source Port, Destination Port, Length and Checksum.</li>
</ol>
</ol>

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/04/packet-header.jpg" >}}" alt="Wireshark Example Tutorial"></figure>

<strong><em>Figure 1.</em></strong> An example of a Wireshark capture.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/2intro-summ.jpg" >}}"><img class="size-full wp-image-278 aligncenter" title="Wireshark Packet Summary" alt="" src="{{< relurl "/wp-content/uploads/2012/04/2intro-summ.jpg" >}}" width="500" height="306" /></a></p>
<strong><em>Figure 2.</em></strong> The summary before the protocols in a Wireshark packet. Information about the packet characteristic.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/04/ethernet-header.jpg" >}}" alt="Ethernet II Header and Capture"></figure>

<strong><em>Figure 3.</em></strong> Ethernet II (Layer 2) header along with the Wireshark

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/04/IP-Header-Packet2.jpg" >}}" alt="IP Header Wireshark"></figure>

<strong><em>Figure 4.</em></strong> IP Header (Layer-3)
<h2>IP Header</h2>

<ul>
	<li>Version IPv4, IPv6 etc.</li>
	<li>IP Header Length (number of 32 -bit words forming the header, usually five)</li>
	<li>Type of Service (ToS), now known as Differentiated Services Code Point (DSCP) (usually set to 0, but may indicate particular Quality of Service needs from the network, the DSCP defines the way routers should queue packets while they are waiting to be forwarded).</li>
	<li>Size of Datagram (in bytes, this is the combined length of the header and the data)</li>
	<li>Identification ( 16-bit number which together with the source address uniquely identifies this packet - used during reassembly of fragmented datagrams)</li>
	<li>Flags (a sequence of three flags (one of the 4 bits is unused) used to control whether routers are allowed to fragment a packet (i.e. the Don't Fragment, DF, flag), and to indicate the parts of a packet to the receiver)</li>
	<li>Fragmentation Offset (a byte count from the start of the original sent packet, set by any router which performs IP router fragmentation)</li>
	<li>Time To Live (Number of hops /links which the packet may be routed over, decremented by most routers - used to prevent accidental routing loops)</li>
	<li>Protocol (Service Access Point (SAP) which indicates the type of transport packet being carried (e.g. 1 = ICMP; 2= IGMP; 6 = TCP; 17= UDP).</li>
	<li>Header Checksum (A 1's complement checksum inserted by the sender and updated whenever the packet header is modified by a router - Used to detect processing errors introduced into the packet inside a router or bridge where the packet is not protected by a link layer cyclic redundancy check. Packets with an invalid checksum are discarded by all nodes in an IP network)</li>
	<li>Source Address (the IP address of the original sender of the packet)</li>
	<li>Destination Address (the IP address of the final destination of the packet)</li>
	<li>Options (not normally used, but, when used, the IP header length will be greater than five 32-bit words to indicate the size of the options field)</li>
</ul>


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/04/tcp-header.jpg" >}}" alt="TCP Header"></figure>

<strong><em>Figure 5.</em></strong> TCP headers.
<h2>TCP IP Header Explained</h2>

<hr />


<ul>
	<li>Source port (16 bits) – identifies the sending port</li>
	<li>Destination port (16 bits) – identifies the receiving port</li>
	<li>Sequence number (32 bits) – has a dual role:</li>
	<li>If the SYN flag is set (1), then this is the initial sequence number. The sequence number of the actual first data byte and the acknowledged number in the corresponding ACK are then this sequence number plus 1.</li>
	<li>If the SYN flag is clear (0), then this is the accumulated sequence number of the first data byte of this packet for the current session.</li>
	<li>Acknowledgment number (32 bits) – if the ACK flag is set then the value of this field is the next sequence number that the receiver is expecting. This acknowledges receipt of all prior bytes (if any). The first ACK sent by each end acknowledges the other end's initial sequence number itself, but no data.</li>
	<li>Data offset (4 bits) – specifies the size of the TCP header in 32-bit words. The minimum size header is 5 words and the maximum is 15 words thus giving the minimum size of 20 bytes and maximum of 60 bytes, allowing for up to 40 bytes of options in the header. This field gets its name from the fact that it is also the offset from the start of the TCP segment to the actual data.</li>
	<li>Reserved (3 bits) – for future use and should be set to zero</li>
	<li>Flags (9 bits) (aka Control bits) – contains 9 1-bit flags</li>
	<li>NS (1 bit) – ECN-nonce concealment protection (added to header by RFC 3540).</li>
	<li>CWR (1 bit) – Congestion Window Reduced (CWR) flag is set by the sending host to indicate that it received a TCP segment with the ECE flag set and had responded in congestion control mechanism (added to header by RFC 3168).</li>
	<li>ECE (1 bit) – ECN-Echo indicates</li>
	<li>If the SYN flag is set (1), that the TCP peer is ECN capable.</li>
	<li>If the SYN flag is clear (0), that a packet with Congestion Experienced flag in IP header set is received during normal transmission (added to header by RFC 3168).</li>
	<li>URG (1 bit) – indicates that the Urgent pointer field is significant</li>
	<li>ACK (1 bit) – indicates that the Acknowledgment field is significant. All packets after the initial SYN packet sent by the client should have this flag set.</li>
	<li>PSH (1 bit) – Push function. Asks to push the buffered data to the receiving application.</li>
	<li>RST (1 bit) – Reset the connection</li>
	<li>SYN (1 bit) – Synchronize sequence numbers. Only the first packet sent from each end should have this flag set. Some other flags change meaning based on this flag, and some are only valid for when it is set, and others when it is clear.</li>
	<li>FIN (1 bit) – No more data from sender</li>
	<li>Window size (16 bits) – the size of the receive window, which specifies the number of bytes (beyond the sequence number in the acknowledgment field) that the sender of this segment is currently willing to receive (see Flow control and Window Scaling)</li>
	<li>Checksum (16 bits) – The 16-bit checksum field is used for error-checking of the header and data</li>
	<li>Urgent pointer (16 bits) – if the URG flag is set, then this 16-bit field is an offset from the sequence number indicating the last urgent data byte.</li>
	<li>Options (Variable 0-320 bits, divisible by 32) – The length of this field is determined by the data offset field. MSS etc.</li>
</ul>

If this helps anyone I will do a second post including MPLS encap, 802.1Q trunking, IPv6, ICMP and ARP on another post.

<a href="http://networkstatic.wordpress.com/2012/04/10/how-headers-encapsulate-in-the-osi-stack/">Part 2</a> rolls the headers together in the stack.

References:

<ul>
	<li><a href="http://en.wikipedia.org/wiki/Internet_Protocol" target="_blank">http://en.wikipedia.org/wiki/Internet_Protocol</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Transmission_Control_Protocol" target="_blank">http://en.wikipedia.org/wiki/Transmission_Control_Protocol</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Ethernet_frame" target="_blank">http://en.wikipedia.org/wiki/Ethernet_frame</a></li>
</ul>


<hr />

Thanks for stopping by.

<hr />