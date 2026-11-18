+++
title = "OpenDaylight OpenFlow Tutorial"
date = "2013-04-12T20:12:37+00:00"
lastmod = "2015-05-11T00:40:03+00:00"
author = "Brent Salisbury"
wp_id = 6308
categories = ["In the Lab"]
tags = ["OpenDaylight", "OpenFlow", "Tutorials"]
description = ""
url = "/opendaylight-openflow-tutorial/"
image = "/wp-content/uploads/2013/05/OpenDaylight-Logo-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8b8eae82db2f4e2d40d90292773096b3383074eb242b2c03110529631b8b2b09"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenDaylight OpenFlow Tutorial</h2>
The OpenDaylight project was announced this week and they already have working controller code up on a repositry. Under the controller hood, looks to be the OSGI framework originally forked from <a href="https://openflow.stanford.edu/forums/topic/243-looking-for-beta-testers/" target="_blank">David Erickson's</a> Beacon controller. It's a simple tutorial to help kickstart the dependencies and getting a chance to learn how instantiating OpenFlow flow rules work. This was the first time I have looked at OpenDaylight, so I was learning as I did the screencast.
<h2>OpenDaylight Installation and Setup</h2>

If you do not want to mess with the code and just run the controller it is super simple. Download the <a href="http://mininet.org" target="_blank">Mininet</a> image now managed by the <a href="http://onlab.us" target="_blank">On.lab</a>. I personally prefer Mininet for dev/test.

<a href="http://mininet.org" target="_blank" rel="noopener noreferrer">Download Mininet</a>

Once in Mininet you can download the daily OpenDaylight build from OpenDaylight Jenkins server.

<a href="https://jenkins.opendaylight.org/controller/job/controller-merge/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/" target="_blank" rel="noopener noreferrer">Download the OpenDaylight Daily Build</a>

<em>From Mininet run the following</em>:
<pre class="code-sample"><code>
apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk unzip
wget https://jenkins.opendaylight.org/controller/job/controller-merge/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/distribution.opendaylight-osgipackage.zip
unzip distribution.opendaylight-osgipackage.zip
cd opendaylight
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64
./run.sh
### Then go to http://<ip>:8080 ###
### On Mininet ###
mn --controller=remote,ip=<IP of Controller> --topo=linear,2 --listenport=6633</code></pre>

<hr>
For those wanting to hack on code, a good place to start is building the project into your dev environment. I did a quick screencast tutorial for downloading and installing OpenDaylight on Ubuntu. For a tutorial on getting VirtualBox and Ubuntu up and going check <a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}" target="_blank">here</a>. Once OpenDaylight is installed, I used Mininet as a software switch so that anyone can give it a try. Mininet can be downloaded <a href="http://yuba.stanford.edu/foswiki/bin/view/OpenFlow/MininetDocumentation" target="_blank">here</a>. Once you download Mininet just import the ISO into your hypervisor.


<em>Install the dependencies and pull down the code using git:</em>

<hr />



<pre class="code-sample"><code>apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk 
git clone http://git.opendaylight.org/gerrit/p/controller.git
cd controller/opendaylight/distribution/opendaylight/
mvn clean install
cd target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight</code></pre>


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

 In the meantime run the following instead of "mvn clean install" and it will skip the integration tests that seem to be the source of the GC leak.


<pre class="code-sample"><code>
mvn clean install -DskipTests</code></pre>

Also adjust the memory allocation to Maven temporarily with the export command or permanently in your ~/.bashrc directory.
<pre class="code-sample"><code> export MAVEN_OPTS="-Xmx1024m -XX:MaxPermSize=256m"</code></pre>

More install help on the <a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank">OpenDaylight Wiki Troubleshooting Section</a>
<hr />
In the shell, setup your JAVA_HOME ENV. It can be viewed with 'echo $JAVA_HOME'. It will likely be undefined so define it here. Make sure Java releases synch with the ENV. Export the JAVA_HOME ENV variable. You can write it to .bashrc (located in the user account home directory) to have it be persistent through reboots and logins.

<hr />

<pre class="code-sample"><code>export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64 Place JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64
at the bottom of your ~/.bashrc 
Or, for a one time:
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64</code></pre>

<hr />

Then start OpenDaylight in all its glory with ./run from the target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight directory.

<hr />


<pre class="code-sample"><code>#From the directory
~/controller/opendaylight/distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
./run.sh will start the controller.</code></pre>

<hr />

Give it a couple minutes to get all of the modules loaded and point your browser to: 127.0.0.1:8080 Or you can point to another address bound to your system, just append :8080 on the end.
<h2>Adding an OpenFlow Switch To OpenDaylight</h2>
When you point an OpenFlow switch at the OpenDaylight controller it will pop up as a device waiting to be configured. That is pretty magical in and of itself. Give it an arbitrary name. The datapath ID (ID) is the unique key identifier made up of the switch MAC and an ID assigned by the controller. Mininet will use all zeroes with a one at the end. OpenFlow uses LLDP for topology discovery by using packet_out instruction in which the controller tells the forwarding element to do something like send an LLDP discovery.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/OpenDaylight-OpenFlow-Switch-650x405.png" >}}" alt="OpenFlow Switch in OpenDaylight"></figure>

<hr />

<h2>Installing OpenFlow Flow Rules to the OpenDaylight Controller</h2>
Next specify the action for the flowmod (Flow Modification). Here we choose the output port. Remember OpenFlow only forwards what you tell it to, so either add rules to handle 0x0806 Ethertype traffic for ARP broadcast requests and unicast replies or delete the Etherype default IPv4 0x0800 value when you add a flowmod. You also need to setup a match on traffic from port 1 with an action to forward to port 2 along with the return traffic of matching port 2 with an output action of port 1. You can specify reserved ports like normal, controller, flood and all of the others listed in the dropdown boxes from the <a href="http://www.openflow.org/documents/openflow-spec-v1.0.0.pdf" target="_blank">OpenFlow v1.0</a> specification. The controller is OFv1.0 but I would imagine that to transition fairly quickly to OFv1.3 compliant.

<hr />

<a href="{{< relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" >}}" target="_blank" rel="noopener noreferrer">Download OpenFlow v1.3</a>

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/OpenDaylight-Match-Add-Flow.png" >}}" alt="OpenDaylight Flow Rules"></figure>

<hr />

Choose an action that can be logical or physical. Logical tend to be named with symbolic representation while physical is numeric. Ports are learned by the switch sending configuration information and also updated if a port or link go down. Port and link are two separate data structures but most controllers so far just report PORT_DOWN for both link and port, rather then LINK_DOWN for link disconnections.

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/04/OpenDaylight-Output-port.png" >}}" alt="OpenDaylight Flowmod Static Flow"></figure>

<hr />

For troubleshooting you can use dpctl to see flows instantiated in the datapath in Mininet. The <a href="{{< relurl "/installing-wireshark-on-linux-for-openflow-packet-captures/" >}}" target="_blank">Wireshark OpenFlow dissector</a> maintained by Nick Bastin of BigSwitch is great for troubleshooting ant viewing OpenFlow messages.
<h2>OpenDaylight Installation and Adding Flow Rules Video</h2>

<hr />

<p><a href="http://www.youtube.com/watch?v=hXWhgWMoNHM">Watch video on YouTube</a></p>

<hr />

<h2>Additional OpenDaylight and OpenFlow Resources</h2>
Excellent work by the OpenDaylight group. Since this appears to be OSGI and the <a href="{{< relurl "/the-cisco-one-sdn-controller/" >}}" target="_blank">ONE GUI</a> I am guessing the blob came from Cisco. I am looking forward to all of the other contributions from those who have been spending R&amp;E on OpenFlow dev. Kudos to the vendors on this, very impressive.


<ul>
	<li><a href="http://yuba.stanford.edu/foswiki/bin/view/OpenFlow/MininetDocumentation" target="_blank">Mininet Information</a></li>
	<li><a href="https://wiki.opendaylight.org">OpenDaylight Wiki</a></li>
	<li><a href="{{< relurl "/installing-wireshark-on-linux-for-openflow-packet-captures/" >}}">Installing Wireshark On Linux for OpenFlow Packet Captures</a></li>
	<li><a href="{{< relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" >}}" target="_blank" rel="noopener noreferrer">Download OpenFlow v1.3</a></li>
	<li><a href="http://openvswitch.org" target="_blank">Open vSwitch</a> project</li>
</ul>


<hr />

Thanks for stopping by!