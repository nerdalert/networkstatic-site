+++
title = "Django Installation and First App Tutorial"
date = "2012-09-15T08:03:29+00:00"
lastmod = "2013-03-27T02:02:11+00:00"
author = "Brent Salisbury"
wp_id = 2695
categories = ["Programming"]
tags = ["Programming", "Python", "Tutorials", "django"]
description = ""
url = "/django-installation-and-first-app-tutorial/"
image = "/wp-content/uploads/2012/09/python.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "b94587a3b3d66d7c14250d82f9938d1cb03f3654a56bbae4a3d84bf5aea83bc3"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Django Installation and First App Tutorial </h2>


<strong>Django Installation and First App Tutorial:</strong> Django is a powerful web framework written in Python used to create pluggable database driven websites that are complex, but simplified by the abstraction of the Django framework. I am using Ubuntu for this install but beyond it will work for most OS's. I will configure Django to use sqlite as a database. It can easily be swapped to use <a href="http://postgresql.org" target="_blank">PostgreSQL</a>, <a href="http://www.mysql.com/" target="_blank">MySql</a>, <a href="http://www.sqlite.org/" target="_blank">Sqlite</a> or an <a href="http://www.oracle.com/technetwork/indexes/downloads/index.html" target="_blank">Oracle</a> database. The installation is pretty simple, getting to know the configuration files and framework is quite a bit more complicated depending on how much experience with Python and web development you have. For that reason, this is a super simple tutorial to break someone in to how Django operates.

For a quick review of Python a couple of tutorials can be found <a href="{{< relurl "/tag/python/" >}}" target="_blank">here.</a> This tutorial has lots of pictures and makes the default polls tutorial a little easier to follow, theoretically :). One other reason to learn the Django framework is <a href="{{< relurl "/quantum-openstack-python-installer/" >}}" target="_blank">OpenStack</a> uses it for Dashboard so it might help for editing templates or custom scripting.
<h2>Django Installation Tutorial</h2>
We will use Pip for the installation. Pip is a package management system used to install and manage software packages. Pip is platform agnostic just as Python itself. It is a replacement/wrapper for easy_install.
<pre class="brush: bash; gutter: true">$ apt-get install git python-pip python-dev build-essential sqlite3 python-sqlite
 $ sudo pip install Django</pre>
That put files into the /usr/local/lib/python2.7/dist-packages/django/ directory.
<h2>First Django Project</h2>
We will create out first project with the 'django-admin.py startproject' command. Get to know Django admin with
<pre class="brush: bash; gutter: false">&#039;django-admin.py --help&#039;.
 $ cd /home/
 $ django-admin.py startproject firstsite
 $ cd /home/brent/firstsite/firstsite
 $ ls #These are your site files.
 Now configure the Django settings.py file. That is the main configuration file for projects. First we will add the Sqlite database.
 $ nano /home/brent/firstsite/firstsite/settings.py</pre>
from:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">DATABASES = {
    &#039;default&#039;: {
        &#039;ENGINE&#039;: &#039;django.db.backends.&#039;, # Add &#039;postgresql_psycopg2&#039;, &#039;mysql&#039;, &#039;sqlite3$
        &#039;NAME&#039;: &#039;&#039;,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        &#039;USER&#039;: &#039;&#039;,
        &#039;PASSWORD&#039;: &#039;&#039;,
        &#039;HOST&#039;: &#039;&#039;,                      # Empty for localhost through domain sockets o$
        &#039;PORT&#039;: &#039;&#039;,                      # Set to empty string for default.</pre>
To:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">DATABASES = {
    &#039;default&#039;: {
        &#039;ENGINE&#039;: &#039;django.db.backends.sqlite3&#039;, # Add &#039;postgresql_psycopg2&#039;, &#039;mysql&#039;, &#039;$
        &#039;NAME&#039;: &#039;firstProject.db&#039;,                      # Or path to database file if u$
        # The following settings are not used with sqlite3:
        &#039;USER&#039;: &#039;&#039;,
        &#039;PASSWORD&#039;: &#039;&#039;,
        &#039;HOST&#039;: &#039;&#039;,                      # Empty for localhost through domain sockets o$
        &#039;PORT&#039;: &#039;&#039;,                      # Set to empty string for default.</pre>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/settings.py_.db_.django.jpg" >}}"><img class="aligncenter  wp-image-2698" title="settings.py.db.django" src="{{< relurl "/wp-content/uploads/2012/09/settings.py_.db_.django.jpg" >}}" alt="settings.py django python" width="554" height="77" /></a>
<strong>Figure 1</strong>. settings.py should look like this.
$ cd /home/brent/firstsite
Synchronize the manage.db Sqlite database file. *Note, manage.py is in the root of the site directory not in the project directory.
$ python manage.py syncdb</p>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/synch.db_.django.super_.user_.jpg" >}}"><img class="aligncenter  wp-image-2697" title="synch.db.django.super.user" src="{{< relurl "/wp-content/uploads/2012/09/synch.db_.django.super_.user_.jpg" >}}" alt="django root account password" width="590" height="281" /></a>
<strong>Figure 2</strong>. You will asked some questions to setup an account and password at this point.
Look in the directory now, you should see firstsite.db for the sqlite database</p>

<pre class="brush: text; gutter: false; first-line: 1; highlight: []; html-script: false">$ ls
firstsite firstsite.db manage.py</pre>
<h4>Start the Django Development Server</h4>
<p style="text-align: left;">Let's start the barebones Django framework.
Run this to start the server on all interfaces on TCP port 8000:</p>

<pre class="brush: bash; gutter: true">$ python manage.py runserver 0.0.0.0:8000
 Validating models...
 0 errors found
 September 11, 2012 - 00:09:12
 Django version 1.5.dev20120910173111, using settings &#039;firstProject.settings&#039;
 Development server is running at http://0.0.0.0:8000/
 Quit the server with CONTROL-C.</pre>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/django.manage.project.settings.jpg" >}}"><img class="aligncenter  wp-image-2699" title="django.manage.project.settings" src="{{< relurl "/wp-content/uploads/2012/09/django.manage.project.settings.jpg" >}}" alt="python manage.py runserver 0.0.0.0" width="591" height="112" /></a> <strong></strong></p>
<p style="text-align: left;"><strong>Figure 3</strong>. Server will look like this on startup on the CLI.
Test the default page in a browser at http://Host IP:8000
Ctrl+C to stop the server</p>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/default.django.web_.jpg" >}}"><img class="aligncenter  wp-image-2696" title="default.django.web" src="{{< relurl "/wp-content/uploads/2012/09/default.django.web_.jpg" >}}" alt="default django website" width="574" height="163" /></a>
<strong>Figure 4.</strong> The default page will look something like this.</p>

<h4>Enable the Django Admin Control Panel</h4>
The admin site is not active by default. We already edited settings.py to enable the admin panel in that file. Now we need to edit urls.py in your project folder and uncomment three lines. These are the mappings to project pages. Since these sites are dynamically created there isn't a htdocs like file.
Edit settings.py
$ nano cd /home/brent/firstsite/firstsite/settings.py
Edit settings.py from:
Under installed Apps list:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">INSTALLED_APPS = (
    &#039;django.contrib.auth&#039;,
    &#039;django.contrib.contenttypes&#039;,
    &#039;django.contrib.sessions&#039;,
    &#039;django.contrib.sites&#039;,
    &#039;django.contrib.messages&#039;,
    &#039;django.contrib.staticfiles&#039;,
    # Uncomment the next line to enable the admin:
    # &#039;django.contrib.admin&#039;, &lt;--- Uncomment
    # Uncomment the next line to enable admin documentation:
    # &#039;django.contrib.admindocs&#039;,
)</pre>
To the following Uncomment 'django.contrib.admin',:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">INSTALLED_APPS = (
    &#039;django.contrib.auth&#039;,
    &#039;django.contrib.contenttypes&#039;,
    &#039;django.contrib.sessions&#039;,
    &#039;django.contrib.sites&#039;,
    &#039;django.contrib.messages&#039;,
    &#039;django.contrib.staticfiles&#039;,
    # Uncomment the next line to enable the admin:
    &#039;django.contrib.admin&#039;,
    # Uncomment the next line to enable admin documentation:
    # &#039;django.contrib.admindocs&#039;,</pre>
<a href="{{< relurl "/wp-content/uploads/2012/09/django.polls_.app_.jpg" >}}"><img class="aligncenter size-full wp-image-2700" title="django.polls.app" src="{{< relurl "/wp-content/uploads/2012/09/django.polls_.app_.jpg" >}}" alt="django app" width="554" height="245" /></a>
<strong>Figure 5.</strong> settings.py should look like this.
<h4>URLS.py</h4>
Next we need to enable Django to answer the url.py to answer for the /admin/ directory. urls.py uses regular expressions to match URL calls. For a tutorial on regular expressions click <a href="http://docs.python.org/howto/regex.html" target="_blank">here</a>. We will also add a regular expression to match the site of the App we will be creating 'polls.views.index' to setup the default index view for the App "polls".
<pre class="brush: text; gutter: false">$ nano cd /home/brent/firstsite/firstproject/urls.py</pre>
Edit From:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns(&#039;&#039;,
    # Examples:
    # url(r&#039;^$&#039;, &#039;firstsite.views.home&#039;, name=&#039;home&#039;),
    # url(r&#039;^firstsite/&#039;, include(&#039;firstsite.foo.urls&#039;)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r&#039;^admin/doc/&#039;, include(&#039;django.contrib.admindocs.urls&#039;)),

    # Uncomment the next line to enable the admin:
    # url(r&#039;^admin/&#039;, include(admin.site.urls)),
)</pre>
In the following, uncomment three lines and it to:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns(&#039;&#039;,
    # Examples:
    # url(r&#039;^$&#039;, &#039;firstsite.views.home&#039;, name=&#039;home&#039;),
    # url(r&#039;^firstsite/&#039;, include(&#039;firstsite.foo.urls&#039;)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r&#039;^admin/doc/&#039;, include(&#039;django.contrib.admindocs.urls&#039;)),

    # Uncomment the next line to enable the admin:
    url(r&#039;^admin/&#039;, include(admin.site.urls)),
    url(r&#039;^polls/$&#039;, &#039;polls.views.index&#039;),
)</pre>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/django.urls_.py_.jpg" >}}"><img class="aligncenter  wp-image-2701" title="django.urls.py" src="{{< relurl "/wp-content/uploads/2012/09/django.urls_.py_.jpg" >}}" alt="django urls.py" width="591" height="299" /></a>
<strong>Figure 6.</strong> urls.py will look like this.</p>

<h2>Create Your First Django App</h2>
Create an App named "polls". This is part of the modularity of Django since the App is decoupled from the web framework. A more advanced approach would be to create a urls.py file in your App directory instead of using the sites urls.py. For now we will keep it simple.
<pre class="brush: bash; gutter: true">$ cd /home/brent/firstproject
 $ python manage.py startapp polls
 $ nano /home/brent/firstproject/firstproject/settings.py</pre>
Change From:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">INSTALLED_APPS = (
    &#039;django.contrib.auth&#039;,
    &#039;django.contrib.contenttypes&#039;,
    &#039;django.contrib.sessions&#039;,
    &#039;django.contrib.sites&#039;,
    &#039;django.contrib.messages&#039;,
    &#039;django.contrib.staticfiles&#039;,
    # Uncomment the next line to enable the admin:
    &#039;django.contrib.admin&#039;,
    # Uncomment the next line to enable admin documentation:
    # &#039;django.contrib.admindocs&#039;,
)</pre>
To:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">INSTALLED_APPS = (
    &#039;django.contrib.auth&#039;,
    &#039;django.contrib.contenttypes&#039;,
    &#039;django.contrib.sessions&#039;,
    &#039;django.contrib.sites&#039;,
    &#039;django.contrib.messages&#039;,
    &#039;django.contrib.staticfiles&#039;,
    # Uncomment the next line to enable the admin:
    &#039;django.contrib.admin&#039;,
    # Uncomment the next line to enable admin documentation:
    # &#039;django.contrib.admindocs&#039;,
    &#039;polls&#039;,
)</pre>
<a href="{{< relurl "/wp-content/uploads/2012/09/django.polls_.app_1.jpg" >}}"><img class="aligncenter size-full wp-image-2702" title="django.polls.app" src="{{< relurl "/wp-content/uploads/2012/09/django.polls_.app_1.jpg" >}}" alt="django app" width="554" height="245" /></a>
<strong>Figure 7.</strong> Add your polls App into settings.py
<h4>Edit models.py</h4>
$ nano /home/brent/firstproject/polls/models.py
Change /home/brent/firstproject/polls/models.py
From:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.db import models
# Create your models here.</pre>
To:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.db import models
# Create your models here.

class Poll(models.Model):
    print(&#039;These are your classes as you start building real apps&#039;)</pre>
<a href="{{< relurl "/wp-content/uploads/2012/09/mode.py_.django.jpg" >}}"><img class="aligncenter size-full wp-image-2703" title="mode.py.django" src="{{< relurl "/wp-content/uploads/2012/09/mode.py_.django.jpg" >}}" alt="models.py django" width="345" height="129" /></a>
<strong>Figures 8.</strong> models.py will look like this.
<h4>Add the App to the Admin Control Panel in admin.py</h4>
Create admin.py in the polls directory
$ nano /home/brent/firstproject/polls/admin.py
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.contrib import admin
from polls.models import Poll

admin.site.register(Poll)</pre>
<a href="{{< relurl "/wp-content/uploads/2012/09/django.admin_.py_.jpg" >}}"><img class="aligncenter size-full wp-image-2704" title="django.admin.py" src="{{< relurl "/wp-content/uploads/2012/09/django.admin_.py_.jpg" >}}" alt="django admin.py" width="376" height="88" /></a>
<strong>Figure 9.</strong> The admin.py file
<h4>Views.py</h4>
The last configuration is to edit view.py. That is the view you will see in that directory that is called from urls.py.
$ nano /home/brent/firstproject/polls/views.py
# Create your views here.
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">from django.http import HttpResponse

def index(request):
    return HttpResponse(&quot;Hello, world from the polls App! L33t&quot;)</pre>
<p style="text-align: left;"><a href="{{< relurl "/wp-content/uploads/2012/09/django.hello_.world_.views_.py_.jpg" >}}"><img class="aligncenter  wp-image-2706" title="django.hello.world.views.py" src="{{< relurl "/wp-content/uploads/2012/09/django.hello_.world_.views_.py_.jpg" >}}" alt="" width="543" height="109" /></a>
<strong>Figure 10.</strong> views.py will look like this.</p>
<p style="text-align: left;">Sync the DB and start the development server.</p>

<pre class="brush: bash; gutter: true">$ python manage.py syncdb
 $ python manage.py runserver 0.0.0.0:8000
 Point your web browser at the Django /admin/ directory.
 http://IP of Host:8000/admin/</pre>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/django.admin_.console.jpg" >}}"><img class="aligncenter  wp-image-2710" title="django.admin.console" src="{{< relurl "/wp-content/uploads/2012/09/django.admin_.console.jpg" >}}" alt="django admin control panel app" width="583" height="241" /></a></p>
<strong>Figure 11.</strong> The admin control panel looks like this with your app in there.

Now point your web browser at the polls directory. http://host ip:8000/polls/

<a href="{{< relurl "/wp-content/uploads/2012/09/django.hello_.world_.jpg" >}}"><img class="aligncenter size-full wp-image-2707" title="django.hello.world" src="{{< relurl "/wp-content/uploads/2012/09/django.hello_.world_.jpg" >}}" alt="" width="380" height="156" /></a> <strong>Figure 12.</strong> You should see your first ub3r l33t App!
<h2>Tutorials</h2>
This tutorial is barely touching the surface. There are tons of them at the following links.

Tutorials: <a href="https://code.djangoproject.com/wiki/Tutorials" target="_blank">https://code.djangoproject.com/wiki/Tutorials</a>
Installation Guide and the Complete Polls tutorial to actually do something: <a href="https://docs.djangoproject.com/en/dev/intro/install/" target="_blank">https://docs.djangoproject.com/en/dev/intro/install/</a>

Hope this helps a couple folks cause I have spent some frustrating times learning the bits and pieces I know now of the framework here and there :) Happy Hacking!