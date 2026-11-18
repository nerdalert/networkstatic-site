+++
title = "Juniper Default Routing Tables"
date = "2012-04-15T19:38:53+00:00"
lastmod = "2013-07-30T04:58:32+00:00"
author = "Brent Salisbury"
wp_id = 360
categories = ["Study Time"]
tags = ["Tutorials"]
description = ""
url = "/juniper-default-routing-tables/"
image = "/wp-content/uploads/2012/04/juniper_01.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cb5afc1ae251279b8239465fc841d2133973aaff197a63dfe45ea09c1f4472e1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Juniper Default Routing Tables </h2>

The first time I saw these I remember thinking what is going on here. It can be pretty foreign the first time someone sees it especially coming from Cisco IOS. The two CLIs wrap and abstract the underlying standardized frameworks pretty differently. I think it helps to decouple what the function of the table is before ever operating the gear. I tended to start banging away on the gear and wind up with holes since I didn’t breakdown the architectural pieces first. It would have saved many days of back tracking if I had started with a clear breakdown of the tables and still does to this day :)
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/inet-tables.jpg" >}}"><img class="size-full wp-image-361 aligncenter" title="Juniper inet tables" src="{{< relurl "/wp-content/uploads/2012/04/inet-tables.jpg" >}}" alt="" width="500" height="566" /></a></p>
JUNOS maintains various tables routing tables. Most are default names that cannot be changed except for routing-instance prepends e.g. &lt;routing-instance-name&gt;.inet.0. I threw together some examples of what the output looks like. Despite our mix of bizarre APIs in networking, the fundamentals are the same though out. Control, Data and Management Planes.

Below are examples of the CLI output from some of these tables from a Juniper MX960.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/i2-inet01.jpg" >}}"><img class="size-full wp-image-373 aligncenter" title="i2-inet0" src="{{< relurl "/wp-content/uploads/2012/04/i2-inet01.jpg" >}}" alt="" width="500" height="416" /></a></p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/mpls-0.jpg" >}}"><img class="size-full wp-image-372 aligncenter" title="mpls.0" src="{{< relurl "/wp-content/uploads/2012/04/mpls-0.jpg" >}}" alt="" width="500" height="599" /></a><a href="{{< relurl "/wp-content/uploads/2012/04/l2vpn-inet.jpg" >}}"><img class="size-full wp-image-371 aligncenter" title="l2vpn.inet" src="{{< relurl "/wp-content/uploads/2012/04/l2vpn-inet.jpg" >}}" alt="" width="500" height="254" /></a></p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/inet0.jpg" >}}"><img class="size-full wp-image-362 aligncenter" title="inet0" src="{{< relurl "/wp-content/uploads/2012/04/inet0.jpg" >}}" alt="" width="500" height="517" /></a></p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/inet32.jpg" >}}"><img class="size-full wp-image-370 aligncenter" title="inet3" src="{{< relurl "/wp-content/uploads/2012/04/inet32.jpg" >}}" alt="" width="500" height="233" /></a></p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/bgp-l3vpn1.jpg" >}}"><img class="size-full wp-image-366 aligncenter" title="bgp-l3vpn" src="{{< relurl "/wp-content/uploads/2012/04/bgp-l3vpn1.jpg" >}}" alt="" width="500" height="410" /></a></p>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/bgp-l3vpn2.jpg" >}}"><img class="size-full wp-image-368 aligncenter" title="bgp.l3vpn" src="{{< relurl "/wp-content/uploads/2012/04/bgp-l3vpn2.jpg" >}}" alt="" width="500" height="362" /></a></p>