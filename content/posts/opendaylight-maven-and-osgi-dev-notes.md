+++
title = "OpenDaylight Maven and OSGI Dev Notes"
date = "2013-06-04T05:09:35+00:00"
lastmod = "2014-02-18T02:57:23+00:00"
author = "Brent Salisbury"
wp_id = 6627
categories = ["In the Lab", "Programming"]
tags = ["OpenDaylight", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/opendaylight-maven-and-osgi-dev-notes/"
image = "/wp-content/uploads/2013/06/osgi-maven.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3e545c16906b0e48b0a8df7e9a6829f07849cf3b66a44be9424ebf4cefdc70d0"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OPENDAYLIGHT MAVEN AND OSGI DEV NOTES</h2>
Prior to OpenDaylight I had only used the ODGI framework with David Ericson's Beacon contorller. I wanted to dump some of my notes from code hacking over the past couple of weeks. Most of the time has been spent getting used to OSGI and Maven. After the Maven and OSGI overviews, I list my dev notes for setting OSGI log levels, building an individual specific OpenDaylight bundle with Maven and making a creating a new module to hack on.
<h2>WHAT IS OSGI?</h2>
OSGI is adds a modular framework that allows for dynamic loading of Java modules. This means you can load and unload , start and stop applications without taking down the running JVM platform. This seems to fits the theme of OpenDaylight to allow applications and protocols to plug into the framework to fit different use cases and vendor strategies. The platform is merely a series of Java interfaces. The projects that plug into the framework are referred to as bundles. The bundles need a few things to get started.
<h2>WHAT IS MAVEN?</h2>
Here are some high points of the value Maven brings. Maven is awesome becuase it pulls dependencies automagically and lets you change version by merely changing the release number.

<ul>
	<li>Making the build process easy</li>
	<li>Providing a uniform build system</li>
	<li>Providing quality project information</li>
	<li>Providing guidelines for best practices development</li>
	<li>Allowing transparent migration to new features</li>
	<li>Change log document created directly from source control</li>
	<li>Cross referenced sources</li>
	<li>Mailing lists</li>
	<li>Dependency list</li>
	<li>Unit test reports including coverage</li>
	<li>Keeping your test source code in a separate, but parallel source tree</li>
	<li>Using test case naming conventions to locate and execute tests</li>
	<li>Have test cases setup their environment and don’t rely on customizing the build for test preparation.</li>
</ul>


<hr />

<h2>ENABLING LOGGING LEVELS AND TRACES IN THE OSGI CONSOLE</h2>
Lets say you want to see all log messages from the bundle. Change the logging level to arphandler to trace from the OSGI console.
<pre class="code-sample"><code>
osgi setLogLevel org.opendaylight.controller.arphandler trace
</code></pre>
Next verify your logging level.

<pre class="code-sample"><code>
osgi getloglevel | grep arp
Logger org.opendaylight.controller.arphandler at level INFO
Logger org.opendaylight.controller.arphandler.internal at unknown level
Logger org.opendaylight.controller.arphandler.internal.Activator at unknown level
Logger org.opendaylight.controller.arphandler.internal.ArpHandler at unknown level
Logger org.opendaylight.controller.arphandler_0 at unknown level
Logger org.opendaylight.controller.arphandler_0.4 at unknown level
Logger org.opendaylight.controller.arphandler_0.4.0 at unknown level
Logger org.opendaylight.controller.arphandler_0.4.0.SNAPSHOT at level TRACE
</code></pre>

Logs will appear in the OSGI console and also in your opendaylight.log file.
<pre class="code-sample"><code>
~/controller/opendaylight/distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight/logs/opendaylight.log
</code></pre>

To enable logging in a bundle the following is an example. I am assuming each bundle will maintain separate logging per class/bundle for logical separation.

<pre class="code-sample"><code>
//Import Java logging packages
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
//Class object for your logger would be the bundle name e.x HostTracker
private static Logger cnameLogger = LoggerFactory.getLogger(ClassName.class);
//Different levels of logging.
cnameLogger.info("Throw an informational log");
cnameLogger.error("Throw an error log");
cnameLogger.debug("Throw an debug log");
</code></pre>
<h2>BUILDING OPENDAYLIGHT MODULES INDIVIDUALLY AFTER CHANGING THE CODE</h2>
Once you edit code on an individual bundle, you need to rebuild the bundle for the code to take effect. It is way to slow to rebuild the entire platform, not to mention very un-agileish.

First, if the project is running, stop the module with the following from the OSGI console. In this case I am using the arphandler bundle as an example.

<pre class="code-sample"><code>
osgi ss | grep arphandler
35 ACTIVE org.opendaylight.controller.arphandler_0.4.0.SNAPSHOT
Stop a bundle:
osgi stop 35
</code></pre>
Next, rebuild the bundle. When you build the project using mvn clean install, it will delete the existing jar file and create a new one. In order to get the new jar to load it needs to match the pom.xml loaded module. That is why I copy it in the second line in the following snippet.

<pre class="code-sample"><code>
cd ~/controller/opendaylight/arphandler
#Build the new bundle jar and create a new one.
mvn clean install
cp target/arphandler-0.4.0-SNAPSHOT.jar ../distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight/plugins/org.opendaylight.controller.arphandler-0.4.0-SNAPSHOT.jar
</code></pre>
Finally load the new jar into the framework. The cool thing is the JVM was never stopped in this process.

<pre class="code-sample"><code>
Start a bundle:
osgi start 35
</code></pre>
You can also never stop the bundle and perform an upgrade using OSGI with:

<pre class="code-sample"><code>
Start a bundle:
osgi upgrade 35
</code></pre>
OSGI will pull the current jar in the path and reload it.
<h2>HACKING BUNDLES : CREATE YOUR OWN MODULE</h2>
I am using bundles and projects (right or wrong) interchangeably. There are various ways to start bundles, but an easy starter could be to copy and paste an existing application. There are some example application bundles located in the “~/controller/opendaylight/samples/” directory. It can also be done using declarative services, but I have not explored that yet. This is just a total sample of how to hack and even better break things to learn the OSGI/Maven framework and the code order of operations. Keep in mind, there isn’t a main method with OSGI. It is more of blob projects/modules/bundles can plug into and dynamically loaded and unloaded without restarting the entire JVM.

Copy and application like samples.simpleforwarding and paste it into the project explorer.
Edit the project bundle pom.xml to match your new bundle: ~/controller/opendaylight/samples/simpleforwarding
Edit the parent pom.xml located in distribution.opendaylight and add the new bundle: ~/controller/opendaylight/distribution/opendaylight/pom.xml. The parent pom.xml denoted by is located in opendaylight/commons/opendaylight/pom.xml
The Activator.java can be used to start/stop/initialize/destroy bundles into the JVM. Simple examples are two methods starting a bundle, start/stop.
<pre class="code-sample"><code>
A method starting a bundle:
public void start(BundleContext context) {
A method to stop the bundle:
public void stop(BundleContext context) {
An array is run to get all of the class objects inside of OpenDaylight. Just copy and paste the bundle:

public Object[] getImplementations() {
Object[] res = { NewClass.class };
return res;
}
</code></pre>

Project Object Model or POM is the main piece of Maven that ties all of the projects in together. Each project has a pom.xml and the whole platform has a super pom.xml. The format is XML and fairly easy to discern what is going on. There is a patch in from David Erickson to bring the net-virt platform into the controller which will be awesome. The net-virt L2 forwarding module is very mature coupled with its host tracker. I hope to use it in production soon to proof reactive BUM traffic scale (may need a job:-).
<h2>UPDATE OPENDAYLIGHT USING GIT</h2>
Running git pull from anywhere south of the parent controller directory will update the code set. Then just rebuild it w/ mvn clean install. mvn clean will delete the existing built jars. Install will build and leave them in the target directory.

<pre class="code-sample"><code>$ pwd
$ git pull
remote: Counting objects: 1009, done
remote: Finding sources: 100% (709/709)
remote: Total 709 (delta 156), reused 667 (delta 156)
Receiving objects: 100% (709/709), 181.46 KiB, done.
Resolving deltas: 100% (156/156), completed with 87 local objects.
From http://git.opendaylight.org/gerrit/p/controller
827a499..191acb8 master - origin/master
Updating 827a499..191acb8
Fast-forward
opendaylight/clustering/test/pom.xml | 15 +-
.../clustering/test/internal/Activator.java | 73 +++
.../test/src/main/resources/OSGI-INF/component.xml | 19 -
.../tranform/CompositeConditionalTransformer.java | 28 +-
.../opendaylight-osgi-launcher-local.launch | 5 +-
#Next rebuild the jar and copy it to replace the old jar for run.sh.
$ mvn clean install
$ cd ~/controller/opendaylight/distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight/
$ mvn clean install </code></pre>
You can always manually install jars with the following:

<pre class="code-sample"><code>
install -start file:/Users/brent/Downloads/ra-controller/controller/opendaylight/configuration/implementation/target/configuration.implementation-0.4.0-SNAPSHOT.jar
</code></pre>
<h2>MORE OPENDAYLIGHT HOW-TOS</h2>
We are starting to have a good list of resources. Hack around and break it and fix it. I am great at the breaking part personally. Dont be overwhelmed, if you want to learn ODP or even programming you can if you put in the time. It is a unique time in networking to shape the future.

See more blogs from the ODP community and visit the OpenDaylight Wiki. If you do any how-tos feel free to shoot them to me and I will post them on the wiki.

<hr />



<ul>
	<li>Join the OpenDaylight IRC channel at <em>irc.freenode.net</em> at <em>#opendaylight </em>and colaborate with others from the community.</li>
	<li>Listen to the TSC calls weekly <a href="https://wiki.opendaylight.org/view/TSC:Main" target="_blank">Weekly TSC</a> and <a href="https://wiki.opendaylight.org/view/Tech_Work_Stream:Main" target="_blank">Technical Work Stream Calls</a>.</li>
</ul>

<hr>
<a href="https://lists.opendaylight.org/mailman/listinfo/" target="_blank" rel="noopener noreferrer">Join the ODP Listserv</a>

<a href="https://wiki.opendaylight.org/view/OVSDB_Integration:Design" target="_blank" rel="noopener noreferrer">Come Help Us Code in the OVSDB Project</a>

<a href="https://www.youtube.com/channel/UCMYntfZ255XGgYFrxCNcAzA" target="_blank" rel="noopener noreferrer">Check Out Our Recordings of the OVSDB Project</a>

<hr />

Regardless of any claims, no one really knows what the future of networking should or will be but open source is a safe bet based on history. Companies like Red Hat and IBM are well positioned in the Daylight project so keep that in mind when parsing through the FUD. Little if any of SDN is proofed beyond a few fixed scenarios. It is a great chance for both vendors and community to collaborate and evolve together for the future. The Linux Foundation is an appropriate organization for ODP to be under the auspices of. OpenDaylight has the makings of becoming the Linux kernel of networking.

To get there it will take community. The TSC’s role should be focused on community enablement. The broader OpenDaylight project goal should not only be bootstrapping code, but the equally important mission of bootstrapping a the fledgling network community. The vendors on the IRC channel everyday helping field dev questions are nothing short of phenomenal. Come grow with networking, I am happy to help, as are others in channel. No such thing as dumb questions.