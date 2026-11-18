+++
title = "Install WordPress on Ubuntu"
date = "2012-10-24T05:45:02+00:00"
lastmod = "2013-09-08T02:39:21+00:00"
author = "Brent Salisbury"
wp_id = 3355
categories = ["Tools"]
tags = ["Ubuntu", "wordpress"]
description = ""
url = "/install-wordpress-on-ubuntu/"
image = "/wp-content/uploads/2012/10/wordpress-logo.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "a8fbd1f21bc6886c5fb78518c08748b64db94a2af28328d7d2f3ae45c940a3a1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Install WordPress on Ubuntu and Migrate an Existing Site</h2>


Install WordPress on Ubuntu and Migrate an Existing Site: This is a guide on how to install <a href="http://wordpress.org">WordPress</a> on Ubuntu and migrate and existing site to  new host or a test/dev environment. Wordpress is an Open Source free package that started out as a platform for blogging and has since morphed into other more CMS like uses. Their are thousands of plugins that have been written for WordPress for styling and functionality. I like it for  blogging but have done installs for business centric usage for other folks. The simplicity is appealing along with the many tools that lower the barrier to entry into getting content to the customer or reader with little to no development work if setup properly. This post is for folks to get their feet wet or to install a "sandbox" development environment to test new themes, plugins or functionality using Ubuntu as the OS platform.

The first half of the post is just installing a generic WordPress server so if thats all you need that will take care of you. The second half will be exporting data and importing it into the sandbox or new host.

<h2>Installing Wordpress Requirements</h2>


First get a working physical or even easier virtual machine running. You can use VirtualBox for free or some of the commercial desktop/laptop focused <a href="{{< relurl "/nested-kvm-hypervisor-support/" >}}">hypervisors</a> like <a href="http://www.parallels.com">Parallels</a> or <a href="http://www.vmware.com/products/fusion/overview.html">VM Fusion</a>. Then get a working Ubuntu install as shown in this <a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}">how-to</a>.

<h2>Install WordPress from Ubuntu Packages</h2>
As root:
<pre class="brush: bash; gutter: true">apt-get install wordpress libapache2-mod-php5 php5-mysql mysql-server apache2 php5</pre>
Create a symbolic link from the WordPress directory to the default Apache2 directory for serving pages.
<pre class="brush: bash; gutter: true">ln -s /usr/share/wordpress /var/www/wordpress</pre>
Run the included bash script to pre-configure your Wordpress framework. Add the IP you want the service bound to. If you do not want anyone off the box to be able to create a socket to the service you can substitute the IP with localhost.
<pre class="brush: bash; gutter: true">
gunzip /usr/share/doc/wordpress/examples/setup-mysql.gz 
bash /usr/share/doc/wordpress/examples/setup-mysql -n wordpress &lt;Insert IP Here&gt;</pre>
For a dev environment this is acceptable for changing permissions of the WordPress directory.
<pre class="brush: bash; gutter: true">chown -R www-data /usr/share/wordpress</pre>
Restart Apache2 or else you will get PHP module errors.
<pre class="brush: bash; gutter: true">/etc/init.d/apache2 restart</pre>
If not you will get the following error in your browser.
<pre class="brush: bash; gutter: true">Your PHP installation appears to be missing the MySQL extension which is required by WordPress.</pre>
Here is the command line output of the installation at <a href="http://pastebin.com/t9JLxzFS" target="_blank">Pastebin</a>

The WordPress install is complete, now lets configure the WordPress platform.
<h2>Configure WordPress</h2>


<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/torn-install.p_h_p.jpg" >}}"><img class="aligncenter  wp-image-3359" title="wordpress-install.p_h_p" src="{{< relurl "/wp-content/uploads/2012/10/torn-install.p_h_p.jpg" >}}" alt="wordpress-install.p_h_p" width="579" height="455" /></a></p>
<strong>Figure 1.</strong> Point your browser at your ip and the 'wordpress' directory.
<pre class="brush: bash; gutter: true">e.g. http://192.168.1.145/wordpress/</pre>
Setup your site title and username and password, submit and login.

Before we go any further we need to adjust the default 2MB upload limit.

<img style="display: block; margin-left: auto; margin-right: auto;" title="php.ini-upload2.jpg" src="{{< relurl "/wp-content/uploads/2012/10/php.ini-upload21.jpg" >}}" alt="Php ini upload2" width="600" height="270" border="0" />

<strong>Figure 2.</strong> Edit /etc/php5/apache2/php.ini and adjust the upload_max_filesize = to 64M or something around there to avoid memory issues much larger.
<pre class="brush: bash; gutter: true">nano /etc/php5/apache2/php.ini
/etc/init.d/apache2 restart</pre>
Be sure to restart Apache after you edit php.ini . If not you will get the following error in your browser.
<pre class="brush: bash; gutter: true">Your PHP installation appears to be missing the MySQL extension which is required by WordPress.</pre>
Next log into the site and go to Settings -&gt; Media, Change adjust your paths. Store uploads in this folder to -&gt; wp-content/uploads. and clear the path box.

<img style="display: block; margin-left: auto; margin-right: auto;" title="upload-before.jpg" src="{{< relurl "/wp-content/uploads/2012/10/upload-before.jpg" >}}" alt="Upload before" width="549" height="600" border="0" />

<strong>Figure 3.</strong> It will look like this from the install script. Change it from this to look like the next image in figure #4.

<img style="display: block; margin-left: auto; margin-right: auto;" title="upload-after.jpg" src="{{< relurl "/wp-content/uploads/2012/10/upload-after.jpg" >}}" alt="Upload after" width="600" height="195" border="0" />

<strong>Figure 4.</strong> You can blank both boxes or explicitly define them.

<img style="display: block; margin-left: auto; margin-right: auto;" title="import-upload-error.jpg" src="{{< relurl "/wp-content/uploads/2012/10/import-upload-error.jpg" >}}" alt="Import upload error" width="600" height="214" border="0" />

<strong>Figure 5.</strong> If you do not edit your path properly you will get an error such as this. "is parent directory writeable by the server?". aka path not found. For troubleshooting consult the Apache logs as shown below.
<pre class="brush: bash; gutter: true">more /var/log/apache2/access.log
more /var/log/apache2/error.log</pre>
That completes a base installation. Now you can browse Wordpress Themes and Wordpress Plugins from Appearance and Plugins menu in the left bar of your Dashboard. FYI, Dashboard will be your main administrative view into your Wordpress site located in the top left of the menu.

<h2>Migrate an Existing Wordpress Site</h2>


You can do this through a full backup in the Cpanel and download the tarball or FTP to your site and copy down the 'wp-content' directory and everything below it.

Check your wp-config.php and get the credentials you are importingand make sure they are the same as your MySql install or change them to reflect what you used or else you will get MySql connection errors like so:

"Error establishing a database connection wordpress"

<h2>Export Existing WordPress Backup</h2>


<img style="display: block; margin-left: auto; margin-right: auto;" title="export-wordpress-database.jpg" src="{{< relurl "/wp-content/uploads/2012/10/export-wordpress-database.jpg" >}}" alt="Export wordpress database" width="438" height="498" border="0" />

<strong>Figure 6.</strong> Export the WordPress DataBase and choose all content.

Next on your production server or wordpress instance export the database pointers to posts and pages. Do this through wp admin, tools -&gt; export "all content". This will give you an XML export to download.


<h2>Import Existing WordPress Data</h2>

<img style="display: block; margin-left: auto; margin-right: auto; line-height: 16px;" title="import-author2.jpg" src="{{< relurl "/wp-content/uploads/2012/10/import-author2.jpg" >}}" alt="Import author2" width="600" height="413" border="0" />

<strong>Figure 7.</strong> Go to Tools -&gt; Import and import what you just exported Wordpress or Server. Locate and import the XML file containing the WordPress database and choose your username to import it under.

You may need to manually download the WP Import Plugin and pop it in wp-content/plugins and then activate it through settings-&gt;plugins. If you get an error about not being able to write the import set your permisions again with:
<pre class="brush: bash; gutter: true">chown -R www-data /usr/share/wordpress</pre>
navigate to /usr/share/wordpress/ and please make SURE you are on the test box and not your PRODUCTION server! First backup the default directory in case you need to check a vanilla config for refrence or worse accidently delete  your production files. Clear out the /usr/share/wordpress/ directory on the new WordPress host.
<pre class="brush: bash; gutter: true">tar -cvf wp-conf-bk.tar /usr/share/wordpress/
mv wp-conf-bk.tar ~
rm -rf /usr/share/wordpress/*</pre>
Then copy your downloaded full wordpress backup "public_html" containing all the php, wp-admin, wp-content etc into /usr/share/wordpress/ from ftp or through the cpanel from your hosting provider. May need to set permissions one more time after you move the existing content in if so just run 'chown' (change ownership) again.
<pre class="brush: bash; gutter: true">chown -R www-data /usr/share/wordpress</pre>


<h2>WordPress Install and Migration Complete</h2>


You should be good to go now and have a sandbox to test themes, plugins, tweaks etc without destroying your production site. I tend to do all of this in a VMfusion or VirtualBox instance so I can snapshot and rollback and don't have to worry about trashing anything or manually rolling back. VM rollbacks nd snapshots are our friends, especially people like me that needs to break something a few times before putting it together. This takes some trial and error getting used to manipulating WordPress at this invasively, so happy blogging!

Thanks for stopping by and don't wait, get out there and share your ideas and thoughts with the community!