+++
title = "Pre-Built OpenDaylight VM Images"
date = "2013-05-06T03:00:59+00:00"
lastmod = "2014-02-18T02:52:49+00:00"
author = "Brent Salisbury"
wp_id = 6505
categories = ["In the Lab", "Tools"]
tags = ["Open Source", "OpenDaylight", "OpenFlow", "Software Defined Networking"]
description = ""
url = "/pre-built-opendaylight-vm-images/"
image = "/wp-content/uploads/2013/05/OpenDaylight-Logo-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "be15ec4cf4bb793c0ead027f49bfe2ca1dc16a67653232d37ae95dd7261c33ec"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Pre-Built OpenDaylight VM Images</h2>

<aside class="legacy-callout"><strong>Update</strong>: We have new images for download now. Please see this post:
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}" target="_blank" rel="noopener noreferrer">OpenDaylight OpenStack Integration with DevStack on Fedora</a>
There are more images on the OpenDaylight web site:
<a href="http://www.opendaylight.org/software" target="_blank" rel="noopener noreferrer"> OpenDaylight Downloads Page</a>
</aside>
<hr>
While there is still some uncertainty on the platform details of OpenDaylight, there isn't uncertainty in my mind, where I will be devoting my time for the rest of the year. I put up a couple of Pre-Built OpenDaylight VM Image, made up of the two proposed bootstrap controllers and OpenFlow tools, on a couple of VM images. I split it into dev and ops images so anyone curious or having trouble getting things installed can pull these down. Very little if any Linux knowledge is required. Once the project consolidates, I will do the same with the VMs. This is not anything official from ODP. This is merely a VM that has two controller proposals. I think it is important for those interested in OpenDaylight and ideally, what direction the community collectively decides is necessary and flexible enough to fit as broad a community as possible, rather then niche hyper-scale networks.

<hr />

<a href="http://www.opendaylight.org" target="_blank">OpenDaylight</a> is run by the Linux foundation based off meritocracy rather then a handful of people. For what it is worth, this is a real life open source project, very much like OpenStack. Someone like myself, who doesn't work for Google, MS, FBook etc, that hasn't paid to join this, or other consortiums, yet still was able to push a <a href="{{< relurl "/wp-content/uploads/2013/05/ODP-Pen-Test.png" >}}" target="_blank">commit</a> to the project. Thus, my optimism and excitement. Take a look at both of the projects, wether ops or dev oriented, both are have had a lot of work put into them and hopefully will blend into a good base for everyone to begin contributing to. I am sure the TSC (Technical Steering Committee) would appreciate feedback from the community over the next few months from actual networking pros who get paid to design, build and operate networks.

<hr />

Last note, don't be shy about asking questions or looking to contribute. I tend to be especially on something as big as this. OSS is all about peer review, but thats a good thing, especially when its constructive. I have found the folks on this project to be incredibly nice, helpful and everything awesome about open source projects. Feel free to ping me for suggestions on Twitter or here, but seriously, this isn't a bunch of terse belittling. The Listerv speaks for itself and is linked at the bottom of the post.

<hr />

The VMs contains the following working components, along with a snapshot of any bugs from the time of pull. I probably recommend at least 1-2GB if memory since both bootstraps run in JVMs that love memory. I haven't really tested them other on my laptop and what not, so there may be some huge problem I am missing. Drop me a comment if you notice one and I would very much appreciate it. I probably watch the ODP <a href="https://lists.opendaylight.org/pipermail/" target="_blank">listserv</a> closer then I do comments here, so probably best to throw questions over there. If nervous about posting that public I totally understand and will try and get back to you here. I am much less versed on the net-virt controller since I had only had Floodlight prior to last week. There will be plenty of bugs in coming months, but this is all brand new so be patient or chip in :) You can update the code by pulling updates, or just deleting the code directory and re-cloning the repo with the instructions in the second part of this post:

<ul>
	<li>A working OpenDaylight bootstrap controller.</li>
	<li>Wireshark w/ OpenFlow dissector.</li>
	<li>Eclipse w/ working OpenDaylight bootstrap controller.</li>
	<li>VM running Ubuntu 12.10. Will be 12.10 with the next update in 2 weeks.</li>
	<li>Intructions for installing all of the software above.</li>
	<li>The only service running outside of the vanilla Ubuntu install is ssh daemon. To remove run "sudo apt-get purge openssh-server". -VM is set to attach to the bridge your Nic is attached to rather then sharing the hosts NIC (PAT).</li>
	<li>DHCP is enabled on the VM.</li>
</ul>


<hr />

<h2>Daylight VM Video</h2>
Next is a brief video of what the VM looks like to determine if worth downloading. Its a quick 1 minute video showing the Ops image. The Dev image has the same w/Eclipse installed.

<hr />

<p><a href="http://www.youtube.com/watch?v=2K6Wnt3eMb8&vq=hd720">Watch video on YouTube</a></p>

<hr />

<h2>Download Daylight VM</h2>
Both ODP and Wireshark are preinstalled on the guest VM image. The second section has instructions to install the software on another host.

<hr />

There are two images to choose from. One is just to run ODP. The other is for hacking on OpenDaylight bootstraps with the Eclipse IDE.


<hr />

<ul>
	<li>The ODP-VM-Ops.zip image contains both current bootstraps Wireshark + Dissector and instructions to start them both.</li>
	<li>The ODP-VM-Dev.zip image contains both bootstraps already built into Eclipse along with the controller, Wireshark + Dissector, both current bootstraps and instructions to start them both.</li>
</ul>


<hr />



New VM images can be found at the following links. Please see the networkstatic link for video and OpenStack instructions.
<a href="{{< relurl "/opendaylight-openstack-integration-devstack-fedora-20/" >}}" target="_blank" rel="noopener noreferrer">OpenDaylight OpenStack Integration with DevStack on Fedora</a>
There are more images on the OpenDaylight web site:
<a href="http://www.opendaylight.org/software" target="_blank" rel="noopener noreferrer"> OpenDaylight Downloads Page</a>

<h2>Virtual Machine Image Import</h2>
The images are in a .OVF format that should interop with about any hypervisor out there. I am leaving the how to below for *.Vmwarevm in case anyone needs it but I have changed the images to *.OVF.

<hr />


<ul>
	<li>Vmware (Commercial - Easy) - If using VMware add a guest host and locate the existing virtual disk or just unzip and double-click the vmwarevm image file.</li>
	<li>VirtualBox (Free - Easyish) - Before importing the guest VM, you just need to convert the ODP-VM-Lab1.vmwarevm image into an OVF format to import into VirtualBox.</li>
	<li>Download VirtualBox at <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">https://www.virtualbox.org/wiki/Downloads</a></li>
	<li>Download the VMware OVF Tool (Open Virtualization Format) <a href="http://www.vmware.com/support/developer/ovf/" target="_blank">http://www.vmware.com/support/developer/ovf/</a></li>
	<li>The tool is freeish other then having to register with Vmware or login.</li>
</ul>


<hr />

<pre class="code-sample"><code>ovftool original-disk.vmx new-disk.ovf</code></pre>

<hr />

For example:
<pre class="code-sample"><code>ovftool ODP-VM-Lab1.vmx ODP-VM-Lab1.ovf</code></pre>

<hr />

Windows Example:
<pre class="code-sample"><code>ovftool “C:\Users\NAME\Documents\Virtual Machines\Windows 7 x64\ODP-VM-Lab1.vmx” C:\ODP-VM-Lab1.ovf</code></pre>

<hr />

Mac OSX Example:
<pre class="code-sample"><code>/Applications/"VMware Fusion.app"/Contents/Library/"VMware OVF Tool"/ovftool ODP-VM-Lab1.vmwarevm/ODP-VM-Lab1.vmx ./ODP-VM-Lab1.ovf</code></pre>
After the conversion, delete the Manifest file created 'ODP-VM-Lab1.mf' to avoid a (VERR_MANIFEST_FILE_MISMATCH) error on import.

<hr />

Once converted, Open VirtualBox -&gt; File -&gt; Import Appliance -&gt; Find ODP-VM-xBox.ovf (or whatever you exported it to).
Adjust any of the resources (CPU, Mem, Nic) and click import.

<hr />

<h2> KVM / Qemu Image Import</h2>
KVM (Free -Advanced) - KVM has native support for VMDK images. Look at the VMX config file for the following attributes:
scsi0:0.fileName, uuid.bios, ethernet0.generatedAddress
<pre class="code-sample"><code>#Example:
kvm -drive file=zimbra-000001.vmdk,boot=on \
-net nic,macaddr=00:0c:29:c3:93:b9 -net tap \
-uuid 564d3f3d-3280-5bf2-9431-21c9b2c393b9
or convert it with:
kvm-img convert -O qcow2 zimbra-000001.vmdk zimbra.qcow2</code></pre>
<h2>ODP VM System Settings</h2>

<hr />

Default VM account UID/password

<hr />


<ul>
	<li>User ID: <strong>odp</strong></li>
	<li>password: <strong>passwd</strong></li>
</ul>


<hr />

Change the root password type: "<strong>passwd odp</strong>" in the console. Enable logging in as the root UID to avoid having to type sudo with "sudo passwd root". The "su" (super user) will allow you to login as root.

<hr />

I recommend installing the guest OS tools whether using VirtualBox or VM Fusion for mem ballooning copy/paste etc. Typically just click in the Virtual Machine menu and choose install guest VM tools.

<hr />

After installing the mini.iso image, you can add a fairly stripped down, but still functional Ubuntu Desktop (lightdm) GUI. To do so install the following binaries from repo (~500MB):
<pre class="code-sample"><code>sudo apt-get install xorg xterm gdm ubuntu-desktop menu firefox gksu synaptic --no-install-recommends</code></pre>

<hr />

<h2>Starting OpenDaylight (ODP) Bootstrap #1</h2>
Start the controller with the following. After a few seconds the controller web UI will be available. To stop the controller, at the OSGI CLI type "quit".

<pre class="code-sample"><code>cd /home/odp/controller/opendaylight/distribution/opendaylight/target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
./run.sh</code></pre>
Click hyperlink on the desktop or any browser that can reach the IP of the guest VM to http://&lt;127.0.0.1 or the IP of the ctrl&gt;:8080 There is a link on the desktop for Bootstrap #1. I didn't see instructions for #2 on the wiki.

<hr />

The ODP strap #1 web UI login is:
Username: admin
Passwork: admin

<hr />

<h2>Operating OpenDaylight SDN Controller Platform (OSCP) Bootstrap #2</h2>
Start a copy of the Controller.
<pre class="code-sample"><code>make start-sdnplatform
or
java -jar target/sdnplatform.jar</code></pre>

<hr />

To stop the controller:
<pre class="code-sample"><code>make stop-sdnplatform</code></pre>
<h2>Starting Wireshark For OpenFlow Packet Cpatures</h2>
If you want to run everything on another machine, ssh to the guest VM using "ssh -X " (upper case) to X11 forwarding.

<hr />

Double click the Wireshark icon on the desktop (run with sudo privs, ignore Lua error).
Capture -&gt; Interfaces -&gt; eth0. Then start the capture.

<hr />

Type "of" (no parentheses as seen below) in the filter window to ignore all packets other then OpenFlow packets.

<hr />

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/05/OpenFlow-Dissector.png" >}}" alt="Wireshark OpenFlow Dissector"></figure>

<hr />

<h2>Using Mininet For OpenFlow Testing
I recommend using X11 forwarding to the mininet instance in order to forward Wireshark w/X11 over the SSH session. Just ssh to the running VM with "ssh -XY ". Then you can run Wireshark off Mininet and tap an individual host if you need more granular tshooting then just on the controller. Alternatively, ask your vendor for a switch with OpenFlow support.</h2>
&nbsp;

<hr />

<ol class="legacy-numbers">
<ol>
	<li>1. Start the Mininet or physical switch.</li>
	<li>2. If physical switch piont it at the running VMs IP addr.</li>
	<li>3. If Mininet, start the mininet VM and from the CLI type:</li>
	<li>sudo mn --controller=remote --ip=&lt;insert_controller_ip&gt; ---port=6633 (Spin up a simple two host network) More at <a href="http://mininet.org" target="_blank">mininet.org</a></li>
</ol>

<hr />

</ol>
<h2><h2 class="legacy-heading">Testing With Mininet</h2>
<a href="http://mininet.org/download/" target="_blank" rel="noopener noreferrer">Download Mininet the OpenFlow Switch Emulator</a>
The newest version of mininet has a different syntax:
<pre class="code-sample"><code>sudo mn --mac --controller=remote -- --port=6633</code></pre>

<hr />

A video using Mininet w/ODP

<hr />

<p><a href="http://www.youtube.com/watch?v=hXWhgWMoNHM">Watch video on YouTube</a></p>

<hr />

Follow this tutorial for configuring ODP Bootstrap #1.
<a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank" rel="noopener noreferrer">OpenDaylight ODP Bootstrap #1</a>

<hr />

Follow this tutorial for configuring ODP Bootstrap #2.
<a href="https://wiki.opendaylight.org/view/OpenDaylight_SDN_Controller_Platform_(OSCP):Installation" target="_blank" rel="noopener noreferrer">OpenDaylight ODP (OSCP) Bootstrap #2</a>
There will be more in coming weeks as functionality increases and projects merge or even better, submit your own to the wiki or your own blog to get linked from the wiki.

<hr />

<h2>Section II. Installing the software on another machine</h2>
The rest of this section if for installing the software that is on the VM image in this repo. If you are just using that image, you don't need to install any of this. Building out your own lab rig would be good experience for anyone unfamiliar with Linux or building software.

<hr />

<h2>Installing a Hypervisor and Guest VM</h2>
Setting up a stripped down Ubuntu VM. Download the Minimal CD.
Ubuntu mini.iso - <a href="https://help.ubuntu.com/community/Installation/MinimalCD" target="_blank">https://help.ubuntu.com/community/Installation/MinimalCD</a>
A video of installing with VirtualBox can be found here:
<a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}" target="_blank" rel="noopener noreferrer">Open vSwitch and OpenFlow Lab Preparation</a>

<hr />

<h2>Installing OpenDaylight Controller Bootstrap #1</h2>
Once you have built the controller with Maven (mvm clean install). If the ./run.sh script is not in the target directory, then maven must not have built properly. FYI, you need Internet access to build bootstrap #1. If you have poor or congested Internet connection it could cause the maven build to fail. If the build fails, just delete the controller directory to eliminate that as a problem ( rm -rf controller/ ). Then download the controller again and run (mvn clean install).


In order to download and install on a Linux box, do the following. Since this is using JVM, it builds rather easily on any platform. Hmm platform agnostic..
<pre class="code-sample"><code>apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk
git clone http://git.opendaylight.org/gerrit/p/controller.git
cd controller/opendaylight/distribution/opendaylight/
mvn clean install
cd target/distribution.opendaylight-0.1.0-SNAPSHOT-osgipackage/opendaylight
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-i386/ (add to ~/.bashrc for ENV persistency)
#For 64-bit
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64/
./run.sh </code></pre>


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
If you don't feel like building the controller you can simply download the <a href="https://jenkins.opendaylight.org/controller/job/controller-nightly/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/" target="_blank">nightly build</a> as follows.
<pre class="code-sample"><code>
Download the nightly build at:
https://jenkins.opendaylight.org/controller/job/controller-nightly/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/
#Unzip
./run.sh </code></pre>

<h2> maven : Depends: libwagon2-java (&gt;= 2.2-2) but it is not going to be installed </h2>
<aside class="legacy-callout">
There is a Bug w/ Ubuntu 13.04 with a dependency. Force the package install and try it again to satisfy the dependancy.

### Error ###
% sudo apt-get install maven2
/*
The following packages have unmet dependencies:
maven : Depends: libwagon2-java (&gt;= 2.2-2) but it is not going to be installed
E: Unmet dependencies. Try 'apt-get -f install' with no packages (or specify a solution).
*/
### Workaround – force the package install: ###
% sudo dpkg -i --force-all /var/cache/apt/archives/libwagon2-java_2.2-3+nmu1_all.deb

### Then try Maven2 again and it should install: ###
% sudo apt-get install maven2

Bug at Launchpad:

[SRU] 2.2-3+nmu1 upgrade fails on conflict with libwagon-java
<a href="https://bugs.launchpad.net/ubuntu/+source/wagon2/+bug/1171056" target="_blank">https://bugs.launchpad.net/ubuntu/+source/wagon2/+bug/1171056</a></aside>
<h2>Installing OpenDaylight SDN Controller Platform (OSCP) Bootstrap #2</h2>
<pre class="code-sample"><code>sudo apt-get install unzip python-dev python-virtualenv build-essential ant git openjdk-7-jdk
git clone http://git.opendaylight.org/gerrit/p/net-virt-platform.git
cd net-virt-platform/
./setup.sh
make</code></pre>
<h2>Prepare the Bootstrap #2 CLI</h2>
<pre class="code-sample"><code>source /home/odp/net-virt-platform/workspace/ve/bin/activate
make stop-sdncon reset-cassandra start-sdncon</code></pre>
<h2>Installing Wireshark and the OpenFlow dissector</h2>
<pre class="code-sample"><code>apt-get update
apt-get install wireshark-dev wireshark mercurial git scons
hg clone https://bitbucket.org/barnstorm/of-dissector
cd of-dissector/src
alias sudo='sudo env WIRESHARK=/usr/include/wireshark/'
sudo scons install
#This creates a shared object (so) named openflow.so.
#Move openflow.so to the Wireshark plugin directory.
sudo mv /home/odp/.wireshark/plugins/openflow.so /usr/lib/wireshark/libwireshark2/plugins/</code></pre>

<hr />

Start Wireshark, look in Help-&gt;About-&gt;Plugins tab. You should see openflow.so as a listed dissector.

<hr />

<h2>Installing Eclipse For Bootstrap #1</h2>
Download Eclipse IDE for Java Developers:
<a href="http://www.eclipse.org/downloads/packages/eclipse-ide-java-developers/junosr2" target="_blank" rel="noopener noreferrer">Eclipse IDE for Java Developers</a>
Once you unzip the tar, find the Eclipse icon in the root directory and double click it to run Eclipse. It will ask you to choose a worksapce. Locate the workspace for either of the bootstraps in the ODP user directory. To switch between proposed bootstraps, go to File-&gt; Switch Workspace.
<pre class="code-sample"><code> tar xvfz eclipse-jee-juno-SR2-linux-gtk-x86_64.tar.gz</code></pre>
Instructions for importing Bootsrap #1 into Eclipse see:
<a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Eclipse_CLI_Setup" target="_blank">https://wiki.opendaylight.org/view/OpenDaylight_Controller:Eclipse_CLI_Setup</a>
<h2>Video for importing ODP Bootstrap #1 into Eclipse</h2>
Video for importing ODP Bootstrap #1 into Eclipse:
<a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Importing_OpenDaylight_Controller_into_Eclipse" target="_blank">OpenDaylight Controller:Importing OpenDaylight Controller into Eclipse</a>

I did this before I realized there were two bootstraps. As soon as time permits I will do the other proposed build. It doesn't use the OSGI modular framework, so it is pretty simple.
<a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Importing_OpenDaylight_Controller_into_Eclipse" target="_blank">https://wiki.opendaylight.org/view/OpenDaylight_Controller:Importing_OpenDaylight_Controller_into_Eclipse</a>
For a Pull only Eclipse build the following will get you started.

<hr />

<ol class="legacy-numbers">
<ol>
	<li>git clone http://git.opendaylight.org/gerrit/p/controller.git</li>
	<li>cd controller/opendaylight/distribution/opendaylight/</li>
	<li>From the CLI run -&gt; mvn clean install (5-10 minutes and requires decent bandwidth. It is slightly sensitve to lame bandwidth like my DSL.)</li>
	<li>Open Eclipse and install m2e.</li>
	<li>Help -&gt; Install software -&gt; "work with" enter the URI http://download.eclipse.org/technology/m2e/releases</li>
	<li>Choose the latest m2e release v1.3x. next, next, yes, finish, restart, etc.</li>
	<li>Import ODP: File -&gt; import -&gt; Maven -&gt; Existing Maven Project -&gt; Find the ODP dir. Anywhere at the top of the git clone</li>
	<li>Eclipse will parse out the pom.xml files and present all builds (leave everything checked). There should be 0 errors at this point.</li>
	<li>Click finish. Eclipse will install Tycho and buildhelper automatically. Next, next, finish, except warning of non-signed SW. Eclipse will ask to restart again.</li>
	<li>If a new install you will get the welcome screen again, just close that. Next Maven will reconcile the project, watch the status bar in the bottom right. Avoid too much clicking around until it is done to avoid any issues.</li>
	<li>After the bottom right status gets to 100%. In the left window, drill down into distribution.opendaylight. Find opendaylight.assembleit.launch, right click on it -&gt; run-as -&gt; 1. assembleit.launch. Maven will again build the project for a few minutes. You will likely have some errors in the bottom window and can likely ignore them.</li>
	<li>If successful, the console will eventually return "[INFO] Build Seccesful".</li>
	<li>You can now run the controller directly from Eclipse by right clicking on "opendaylight-application.launch" -&gt; run-as -&gt; oepndaylight-application. To stop the controller click the red square red stop button.</li>
</ol>
</ol>

<hr />

<h2>Importing ODP Bootstrap #2 into Eclipse</h2>
Instructions for importing Bootsrap #2 into Eclipse see:
<a href="https://wiki.opendaylight.org/view/OpenDaylight_SDN_Controller_Platform_(OSCP):Installation" target="_blank">https://wiki.opendaylight.org/view/OpenDaylight_SDN_Controller_Platform_(OSCP):Installation</a>

<hr />

In the netvirt directory:
<pre class="code-sample"><code> make eclipse</code></pre>
Import "sdnplatform" project into any eclipse workspace
<h2>Installing Open vSwitch as a Forwarding Element</h2>
OVS can be used much like mininet for integrating hosts, and is by many HW vendors.
<pre class="code-sample"><code>apt-get install openvswitch-datapath-source bridge-utils
module-assistant auto-install openvswitch-datapath
apt-get install openvswitch-brcompat openvswitch-common openvswitch-controller </code></pre>
Once installed, you can create a <a href="http://openvswitch.org" target="_blank">Open vSwitch</a> bridge on the host, attach a physical interface to the bridge and attach it to the controller.

<pre class="code-sample"><code>ovs-vsctl add-br br-int
$ ovs-vsctl add-port br-int eth0
$ ifconfig eth0 0
#Zero out your eth0 interface and slap it on the bridge interface
#(warning will clip you unless you script it)
$ifconfig br-int 192.168.1.208 netmask 255.255.255.0
#Change your default route
$route add default gw 192.168.1.1 br-int and $route del default gw 192.168.1.1 eth0
ovs-vsctl set-controller br-int tcp:192.168.1.208:6633</code></pre>

<hr />

More on Open vSwitch in some other tutorials <a href="{{< relurl "/tag/openvswitch/" >}}" target="_blank">here</a>, or a <a href="{{< relurl "/openflow-openvswitch-and-kvm-sdn-lab-installation-app/" >}}" target="_blank">Python installer</a> I wrote that will build some different options of KVM, Open vSwitch and various controllers. Leave out the controller option since ODP is the bees knees.

controller/opendaylight/distribution/opendaylight
Update OpenDaylight with Maven and Git</h2>

To update the OpenDaylight bootstraps, just pull the changed files from the repository and in the case of the Maven project rebuild it. If you are modifying code in Eclipse, you can just right click on the bundle, top level right click, run-as "maven build". A popup window will appear and choose "opendaylight-assembleit-fast: clean install". Eclipse will build that module assuming its not broken :)
<pre class="code-sample"><code>
## Update the clone with the latest files from the clone root directory.
git pull
controller/opendaylight/distribution/opendaylight
## Rebuild with Maven
mvn clean install
</code></pre>

For the net-virt controller. It easier with just a "git pull" and "make" from the net-virt root directory.
<h2 class="legacy-heading">Help Shape The Future</h2>
If you have the cycles, come contribute to the project. It is a great time to shape the direction of networking. This is one of those 15-20 year disruptions that come about that will take another decade+ to absorb. It doesn't matter who you work for, who you know, what consortium you belong to or any other exclusion. I am happy to give you my humble advice on a good place to start or how to get up to speed to. You dont have to be a programmer to contribute. Lots of documentation and architectural frameworks need to be created so jump in! Even just learning about OpenFlow / SDN and sharing that with someone else is a contribution. Hopefully this can cut down on basic build problems to keep dev focused. I will update as ODP milestones make sense.

<hr />

Feel free to contact me for information and be sure to join the <a href="https://lists.opendaylight.org/pipermail/" target="_blank">OpenDaylight mailing lists</a> to share and collaborate with others using SDN. For support using the projects check out the <a href="https://lists.opendaylight.org/pipermail/net-virt-platform-users/" target="_blank">Bootstrap #2 net-virt-platform-users</a> and <a href="https://lists.opendaylight.org/pipermail/controller-users/">Bootstrap #1 controller-users</a> for help. There aren't very many questions yet, but any questions get answered quickly.

<ul>
	<li><a href="http://mrfogg97.blogspot.com/2013/04/opendaylight-sdn-on-windows.html" target="_blank">OpenDaylight SDN on Windows</a></li>
	<li><a href="http://www.dasblinkenlichten.com/installing-opendaylight-on-centos/" target="_blank">Installing OpenDaylight on CentOS</a></li>
	<li><a href="http://packetpushers.net/show-148-talking-with-opendaylight-leadership/" target="_blank">Packet Pushers - Talking With OpenDaylight Leadership</a></li>
</ul>
