+++
title = "OTV configuration notes"
date = "2012-02-27T07:22:23+00:00"
lastmod = "2012-09-09T00:16:21+00:00"
author = "Brent Salisbury"
wp_id = 223
categories = ["In the Lab"]
tags = ["Data Centers"]
description = ""
url = "/otv-configuration-notes/"
aliases = ["/2012/02/otv-configuration-notes/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "61123cb5d0ddefa02d26459b877b4a2b0f03413a88f7a522416cae5bbbf084b0"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

Quick notes on OTV. I have not put this on lab gear yet so there may be typos. It does require licensing so make sure you have that budgeted, if not its a 20kish surprise which sucks.

<a href="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/dci1.jpg"><img src="http://184.173.232.53/~bbsali0/wp-content/uploads/2012/05/dci1.jpg" alt="" title="DCI" width="432" height="279" class="aligncenter size-full wp-image-590" /></a>
<pre>#enable the feature&lt;/br&gt;
feature otv&lt;/br&gt;
#create site Vlan&lt;/br&gt;
vlan 200&lt;/br&gt;
name otv-overlay-vlan</pre>
#The Overlay interface ID (int overlay1) must match at both sites. A Vlan can only be assigned to one overlay.
<pre>otv site-identifier 250</pre>
#Join-interface. From what I see this interface has to be physical or a subint on a physical. I would have thought that we could use a loopback or SVI but everything I see has only physical interfaces. I saw mention of loopback support in future SW releases. I would like to have that interface in an MPLS/VPN vrf but need to lab if that is able. If not it would need to route in the IGP.
<pre>int fas 4/1&lt;/br&gt;
desc ovlay-phy-int-to-DCI&lt;/br&gt;
no switch&lt;/br&gt;
mtu 9216&lt;/br&gt;
ip add 192.168.200.1/24&lt;/br&gt;
ip igmp version 3</pre>
#Create the logical Overlay interface. The site identifier needs to be unique per location. If two nodes at one site are in the same DC it should match. Each data center needs to be unique.
<pre>interface Overlay1&lt;/br&gt;
descrip Overlay-virt-interface&lt;/br&gt;
otv control-group 239.1.1.1&lt;/br&gt;
otv data-group 232.1.1.0/28&lt;/br&gt;
otv join-interface ethernet 4/1&lt;/br&gt;
#Extend the Vlan&lt;/br&gt;
otv extend-vlan 50-55</pre>
I will add FHRP once I lab it up. Looks a bit cumbersome with VACLs.