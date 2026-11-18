+++
title = "Big Switch Introduces Switch Light"
date = "2013-03-26T12:18:50+00:00"
lastmod = "2014-02-18T02:57:08+00:00"
author = "Brent Salisbury"
wp_id = 6095
categories = ["Speculative"]
tags = ["OpenFlow", "Software Defined Networking"]
description = ""
url = "/big-switch-introduces-switch-light/"
image = "/wp-content/uploads/2013/03/whitebox.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "7c1410e25aa7c87a0997663fe6c94bb30d73f16fa5c81242217fce691d2095d1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Big Switch Introduces Switch Light</h2>
Big Switch took a step towards rounding out their portfolio with introducing plans to release a software switching software to integrate into <a href="https://nerdtwilight.wordpress.com/category/odms/" target="_blank">ODM</a> (Original Design Manufacturer) and vendor hardware switches. The “thin switching” software is made up using the FOSS (Free and Open Source Software) Indigo project from Stanford University and Project <a href="http://www.projectfloodlight.org" target="_blank">Floodlight</a>. Just as various vendors have used <a href="http://openvswitch.org" target="_blank">Open vSwitch</a> as their early OpenFlow agent, so have other vendors used Indigo.

<h2 class="legacy-heading">OpenFlow Enablement for More Switching Platforms</h2>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/Big-Light-Architecture1.png" >}}" alt="Big Light SDN OpenFlow"></figure>

Big Switch will provide a forwarding driver to the ODM to place above the Broadcom ASIC firmware that will provide hooks into the ODM hardware. There is also support for Open vSwitch that will be open sourced. That would be to presumably get more specific features from OVS then would be available from the project.

<h2>The Monolith vs Horizontalization</h2>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/SDN-New-v-Old.png" >}}" alt="Big Light SDN OpenFlow"></figure>

Big Switch and SDN proponents believe the days of the mainframe era are at an end, more people are tending to agree. 

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/monolith-sdn-comparison1.png" >}}" alt="SDN Evolution"></figure>


<h2>Management Protocols</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/SDN-Management.png" >}}" alt="Big Light SDN OpenFlow"></figure>

There are CLI and Web management interfaces for Indigo. The early release does not support OF-Control (OpenFlow provisioning component) but does support some management protocols.
<h2>OpenFlow Whitebox Hardware</h2>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/SDN-ODM1-650x282.png" >}}" alt="OpenFlow Whitebox ODM"></figure>

Whitebox hardware is used by hyper-scale content providers like Facebook. This has implications if it begins to happen in networking. The forwarding driver is built to work with the Broadcom <a href="http://www.broadcom.com/products/Switching/Carrier-and-Service-Provider/BCM56840-Series" target="_blank">StrataXGS</a> chips, but no mention of any particulars in that family. No mention of the heralded TridentII chip that is still in "sampling" nine months after announcement.



<h2>Switch Light Availability</h2>
The source code for Switch Light is available at <a href="http://projectfloodlight.org" target="_blank">projectfloodlight.org</a>. The commercial offering is in early access with beta in June and GA second half 2013. The first hardware switch supporting the forwarding layer is the <a href="http://www.quantaqct.com/en/01_product/01_list.php?mid=30&sid=114">Quanta LB9 (T1048-LB9)</a> with 48x 1GigE south and 4x 10GigE north.

<h2>My Thoughts</h2>

Big Switch has suffered in the past by being beholden to both software and hardware that is out of their control. While they are still constrained by off the shelf ASIC limitations with regard to OpenFlow, they are in a much better place to add features and functionality in hardware as desired. Revenue from software and services for BigSwitch and partnerships with resellers and ODMs make this very interesting. While BigSwitch has missed an opportunity here or there in hindsight, this is the best move they have made yet.

A viable alternative vSwitch and more OpenFlow enabled hardware will quicken the pace of OpenFlow and SDN proofs and production deployments. The Whitebox CapEx reduction is attractive to many that do not require white glove services. If looking for significant macro trends, this is merely another step towards following in trace of the computing market and technological evolutions. Networking is starting to pickup steam and is barreling through the 1980's somewhere between the i486 micro-processor and Microsoft Office being released.

Big Switch has been the leading OpenFlow evangelist, both in thought and action. The days of sizing a piece of hardware to solve all problems does not have another decade left in the tank. Big Switch is still acutely focused on the data center and they are not alone in that since almost every other vendor is also. The <a href="http://etherealmind.com/sdn-use-case-firewall-migration-in-the-enterprise/" target="_blank">Enterprise</a>, Data Center and <a href="{{< relurl "/sdn-use-cases-for-service-providers/" >}}" target="_blank">Service Provider</a> are still wide open at this point. We will be watching for early adopters and deploying our own <a href="{{< relurl "/openflow-sdn-hybrid-deployment-strategies/" >}}" target="_blank">SDN architectures</a> in the meantime. 
