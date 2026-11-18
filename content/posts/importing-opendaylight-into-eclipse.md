+++
title = "Importing OpenDaylight Into Eclipse"
date = "2013-04-14T16:49:16+00:00"
lastmod = "2014-02-18T02:57:20+00:00"
author = "Brent Salisbury"
wp_id = 6358
categories = ["In the Lab", "Programming"]
tags = ["OpenDaylight", "OpenFlow", "Programming", "Software Defined Networking"]
description = ""
url = "/importing-opendaylight-into-eclipse/"
image = "/wp-content/uploads/2013/04/Openflow-Programming-header-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "bdb292fe80b95f902a3bd3db2f3b4af4378965b178d897c42b1e60fecb3dc364"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Importing OpenDaylight Into Eclipse</h2>
This is a quick video for importing OpenDaylight into Eclipse for development. You need to build OpenDaylight with Maven prior to importing it into Eclipse. Once you build ODL from the CLI, you can either run it from there for learning OpenFlow or getting to know the OpenDaylight controller or go on to importing the controller into Eclipse. For those new to Eclipse, it is a free and open source (FOSS) integrated development environment (IDE) that supports Windows, Mac and Linux. Once imported and built in Eclipse, you can run the project from within the IDE for test/dev.
<hr>
Here is a recording from ONS 2013. This was a Q&A session with the technical steering committee (TSC). The recording is pretty grainy since it was just a pocket recorder. You can't hear David Meyer very well in the audio but you can hear the panel well enough. The ONS does a nice job of getting a lot of the content on their <a href="http://www.youtube.com/user/OpenNetSummit" target="_blank">YouTube</a> channel. I will replace this with a link to that once it posts.<a href="{{< relurl "/wp-content/uploads/2013/04/OpenDaylight-ONS-ODP.mp3" >}}" target="_blank" rel="noopener noreferrer">OpenDaylight TSC Q&A from ONS 2013</a>


<hr />

<h2>Video: Importing OpenDaylight Into Eclipse </h2>

<hr />

I will keep this page or some pointer to a page updated as the project matures. Make sure you use JDK7 and not JDK6. See this thread on the ODL <a href="https://lists.opendaylight.org/pipermail/controller-dev/2013-April/000171.html" target="_blank">Listserv</a>. The audio is very low, I will remix it in the next day or two and upload it.
[youtube url="http://youtu.be/vjRJ8d_0Jwo&vq=hd720" width="630" height="360" hd="1"]

<hr />

<h2>OpenDaylight Mac OSX CLI Build</h2>
If you don't build ODL from the CLI prior to importing it into Eclipse you will end up with thousands of errors. This sort of thing seems easier to follow along a video rather then following 30 steps of instructions. If you have never used Eclipse, keep an eye in the bottom right of the main window for its progress bar. It is always best to leave Eclipse alone while it is downloading dependences or project code.

<pre class="code-sample"><code>git clone http://git.opendaylight.org/gerrit/p/controller.git
cd controller/opendaylight/distribution/opendaylight/
mvn clean install</code></pre>

<hr />

If you want to just run the controller from the CLI the following will start it up. First you need to set the $JAVA_HOME ENV variable and then run the shell script to start the controller.

<pre class="code-sample"><code>export JAVA_HOME=$(/usr/libexec/java_home)
#Verify with:
echo $JAVA_HOME
#Replace 0.1.0 with the current version that is built.
cd target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
./run.sh</code></pre>

<hr />

Then point your browser at IP addr on port 8080 or use the REST API (API subject to change) along with everything else since this is in its infancy.

<pre class="code-sample"><code>cd target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
http://127.0.0.1:8080 
Login: admin
Password: admin</code></pre>

<hr />

<h2>Building OpenDaylight Into Eclipse</h2>

<hr />


<ul>
	<li>It is probably best to use Eclipse IDE for Java EE Developers - <a href="http://www.eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/junosr2" target="_blank" rel="noopener noreferrer">Eclipse IDE for Java EE Developers</a></li>
	<li>I used this Wiki entry for the m2e (Maven Integration for Eclipse) dependencies I was getting tripped up on: <a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Eclipse_CLI_Setup" target="_blank">OpenDaylight - Eclipse CLI Setup</a></li>
	<li>Make sure you use m2e v1.2 rather then v1.3. If you are using an existing Eclipse install it is probably running the latest. Just uninstall it under Eclipse-&gt; About Eclipse -&gt; Installation Details and remove the two m2e dependencies. Then go to help -&gt; install new software and plug in the URI <a href="http://download.eclipse.org/technology/m2e/releases" target="_blank">http://download.eclipse.org/technology/m2e/releases</a></li>
	<li>You may get 40-50 errors or so after you import ODL as an existing Maven project. That is a missing dependency, Tycho. Eclipse will downloaded Tycho automatically, just click "auto select" as shown in the video.</li>
	<li>Prior to being able to run the controller within Eclipse you need to run the configuration /distribution.opendaylight/opendaylight-assembleit.launch with "run-as" opendaylight-assembleit.launch to finish the build. There is probably be a better way, but this was where I ended up after poking around for a while to get it working.</li>
	<li>The pom.xml (Project Object Model) instructs maven to create a jar file and basically contains everything that is significant about the project. The pom.xml file is located in distribution.opendaylight/pom.xml.</li>
</ul>


<hr />

<h2>Building OpenDaylight In Linux</h2>
If you are using Linux, the following will cover the CLI Maven build.

<pre class="code-sample"><code>apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk 
git clone http://git.opendaylight.org/gerrit/p/controller.git
cd controller/opendaylight/distribution/opendaylight/
mvn clean install
cd target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64
echo JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64 &gt;&gt; ~/.bashrc
#From the directory
~/controller/opendaylight/distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
./run.sh will start the controller.</code></pre>


<h2>OpenDaylight Maven Build Error</h2>
<aside class="legacy-callout">If you receive any OutOfMemory resembling the following:
If your Maven build fails with a  " OutOfMemory: PermGen Space " Re-run Maven using the -X switch to enable full debug logging.  This is due to a memory leak somewhere in the Maven build and is being tracked as a bug.</aside>


<pre class="code-sample"><code>
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-failsafe-plugin:2.15:integration-test (default) on project northbound.integrationtest: Execution default of goal org.apache.maven.plugins:maven-failsafe-plugin:2.15:integration-test failed: The forked VM terminated without saying properly goodbye. VM crash or System.exit called ?
[ERROR] Command was/bin/sh -c cd /Users/brent/Downloads/controller/opendaylight/northbound/integrationtest && /Library/Java/JavaVirtualMachines/jdk1.7.0_07.jdk/Contents/Home/jre/bin/java -jar /Users/brent/Downloads/controller/opendaylight/northbound/integrationtest/target/surefire/surefirebooter4405430530997069603.jar /Users/brent/Downloads/controller/opendaylight/northbound/integrationtest/target/surefire/surefire1749047358112582031tmp /Users/brent/Downloads/controller/opendaylight/northbound/integrationtest/target/surefire/surefire_66025253661421325818tmp
20:24:00.137 [http-bio-8080-exec-9] ERROR o.o.c.l.b.i.UncaughtExceptionHandler - Uncaught ExceptionHandler:
java.lang.OutOfMemoryError: PermGen space
20:24:03.594 [Timer-2,ISPN,brents-MacBook-Pro-2-567] ERROR o.o.c.l.b.i.UncaughtExceptionHandler - Uncaught ExceptionHandler:
java.lang.OutOfMemoryError: PermGen space</code></pre>

 In the meantime run the following instead of "mvn clean install" and it will skip the integration tests that seem to be the source of the GC leak. Also increase memory allocation for Maven.


<pre class="code-sample"><code>
MAVEN_OPTS="-Xmx1024m -XX:MaxPermSize=256m"
mvn clean install -DskipTests</code></pre>


<hr />

You will need at least around 1.5GB of memory or you may run out of memory during the Maven build. The error will look like this:
<hr>


<pre class="code-sample"><code>Compilation failure
Failure executing javac, but could not parse the error:
The system is out of resources.
Consult the following stack trace for details.</code></pre>

<hr>
<hr />

I started hacking on a module, by just copying an existing module and adding it to pom.xml file. I am more familiar with Floodlight then Beacon.

<hr />

I did a screencast of installing OpenDaylight and installing some flowmods with Mininet and the link to the ODL Eclipse install Wiki entry:




<ul>
	<li><a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Eclipse_CLI_Setup" target="_blank">OpenDaylight – Eclipse CLI Setup</a></li>
	<li><a href="{{< relurl "/opendaylight-openflow-tutorial/" >}}" target="_blank">OpenDaylight OpenFlow Tutorial</a></li>

<li><a href="http://packetpushers.net/show-148-talking-with-opendaylight-leadership/" target="_blank">Packet Pushers - Talking With OpenDaylight Leadership</a></li>

</ul>

Good stuff. This is a unique time to say the least. Its probably one of those 15-20 year disruption cycles, last one was the Internet in the late 90's. Jump in and shape its direction.


<hr />

Thanks for stopping by.