+++
title = "NOX OpenFlow Controller Install on Ubuntu 12.04"
date = "2012-05-31T06:09:09+00:00"
lastmod = "2012-09-09T00:09:56+00:00"
author = "Brent Salisbury"
wp_id = 771
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/nox-openflow-controller-install-on-ubuntu-12-04-precise-lts/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "06753dadac3afc9a342a7e53cfdbf4b535cdd0e8208ae854a8681468aa7dc031"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

http://www.youtube.com/watch?v=RQzFgFjPlD8

Screencast w/o audio. I think it's quick and self explanatory.

This is an install for the newer NOX release on Ubuntu 12.04. I believe the branch name is 'verity'. It was just upped a couple weeks ago to Github with the new repo linked from noxrepo.org. It isn't fully released but the site said Q1 2012, at the least, it will be a base to work from on 12.04. Classic doesn't seem to build without downgrading everything on Precise. The Nox "classic" build seems to have been dormant or not maintained for a while from what I can tell. It is important to have readily available Nox controllers since most of the projects are built on that controller. That said I like Floodlight a lot and the community is active with BidSwitch behind it. Nox has an amazing backing from Nicira so that is critical also.

RouteFlow has support for Nox now which is a project I am going to be in the lab on pretty heavy over the next few days to try and nail down a good native IGP -&gt; SDN FIB exchange. It feels like a route server approach on QUAGGA which is pretty neat. I am assuming it is similar to what I expect Google did in their deployment. There is a NANOG presentation that Scott Whyte described his MPLS LSR which was QUAGGA w/LDP support. <a href="http://www.nanog.org/meetings/nanog50/abstracts.php?pt=MTYzNSZuYW5vZzUw&nm=nanog50">http://goo.gl/hdKC8</a>

If we think about it, the OpenFlow classification of a stitched route through and OF network is not far off from a LSP FEC stitching through a label swapped domain. Instead of swapping labels it is injecting JSON mappings through a REST API and orchestrated from the ingress controller just like an LSR would define the FEC on entry. Ok rambling, but fascinating stuff.

Setup Nox repo for 'nox-dependencies' package
<strong>$ cd /etc/apt/sources.list.d/</strong>
<strong> $ wget http://openflowswitch.org/downloads/debian/nox.list</strong>
<strong> $ apt-get update</strong>
<strong> $ apt-get install nox-dependencies</strong>

Install dependencies:
<strong>$ apt-get install nox-dependencies</strong>
<strong> $ apt-get install libtbb-dev</strong>
<strong> $ apt-get install libboost-serialization-dev libboost-all-dev</strong>
<strong> $ git clone git://github.com/noxrepo/nox</strong>

<strong> $ ./boot.sh</strong>
<strong></strong>$cd nox
<strong> $ mkdir build</strong>
<strong> $ cd build</strong>

Configure, make &amp;&amp; make install
<strong>$ ../configure</strong>
<strong> $ make</strong>
<strong> $ make install</strong>

Verify install:
<strong>$ cd src</strong>
<strong> $ pwd</strong>
/home/brent/nox/build/src (Path)
<strong>$ make check</strong>
<strong>$ ./nox_core -v</strong>
<strong> $ ./nox_core -h</strong>
<strong> $ ./nox_core -i ptcp:6633</strong>
<strong>./nox_core -i ptcp:6633 routing or add a routing module</strong>