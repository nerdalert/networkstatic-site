+++
title = "SDN Use Cases for Service Providers"
date = "2012-11-18T18:34:15+00:00"
lastmod = "2013-04-02T09:07:44+00:00"
author = "Brent Salisbury"
wp_id = 3996
categories = ["Speculative"]
tags = ["Service Provider", "Software Defined Networking"]
description = ""
url = "/sdn-use-cases-for-service-providers/"
image = "/wp-content/uploads/2012/11/telco2.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "61762993607e6329057e25fb8d61e1263adb7c2571426d2ac7abd59cb81c5d52"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>NFV Defines SDN Use Cases for Service Providers</h2>
<span class="drop-cap">T</span>
he service provider community has been active with the research community since the early incubation of software define networking (SDN). Recently, there has been quite a bit of collaborative efforts amongst carrier operators to define SDN use cases for service providers. Currently, there are three Service Provider's on the Open Networking Foundation (ONF) Board today; Deutsche Telekom, Verizon, NTT. Obviously missing there is AT&amp;T, who until recently, had been rather quiet about their plans. They have not been part of the ONF as a member, but appear to be taking a leadership role moving forward. Showing the most public leadership has been Deutsche Telekom (DT) and Verizon. Operators are looking to SDN concepts to increase provisioning agility in revenue generating service and reduce service time to market, capital and operational expenditure spelled out in the NFV vision. The onslaught of exponential growth in connected devices in the order of tens of billions by 2020 leaves them no choice to evolve. The sleeping giants are also eager to take profit from cloud computing and above the net services and why not, the own the last mile which is the lifeline to the cloud. 


<ul>
	<li><em>Deutsche Telekom</em> was an original partner with the Stanford researchers on <a href="{{< relurl "/the-birth-unicorn-early-openflow-meeting-notes/" >}}" target="_blank">OpenFlow</a>.</li>
	<li><em>Verizon</em>, with Stuart Elby out front, has been crystal clear at the Open Networking Summits as to what Verizon's <a href="http://www.youtube.com/watch?v=WVczl03edi4" target="_blank">motivations</a> behind SDN involvement is, reduction of CapEx hardware spending. This is a theme amongst carriers, since a large portion of their hardware spend is networking equipment, as opposed to Hyper-Scale data center that seems to land around <a href="http://perspectives.mvdirona.com/2010/09/18/OverallDataCenterCosts.aspx" target="_blank">10%-20%</a> of overall cost.</li>
</ul>

<blockquote class="pullquote">“You don’t have to have an MBA to realize there is a problem. We are still ok, but not for very long.” <footer>Stuart Selby,Verizon Open Networking Summit Oct, 2011</footer></blockquote>

Carriers provide services, take profit and pay stakeholders, just like networking vendors. All networking hardware venders use commodity silicon to some degrees to reduce manufacturing cost and increase margin. If carriers can extract more profit, from better architectural constructs and operating models, they will. No one owes anyone anything in business from the shareholders perspective.
<hr>
<a href="{{< relurl "/wp-content/uploads/2012/11/NFV_SDN_White_Paper.pdf" >}}" target="_blank" rel="noopener noreferrer">Download the NFV whitepaper</a>Network Functions Virtualisation An Introduction, Benefits, Enablers, Challenges; Call for Action.

<a href="http://www.slideshare.net/bbsali0/nfv-sdn-whitepaper" target="_blank" rel="noopener noreferrer">View it on Slideshare</a>

<h2>My Thoughts</h2>
The SDN use cases the Service Providers laid out  in the NFV document are as ambitious as any other vertical to date. If this heads the route of the <a href="http://www.ietf.org" target="_blank">IETF</a>, which it appears to be, the debate  will be done in public. While many scoff at the standardization bodies ability to execute in a timely fashion, the upside is it gives vendors and consumers the opportunity of to at least know what is going on, if not in the hyper-scale realm.

These carriers are some of the highest volume customers on the planet. I am willing to bet they will not take too much criticism for articulating what they expect as customers. To surmise, vertically integrated monolithic network systems are not in the long term interest of The carrier business models of applications, rather than plumbing. The following will likely generate some product debate.
<blockquote class="pullquote">We believe that Network Appliances which depend on the development of bespoke Application Specific Integrated Circuits (ASICs) will become increasingly uncompetitive against general purpose processors as the cost of developing ASICs increases exponentially with decreasing feature size. Merchant silicon will still be applicable for commodity functions implemented at scale, and ASICs will still be applicable for some types of very high throughput applications.<footer>NFV Whitepaper</footer></blockquote>
The Data Plane being exposed via OpenFlow is specifically referenced. OpenFlow is a mechanism to instantiate packet based forwarding data plane paths into underlying hardware. OpenFlow comes up short in current draft as it is today for Carrier operators. What is missing awareness of the different layers such as Optical Transport Networks (OTN) or WDM Lambdas.

Operators want overlay abstraction, in order to incorporate all layers of their networks rather than just IP and MPLS data planes. Carrier capacity planning and provisioning to be done programmatically will have the ability to stitch cieruits at all layers.
<h2>Example NFV SDN Usage</h2>

<ul>
	<li>An application or domain object is classified based on some parameter(s).</li>
	<li>Path computation takes into account physical, OTN/Lambda, IP topologies and even economic considerations of the topology.</li>
	<li> Iterate that object through organizational policy functions such as SLAs, security, capacity of each layer, economic, business, analytics etc.</li>
	<li>Instantiate the path across all layers, data plane, OTN, MPLS etc.</li>
</ul>
<div></div>
<em></em>
As of <a href="https://www.opennetworking.org/images/stories/downloads/specification/openflow-spec-v1.3.0.pdf" target="_blank">OpenFlow v1.3</a> MPLS was included which is a start at addressing some of those multi-layer needs. Some early concepts of circuit stitching are starting to show up in some projects leveraging northbound APIs.
<blockquote class="pullquote">Finally, the availability of open APIs for management and data plane control, like OpenFlow, OpenStack, OpenNaaS or OGF’s NSI, provide an additional degree of integration of Network Functions Virtualization and cloud infrastructure.<footer>NFV Whitepaper</footer></blockquote>

The NFV vision of SDN appears to be in congruence with the ONF. The ONF is mentioned once in the document.

<blockquote class="pullquote">We intend to work closely with organisations progressing work on SDN such as the Open Networking Foundation (ONF) whose work we will specifically take into account. Network Functions Virtualisation goals can be achieved using non-SDN mechanisms, relying on the techniques currently in use in many data centers. But approaches relying on the separation of the control and data forwarding planes as proposed by SDN can enhance performance, simplify compatibility with existing deployments, and facilitate operation and maintenance procedures. Network Functions Virtualisation is able to support SDN by providing the infrastructure upon which the SDN software can be run. Furthermore, Network Functions Virtualization aligns closely with the SDN objectives to use commodity servers and switches. We intend to work closely with organizations progressing work on SDN such as the Open Networking Foundation (ONF) whose work we will specifically take into account.<footer>NFV Whitepaper</footer></blockquote>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/11/SP-Use-Cases1.jpg" >}}"><img class="aligncenter  wp-image-4008" title="SDN Service Provider Use Cases" src="{{< relurl "/wp-content/uploads/2012/11/SP-Use-Cases1.jpg" >}}" alt="SDN Service Provider Use Cases" width="540" height="441" /></a></p>

<h2 class="legacy-heading">Agile Carrier Services (Warning: Oxymoron)</h2>

Cross platform management coherency and consistency will help Carriers absorb looming exponential wireless growth by scaling operators more efficiently.
<blockquote class="pullquote">Ensuring that virtualised network platforms will be simpler to operate than those that exist today. A significant and topical focus for network operators is simplification of the plethora of complex network platforms and support systems which have evolved over decades of network technology evolution, while maintaining continuity to support important revenue generating services. It is important to avoid trading one set of operational headaches for a different but equally intractable set of operational headaches.<footer>NFV Whitepaper</footer></blockquote>
Extracting the application from the hardware is a reoccurring theme in data center use cases as well. "Above the Net" services are what every carrier is scrambling to put together because the margins are very high compared to just leasing and over subscribing pieces of their infrastructure. Carriers own the last mile. Operators need to be able to provide on demand bandwidth to facilitate elastic brokering of workloads.

Services are software moving forward that can be delivered much quicker than with tightly couple hardware and software. There are about three pages of specific use cases in the document.

Ecosystem is seen as an enabler to faster service delivery. In <em>Figure 2, </em>it explicitly references 3rd party application competition which will drive cost down and churn innovation through horizontalization.

<a href="{{< relurl "/wp-content/uploads/2012/11/ecosystem.jpg" >}}"><img class="aligncenter size-full wp-image-4006" title="ecosystem" src="{{< relurl "/wp-content/uploads/2012/11/ecosystem.jpg" >}}" alt="sdn ecosystem" width="603" height="355" /></a>

Networking has been an outlier marching in place for the past decade or so. Radical change equaled risk few were willing to take. The network is the bus that stitches together resources. Economic pressures are opening minds to change, OpeEx reduction at all cost has become the new norm since 2007.

<blockquote class="pullquote">Network Functions Virtualisation is already occurring. In a few years, we can expect the 
communications industry to look and feel similar to the IT industry. There will be a wider range of 
business models more suited to a software industry. Operations complexity will be abstracted away 
by more automation and self-provisioning will be more common.<footer>NFV Whitepaper</footer></blockquote>The NFV document predicts something similar to the x86 market disruption. Some companies like a DEC, SGI or Wang failed but more companies like IBM transformed (though reluctantly at first) into services oriented revenue. Apple is the prime example of differentiating themselves in software.

Thirty years later, a special purpose built computer from WANG Laboratories for Word Processing sounds a bit silly. Willing to bet, someone did then also.

This is not a bad little document to have on file to hand to someone who dismisses SDN as hype. The people who put together this document outlining expectations and use cases are architectural strategist for multi-billion dollar Service Providers. Point being, this is a long funnel, don't expect products tomorrow, but do expect a first round of primitives in 2013.
<hr />
Thanks for stopping by.
<hr />