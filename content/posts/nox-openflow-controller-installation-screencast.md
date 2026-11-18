+++
title = "NOX OpenFlow Controller Installation Screencast Ubuntu 11.10"
date = "2012-04-22T07:36:55+00:00"
lastmod = "2013-07-30T04:59:24+00:00"
author = "Brent Salisbury"
wp_id = 441
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/nox-openflow-controller-installation-screencast/"
aliases = ["/2012/04/22/nox-openflow-controller-installation-screencast/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8607309c9d131864a22afae9e16fbe63f2b4ae78cace231ab113150deb4d6548"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> NOX OpenFlow Controller Installation Screencast Ubuntu 11.10 </h2>

This post is on the NOX OpenFlow Controller Installation Screencast Ubuntu 11.10. When compiling NOX If you get the error "configure: error: openssl/md5.h not found. NOX requires OpenSSL"

You just need to switch to the 'destiny' branch from the default 'zaku' branch.
<ul>
	<li>Setup dependency repo:</li>
</ul>
<strong>cd /etc/apt/sources.list.d</strong>
<strong> wget http://openflowswitch.org/downloads/debian/nox.list</strong>
<strong>apt-get update</strong>
<strong>cd ~/</strong>&lt;wherever you want to put the src files&gt;
<ul>
	<li>Install dependencies:</li>
</ul>
<strong>apt-get install nox-dependencies</strong>
<strong> apt-get install git</strong>
<strong> git clone git://noxrepo.org/nox</strong>
<strong> cd nox</strong>
<ul>
	<li>Build the App</li>
</ul>
<strong> git checkout -b destiny remotes/origin/destiny  </strong> (&lt;-- If you dont switch branches you will get the MD5 error from the old libraries in the 'zaku' branch)
<strong>cd nox</strong>
<strong> ./boot.sh</strong>
<strong> mkdir build</strong>
<strong> cd build</strong>
<strong> ../configure</strong>
<strong> make</strong>
<strong> cd src/</strong>
<strong> ./nox_core -v</strong>
Now build the next generation network apps and get rich.

http://www.youtube.com/watch?v=CArocYv20W8