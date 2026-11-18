+++
title = "The MPLS and transport roles merge"
date = "2011-10-10T02:17:03+00:00"
lastmod = "2012-06-16T22:24:38+00:00"
author = "Brent Salisbury"
wp_id = 30
categories = ["Speculative"]
tags = ["MPLS", "OpenFlow", "Software Defined Networking", "predictions"]
description = ""
url = "/the-new-mpls-and-transport-roles-merge/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d3775738a28a0f05cc607133653d146a9ef59b3062df374645509424d7a149a9"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

The Juniper PTX in 2011 was a pretty bold merge of the OTN and MPLS functionality into one box.  They are marketing it as the "Converged Supercore" <a href="http://www.juniper.net/as/en/dm/supercore/">http://www.juniper.net/as/en/dm/supercore/</a>. As the debate of packet vs. circuit switched networks has clearly been won by the packet side of the house. Arguably the the increasing demands of service provider bandwidth for triple play and cloud services and need for rapid provisioning of customer and provider needs that packet switched networks provide. We can now virtually provision circuit services via MPLS-TP/PBB-TE and reduce cost.

Why buy routers as a P node when really all you need is an LSR switch? The cost of a layer3 decision is a pricey option to scales one core. The PTX box has a roadmap as a full functional ROADM box. It seems this box could be a logical choice to help migrate or maintain a circuit switched network while migrating to a packet switched network. The cost should be reduced in the core by eliminating the need to provision layer3 services by only switching and pushing the routing decisions to the edge. Operationally it may be that the transport OTN engineers may also pickup LSR switching.