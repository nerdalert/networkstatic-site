+++
title = "Installing NOX OpenFlow Controller on Ubuntu 11.10"
date = "2012-02-01T05:30:03+00:00"
lastmod = "2012-09-09T00:17:17+00:00"
author = "Brent Salisbury"
wp_id = 128
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/installing-nox-openflow-controller-on-ubuntu-11-10/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d4c486990463118ab6a43e2d304a03fae0be893a73f744c89f29892e5eb74580"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<strong>Updated UB 11.10 post <a title="here" href="{{< relurl "/2012/04/22/nox-openflow-controller-installation-screencast/" >}}">here</a></strong>

It is all pretty straight forward except for the default branch is zaku(stable) which has compilation issues. This switches the branch to destiny(unstable).
<strong>$wget http://openflowswitch.org/downloads/debian/binary/nox-dependencies.deb   </strong>

<strong>$dpkg --info nox-dependencies.deb $cd /etc/apt/sources.list.d </strong>
<strong>$sudo wget http://openflowswitch.org/downloads/debian/nox.list </strong>
<strong>$sudo apt-get update $sudo apt-get install nox-dependencies </strong>
<strong>$git clone git://noxrepo.org/nox </strong>
<strong>$cd nox</strong>

Make sure you run the destiny branch from within the Nox directory.
<strong>$git checkout -b destiny remotes/origin/destiny</strong>

To avoid the md5 lib errors I sudoed. The lib was linked but no avail.
<strong>$sudo ./boot.sh
$mkdir build
$cd build
$sudo ../configure --with-boost-filesystem=boost_filesystem --with-boost-unit-test-framework=mt LDFLAGS='-L/usr/include/openssl -lssl -lcrypto'
$sudo make
$cd src</strong>

Verify install with:
<strong>$./nox_core -h</strong>

Some dependencies that may be missed are:
<strong>$sudo apt-get install python-mako python-twisted swig libboost-dev</strong>