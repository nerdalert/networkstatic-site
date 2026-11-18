+++
title = "XRDP Installation: An Easy Remote Desktop Setup for Linux"
date = "2012-08-09T03:19:39+00:00"
lastmod = "2013-12-29T04:20:22+00:00"
author = "Brent Salisbury"
wp_id = 1985
categories = ["Tools"]
tags = ["Tutorials", "linux"]
description = ""
url = "/xrdp-an-easy-remote-desktop-setup-for-your-ubuntu-servers/"
image = "/wp-content/uploads/2012/08/cute-baby-pengions.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "afe7f18c03422f7c149d912680baf2b89c8a583962a0fa7fdb45aebdf6688529"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>XRDP Installation: An Easy Remote Desktop Setup for Linux</h2>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/08/xrdp-logo.jpg" >}}" alt="XRDP for Linux Remote Access"></figure>

XRDP Installation: An Easy Remote Desktop Setup for Linux - Quick tutorial for an installation on Linux (Ubuntu specifically but easily ported) for an easy remote desktop (RDP) setup for Linux. Setting up remote GUI access has always been quite a pain. XRDP is lightweight and really easy to install for a remote administrative GUI desktop. This is a 2 minute setup for a minimal lightdm desktop manager install and setup from a server installed with Ubuntu 12.04 server.

<h2>Installing XRDP for Remote Desktop on Linux</h2>
Here are example installs on Fedora from Red Hat and Ubuntu platforms.

<h2>Remote Desktop for Fedora</h2>

<pre class="code-sample"><code> 
yum install xrdp
systemctl enable xrdp.service
systemctl start xrdp.service
systemctl enable xrdp-sesman.service
systemctl start xrdp-sesman.service

</code></pre>
<h2>Remote Desktop for Ubuntu</h2>

<pre class="code-sample"><code> 
apt-get update
sudo apt-get install ubuntu-desktop --no-install-recommends
sudo apt-get install xrdp

/* 
Check the startup, start if not running 
$ /etc/init.d/xrdp status
 * Checking status of Remote Desktop Protocol server xrdp                                             [ OK ] 
 * Checking status of RDP Session Manager sesman 
*/

/etc/init.d/xrdp start
</code></pre>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/08/xrdp-login-350x178.jpg" >}}" alt="XRDP for Linux Remote Access Installation"></figure>
<strong>Figure 1.</strong> Add your credentials and login.

Point your default installed Remote Desktop Connection application on windows or MAC at the server IP addy and login. Let me know if you have any problems with the installation and I will test it since it is actually an easy remote access setup for a change on Linux. Cheers.
<hr>
Thanks for stopping by. Since we have some cute fuzzy Penguins in the post, check out <a href="http://www.thepetitionsite.com/animal-welfare/" target="_blank">www.thepetitionsite.com </a> and sign a couple of petitions to help out some furry friends. 

Cheers.