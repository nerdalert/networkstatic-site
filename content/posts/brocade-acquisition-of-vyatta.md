+++
title = "Brocade Acquisition of Vyatta"
date = "2012-11-06T06:14:16+00:00"
lastmod = "2012-11-27T06:56:28+00:00"
author = "Brent Salisbury"
wp_id = 3720
categories = ["Speculative"]
tags = ["Brocade", "Vyatta"]
description = ""
url = "/brocade-acquisition-of-vyatta/"
image = "/wp-content/uploads/2012/11/vyatta-logo.crop_.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3c9aadc7e2e115fa9b601e14331cdd7335c3a55389f53dd42baa9de8d4757518"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

The Brocade acquisition of Vyatta was announced today. On the surface Vyatta is functionality we have in today's routers to load in VMs or on physical gear as a software router. It is complete with IGPs, EGPs, QOS, PBR, Crypto (no MPLS) and about everything else you find in a traditional router. Vyatta is not a vSwitch, it is routing functionality in x86. While being delivered in software ,almost everything I see is leveraging our existing bag of networking protocols and encapsulations to integrate into the network along with service provisioning in an on demand fashion. They do mention the ability to accommodate OpenFlow. I would imagine as aggressive as <a href="http://www.brocade.com/index.page" target="_blank">Brocade</a> is on SDN that will be in the works day one, if it is not already in the pipeline.

I snipped some pictures from there documents and grabbed some highlights that might save someone some research time. Think, routers in x86 and how you can use that to manage VM L3 traffic with PBR, QOS and whatever else programmatically in the near term. In the long term sprinkle in whatever mechanism (if) the industry decides to use as its wire protocol for control plane extraction, e.g. OpenFlow, MPLS etc.

<em>Per the Vyatta website is a snippet of how they see SDNs role:</em>

Software-Defined Networking (SDN) allows you to design, provision and scale Layer 2 (L2) networks to meet rapidly changing business needs. Vyatta’s virtual routers, virtual firewalls and VPNs enable you to connect the L2 SDN “islands” to each other, as well as the broader infrastructure.
<h2>Vyatta for Virtualized Environments</h2>
Vyatta supports the following hypervisors VMware, Citrix Xen and XenServer and Red Hat KVM. This means they deliver their software images that can run as a VM or on physical host. This does not mean they have a vSwitch product. These are x86 routers. The vSwitch integration will come from Open vSwitch, VMware vSwitch (presumably also OVS based) and RedHat if they would ever make a vSwitch. Guessing the 1000v is out oO
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/11/remember-when.jpg" >}}"><img class="aligncenter  wp-image-3723" title="remember-when" src="{{< relurl "/wp-content/uploads/2012/11/remember-when.jpg" >}}" alt="vyatta networks" width="467" height="254" /></a></p>
<strong>Figure 1.</strong> I freely admit, I loved this graphic on the homepage of their site.

<a href="{{< relurl "/wp-content/uploads/2012/11/virt.jpg" >}}"><img class="aligncenter size-full wp-image-3724" title="virt" src="{{< relurl "/wp-content/uploads/2012/11/virt.jpg" >}}" alt="vyatta" width="332" height="457" /></a>

<strong>Figure 2</strong>. Heavy emphasis on networking services such as load balancing and firewalling.

<strong>Vyatta Network OS Highlights</strong>
<ul>
	<li>Advanced IPv4 and IPv6 routing (BGP Multipath, PBR, OSPF)</li>
	<li>Stateful firewall</li>
	<li>IPv6 compatible</li>
	<li>Linux-based extensible network OS</li>
	<li>IPSec &amp; SSL-based OpenVPN</li>
	<li>Secure Web filtering</li>
	<li>VMware, Hyper-V, Xen/XenServer, Red Hat KVM Ready</li>
	<li>Restful API, CLI, Web GUI</li>
</ul>
&nbsp;
<h2>Vyatta for x86 Servers</h2>
The roots of Vyatta are from a project called XORP (for eXtensible Open Router Platform) a routing engine developed on Debian and  funded by Intel and the National Science Foundation (<a href="http://www.nsf.gov" target="_blank">NSF</a>) in 2002. At its roots it is software routing on x86 hardware. They refer to this architecture as vPlane.

<a href="{{< relurl "/wp-content/uploads/2012/11/virt-data-model-vyatta.jpg" >}}"><img class="aligncenter size-full wp-image-3725" title="virt-data-model-vyatta" src="{{< relurl "/wp-content/uploads/2012/11/virt-data-model-vyatta.jpg" >}}" alt="virt-data-model-vyatta" width="412" height="203" /></a>

<strong>Figure 3.</strong> This looks like some familiar SDN territory, layers, abstraction, APIs, decoupling etc.

From the <a href="http://www.vyatta.com/files/pdfs/vyatta_vplane_faq.pdf" target="_blank">FAQ</a>:
<blockquote>Vyatta vPlaneTM is a distributed Layer 3 (L3) forwarding plane that is architecturally separate from Vyatta’s network controller. The vPlane technology runs on individual x86 cores and takes advantage of the latest Intel advances related to networking performance. With this architectural separation, vPlane will allow Vyatta to deliver an order of magnitude faster forwarding performance that can scale linearly with the number of available x86 cores.</blockquote>
Here are the features of vPlane. Notice the caveat of "small packet sizes" that is significant.
<ul>
	<li>Near line-­‐rate 10Gb/s throughput at small packet sizes to leverage the new era of 10Gb/s servers</li>
	<li>Physical de-­‐coupling of forwarding plane from control plane</li>
	<li>Full interoperability with existing network infrastructure</li>
	<li>Ability to accommodate new protocols such as OpenFlow</li>
</ul>
<div>

Here is a snippet of what the configuration looks like. It is the C bracketed look of JunOS.
<pre class="brush: text; gutter: true">vyatta@R2# show interfaces wireless wireless wlan0 {
    address dhcp
    security {
       wpa {
          passphrase &quot;Test phrase&quot;
     } 
   }
ssid Test
  type station
 }</pre>
There is also quite a bit of reference material for data center interconnects.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/11/vyatta-dci.jpg" >}}"><img class="aligncenter  wp-image-3727" title="vyatta-dci" src="{{< relurl "/wp-content/uploads/2012/11/vyatta-dci.jpg" >}}" alt="vyatta-dci" width="494" height="274" /></a></p>
<strong>Figure 4</strong>. The DCI from one colo to another. Dell was referenced quite a bit as a user, would allude to some courtship there if I were to guess.

</div>
<h2>Vyatta for Amazon</h2>
Brocade recently demoed OpenStack <a href="http://wiki.openstack.org/Quantum" target="_blank">Quantum</a> integration recently at Network Field Day #4 which can be viewed <a href="http://techfieldday.com/video/brocade-openstack-demo/" target="_blank">here</a>. I would take a guess that a long term strategy will be to get the same level of integration they have in the Amazon Cloud into OpenStack. I could see some use cases for hybrid cloud needs for advanced networking such as tunneling and crypto where having a software interface capable of tunneling could be handy. That said I can do that with OVS as I have done in a post a while back with the HP Public Cloud <a href="{{< relurl "/public-cloud-network-as-a-service/" >}}" target="_blank">here</a>.
<p style="text-align: center;"> <a href="{{< relurl "/wp-content/uploads/2012/11/aws.jpg" >}}"><img class="aligncenter  wp-image-3726" title="aws" src="{{< relurl "/wp-content/uploads/2012/11/aws.jpg" >}}" alt="pub cloud vyatta" width="497" height="279" /></a></p>
 <strong>Figure 5. </strong>How this solution integrates into the public cloud.

The true integration into the hypervisor means having primitives into the vSwitch on the hypervisor.  They will need to rely on partners for that outside of the open source realm.
<h3>My Two Pennies on Vyatta</h3>
What Vyatta represents to me is using x86 hardware in as a swiss army knife to networking. Today if you need load balancing you buy a load balancer, if you need security you buy a firewall, if you need, well you get the point. Provisioning services until recently meant hoping the budget can absorb the purpose built hardware you are going to need. There are certainly benefits of custom and commodity ASICs, NPU, TCAM etc, but it comes at a cost and with constraints. That said am I staking my mortgage payment on x86 networking today? Eh, but in the coming years as software and reference architectures continue to mature I think x86 networking on the edge has a place. Applications controlling the network will become much more interesting in coming years as scalable solutions are worked through, <a href="{{< relurl "/the-potential-impact-of-software-defined-networking-sdn-on-security/" >}}" target="_blank">security</a> is beginning to become an early such play because to date, most solutions are either cost prohibitive network wide or are hacked together by really smart ITSec folks.

If you look at many shipping products today, especially in security or services routers markets, those are silicon with loads of embedded cores. Chip makers are beginning to deliver processors optimized for L7 payload inspection. The ability to RegEx and presumably re.sub() without the traditional performance penalty is becoming realistic. The Broadcom <a href="http://www.broadcom.com/press/release.php?id=s710289" target="_blank">XLP 200-Series </a>Multicore Communications Processor line demonstrates the vendor demand from foundries for application awareness.

Probably the most interesting dynamic is between VMware, Cisco and Brocade with this acquisition. I didn't even know about the CSR and was quite peeved at that, until Network Field Day #4 in October that I was honored to be a part of which can be viewed <a href="http://techfieldday.com/appearance/cisco-presents-at-networking-field-day-4/" target="_blank">here</a>.

Greg Ferro already captured some of the impact (which I highly recommend reading) that filled in many blanks for me in a post at <a href="http://www.networkcomputing.com/next-gen-network-tech-center/brocade-gets-virtual-networking-with-vya/240044437" target="_blank">NetworkComputing</a>. Prior to the acquisition they were certainly looking to cut into Cisco margins based on this <a href="http://www.vyatta.com/sites/vyatta.com/files/pdfs/Vyatta_Cisco_Replacement_Guide_0.pdf" target="_blank">document</a>. I doubt Brocade bought Vyatta to cannibalize their own hardware sales so my guess is the idea of replacing enterprise routers and firewalls will fade, but hey there are significantly higher margins from software sales. Kudos for Brocade not un-publishing all of the documents on the Vyadda website so a nerd like me who needs a new hobby can read up.

All in all, I think the acquisition complements Brocade's existing data center fabric products and their bullish approach to OpenFlow support in their hardware.

<strong>Vyatta references for this article:</strong>

<a href="http://www.cloud-distribution.com/_CDL/files/vyatta_amazon_datasheet.pdf" target="_blank">Control Security, Connectivity and Compliance in the Amazon Cloud</a>

<a href="ftp://ftp.cfar.umd.edu/.snapshot/hourly.2/pub/mvanopst/reader-sync/vyatta/Vyatta-HA_R6.4_v01.pdf" target="_blank">Vyatta System High Availability Reference Guide</a>
<div>

<a href="http://www.vyatta.com/downloads/documentation/VC6.3/Vyatta_LANInterfaces_R6.3_v01.pdf" target="_blank">Vyatta System LAN Interfaces Reference Guide</a>

<a href="http://www.vyatta.com/product/vyatta-network-os/overview" target="_blank">Vyatta Network OS Overview</a>

<a href="http://www.vyatta.com/sites/vyatta.com/files/pdfs/Vyatta_Bostoncolo_case.pdf" target="_blank">Case Study: BostonColocation</a>

<a href="http://www.dabcc.com/documentlibrary/file/Vyatta_app_virt.pdf" target="_blank">Network Virtualization</a>

</div>
P.S. Can someone get the word "Virtualized" added to the universal keeper of spell checkers?

Thanks for stopping by!