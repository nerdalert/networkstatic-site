+++
title = "How to deploy MPLS VPN's on Cisco gear"
date = "2011-05-29T17:27:43+00:00"
lastmod = "2012-09-09T00:18:15+00:00"
author = "Brent Salisbury"
wp_id = 10
categories = ["In the Lab"]
tags = ["MPLS", "Tutorials"]
description = ""
url = "/how-to-deploy-mpls-vpns-on-cisco-gear/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cedb4e12beb4b206ea8abb079f1921d32ec65340f9e1ba1502f8b3831f6d7d5a"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

There is no easier way to simplify your enterprise routing and path isolation than implementing MPLS/VPNs RFC 4364. Label Distribution Protocol (LDP) is the transport method to insert a label into the header to be forwarded down the Label Switch Path (LSP) by the Label Switch Router (LSR)

Most routers past the SOHO market support MPLS in hardware. On the chassis switches it gets trickier. On 6500’s the Sup32 and Sup720 support MPLS in hardware.

There was talk of the new 4500 Sups supporting it but I didn’t see any mention other than VRF support so I am sure it has slipped or fell off, like half the other late delivered features from Cisco recently.

There is no easier way to simplify your enterprise routing and path isolation than implementing MPLS/VPNs RFC 4364. Label Distribution Protocol (LDP) is the transport method to insert a label into the header to be forwarded down the Label Switch Path (LSP) by the Label Switch Router (LSR)

Most routers past the SOHO market support MPLS in hardware. On the chassis switches it gets trickier. On 6500’s the Sup32 and Sup720 support MPLS in hardware.

There was talk of the new 4500 Sups supporting it but I didn’t see any mention other than VRF support so I am sure it has slipped or fell off, like half the other late delivered features from Cisco recently.

&nbsp;

<strong>ip vrf data</strong>

<strong> rd xxx:10</strong>

<strong>route-target export xxx:11</strong> (!--your iBGP ASN = xxx is a good approach)

<strong> route-target import xxx:11</strong>

&nbsp;

<strong>mpls label protocol ldp</strong> (!--Choose LDP in case Cisco tries to default to TDP)

&nbsp;

<strong>interface Loopback0</strong> (!—loopback address for iBGP peering. Loopback is best pr

actice for iBGP peering since you do not want peering to be associated to a physical interface unless it is an eBGP peering.)

<strong>ip address x.x.x.x 255.255.255.255</strong> (/32)

&nbsp;

<strong>interface TenGigabitEthernet1/2</strong>

<strong> mtu 9216</strong> (!--make room for the additional 8bytes in the header.)

<strong> ip address x.x.x.x 255.255.255.252</strong>

<strong> mpls label protocol ldp</strong> (!--redundant but wth)

<strong> mpls ip</strong> (!--enable LDP peering to seek an adjacency with its neighbor)

&nbsp;

<strong>router bgp 65001</strong> (!—iBGP ASN – Autonomous System Number)

<strong> bgp log-neighbor-changes</strong>

<strong> neighbor x.x.x.x remote-as 65001</strong> (!—Your upstream router to peer too)

<strong> neighbor 172.24.68.1 update-source Loopback0</strong> (!—Set the loopback as the iBGP source)

&nbsp;

<strong>address-family ipv4</strong> (!--IP version 4 protocol)

<strong>  neighbor x.x.x.x activate</strong> (!--This is your upstream BGP peer address)

<strong>  neighbor x.x.x.x send-community both</strong>

&nbsp;

<strong> address-family vpnv4</strong> (!-- multiprotocol BGP MP-BGP allows for IPv4, IPv6, multicast etc)

<strong>  neighbor x.x.x.x activate</strong> (!--This is your upstream BGP peer address)

<strong>  neighbor x.x.x.x send-community both</strong>

&nbsp;

<strong>address-family ipv4 vrf data</strong> (!—This is where you advertise or redistribute routes into you VRF routing table)

<strong> redistribute connected</strong> (!—This is what allows for the route to be advertised into the VRF)

<strong>no synchronization</strong>

<strong> exit-address-family</strong>

<strong> </strong>

<strong>interface Vlan151</strong> (!-- add the SVI into the "data" vrf)

<strong> ip vrf forwarding data</strong> (adds the interface to the “data” vrf)

<strong> ip address x.x.x.x 255.255.255.0</strong>

&nbsp;

!--Native IGP. The example has OSPF. ISIS is just as good if not more scalable. Both are link state using Dijkastra’s algorithm.

<strong>router ospf 101</strong>

<strong> log-adjacency-changes</strong>

<strong> network x.x.x.x 0.0.0.0 area 0</strong> (!-- advertise the loopback)

<strong> network x.x.x.x 0.0.0.3 area 0</strong> (!-- advertise the /30)

&nbsp;

Useful commands:

<strong>Show mpls ldp neighbors</strong>

<strong>Show ip route vrf data</strong>

<strong>Show ip bgp summary</strong>

<strong>Show ip ospf neighbor</strong>

<strong>
</strong>