+++
title = "New IETF SDN Drafts"
date = "2012-07-06T06:34:44+00:00"
lastmod = "2012-12-31T04:26:56+00:00"
author = "Brent Salisbury"
wp_id = 1538
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking", "ietf"]
description = ""
url = "/new-ietf-sdn-drafts/"
image = "/wp-content/uploads/2012/07/parliament2.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "090ceeb9560fa7e52cb00807692ede514b29c4618721e550fae72d5dde8aab1e"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>New IETF SDN Drafts</h2>
New IETF SDN Drafts: A Service Provider SDN IETF Draft: There are four new drafts submitted to the IETF in the past few days. These are all informational drafts and a "work in progress" for the 6 month period after submission. It would be reasonable to expect vendors to seek some disruption to be triggered by having multiple standards bodies get involved to have favorable standards fall in their direction. The most recent split is  TRILL and SPB, between the IEEE and IETF slowed that process to a snails pace. IETF, the ONF and the RETF are all either doing or beginning the process of weighing in on standards. Each have unique properties, for example the ONF (Open Networking Foundation) does not have any networking device vendors on it's voting board. Regardless of where these standards and definitions come from the results need to remain open in as many sense of the word possible for the industry to take a run at some efficient and smart abstraction.

<ol class="legacy-numbers">
<h2>Cisco, MPLS and OpenFlow: Defense or Offense?</h2>
<ol>
	<li>This was submitted by Jan Medved of Cisco who is the chair of the ONF Hybrid Working Group.</li>
	<li>The management (northbound) application is the UI from which the operator will provision the pseudowire circuit.</li>
	<li>The draft does not include how the other than a traditional push and pop of the transport label on ingress and egress from the LSP.</li>
	<li>There is an OAM engine on the head and tail of the circuit. The tail engine detects the failure while the headend provisions the failover over LSP.</li>
	<li>The OpenFlow switch has one dedicated flow table and one dedicated table-group table. The table-group table is typically thought to be used for OAM, BFD, bcast and mcast.</li>
	<li>The OF switch has to support matching on input port and the label stack mpls label and bottom of stack label.</li>
</ol>
</ol>
<h2>Use Cases for ALTO with SDN (Huawei and Telefonica)</h2>
Application-Layer Traffic Optimization (ALTO) is the marrying application awareness and the underlying substrate which is one of the primary use cases of SDN in NSPs and CDNs. This reads like a nortbound application that will orchestrate controller domains with coarse aggregate data through extensions. A signaling protocol is not identified in the draft. That signalling would be the Northbound controller interaction to the ALTO server. Some use cases and dependencies for path selection identified are QOS metrics, Bandwidth on Demand, bandwidth availability, delay, CDN ranking and cost maps. I love the idea of working in a brokerage of transport costs in maybe even creating a bandwidth commodities market.
<h2>SDNi: A Message Exchange Protocol for SDN (Huawei and Telefonica)</h2>
SDNi is a protocol proposed for the interface between Software Defined Networking (SDN) domains. An SDN domain has been shaping up to be an SDN subset of the overall network that is made up of a collection of SDN domains. It is probably similar to the reasons we carve failure domains today along with an natural migration path potentially from existing to SDN. OpenFlow or is a north-south transaction from OF enabled hardware making up the data plane(encompassing forwarding) to the controller containing the decoupled control plane. SDNi is an east-west protocol that interconnects controller and the exchange reach ability information.

A single flow can be extended across SDN domains with one controller lookup. This would de-duplicate multiple policy (firewall, PBR, load balancing etc) classification as a flow traverses multiple SDN domains. Sounds an awful lot like an label switch path (LSP) forwarding equivalency class (FEC) on ingress into an label edge router (LER) MPLS domain and choose a path if multiple paths exist. Ok that was too many acronyms. It references that reachability (hosts maybe even presumably even mac) could be exchanged with BGP or SIP over SCTP extensions. It explicitly states that it is to exchange information under the same operator implying it is out of scope to be AS-to-AS peering. This was submitted by Huawei and Telefonica.
<h2>MPLS-TP PseudoWire Configuration using OpenFlow 1.3</h2>
The proposal draft-medved-pwe3-of-config-00 titled MPLS-TP PseudoWire Configuration using OpenFlow submitted by Cisco describes a method by which MPLS-TP Pseudowires (PW) can be configured using OpenFlow 1.3. In addition to the provisioning of the PWs this document also specifies how to enact OAM for these PWs using standard IETF conventions defined by the GAL label method. The primary goal of this document is to show a simple and yet flexible method using tools from the emerging SDN toolkit as opposed to a vendor driven provisioning system.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/mpls-tp2.jpg" >}}" alt="OpenFlow and MPLS"></figure>

<strong>Figure 1.</strong> MPLS-TP SDN Reference Topology

Pseudowires are configured from a network / provisioning Management Application that communicates with MPLS-TP nodes through an OpenFlow Controller (OF Controller). The Management Application configures an end-to-end Pseudo-wire ([PW1]) between Attachment Circuit [AC1] on the headend node and Attachment Circuit [AC2] on the tail-end node. At the head-end, all traffic coming from an input port (Attachment Circuit [AC1]) is switched onto the PW, and at the tail-end all traffic coming from the Pseudo-wire is switched to an output port (Attachment Circuit [AC2]). The Pseudo-wire is assigned a PW Label [PWL1]. The Management Application configures both packet forwarding and OAM function related to pseudowires.

Link to <a href="http://tools.ietf.org/html/draft-medved-pwe3-of-config-00" target="_blank">draft</a>

<hr />

<h2 class="legacy-heading">SDNi: A Message Exchange Protocol in Software Defined Networks for Inter-Domain Exchanges</h2>

The draft draft-yin-sdn-sdni-00.txt proposes a protocol SDNi for the interface between Software Defined Networking (SDN) domains to exchange information between the domain SDN Controllers. It defines the concept of a SDN domain; its need, what are its components and how SDNi helps in inter domain communication.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/SDNi1.jpg" >}}" alt="SDN and SDNi for Service Providers ALTO"></figure>

<strong>Figure 2.</strong> There was no reference to proprietary protocols in the draft but there is above.
<blockquote class="pullquote">SDNi protocol should be able too Coordinate flow setup originated by applications, containing information such as path requirement, QoS, SLA etc. across multiple SDN domains. To Exchange reachability information to facilitate inter-SDN routing. This will allow a single flow to traverse multiple SDNs and have each controller select the most appropriate path when multiple such paths are available. SDNi depends on the types of available resources and capabilities available and managed by the different controllers in each domain. Hence it is important to implement SDNi in a descriptive and open manner so that new capabilities offered by different types of controllers will be supported. Since SDN in essence allows for innovation, it is important that data exchanged between controllers will be dynamic in nature, i.e. there should be some meta-data exchange that will allow SDNi to exchange information about unknown capabilities.</blockquote>

Link to <a href="http://tools.ietf.org/html/draft-yin-sdn-sdni-00" target="_blank">draft</a>

<hr />

<h2 class="legacy-heading">Use Cases for ALTO with Software Defined Networks</h2>

Arguably ALTO in its form today, is an early primitive method of programmatically determining the best path to be chosen based on business algorithms. Applying SDN concepts to ALTO should be like injecting steroids into the process by exposing programable interfaces to assist with determining the best computational path elements (CPE) to use. The draft draft-xie-alto-sdn-use-cases-01.txt the Vertical Architecture and the Horizontal Architecture allowing coherent coexistence of application layer traffic optimization (ALTO) with software defined network (SDN). Unique requirements for design and operations are identified and summarized, suggesting that the Vertical Architecture allows better division, management, flexibility, privacy control and long-term evolution of the network. We also define the main interactions and information flows, and present a set of use cases to illustrate how we extend ALTO to support SDN, in the Vertical Architecture.
<figure class="legacy-figure">ttp://networkstatic.net/wp-content/uploads/2012/07/Alto.jpg</figure>
<strong>Figure 3.</strong> Vertical Architecture, the primary focus of the draft.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/07/Horizontal-alto.jpg" >}}" alt="SDN and SDNi for Service Providers ALTO Orchestration"></figure>
<strong>Figure 4</strong>. Horizontal Architecture.

The ALTO server covers a carrier's network as a whole; however, if the carrier divide the network into multiple SDN domains, each SDN domain covers only a segment of the network. Additionally, the ALTO server has only relatively coarse-grained information, while SDN domain controllers could easily collect more fine-grained information. More importantly, different SDN domains may implement different information aggregation and privacy policies (e.g., when such domains are dedicated to certain customers of the carrier).

These observations suggest that the Vertical Architecture is advantageous over the Horizontal Architecture. With the Vertical Architecture, SDN and ALTO are explicitly separated and as a result the logic is cleaner and this allows them to evolve independently. Furthermore, the Vertical Architecture makes automated information collect possible for ALTO, which could make ALTO deployment and management easier and more attractive. Therefore, in the remainder of this draft, we mainly focus on the Vertical Architecture. We will describe the interactions and the information flows in further details for the vertical architecture

Link to <a href="http://tools.ietf.org/html/draft-xie-alto-sdn-use-cases-01" target="_blank">draft</a>

<hr />

Thanks for stopping by.

<hr />