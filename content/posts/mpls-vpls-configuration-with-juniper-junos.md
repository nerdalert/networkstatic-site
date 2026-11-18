+++
title = "MPLS VPLS configuration with Juniper JunOS"
date = "2012-05-26T09:17:52+00:00"
lastmod = "2013-06-28T03:27:44+00:00"
author = "Brent Salisbury"
wp_id = 718
categories = ["In the Lab"]
tags = ["Juniper", "MPLS", "Tutorials", "vpls"]
description = ""
url = "/mpls-vpls-configuration-with-juniper-junos/"
image = "/wp-content/uploads/2012/05/Juniper-VPLS-MPLS.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "6592910c8dea10619f48c924e41094424cf68dc687b81f62f61a6cb57d88c2ac"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>MPLS VPLS configuration with Juniper JunOS</h2>
Posting a Juniper VPLS how-to on a couple of J-series routers. Have been pretty SDN focused lately so wanted to get some real stuff in for a post. Docs on JunOS VPLS can be shaky so nothing like a couple real configs to plugin your address in the lab if having problems with L2 VPNs. This includes MPLS VPLS configuration with Juniper JunOS.

The two PE routers build MPLS/BGP adjacencies to one another to exchange label information and build the LSPs for the two VRFs. VRF Blue is the VPLS virtual circuit and VRF red is a simple L3 VPN you can use to test MP-BGP to test MP-BGP populating it with loopbacks (or phy ints). VPLS can be multipoint while draft-Martini/Kompella are p2p one being LDP (Martini) to signal the label and the other being BGP (Kompella) signalled.

Feel free to hit me up with any questions. I can do more JunOS stuff if anyone needs a hand with particulars. It's a bit different than IOS starting out but it has structured data model once you get used to it.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/05/l2vpn-topo1.jpg" >}}" alt="JunOS MPLS VPLS VPN"></figure>

<strong>Figure 1.</strong><em> Orange line is the pseudowire or VPLS circuit going through the provider edge nodes to the customer edge nodes.</em>

<h2>MPLS VPLS configuration Node 1</h2>
root@J1# show
<pre class="code-sample"><code>## Last changed:
version 10.0R3.10;
system {
host-name J1;
root-authentication {
encrypted-password ## SECRET-DATA
}
services {
ftp;
web-management {
http {
interface [ ge-0/0/0.0 ge-0/0/1.0 ge-0/0/2.0 ge-0/0/3.0 ];
}
}
}
syslog {
file logs {
any any;
}
}
}
ge-1/0/1 {
unit 0 {
family inet {
address 10.1.1.1/24;
}
family mpls;
}
}
ge-1/0/2 {
encapsulation ethernet-vpls;
unit 0;
}
lo0 {
unit 0 {
family inet {
address 1.1.1.1/32;
}
}
unit 10 {
family inet {
address 11.11.11.11/32;
}
}
}
}
routing-options {
autonomous-system 65001;
}
protocols {
mpls {
interface lo0.0;
interface ge-1/0/0.10;
}
bgp {
group ibgp {
type internal;
local-address 1.1.1.1;
family inet {
unicast;
}
family inet-vpn {
unicast;
}
family l2vpn {
signaling;
}
local-as 65001;
neighbor 2.2.2.2;
}
}
ospf {
area 0.0.0.0 {
interface lo0.0;
interface ge-1/0/1.0;
}
}
ldp {
interface ge-1/0/1.0;
}
}
policy-options {
policy-statement direct-int {
from protocol direct;
then accept;
}
policy-statement r2-peer {
term loop1 {
from {
route-filter 192.168.250.1/32 exact;
route-filter 192.168.252.1/32 exact;
}
then accept;
}
term exp-deny {
then reject;
}
}
}
security {
forwarding-options {
family {
mpls {
mode packet-based;
}
}
}
flow {
tcp-session {
no-syn-check;
no-syn-check-in-tunnel;
}
}
}
routing-instances {
blue {
instance-type vpls;
interface ge-1/0/2.0;
route-distinguisher 65001:12;
vrf-target target:65001:15;
protocols {
vpls {
interface ge-1/0/2.0;
no-tunnel-services;
site blue1 {
site-identifier 1;
}
vpls-id 101;
neighbor 2.2.2.2;
}
}
}
red {
instance-type vrf;
interface lo0.10;
route-distinguisher 65001:2;
vrf-target target:65001:1;
}
}</code></pre>
<h2>MPLS VPLS configuration Node 2</h2>
root@J2# show
<pre class="code-sample"><code>## Last changed:
 version 10.0R3.10;
 system {
 host-name J2;
 root-authentication {
 encrypted-password ## SECRET-DATA
 }
 services {
 ftp;
 }
 }
 ge-0/0/1 {
 unit 0 {
 family inet {
 address 10.1.1.2/24;
 }
 family mpls;
 }
 }
 ge-0/0/2 {
 encapsulation ethernet-vpls;
 unit 0;
 }
 lo0 {
 unit 0 {
 family inet {
 address 2.2.2.2/32;
 }
 }
 unit 10 {
 family inet {
 address 22.22.22.22/32;
 }
 }
 }
 }
 routing-options {
 autonomous-system 65001;
 }
 protocols {
 mpls {
 interface ge-0/0/1.0;
 interface lo0.0;
 }
 bgp {
 group ibgp {
 type internal;
 local-address 2.2.2.2;
 family inet {
 unicast;
 }
 family inet-vpn {
 unicast;
 }
 family l2vpn {
 signaling;
 }
 local-as 65001;
 neighbor 1.1.1.1;
 }
 }
 ospf {
 area 0.0.0.0 {
 interface lo0.0;
 interface ge-0/0/1.0;
 }
 }
 ldp {
 interface ge-0/0/1.0;
 }
 }
 security {
 forwarding-options {
 family {
 mpls {
 mode packet-based;
 }
 }
 }
 flow {
 tcp-session {
 no-syn-check;
 no-syn-check-in-tunnel;
 }
 }
 }
 routing-instances {
 blue {
 instance-type vpls;
 interface ge-0/0/2.0;
 route-distinguisher 65001:11;
 vrf-target target:65001:15;
 protocols {
 vpls {
 interface ge-0/0/2.0;
 no-tunnel-services;
 site blue2 {
 site-identifier 2;
 }
 vpls-id 101;
 neighbor 1.1.1.1;
 }
 }
 }
 red {
 instance-type vrf;
 interface lo0.10;
 route-distinguisher 65001:3;
 vrf-target target:65001:1;
 }
 }</code></pre>
<hr>
If you are interested in other L2 provider encapsulations take a look at QinQ and MAC-in-MAC:
<a href="{{< relurl "/putting-together-provider-bridging-provider-backbone-bridging-s-tags-and-c-tags/" >}}">Putting Together Provider Bridging, Provider Backbone Bridging, S-Tags and C-Tags</a>
<hr>
Should get you started with P2MP and P2P pseudowires!