+++
title = "Basic MPLS/VPN with Cisco IOS"
date = "2012-04-11T03:59:03+00:00"
lastmod = "2013-08-29T22:34:36+00:00"
author = "Brent Salisbury"
wp_id = 311
categories = ["In the Lab"]
tags = ["MPLS", "Tutorials"]
description = ""
url = "/basic-mplsvpn-using-cisco-ios/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "fdb73ad4f763ca00e8223efb8a986b0a037e374e1e2524b984ab8f43d8756acd"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Basic MPLS/VPN with Cisco IOS</h2>
This is a quick tutorial for basic MPLS/VPN with Cisco IOS configuration. The tutorial exemplifies basic PE to P to PE configuration on three Cisco 7200s running in GNS3 with IOS. R2 is configured as a route reflector P node and R4, R6 and R3 are PE node route reflector clients. The IGP is OSPF with R2 as the ABR. Loopback1 (Lo1) on R3  &amp; R4 represent a customer VPN (CE) ethernet segment. The loopback 1 interfaces are pushed into the MPLS/VRF named "data" to simulate an Ethernet segment advertised into the VRF.
<h2>Basic MPLS/VPN and Multi-Protocol BGP Topology</h2>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/4-node.jpg" >}}"><img class="size-full wp-image-322 aligncenter" title="4-node" alt="" src="{{< relurl "/wp-content/uploads/2012/04/4-node.jpg" >}}" width="500" height="383" /></a></p>
<strong>FIgure 1.</strong> MPLS VPN Lab Topology
<h2>Cisco IOS MPLS VPN Configuration for 4 routers</h2>
<pre class="code-sample"><code>R3#sho run
Building configuration...
Current configuration : 1297 bytes
 !
 version 12.4
 !
 hostname R3
 !
 ip cef
 !
 !
 ip vrf data
 rd 65001:3
 route-target export 65001:20
 route-target import 65001:20
 !
 mpls label protocol ldp
 !
 !
 !
 interface Loopback0
 ip address 3.3.3.3 255.255.255.255
 !
 interface Loopback1
 ip vrf forwarding data
 ip address 6.6.6.6 255.255.255.255
 !
 interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
 !
 interface GigabitEthernet1/0
 ip address 10.10.10.2 255.255.255.252
 negotiation auto
 mpls ip
 !
 router ospf 101
 log-adjacency-changes
 network 0.0.0.0 255.255.255.255 area 0
 !
 router bgp 65001
 no synchronization
 bgp log-neighbor-changes
 neighbor 2.2.2.2 remote-as 65001
 neighbor 2.2.2.2 update-source Loopback0
 no auto-summary
 !
 address-family vpnv4
 neighbor 2.2.2.2 activate
 neighbor 2.2.2.2 send-community extended
 exit-address-family
 !
 address-family ipv4 vrf data
 redistribute connected
 no synchronization
 exit-address-family
 !
 !
 end</code></pre>

<hr />

<pre class="code-sample"><code>R4#sho run
 Building configuration...
Current configuration : 1417 bytes
 !
 version 12.4
 !
 ip cef
 !
 !
 ip vrf data
 rd 65001:4
 route-target export 65001:20
 route-target import 65001:20
 !
 !
 interface Loopback0
 ip address 4.4.4.4 255.255.255.255
 !
 interface Loopback1
 ip vrf forwarding data
 ip address 8.8.8.8 255.255.255.255
 !
 interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
 !
 interface GigabitEthernet1/0
 ip address 10.10.11.2 255.255.255.252
 negotiation auto
 mpls ip
 !
 interface GigabitEthernet2/0
 no ip address
 shutdown
 negotiation auto
 !
 router ospf 101
 log-adjacency-changes
 network 4.4.4.4 0.0.0.0 area 1
 network 10.10.11.0 0.0.0.3 area 1
 !
 router bgp 65001
 bgp log-neighbor-changes
 neighbor 2.2.2.2 remote-as 65001
 neighbor 2.2.2.2 update-source Loopback0
 !
 address-family ipv4
 neighbor 2.2.2.2 activate
 no auto-summary
 no synchronization
 exit-address-family
 !
 address-family vpnv4
 neighbor 2.2.2.2 activate
 neighbor 2.2.2.2 send-community extended
 exit-address-family
 !
 address-family ipv4 vrf data
 redistribute connected
 no synchronization
 exit-address-family
 !
 end</code></pre>

<hr />

<pre class="code-sample"><code>R2#sho run
Building configuration...
Current configuration : 1811 bytes
 !
 version 12.4
 !
 hostname R2
 !
 ip cef
 !
 !
 ip vrf data
 rd 65001:2
 route-target export 65001:20
 route-target import 65001:20
 !
 mpls label protocol ldp
 !
 !
 interface Loopback0
 ip address 2.2.2.2 255.255.255.255
 !
 interface Loopback1
 ip vrf forwarding data
 ip address 9.9.9.9 255.255.255.255
 !
 interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
 !
 interface GigabitEthernet1/0
 ip address 10.10.11.1 255.255.255.252
 negotiation auto
 mpls ip
 !
 interface GigabitEthernet2/0
 ip address 10.10.10.1 255.255.255.252
 negotiation auto
 mpls ip
 !
 interface GigabitEthernet3/0
 no ip address
 shutdown
 negotiation auto
 !
 router ospf 101
 log-adjacency-changes
 network 2.2.2.2 0.0.0.0 area 0
 network 10.10.10.0 0.0.0.3 area 0
 network 10.10.11.0 0.0.0.3 area 1
 !
 router bgp 65001
 no synchronization
 bgp log-neighbor-changes
 neighbor 3.3.3.3 remote-as 65001
 neighbor 3.3.3.3 update-source Loopback0
 neighbor 3.3.3.3 route-reflector-client
 neighbor 4.4.4.4 remote-as 65001
 neighbor 4.4.4.4 update-source Loopback0
 neighbor 4.4.4.4 route-reflector-client
 no auto-summary
 !
 address-family vpnv4
 neighbor 3.3.3.3 activate
 neighbor 3.3.3.3 send-community extended
 neighbor 3.3.3.3 route-reflector-client
 neighbor 4.4.4.4 activate
 neighbor 4.4.4.4 send-community extended
 neighbor 4.4.4.4 route-reflector-client
 exit-address-family
 !
 address-family ipv4 vrf data
 redistribute connected
 no synchronization
 exit-address-family
 !
end</code></pre>

<hr />

<pre class="code-sample"><code>!
hostname R6
 !
 boot-start-marker
 boot-end-marker
 !
 !
 no aaa new-model
 !
 !
 ip cef
 !
 !
 ip vrf data
 rd 65001:7
 route-target export 65001:20
 route-target import 65001:20
 !
 mpls label protocol ldp
 !
 !
 interface Loopback0
 ip address 7.7.7.7 255.255.255.255
 !
 interface Loopback1
 ip vrf forwarding data
 ip address 1.1.1.1 255.255.255.255
 !
 interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
 !
 interface GigabitEthernet1/0
 ip address 10.10.12.2 255.255.255.252
 negotiation auto
 mpls ip
 !
 interface GigabitEthernet2/0
 no ip address
 negotiation auto
 !
 router ospf 101
 log-adjacency-changes
 network 10.10.12.0 0.0.0.255 area 1
 network 0.0.0.0 255.255.255.255 area 1
 !
 router bgp 65001
 bgp log-neighbor-changes
 neighbor 4.4.4.4 remote-as 65001
 neighbor 4.4.4.4 update-source Loopback0
 !
 address-family ipv4
 redistribute connected
 neighbor 4.4.4.4 activate
 neighbor 4.4.4.4 route-reflector-client
 no auto-summary
 no synchronization
 exit-address-family
 !
 address-family vpnv4
 neighbor 4.4.4.4 activate
 neighbor 4.4.4.4 send-community extended
 exit-address-family
 !
 address-family ipv4 vrf data
 redistribute connected
 no synchronization
 exit-address-family</code></pre>


R6#ping vrf data 6.6.6.6

Type escape sequence to abort.

Sending 5, 100-byte ICMP Echos to 6.6.6.6, timeout is 2 seconds:

!!!!!

Success rate is 100 percent (5/5), round-trip min/avg/max = 52/60/80 ms