+++
title = "Use case for MPLS in the Enterprise for PCI Compliance"
date = "2012-04-13T04:07:15+00:00"
lastmod = "2013-07-30T05:13:38+00:00"
author = "Brent Salisbury"
wp_id = 325
categories = ["Speculative"]
tags = ["MPLS", "PCI"]
description = ""
url = "/an-no-brainer-use-case-for-mpls-in-the-enterprise-pci-compliance/"
image = "/wp-content/uploads/2013/04/stop-cant-do-it-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "c76d9193596fd02b129af0bb747cdec8092ff0f7cd90c411202b2d29622e4e80"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Use case for MPLS in the Enterprise for PCI Compliance</h2>
MPLS is today's only form of scalable network virtualization we have for now. I personally think the promise of something called SDN will move into that space soon but until then, we need network virtualization. PCI is a joke. It is a racket by Visa and banks to spread fear without any brains behind the architecture. PCI DSS v2.0 soon to be v3.0 is on of the few technological security documents that clearly states the requirements. Path Isolation is very clear for the network architect to build a design around.

That happens to be the bread and butter of MPLS as it has been used for well over a decade by service providers to provide multi tenant virtualized networks. Virtual logical and scalable networks overlaid on top of a single physical network.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/containers1.jpg" >}}"><img class="size-full wp-image-328 aligncenter" title="containers" alt="" src="{{< relurl "/wp-content/uploads/2012/04/containers1.jpg" >}}" width="500" height="360" /></a></p>
<strong>Figure 1</strong> MPLS/VPNs create logical routed containers to apply meny types of policy.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/ent-flow.jpg" >}}"><img class="size-full wp-image-329 aligncenter" title="ent-flow" alt="" src="{{< relurl "/wp-content/uploads/2012/04/ent-flow.jpg" >}}" width="500" height="561" /></a></p>
<strong>Figure 2</strong> Layer 2 traffic from access to distribution is isolated using typical 802.1Q trunking. There is a different Vlan ID associated to each VRF south of each pair of distribution routers. Vlans maintain the layer2 bridging or broadcast domain isolation. In traditional and still the majority of Enterprise networks that is the extent of path isolation. The problem is that layer2 bridging does not scale.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/mpls-stacking.jpg" >}}"><img class="size-full wp-image-330 aligncenter" title="MPLS-Stacking" alt="" src="{{< relurl "/wp-content/uploads/2012/04/mpls-stacking.jpg" >}}" width="500" height="306" /></a></p>
<strong>Figure 3. </strong>MPLS Label Stacking.

<strong></strong>Once a bridged Ethernet frame reaches it's Layer 3 demarcation, traffic is logically separated in the core with MPLS encapsulation/framing or "tag/label switching". Labels are inserted in between the Ethernet header (Layer2) and IP header (Layer3) thus MPLS is often referred to as Layer 2 1/2. A label stack is imposed into the Ethernet frame at the ingress label switch router (LSR). The inner label (e.g. PCI, mc-data, VOIP, campus-data) is preserved throughout the MPLS cloud and while the outer tag is pushed on ingress, swapped traversing the core and both are popped on the egress router. That inner label is the path isolation between two security zone, customers etc.

For a vanilla MPLS configuration in IOS here is a <a href="http://networkstatic.wordpress.com/2012/04/11/basic-mplsvpn-using-cisco-ios/">link</a> .