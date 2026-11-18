+++
title = "Juniper and Cisco Comparisons of RIB, LIB, FIB and LFIB Tables"
date = "2012-04-15T10:06:46+00:00"
lastmod = "2013-07-30T04:51:11+00:00"
author = "Brent Salisbury"
wp_id = 349
categories = ["Study Time"]
tags = ["Tutorials"]
description = ""
url = "/juniper-and-cisco-comparisons-of-rib-lib-fib-and-lfib-tables/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "01d3d6f52497283dacd0b5eb91136879731c455924d0e051cccce4c68abfdbc3"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Juniper and Cisco Comparisons of RIB, LIB, FIB and LFIB Tables</h2>
A quick overview before we start:

<ul>
	<li>RIBs maintain the network topologies and routing tables for each protocol. This would include many routes going to the same destination prefix.</li>
	<li>FIBs are the best route from the possibly many protocols in the RIBs pushed down to fast forwarding lookup memory for the best path(s).</li>
	<li>I wanted to get on paper some of the differences between Junos and IOS commands with regards to MPLS related forwarding tables.</li>
</ul>

It starts off with the ingress packet. As a packet comes into the Label Edge Router (LER) the Layer2 frame header will be examined and forwarded to the appropriate table, based on the Ethertype field to determine what protocol in payload of the Ethernet frame.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/ethertype.jpg" >}}"><img class="size-full wp-image-351 aligncenter" title="ethertype header" alt="ethertype header" src="{{< relurl "/wp-content/uploads/2012/04/ethertype.jpg" >}}" width="500" height="290" /></a></p>

<ul>
	<li>0x0800 - IPv4:  Lookup in FIB</li>
	<li>0x86DD – Ipv6:  Lookup in FIB</li>
	<li>0x8847 - MPLS Unicast:  Lookup in LFIB</li>
	<li>0x8848 - MPLS Multicast:  Lookup in LFIB</li>
</ul>


The table interactions in principle are the same between both Cisco and Juniper. It helps me get a feel for how the tables all help build one anther.

<a href="{{< relurl "/wp-content/uploads/2012/04/flow.jpg" >}}"><img class="alignleft size-full wp-image-352" title="flow" alt="" src="{{< relurl "/wp-content/uploads/2012/04/flow.jpg" >}}" width="500" height="417" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;
<h2>Definitions of RIB, LIB, FIB and LFIB Tables</h2>
The RIB, LIB, LFIB and FIB are from Wikipedia because I am feeling to lazy to reword the definitions myself.

Definition: Routing Information Base (RIB), is a data table stored in a router or a networked computer that lists the routes to particular network destinations, and in some cases, metrics (distances) associated with those routes. The routing table contains information about the topology of the network immediately around it. The construction of routing tables is the primary goal of routing protocols. Static routes are entries made in a routing table by non-automatic means and which are fixed rather than being the result of some network topology 'discovery' procedure.

Basically, show ip route is the FIB which is a collection of best routes from each RIB. Each routing protocol will have an associated RIB with it. All routes for BGP would have a routing database as would all OSPF routes have a separate routing database (RIB). Preferred routes out of each of those would be loaded into fast lookup ASICs for wire speed forwarding in fast path memory.
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="370"><strong>Cisco RIB in native table:</strong></td>
</tr>
<tr>
<td valign="top" width="370"><strong>#show ip route</strong>Codes: C - connected, S - static, R - RIP, M - mobile, B - BGPD - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area

N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2

E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP

i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2

ia - IS-IS inter area, * - candidate default, U - per-user static route

o - ODR, P - periodic downloaded static route

B    216.238.54.0/24 [20/0] via 74.143.0.169, 3w6d

B    216.221.5.0/24 [20/0] via 74.143.0.169, 3w6d

B    216.187.99.0/24 [20/0] via 10.1.221.142, 2w2d

B    210.51.225.0/24 [20/0] via 74.143.0.169, 3w6d

B    209.170.123.0/24 [20/0] via 74.143.0.169, 3w6d

B    209.34.243.0/24 [20/0] via 10.1.221.142, 7w0d

B    208.85.133.0/24 [20/0] via 74.143.0.169, 3w6d

B    208.0.208.0/24 [20/0] via 74.143.0.169, 3w6d

B    203.238.37.0/24 [20/0] via 10.1.221.142, 7w0d

B    203.221.22.0/24 [20/0] via 10.1.221.142, 4d11h

B    203.170.97.0/24 [20/0] via 10.1.221.142, 7w0d

B    203.34.233.0/24 [20/0] via 10.1.221.142, 7w0d

B    203.17.218.0/24 [20/0] via 10.1.221.142, 7w0d

B    202.85.159.0/24 [20/0] via 10.1.221.142, 7w0d

B    202.51.249.0/24 [20/0] via 74.143.0.169, 3w6d

B    199.204.11.0/24 [20/0] via 74.143.0.169, 3w6d

B    198.17.215.0/24 [20/0] via 10.1.221.142, 7w0d</td>
</tr>
</tbody>
</table>
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="370"><strong>Cisco RIB from a VRF</strong></td>
</tr>
<tr>
<td valign="top" width="370"><strong>#sho ip route vrf campus-data</strong></td>
</tr>
<tr>
<td valign="top" width="370">Routing Table: campus-dataCodes: C - connected, S - static, R - RIP, M - mobile, B - BGPD - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area

N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2

E1 - OSPF external type 1, E2 - OSPF external type 2

i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2

ia - IS-IS inter area, * - candidate default, U - per-user static route

o - ODR, P - periodic downloaded static route

Gateway of last resort is 10.1.221.36 to network 0.0.0.0

S    199.76.146.0/24 [120/0] via 10.1.110.65

170.201.0.0/32 is subnetted, 3 subnets

O E2    170.201.173.15 [110/20] via 10.1.221.162, 1w0d, Vlan267

O E2    170.201.41.79 [110/20] via 10.1.221.162, 1w0d, Vlan267

O E2    170.201.41.43 [110/20] via 10.1.221.162, 1w0d, Vlan267

S    199.76.147.0/24 [1/0] via 10.1.110.65

208.25.211.0/29 is subnetted, 1 subnets

O E2    208.25.211.168 [110/20] via 10.1.221.162, 1w0d, Vlan267

B    199.76.165.0/24 [200/20] via 172.24.68.5, 7w0d

208.251.244.0/30 is subnetted, 1 subnets

B       208.251.244.164 [200/0] via 172.24.68.5, 7w0d

S    172.17.0.0/16 [1/0] via 10.1.222.2</td>
</tr>
</tbody>
</table>
<table width="442" border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="442"><strong>Juniper RIB in of the Internet2 tables in a VRF </strong></td>
</tr>
<tr>
<td valign="top" width="442"><strong>&gt;show route table i2.inet.0 </strong></td>
</tr>
<tr>
<td valign="top" width="442">i2.inet.0: 13545 destinations, 13553 routes (13545 active, 0 holddown, 0 hidden)+ = Active Route, - = Last Active, * = Both1.8.1.0/24         *[BGP/170] 3d 01:14:23, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 4641 4641 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18

1.8.8.0/24         *[BGP/170] 3d 01:14:23, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 4641 4641 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18

1.8.101.0/24       *[BGP/170] 2d 17:38:40, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 9264 7497 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18

1.8.102.0/24       *[BGP/170] 3d 01:14:23, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 4641 4641 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18

1.8.150.0/24       *[BGP/170] 3d 01:14:23, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 4641 4641 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18

1.8.151.0/24       *[BGP/170] 3d 01:14:23, MED 3090, localpref 100, from 10.2.136.63

AS path: 11537 22388 7660 4641 4641 38345 I

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 18</td>
</tr>
</tbody>
</table>
Label Information Base is the software table maintained by IP/MPLS capable routers to store the details of port and the corresponding MPLS router label to be popped/pushed on incoming/outgoing MPLS packets. Entries are populated from label-distribution protocols. LIB functions in the control plane of cisco routers MPLS layer. It is used by the label distribution protocol for mapping the next hop labels
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="302"><strong>Cisco LIB Label Information Base</strong></td>
</tr>
<tr>
<td valign="top" width="302"><strong>show mpls ldp bindings </strong></td>
</tr>
<tr>
<td valign="top" width="302">  lib entry: 10.1.55.128/26, rev 986local binding:  label: imp-nullremote binding: lsr: 172.24.68.18:0, label: 18

remote binding: lsr: 172.24.68.9:0, label: 21

remote binding: lsr: 172.24.68.21:0, label: 16

remote binding: lsr: 172.24.68.7:0, label: 17

remote binding: lsr: 172.24.68.2:0, label: imp-null

remote binding: lsr: 172.24.68.6:0, label: 19

remote binding: lsr: 172.24.68.25:0, label: 179

remote binding: lsr: 172.24.68.4:0, label: 20

remote binding: lsr: 172.24.68.5:0, label: 33

remote binding: lsr: 172.24.68.11:0, label: 16

remote binding: lsr: 172.24.68.66:0, label: 358

remote binding: lsr: 172.24.68.15:0, label: 22

remote binding: lsr: 172.24.68.19:0, label: 19

remote binding: lsr: 172.24.68.17:0, label: 20

remote binding: lsr: 172.24.68.14:0, label: 19

lib entry: 10.1.110.0/30, rev 11026

local binding:  label: 347

remote binding: lsr: 172.24.68.2:0, label: imp-null

remote binding: lsr: 172.24.68.66:0, label: 294

remote binding: lsr: 172.24.68.19:0, label: 82

remote binding: lsr: 172.24.68.6:0, label: 158

remote binding: lsr: 172.24.68.18:0, label: 239

remote binding: lsr: 172.24.68.4:0, label: 159

remote binding: lsr: 172.24.68.21:0, label: 17

remote binding: lsr: 172.24.68.15:0, label: 159

remote binding: lsr: 172.24.68.11:0, label: 17

remote binding: lsr: 172.24.68.9:0, label: 157

remote binding: lsr: 172.24.68.5:0, label: 219

remote binding: lsr: 172.24.68.25:0, label: 34

remote binding: lsr: 172.24.68.7:0, label: 230

remote binding: lsr: 172.24.68.17:0, label: 244

remote binding: lsr: 172.24.68.14:0, label: 163</td>
</tr>
</tbody>
</table>
A forwarding information base (FIB), also known as a forwarding table, is most commonly used in network bridging, routing, and similar functions to find the proper interface to which the input interface should send a packet to be transmitted by the router. In contrast to routing information bases (RIB), also known as routing tables, FIBs are optimized for fast lookup of destination addresses. Earlier implementations cached only a subset of the routes most frequently used in actual forwarding, and this worked reasonably well for enterprises where there is a meaningful most-frequently-used subset. Routers used for accessing the entire Internet, however, experienced severe performance degradation in refreshing a small cache, and various implementations moved to having FIBs in one-to-one correspondence with the RIB [1]. RIBs are optimized for efficient updating by routing protocols and other control plane methods, and contain the full set of routes learned by the router.

FIBs may also be implemented with fast hardware lookup mechanisms, such as ternary content addressable memory (TCAM). TCAM, however, is quite expensive, and tends to be used more in edge routers with relatively small numbers of routes than in routers that must carry full Internet routing tables, with supplementary internal routes.
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="338"><strong>Cisco VRF installed FIB</strong></td>
</tr>
<tr>
<td valign="top" width="338"><strong>#sho ip cef vrf campus-data</strong></td>
</tr>
<tr>
<td valign="top" width="338">Prefix              Next Hop             Interface0.0.0.0/0           10.1.221.65       Vlan2570.0.0.0/32          receive

1.0.4.0/22          10.1.221.142      Vlan271

1.0.16.0/23         10.1.221.142      Vlan271

1.0.18.0/23         10.1.221.142      Vlan271

1.0.20.0/23         10.1.221.142      Vlan271

1.0.22.0/23         10.1.221.142      Vlan271

1.0.25.0/24         10.1.221.142      Vlan271

1.0.26.0/23         10.1.221.142      Vlan271

1.0.28.0/22         10.1.221.142      Vlan271

1.0.64.0/18         10.1.221.142      Vlan271

1.0.128.0/17        10.1.221.142      Vlan271

1.0.128.0/18        10.1.221.142      Vlan271

1.0.128.0/19        10.1.221.142      Vlan271

1.0.160.0/19        10.1.221.142      Vlan271

1.0.192.0/18        10.1.221.142      Vlan271

1.0.192.0/19        10.1.221.142      Vlan271

1.0.224.0/19        10.1.221.142      Vlan271

1.1.64.0/19         10.1.221.142      Vlan271

1.1.128.0/17        10.1.221.142      Vlan271</td>
</tr>
</tbody>
</table>
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="338"><strong>Cisco VRF installed FIB</strong></td>
</tr>
<tr>
<td valign="top" width="338"><strong>#sho ip cef vrf campus-data</strong></td>
</tr>
<tr>
<td valign="top" width="338">Prefix               Next Hop             Interface0.0.0.0/0            10.1.220.225      TenGigabitEthernet1/10.0.0.0/8            drop

0.0.0.0/32           receive

10.2.1.0/24          10.1.220.225      TenGigabitEthernet1/1

10.1.220.229      TenGigabitEthernet1/2

10.2.5.0/24          10.1.220.225      TenGigabitEthernet1/1

10.1.220.229      TenGigabitEthernet1/2

10.20.0.0/22         10.1.220.229      TenGigabitEthernet1/2

10.20.4.0/22         10.1.220.229      TenGigabitEthernet1/2

10.20.8.0/22         10.1.220.229      TenGigabitEthernet1/2

10.20.12.0/22        10.1.220.229      TenGigabitEthernet1/2

10.20.16.0/22        10.1.220.229      TenGigabitEthernet1/2

10.20.20.0/22        10.1.220.229      TenGigabitEthernet1/2

10.20.24.0/22        10.1.220.229      TenGigabitEthernet1/2</td>
</tr>
</tbody>
</table>
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="383">Juniper FIB</td>
</tr>
<tr>
<td valign="top" width="383">&gt; show route forwarding-table vpn i2</td>
</tr>
<tr>
<td valign="top" width="383">Routing table: i2.inetInternet:Destination        Type RtRef Next hop           Type Index NhRef Netif

default            perm     0                    rjct   868     1

0.0.0.0/32         perm     0                    dscd   864     1

1.8.1.0/24         user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002

1.8.8.0/24         user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002

1.8.101.0/24       user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002

1.8.102.0/24       user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002

1.8.150.0/24       user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002

1.8.151.0/24       user     0                    indr 1048576 13503

10.2.136.29    Push 18   856     2 xe-0/2/0.3002</td>
</tr>
</tbody>
</table>
Label forwarding information base (LFIB) is a data structure and way of managing forwarding in which destinations and incoming labels are associated with outgoing interfaces and labels.

The forwarding paradigm employed by MPLS is based on the notion of label swapping. When a packet with a label is received by an LSR, the switch uses the label as an index in its label information base (LFIB).

Each entry in the LFIB consists of an incoming label and one or more subentries (of the form outgoing label, outgoing interface, outgoing link-level information). If the switch finds an entry with the incoming label equal to the label carried in the packet, then, for each component in the entry, the switch replaces the label in the packet with the outgoing label, replaces the link-level information (such as the MAC address) in the packet with the outgoing link-level information, and forwards the packet over the outgoing interface.
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="401"><strong>Cisco LFIB</strong></td>
</tr>
<tr>
<td valign="top" width="401"><strong>#sho mpls forwarding-table </strong></td>
</tr>
<tr>
<td valign="top" width="401">Local      Outgoing   Prefix           Bytes Label   Outgoing   Next HopLabel      Label      or Tunnel Id     Switched      interface16         Pop Label  IPv4 VRF[V]      11118051466   aggregate/campus-data

66         Pop Label  172.24.68.1/32   62922724      Te1/1      10.1.220.225

67         Pop Label  172.24.68.2/32   22780924      Te1/2      10.1.220.229

68         532              172.24.68.3/32   0                  Te1/2      10.1.220.229

69         200              192.168.253.236/30    0             Te1/2      10.1.220.229

70         505              172.24.68.5/32   0             Te1/1      10.1.220.225

71         1041            172.24.68.6/32   0             Te1/1      10.1.220.225

72         489              172.24.68.7/32   0             Te1/1      10.1.220.225

73         461              172.24.68.8/32   0             Te1/2      10.1.220.229</td>
</tr>
</tbody>
</table>
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="401"><strong>Juniper mpls.0 table (LFIB)</strong></td>
</tr>
<tr>
<td valign="top" width="401"><strong>show route table mpls.0           </strong></td>
</tr>
<tr>
<td valign="top" width="401">mpls.0: 12 destinations, 12 routes (12 active, 0 holddown, 0 hidden)+ = Active Route, - = Last Active, * = Both0                  *[MPLS/0] 37w2d 02:54:24, metric 1

Receive

1                  *[MPLS/0] 37w2d 02:54:24, metric 1

Receive

2                  *[MPLS/0] 37w2d 02:54:24, metric 1

Receive

16                 *[VPN/0] 37w2d 01:24:25

to table kpen-i1.inet.0, Pop

17                 *[VPN/0] 34w1d 04:51:43

to table i2.inet.0, Pop

18                 *[VPN/0] 31w1d 06:16:20

to table i2-cps.inet.0, Pop

262153             *[VPLS/7] 7w2d 03:02:03

&gt; via lsi.1051648, Pop

300736             *[LDP/9] 5w4d 17:23:47, metric 1

&gt; to 10.2.136.29 via xe-0/2/0.3002, Pop

300736(S=0)        *[LDP/9] 5w4d 17:23:47, metric 1

&gt; to 10.2.136.29 via xe-0/2/0.3002, Pop

514816             *[LDP/9] 5w4d 17:24:00, metric 1

&gt; to 10.2.137.194 via xe-2/3/0.0, Pop

514816(S=0)        *[LDP/9] 5w4d 17:24:00, metric 1

&gt; to 10.2.137.194 via xe-2/3/0.0, Pop

lsi.1051648        *[VPLS/7] 7w2d 03:02:03, metric2 1

&gt; to 10.2.136.29 via xe-0/2/0.3002, Push 262148</td>
</tr>
</tbody>
</table>
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="top" width="401">show route table mpls.0  details (snipped)</td>
</tr>
<tr>
<td valign="top" width="401">262153 (1 entry, 1 announced)*VPLS   Preference: 7Next hop type: Router, Next hop index: 788

Address: 0x2df36e68

Next-hop reference count: 2

Next hop: via lsi.1051648, selected

Label operation: Pop

State: &lt;Active Int&gt;

Age: 7w2d 3:00:54

Task: Common L2 VC

Announcement bits (1): 0-KRT

AS path: I</td>
</tr>
</tbody>
</table>
I didn’t get into FECs.

At ingress the PE classifies packets into a FEC (inet.3 table) with a next-hop (loopbacks) and then a label is bound with a label (up/down allocations etc) and those labels are then, advertised through by a distribution protocol such as LDP or RSVP throughout the MPLS domain. There is a killer post that explains them better than I would at http://blog.ioshints.info/2011/12/junos-day-one-mpls-behind-scenes.html

&nbsp;

&nbsp;