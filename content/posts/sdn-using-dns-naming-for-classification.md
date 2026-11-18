+++
title = "SDN Using DNS Naming for Classification"
date = "2012-10-16T06:51:21+00:00"
lastmod = "2012-11-27T07:40:43+00:00"
author = "Brent Salisbury"
wp_id = 3082
categories = ["Programming"]
tags = ["OpenFlow", "Software Defined Networking", "dns"]
description = ""
url = "/sdn-using-dns-naming-for-classification/"
image = "/wp-content/uploads/2012/10/Internet-Change.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d157f995ef6011a77d3a9d4164df1ec71710ef28c049125151da70aa786f93ec"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

SDN Using DNS Naming for Classification Update: First, a Refresher. The initial project was outlined <a href="{{< relurl "/sdn-using-names/" >}}" target="_blank">here</a>
<h4>Abstract</h4>
Current generation networks are under scrutiny for not presenting the proper amount of flexibility at scale to accomplish technical and business objectives. At the core of the problem are the constraints imposed by the network revolving around the inflexible nature of IP addressing being so tightly coupled to geography. Traffic classification and policy application has been far too entwined with IP prefixes rather than providing any abstractions to extract flexibility while still maintaining the scalability that is required in networks that require constant availability with ability to absorb exponential growth. This project proposes using canonical naming structures and mapping them to policy classification and policy application.

In order to apply this concept the underpinning network is assumed to support basic flow based forwarding leveraging a wire protocol such as OpenFlow. Basic forwarding primitives are required in order to instantiate proper forwarding with applied policy instructions. Using naming conventions for IP mapping and compute classification has been used by applications for decades. The same naming construct in the network as objects and leveraging network elements that are, name to policy mappings aware will insert a layer of abstraction. This framework could reduce operational complexity while increasing provisioning overhead and begin to create networks that are taxonomically application aware.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/Required.v1.3.Openflow.Feilds.jpg" >}}"><img class="aligncenter  wp-image-3087" title="Required.v1.3.Openflow.Feilds" src="{{< relurl "/wp-content/uploads/2012/10/Required.v1.3.Openflow.Feilds.jpg" >}}" alt="Required.v1.3.Openflow.Feilds" width="540" height="220" /></a></p>
<em><strong>Figure 1.</strong></em> Minium required support for headers in OpenFlow <a href="https://www.opennetworking.org/images/stories/downloads/specification/openflow-spec-v1.3.0.pdf" target="_blank">v1.3 spec</a>. Those headers capture anything that is a Layer-2-4 device such as switches, routers, firewalls and load balancers (minus packet inspection) to name a few.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/sdn.paths_.jpg" >}}"><img class="aligncenter size-full wp-image-3204" title="sdn.paths" src="{{< relurl "/wp-content/uploads/2012/10/sdn.paths_.jpg" >}}" alt="sdn.paths" width="387" height="337" /></a></p>
<em><strong>Figure 2.</strong></em> Conceptual Quite Simple.
<h4>Two Quick Example SDN Naming Use Cases</h4>
<strong><em>Use Case #1: Traffic Engineering</em></strong> - Mapping any portion of the Fully Qualified Domain Name (FQDN) or combinations thereof to the forwarding paths in the network elements would abstract the strict nature of being confined to IP prefixes in order to participate in colored path classifications. The name to policy conventions could even theoretically be exchanged between two autonomous entities and overcome administrative boundary limitations.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/TE-OpenFlow-Names-border1.jpg" >}}"><img class="size-full wp-image-3113 aligncenter" title="TE-OpenFlow-DNS" src="{{< relurl "/wp-content/uploads/2012/10/TE-OpenFlow-Names-border1.jpg" >}}" alt="TE-OpenFlow-DNS" width="497" height="651" /></a></p>
<strong><em>Figure 3.</em></strong> Mapping for any host *.<span style="color: #ff0000;">erp.foo</span>.* (host1.erp.foo.org) -&gt; gold traffic path with the highest priority, bandwidth etc. host2.<span style="color: #ff0000;">foo</span>.org -&gt; silver traffic policy with lower priority since it is a less critical application than the gold path policy. Foo has to be checked to be in the proper field in this case domain name since a host could have a hostname of foo and match improperly. Programmatically that is easily solved by extracting the ArrayList&lt;E&gt; with this snippet for those who have contacted me about this project (int size = ListArray.length); and then subtracting top levels.

<strong><em>Use Case #2: Security Policy</em> </strong>- A major pain point in todays data centers and enterprises is security classification. Mapping DNS naming to polict would simplify the inefficient processes of workflow from Systems to Security to Network to get resources in place and provisioned. Again this is agnostic to the network IP addressing since the interesting fields being matched upon in the FQDN determine policy mapping.

<a href="{{< relurl "/wp-content/uploads/2012/10/Sec-Policy-SDN-Naming-border.jpg" >}}"><img class="aligncenter size-full wp-image-3085" title="Sec-Policy-SDN-Naming-border" src="{{< relurl "/wp-content/uploads/2012/10/Sec-Policy-SDN-Naming-border.jpg" >}}" alt="Sec-Policy-SDN-Naming-border" width="506" height="649" /></a>

<strong><em>Figure 4.</em></strong> Mappings for any host (denoted with the * wildcard "match anything" or "don't care" bit) *<span style="color: #ff0000;">.erp.foo</span>.org -&gt; Security policy with highest restriction (and any other resource, IDS, Flow Monitoring etc). Mappings for any host with *.<span style="color: #ff0000;">foo</span>.org -&gt; Security policy with lower restrictions.
<h4>Back to the IDE</h4>
The use case list could go on for miles which is reflective of the enormous amount of flexibility combining programmatic abstractions and networking elements acting as hardware rather than distributed mainframes. Back to the IDE, I will update algorithms later as we work through the logic of storing and updating the key/value mappings. After that we will start looking to the <a href="http://floodlight.openflowhub.org" target="_blank">FloodLight-Dev</a> group for the best method of integration into our fork to get closer to a demo in coming weeks.