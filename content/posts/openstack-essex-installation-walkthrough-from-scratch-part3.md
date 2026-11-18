+++
title = "OpenStack Essex Installation Walkthrough from Scratch (Part3)"
date = "2012-05-12T06:21:55+00:00"
lastmod = "2012-09-09T00:12:15+00:00"
author = "Brent Salisbury"
wp_id = 539
categories = ["In the Lab"]
tags = ["OpenStack", "Tutorials"]
description = ""
url = "/openstack-essex-installation-walkthrough-from-scratch-part3/"
aliases = ["/2012/05/12/openstack-essex-installation-walkthrough-from-scratch-part3/"]
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "860b5ac2c1ec196610943b8462f941e2c28a9958ac78068c83fb6584f28a31af"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

http://www.youtube.com/watch?v=zdswg5Lj-Hc&amp;hd=1
<h2>Dashboard Installation</h2>
/*Install packages
<strong>$apt-get install libapache2-mod-wsgi openstack-dashboard</strong>

/*Restart Apache
<strong>$restart apache</strong>
<strong> $service apache2 restart</strong>

/*Connect to the Dashboard web page.
<strong>http://localhost or http://x.x.x.x</strong>

So easy a caveman (me) can do it. Not really it is a pain to get it working smoothly but mainly for me was lack of good directions and learning the pieces and parts to something a vast as this project.

For troubleshooting refer to the troubleshooting this <a href="{{< relurl "/2012/05/12/troubleshooting-common-openstack-errors/" >}}">post</a>.
See a post for how to operate Dashboard visit <a href="{{< relurl "/2012/05/09/openstack-essex-operational-demo/" >}}" target="_blank">here.</a>