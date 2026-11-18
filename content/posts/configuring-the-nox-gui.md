+++
title = "Configuring the NOX GUI"
date = "2012-04-24T04:07:11+00:00"
lastmod = "2013-07-30T05:13:16+00:00"
author = "Brent Salisbury"
wp_id = 497
categories = ["In the Lab"]
tags = ["OpenFlow", "Software Defined Networking", "Tutorials"]
description = ""
url = "/configuring-the-nox-gui/"
image = "/wp-content/uploads/2012/04/nox.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3ca0cccb4808229587eb3267faa8c1a463d46f7b9d3f8176a297d595748a6b96"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2 class="legacy-heading">Configuring the NOX GUI</h2>

<aside class="legacy-callout"><strong>Configuring the NOX GUI Update: </strong>The NOX libraries are not maintained for most distros at the moment. Everything has been stripped out of NOX except for the core implementation as a C++ base for development.  I <strong>recommend</strong> trying either <a href="{{< relurl "/floodlight-openflow-controller-screencast-with-hp-switches/" >}}">FloodLight</a> or <a href="{{< relurl "/pox-openflow-controller-installation-screencast/" >}}">POX</a>.</aside>

<h2>Configuring the NOX GUI</h2>
To install NOX Destiny branch refer to this <a href="{{< relurl "/2012/04/22/nox-openflow-controller-installation-screencast/" >}}" target="_blank">post</a>.

To get the little test web page going run the following on startup.
<pre>./nox_core -v dummywebpage
then go to in a web browser http://localhost</pre>
To run the NOX GUI you can do the following. I am showing the errors you get if you don't have the Python GUI classes loaded.
<h2>Start the NOX GUI</h2>
Start NOX with the 'monitoring' argument passed.
<pre class="brush: bash; gutter: true">~/nox/build/src# ./nox_core monitoring
NOX 0.9.1~full~beta (nox_core), compiled Apr 22 2012 02:15:38
Compiled with OpenFlow 0x01</pre>
Then find the GUI Py script.
<pre class="brush: bash; gutter: true">cd &lt;path&gt;/nox/src
root@ub-11:/home/brent/nox/src# ls
builtin gui lib Makefile.in nox nox_main.cc 
tests etc include Makefile.am Make.vars 
nox-gui.py scripts utilities</pre>
Run the NOX GUI errors should be expected if you do not have the right Python GUI modules.
<pre class="brush: bash; gutter: true">root@ub-11:/home/brent/nox/src# ./nox-gui.py
Traceback (most recent call last):
File &quot;./nox-gui.py&quot;, line 18, in &lt;module&gt;
from PyQt4 import QtGui, QtCore
ImportError: No module named PyQt4</pre>
To fix that error grab a couple packages.
<pre class="brush: bash; gutter: true">#apt-get install pyqt4-dev-tools 
python-qt4 python-simplejson python-qt4-sq</pre>
Then run the Python script again and you will get a GUI pop up for you.
<pre class="brush: bash; gutter: true">/nox/src# ./nox-gui.py</pre>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/04/gui.jpg" >}}"><img class="size-full wp-image-498 aligncenter" title="NOX GUI" src="{{< relurl "/wp-content/uploads/2012/04/gui.jpg" >}}" alt="" width="621" height="400" /></a></p>
<p style="text-align: left;">A good beginning tutorial if you dont have any hardware to attach to a controller is over at the <a href="http://www.openflow.org/wk/index.php/OpenFlow_Tutorial" target="_blank">OpenFlow wiki</a>. Another option a bit more advanced without gear is installing <a href="http://openvswitch.org/" target="_blank">OpenvSwitch</a> and attaching it to the controller.</p>
<p style="text-align: left;">Here is one I put together with some different <a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}">combinations</a>.</p>

<h5></h5>