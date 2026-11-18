+++
title = "The Good and Bad of Wireless"
date = "2013-03-10T17:52:07+00:00"
lastmod = "2014-02-18T02:57:04+00:00"
author = "Brent Salisbury"
wp_id = 5931
categories = ["Speculative"]
tags = ["Cisco", "Network Field Day", "Wireless"]
description = ""
url = "/the-good-and-bad-of-wireless/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "1aff5e14006a40402ff122a884347c7c99771ff0d74039cc390fd11cb1b0b341"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>The Good and Bad of Wireless</h2>
The Good and Bad of Wireless :A while back, I posted some numbers on campus 802.11 growth. Wether cellular or 802.11, the numbers are big. The numbers show <a href="{{< relurl "/enterprise-802-11-wireless-growth-part-3/" >}}" target="_blank" rel="noopener noreferrer">%1000 annual growth</a>in the 802.11 campus which reflects smart phones, tablets, laptops and soon to be glasses and watches painted all over people. In networking, customer growth typically linearly correlates into the need for more engineers, architects and operators to absorb the growth. When it comes to managing wireless networks, that trend is consistently disproved. That said, all is not rosey in wireless space, there is a major lack of interoperability that needs to be dealt with at some point. Before we dig into the good and bad of wireless, let's level set the framework.
<h2>How is wireless so different?</h2>


<ul>
	<li>Management - Centralized management for provisioning, orchestration and troubleshooting. The driver was RF orchestration.</li>
	<li>Oversubscription and Zero Touch Provisioning - The ability to oversubscribe clients on RF since it is a shared medium can readily absorb growth without the need for new physical elements. New clients do not require slow provisioning cycles, cabling, VIDs etc.</li>
	<li>Policy Application - Bring Your Own Disaster (BYOD) is less then awful in wireless then the wired side. This is enabled because almost all solutions have various centralization techniques that wedge a bump in the forwarding pipeline to apply policy. Reasonable tight control loops in networking only exist in wireless orchestration today.</li>
</ul>

<h2>The Good: Wireless Management</h2>
Early wireless was a monolithic device. All functionality was self contained. Some early startups (particularly Aruba) saw the lack of functionality a completely distributed system presented. The inability to orchestrate RF, made for poor performance on the client side. Centralized controllers often leverage centralized forwarding or centralized forwarding institutions. What this enabled was a rich set of policy application in the security and QoS realm. This does not necessarily mean, tunnel all traffic through a controller or a collection of federated controllers. A TCO including bandwidth availability and component cost, should dictate the levels of centralized forwarding. There are also some emerging technologies that are presumably using a proprietary wire protocol to instantiate forwarding policy while maintaining centralized management and orchestration.
<h2>The Bad: Wireless Management</h2>
While the wireless industry can pat itself on the back for delivering products that are manageable, it represents one of the biggest vendor lock-ins in networking. Since wireless is so proprietary, there are hardly any mechanisms to have rich interoperability between vendor controllers and AP. Proprietary
How would a large campus, hospital or any other enterprise with thousands of contiguous APs that require L3 roaming, RF orchestration, feature parity and all of the other tricks required to have a stable RF environment and an acceptable user experience. I expect those questions are being asked by the wireless community leaders in the industry. If they aren't they should be. I'm willing to bet some of the <a href="http://techfieldday.com/event/wfd4/" target="_blank">Wireless Field Day</a> delegates are all over it. 

<h2>Wireless at Network Field Day #5</h2>

<ul>
	<li>At network field day we had two vendors talk to us about their wireless solutions, Cisco and Ruckus.</li>
</ul>

<h2 class="legacy-heading">The Future is Software</h2>
The 1Q12 market share looked as follows:

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/Wireless-Marketshare.png" >}}" alt="Wireless Market Share"></figure>


In my opinion this is much less pure RF differentiation. Who has a better widget than the next guy is rarely ferreted out in RFPs. At the end of the day, the pieces and parts are commodity. Other then Cisco's dominance in the enterprise the first reason for such disproportionate market share is the vendor lock mentioned earlier, rip and replace at scale is typically a touch TCO. The second reason being, Cisco's tight integration into its NAC product line. Centralized operating systems (even if only the management plane) enable policy. The following silly quadrants, reflect the efforts at vertical integration Cisco does a phenomenal job at selling:

 
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/NAC-Wireless-Magic-Quadrant.png" >}}" alt="NAC Wireless Magic Quadrant"></figure>



<h2>Cisco Wireless</h2>
Cisco discussed their new 3850 platform that contains an embedded wireless controller into the new <a href="http://www.cisco.com/en/US/products/hw/wireless/index.html" target="_blank">Catalyst 3850</a> product. Where the wired ports fit into this strategy was slightly unclear. There should be ubiquity between managing wired and wireless. Ideally all of the wireless controller libraries will be rolled into the <a href="{{< relurl "/more-details-about-the-cisco-one-controller-announced/" >}}" target="_blank">Cisco ONE</a> controller. A ubiquitous management environment between the wired and wireless network for Cisco would be a big win for them in the enterprise. The Catalyst 3750-X seems to have disappeared from future software support for emerging products. Seems anything other than bug fixes is about all the product development that platform will be seeing anymore. If you are buying Catalyst 3750-X switches today and are committed to buying Cisco products, it would probably be wise to opt for the Catalyst 3850 so you can actually get support for onePK to have future investment protection. There are a few features at L3 that are not available yet like GRE tunneling, v6 multicast NBAR I am happy to see embedded systems going into edge equipment. The edge is the future core in an SDN driven network.


<ul>
	<li>The overall architecture for a branch and campus looks like so:</li>
</ul>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/Cisco-Prime-Wireless.png" >}}" alt="Cisco Wireless"></figure>
<h2>Cisco Catalyst 3850 Converged Access Switch Overview</h2>

<p><a href="http://vimeo.com/61490430">Watch video on Vimeo</a></p>

<h2>Cisco Wireless Demo</h2>


<p><a href="http://vimeo.com/61490416">Watch video on Vimeo</a></p>

<h2>Ruckus Wireless</h2>
<a href="http://www.ruckuswireless.com" target="_blank">Ruckus</a> gave a nice presentation with lots of RF fundamentals that was a great refresher for me. I like having content like this on hand to shoot to someone like an intern or junior engineer to get them up to speed. Education beyond just products is the mark of vendors with solid products. Post IPO, Ruckus seems to be in a good place and there is certainly plenty of room in the wireless space for disruption. Here is an overview of their campus strategy.


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/03/Ruckus-wireless-enterprise.png" >}}" alt="Ruckus Enterprise"></figure>


<h2>Ruckus Refresher on Wireless</h2>

<p><a href="http://vimeo.com/61490413">Watch video on Vimeo</a></p>

<h2>Ruckus Wireless Places 802.11ac in the History of Wi-Fi</h2>


<p><a href="http://vimeo.com/61490411">Watch video on Vimeo</a></p>

Thanks to my friends Network Field Day and the vendors for sharing with the community. It takes vendors with strong products to step in front of the Field Day delegates for the smell test. To see the rest of the videos stop by the <a href="http://techfieldday.com/event/nfd5/" target="_blank" rel="noopener noreferrer">Network Field Day #5 website.</a>

<h2>For good or bad, wireless is the future last mile</h2>
Vertically integrated markets are sustainable for only so long. At some point horizontalization becomes important for innovation. Wireless is the future edge. The majority of wired national broadband infrastructures are too weak to keep up with exponential growth. Carriers are unwilling to invest the CapEx required to support a robust national broadband. For better or worse, good or bad, the cost avoidance of wireless last mile oversubscription is a much better business case than wired. Thus the need for a healthy competitive market. Companies like Cisco and Ruckus are both important to that future horizontal ecosystem. 
<hr>
If you don't have any significant market share in wireless, which is basically almost everyone, visit an ODM in SE Asia, grab an OpenFlow controller, use the vendor extension OFPP_Vendor_Extensions to augment southbound OpenFlow and get to it.

<hr>
<pre class="brush: bash; gutter: true; first-line: 1; highlight: []; html-script: false">struct ofp_action_vendor_header {  /* OFPAT_VENDOR. */
    uint16_t type;  		/* Length is 8. */
    uint16_t len;		/* Vendor ID, which takes the same form
    uint32_t vendor;		   as in &quot;struct ofp_vendor&quot;. */
};</pre>
<hr>
<a href="{{< relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" >}}" target="_blank" rel="noopener noreferrer">Download OpenFlow v1.3</a>

<hr>
While on this topic of wireless inerop or lack thereof, <a href="http://blog.fosketts.net" target="_blank">Stephen Foskett</a> mentioned a presentation from <a href="http://techfieldday.com/event/wfd3/" target="_blank">Wireless Field Day #3</a> that is exploiting APIs to try and interoperate multiple vendors APs. Worth a look.
<p><a href="http://vimeo.com/50076741">Watch video on Vimeo</a></p>
<hr>
Thanks for stopping by