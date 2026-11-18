+++
title = "WireShark Install on Mac OS X"
date = "2012-10-28T07:27:53+00:00"
lastmod = "2013-09-13T16:40:40+00:00"
author = "Brent Salisbury"
wp_id = 3489
categories = ["Tools"]
tags = ["Tutorials", "Wireshark"]
description = ""
url = "/wireshark-install-on-mac-os-x/"
image = "/wp-content/uploads/2012/10/broken.computer.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b2cb6bae98a9ea18f657b9a32ccc3c49ffcade1406ef2d2a059646f040f8fd19"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>WireShark Install on Mac OS X</h2>
Seems like the WireShark install on Mac OS X has always been a total disaster for me. Packet capture utility are vital for developers, network and systems engineers alike. For troubleshooting or supporting SLAs it is often the only tool the defines fact vs. misconception. The WireShark installation process prior to XQuartz was long and convoluted and more often than not would end miserably. For whatever reason the WireShark download site does not list XQuartz the key to end the pain that I saw anywhere.
<h2>WireShark Installation on Mac OSX</h2>
Thanks to XQuartz the Mac install is as easy as installing two applications.

<ol class="legacy-numbers">
<ol>
	<li>Download and install XQuartz from <a href="http://xquartz.macosforge.org/landing/" target="_blank">xquartz.macosforge.org</a>.</li>
	<li>Log out and log back in to restart your X session.</li>
	<li>Download and install WireShark from <a href="http://www.wireshark.org/download.html" target="_blank">wireshark.org</a>.</li>
	<li>Run WireShark.</li>
</ol>
</ol>
<h2>Additional Wireshark Resources</h2>

Gerald touched on the interoperability problems with Mac OS X and it sounded as if there was some issues with libpcap, Mac and Wireshark. Who knows, but that recipe led to plenty of frustration in the community as more of us migrate to Mac's for Unix capability under the hood while still maintaining the corporate application support from business suite applications.

<ul>
	<li>To learn more about Wireshark <a href="http://www.lovemytool.com/blog/sharkfest/" target="_blank">lovemytool.com</a> is probably a good place to start.</li>
	<li>Packet Pushers Podcast <a href="http://packetpushers.net/show-108-wireshark-with-gerald-combs/" target="_blank">Show 108 – Wireshark With Gerald Combs</a></li>
</ul>

<hr>
Thanks for stopping by!