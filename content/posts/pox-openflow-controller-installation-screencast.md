+++
title = "POX Openflow Controller Installation Screencast"
date = "2012-04-22T07:30:54+00:00"
lastmod = "2013-04-01T02:42:46+00:00"
author = "Brent Salisbury"
wp_id = 432
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/pox-openflow-controller-installation-screencast/"
image = "/wp-content/uploads/2012/04/pox.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "d47b6374b97eb8c1a48d21b6a527cc8bf145cc149909bc349e3cdddc9c0fdada"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>POX Openflow Controller Installation Screencast</h2>
POX Openflow Controller Installation: POX is a lightweight OpenFlow controller that is written completely in Python that is targeted for developers to spin up their own controllers. The nice thing about POX is if you want an OF controller spun up in as fast as you can type git clone etc, you got it.

It supports the same tools that NOX does but you dont have the C++ compilation dependencies that without maintenance get stale quickly as libraries evolve.
<h2>Install The POX OpenFlow Controller</h2>
<em>Installation:</em>
<a href="https://github.com/noxrepo/pox/downloads">https://github.com/noxrepo/pox/downloads</a>
Or clone from GitHub, even easier!
<pre class="brush: text; gutter: false">sudo apt-get install git
 git clone http://github.com/noxrepo/pox
 cd pox
 ./pox.py openflow.of_01 --address=&lt;your ip&gt; --port=6633</pre>
<span style="color: #0000ff;">NOX&gt; Yay!</span>
<a href="https://github.com/noxrepo/pox/downloads">https://github.com/noxrepo/pox/downloads</a>

You have an OF controller running now ready to be attached to!
That said I haven’t tried this with real gear.The README looks like anything Openflow v1.0 is fair game though.
<h2>POX Openflow Controller Installation Video</h2>
<div><p><a href="http://www.youtube.com/watch?v=CArocYv20W8">Watch video on YouTube</a></p></div>

<blockquote class="pullquote"><a href="http://www.noxrepo.org/2012/05/381/#more-381" target="_blank" rel="noopener noreferrer">NoxRepo.org</a> Brent Salisbury, the author of the Network Static blog recently posted a YouTube video showing how to get POX up and running on Ubuntu. I wanted to give out a shout of thanks for that, and throw in another little tip or two.I think people who aren't at all familiar with git and the command line will find the blog post and videoparticularly useful.One thing I'll point out is that this isn't even as easy as it could be! If you want to avoid using git, you can just download a tarball or zipball. And you only need to specify arguments to the of_01 module (which handles communication with OpenFlow 1.0 switches) if you don't like the defaults, which are to listen to connections on all interfaces at port 6633 (equivalent to putting openflow.of_01 --address=0.0.0.0 --port=6633 on the command line).<footer>Murphy McCauley</footer></blockquote>

Thanks Murphy, keep up the great work!
<hr>
More OpenFlow Tutorials:
 <a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank" rel="noopener noreferrer">OpenFlow and OpenvSwitch Tutorial </a>
 <a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank" rel="noopener noreferrer">OpenFlow, OpenvSwitch and KVM SDN Lab Installation App </a>

Thanks for stopping by.