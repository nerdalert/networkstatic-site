+++
title = "MVPN Multicast with Multi-Protocol BGP MPLS VPN on Cisco IOS"
date = "2011-06-14T02:14:26+00:00"
lastmod = "2013-07-30T05:02:17+00:00"
author = "Brent Salisbury"
wp_id = 27
categories = ["In the Lab"]
tags = ["MPLS", "Tutorials"]
description = ""
url = "/mvpn-multicast-with-multi-protocol-bgp-mpls-vpn-on-cisco-ios/"
image = "/wp-content/uploads/2012/10/cisco-logo.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8308a7d9d5d1da899774cd274dc8b68c126849879e85454e25d12cbcbf88dd68"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>MVPN Multicast with Multi-Protocol BGP MPLS VPN on Cisco IOS</h2>
Below assumes you have the basic MPLS transport setup. MVPN or multicast vpn is deployed on Cisco gear using Multicast Distribution Trees (MDT). This information is encapsulated in the MPBGP MPLS sessions to be distributed into label switch paths (LSPs) for forwarding. The following code will produce a basic functioning Cisco IOS MDT multicast environment. A tutorial for that can be found in this post <a href="{{< relurl "/basic-mplsvpn-using-cisco-ios/" >}}" target="_blank">Basic MPLS/VPN with Cisco</a>.

<h2 class="legacy-heading">Configuring MVPN Multicast with MBGP MPLS VPN</h2>

Global multicast configuration:
<pre class="brush: bash; gutter: true">ip multicast-routing &lt;strong&gt;&lt;em&gt;(!—Globally enable Multicast routing)&lt;/em&gt;&lt;/strong&gt;
ip multicast-routing vrf data  &lt;strong&gt;&lt;em&gt;(!—Enable Multicast for the VRF instance)&lt;/em&gt;&lt;/strong&gt;
ip multicast-routing vrf voice &lt;strong&gt;&lt;em&gt;(!—Enable Multicast for the VRF instance)&lt;/em&gt;&lt;/strong&gt;</pre>
<ul>
	<li> VRF Configurations:</li>
</ul>
<pre class="brush: bash; gutter: true">ip vrf campus-data
rd 65001:10
route-target export 65001:11
route-target import 65001:11
mdt default 232.2.2.2 (!—Multicast MDT group. Must be same across all PE routers per VRF)
ip vrf voice
rd 10437:4
route-target export 10437:5
route-target import 10437:5
mdt default 232.1.1.1 &lt;strong&gt;&lt;em&gt;(!—Multicast MDT group. Must be same across all PE routers per VRF)&lt;/em&gt;&lt;/strong&gt;</pre>
<ul>
	<li>More Global Configurations:</li>
</ul>
<pre class="brush: bash; gutter: true">interface Vlan10
ip vrf forwarding data &lt;strong&gt;&lt;em&gt;(!—Add an interface into the VRF)&lt;/em&gt;&lt;/strong&gt;
ip address x.x.x.x 255.255.255.0
ip pim sparse-mode &lt;strong&gt;&lt;em&gt;(!—enable PIM (Protocol Independent Multicast, sparse or dense. Sparse recommended in order to avoid flooding)&lt;/em&gt;&lt;/strong&gt;
ip pim rp-address 172.24.68.1 override &lt;strong&gt;&lt;em&gt;(Explicitly state the PIM RP. This is the core loopback for the network native Multicast table)&lt;/em&gt;&lt;/strong&gt;
ip pim vrf campus-data rp-address 128.163.220.8
ip pim vrf voice rp-address 172.17.1.9 override &lt;strong&gt;&lt;em&gt;(Explicitly state the PIM RP. This is the core loopback for the network VRF &amp;lt;instance name&amp;gt; Multicast table. This is the RP of the loopback in the Voice core for paging)&lt;/em&gt;&lt;/strong&gt;</pre>
<ul>
	<li>Useful commands to verify operations:</li>
</ul>
<pre class="brush: bash; gutter: true">xxx-c1#sho ip pim vrf data neighbor &lt;strong&gt;&lt;em&gt;(Look for established tunnels to all other PE’s in the VRF)&lt;/em&gt;&lt;/strong&gt;
PIM Neighbor Table
Mode: B - Bidir Capable, DR - Designated Router, N - Default DR Priority,
P - Proxy Capable, S - State Refresh Capable, G - GenID Capable
Neighbor          Interface                Uptime/Expires    Ver   DR
Address                                                            Prio/Mode
172.24.68.98      Tunnel0                  6w0d/00:01:36     v2    1 / DR S P G
172.24.68.87      Tunnel0                  8w4d/00:01:40     v2    1 / S P G
172.24.68.91      Tunnel0                  19w6d/00:01:23    v2    1 / S G
172.24.68.4       Tunnel0                  23w5d/00:01:23    v2    1 / S P G
172.24.68.5       Tunnel0                  23w5d/00:01:32    v2    1 / S P G
172.24.68.9       Tunnel0                  23w5d/00:01:28    v2    1 / S P G
172.24.68.15      Tunnel0                  23w5d/00:01:20    v2    1 / S P G
172.24.68.6       Tunnel0                  23w5d/00:01:26    v2    1 / S P G
172.24.68.78      Tunnel0                  23w5d/00:01:15    v2    1 / S P G
172.24.68.97      Tunnel0                  23w5d/00:01:38    v2    1 / S P G
172.24.68.2       Tunnel0                  23w5d/00:01:38    v2    1 / S P G
172.24.68.1       Tunnel0                  23w5d/00:01:43    v2    1 / S P G</pre>
Thanks for stopping by.

<hr />