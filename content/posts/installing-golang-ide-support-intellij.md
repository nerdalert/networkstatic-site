+++
title = "Installing Golang IDE Support in Intellij"
date = "2015-02-08T23:03:39+00:00"
lastmod = "2015-05-24T11:40:12+00:00"
author = "Brent Salisbury"
wp_id = 7478
categories = ["Programming"]
tags = ["Go", "IDE", "Intellij"]
description = ""
url = "/installing-golang-ide-support-intellij/"
image = "/wp-content/uploads/2015/02/Docker-Gopher-Banner.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "cac3d355a37af7ac49c6b0ca44d15d5d7231bd038fe2ebecfcd3df54e84a3929"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2> Installing Golang IDE Support in Intellij </h2>

I have always preferred Intellij Community Edition IDE for Java, Bash, Python, Node and anything else I have needed, including recently <a href="https://www.jetbrains.com/clion/" target="_blank">C/C++</a> which is pretty slick. The plus is I can hang on to key-mappings, syntax color and general workflow all in a ubiquitous dev environment. There are some good IDE <a href="https://github.com/golang/go/wiki/IDEsAndTextEditorPlugins" target="_blank">options</a> for Go and of course support for the staunch EMACS/VIM purist. I like the background support an IDE offers but to each their own. There is a nice community driven project for an Intellij <a href="https://github.com/go-lang-plugin-org/go-lang-idea-plugin" target="_blank">Golang plugin</a> hosted on github. It is a Java project that is very active. At any time you can go to Intellij Prefrences -&gt; Plugins -&gt; search for 'golang'. 

<h2> Golang IDE Intellij Plugin Nightly Build </h2>

<aside class="legacy-callout"><strong>Update go-lang-idea-plugin 1.0.0.alpha</strong>Update: you the plugin is now integrated into the Jetbrains plugin CI for nightly builds. If you are only interested in getting the latest nightly or versioned release you can add the Jetbrains "Custom Plugin Repository" under Settings -> Plugins -> Browse Repositories -> Manage Repositories. Once added, if you chose the nightly build you will get a notification when the nightly build runs that you have an update to the Go plugin. I didn't try and force the update right away because I had already had the latest build running in a cronjob locally, but you will start seeing update notifications within 24 hours of adding the repo.

More from the Github repo: <a href="https://github.com/go-lang-plugin-org/go-lang-idea-plugin#pre-release-builds" target="_blank" rel="noopener noreferrer">IDEA Golang Pre-Release Builds</a>

The rest of the post is still valid for hacking and compiling the plugin with your modifications or is you just want to build it yourself.
 </aside>



The two build repos are:


<ul><li>
alpha releases: https://plugins.jetbrains.com/plugins/alpha/list
</li><li>
nightly: https://plugins.jetbrains.com/plugins/nightly/list
</li></ul>


Here is a screen cap of the custom repo add/edit:
<hr>
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/04/Intellij-Manage-Repositories-e1427850904203.jpg" >}}" alt=""></figure>
<hr>

The rest of the post is how to install the latest Alpha branch from trunk to build or for development work on the project itself. The alpha has some fantastic improvements from the older packaged in Inellij 3rd party plugins release from last year. We will clone the plugin source code, switch to the v1.0.0-alpha0 branch and build the plugin using the IDEA Java SDK. It is quite simple and quick once you have the right steps nailed down. Lastly, this is all being done on a Mac, I am guessing the process is similar if not the same but no guarantees or nerd rage if it doesn't :)



<ul>
	<li><a href="https://github.com/go-lang-plugin-org/go-lang-idea-plugin" target="_blank">Golang Plugin on Gihtub</a></li> Fyi, the development work is being done on the v1.0.0-alpha0 branch, so if you go to the Github page, use the drop down box to switch from 
	<li><a href="https://www.jetbrains.com/idea/download/" target="_blank">Download IntelliJ IDEA 14</a></li>

	<li>For information on contributing to the project, see <a href="https://github.com/go-lang-plugin-org/go-lang-idea-plugin/blob/master/contributing.md" target="_blank">How to contribute</a> page.</li>

</ul>




<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/slpha.png" >}}" alt=""></figure>


<h2> Clone Golang Plugin Using Git</h2>

This can be done using the Git plugin inside of the Intellij IDE but its just faster and easier to show using the CLI. It can be downloaded anywhere since this is Java and not Go so the static linking locations of Go are irrelevant.

<pre class="code-sample"><code>
git clone git@github.com:nerdalert/go-lang-idea-plugin.git
cd go-lang-idea-plugin
git checkout remotes/origin/v1.0.0-alpha0
git branch -a
 </code></pre>


Here is a more verbose output for those newish to git.

<pre class="code-sample"><code>
github.com # git clone git@github.com:nerdalert/go-lang-idea-plugin.git
Cloning into 'go-lang-idea-plugin'...
remote: Counting objects: 49143, done.
remote: Compressing objects: 100% (13482/13482), done.
remote: Total 49143 (delta 26512), reused 49143 (delta 26512)
Receiving objects: 100% (49143/49143), 18.66 MiB | 332.00 KiB/s, done.
Resolving deltas: 100% (26512/26512), done.
Checking connectivity... done.
github.com # cd go-lang-idea-plugin
go-lang-idea-plugin # git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/app_engine
  remotes/origin/bugfix/go_template
  remotes/origin/coverity_scan
  remotes/origin/error_parsing
  remotes/origin/formatter_work
  remotes/origin/gh-pages
  remotes/origin/master
  remotes/origin/v1.0.0-alpha0
  remotes/origin/wip
go-lang-idea-plugin # git checkout remotes/origin/v1.0.0-alpha0
Note: checking out 'remotes/origin/v1.0.0-alpha0'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b new_branch_name

HEAD is now at 99fbe2d... Update Go libraries on external changes
go-lang-idea-plugin # git branch -a
* (detached from origin/v1.0.0-alpha0)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/app_engine
  remotes/origin/bugfix/go_template
  remotes/origin/coverity_scan
  remotes/origin/error_parsing
  remotes/origin/formatter_work
  remotes/origin/gh-pages
  remotes/origin/master
  remotes/origin/v1.0.0-alpha0
  remotes/origin/wip
 </code></pre>

<h2>Build and Install the Golang Plugin In Intellij </h2>

Now open up Intellij and go to File -> Open and browse to the directory you cloned the Golang plugin into.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-05-29.png" >}}" alt=""></figure>


This will open the project in Intellij, but you will now need to specify the proper Intellij Plugin Dev SDK.  Select 'Project Structure...' from the menu.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-06-15.png" >}}" alt=""></figure>

Next click on 'Project' if it is showing [invalid] since an SDK needs to be specified.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-06-42-650x309.png" >}}" alt=""></figure>


In the drop down menu, choose <a href="https://confluence.jetbrains.com/display/IDEADEV/Getting+Started+with+Plugin+Development" target="_blank">IDEA IC-xxx</a> SDK as shown below. It is recommended to use Java 1.6, not to mention Java on a Mac is crap shoot. Now that I rarely dev in Java anymore I just use the Apple Java lib to try and avoid JDK pain. Anyways, below is what works for me, more on it in the link above :) <strong>Note:</strong> The host I took the screenshot from still had Go v1.3.3 on it. The Alpha plugin supports Go v1.4.1 and supported it within a week or two of release.


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-06-56.png" >}}" alt=""></figure>

Now we are all set to build the plugin with Build -> Build Artifacts


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/1-update-golang-e1423885000615.jpg" >}}" alt=""></figure>


In the popup, choose -> go.zip -> build

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2-update-golang-e1423884940974.jpg" >}}" alt=""></figure>


This generates a zip file named go.zip located in the go-lang-idea-plugin/bin/ directory.


<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/3-update-golang-e1423884956970.jpg" >}}" alt=""></figure>


Finally its time to install the Go plugin itself in the 'Preferences' settings.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-09-42.png" >}}" alt=""></figure>

Click 'install plugin from disk' find the newly built go.zip, reboot and you can start hacking in Intellij and Go using the latest features from the <a href="https://github.com/go-lang-plugin-org/go-lang-idea-plugin" target="_blank">go-lang-idea-plugin</a> project!

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/02/2015-02-07_19-10-29.png" >}}" alt=""></figure>

Just to reiterate, this is only if you want the latest 9 months of feature work or are looking to get started contributing to the project itself. There is a pre-v1.0 release in the Intellij plugin directory. The Intellij IDEA community edition is free and has all the features I need since Im mostly all Go these days but when I use full time Java the added features were super handy and much more sane then the other loosely coupled OSS IDE free for all projects. Not too commercial but they also have free<a href="https://www.jetbrains.com/idea/buy/index.jsp" target="_blank"> license grants</a> to open source projects, students and half off for startups. I like it, they earned plugs from me.


The plugin project maintainers seem very friendly and responsive. They use Gitter on their Github page which I <3 for working with the community and raised issues. So if you use it, help with bugs/issues even if just bringing one up or eventually sending in pull requests with bug fixes.

If you are <a href="http://www.golang-book.com/13/" target="_blank">new to Go</a>, check out some resources and simple intro snippets in this post:  <a href="{{< relurl "/golang-network-ops/" >}}"> Golang for Network Ops</a>. I will be trying to get one out at least every other week. I think the flexibility Go presents for a "get shit done" natively tooled, good for both the Python programmer or the C programmer that intersect nice for Devops. In a world of ever growing density, Go is highly performant that compiles down to native machine code that can be delivered in a binary and makes it a great fit for scaling distributed systems.
<hr>
Thats all for now, Im sure there are lots of ways to do this, I will update as I get feedback if there is a more preferred method to build the plugin but this is quick and simple for a weekly refresh for me. Thanks for stopping by!