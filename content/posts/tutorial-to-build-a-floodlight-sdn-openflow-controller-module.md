+++
title = "Tutorial to Build a FloodLight SDN OpenFlow Controller Module"
date = "2012-11-11T06:35:55+00:00"
lastmod = "2013-03-27T02:00:19+00:00"
author = "Brent Salisbury"
wp_id = 3821
categories = ["In the Lab", "Programming"]
tags = ["Java", "OpenFlow", "Programming", "Software Defined Networking", "Tutorials"]
description = ""
url = "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/"
image = "/wp-content/uploads/2012/11/programming.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "9d881f3585048d66451a05aa131ae76c0291000c37b2b7d0434f5eec5f8079a7"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Tutorial to Build a FloodLight SDN OpenFlow Controller Module</h2>
This how-to is a tutorial to build a FloodLight SDN OpenFlow controller module in Java using the open source OpenFlow controller FloodLight that BigSwitch open sourced to the community. The installation and class creation is documented on the FloodLight <a href="http://www.openflowhub.org/display/floodlightcontroller/Installation+Guide" target="_blank">Wiki</a>. I am adding a screencast of the installation for those who get stuck on any steps. This is just how to extract PacketIn fields, the next step is to create custom actions that can be programmatically executed. If comfortable with getting Floodlight up and running in a development environment you could skip to the 2nd post the not only extracts the packet-in but also a FlowMod is performed: F<a href="{{< relurl "/floodlight-openflow-controller-using-the-static-flow-entry-pusher/" >}}" target="_blank">loodlight OpenFlow Controller: Using the Static Flow Entry Pusher</a>
<h2>Preparing the System for Eclipse and FloodLight</h2>

<ul>
	<li>The screencast is on a Mac running <a href="http://www.vmware.com/products/fusion/overview.html" target="_blank">VMWare Fusion</a> but VirtualBox works just the same for this tutorial and is free. VirtualBox can be downloaded <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">here</a>.</li>
	<li>The OS is Ubuntu 12.04 installed on a VM. A tutorial for preparing the Ubuntu image is <a href="{{< relurl "/openvswitch-and-openflow-lab-preparation/" >}}" target="_blank">here</a>. Just any vanilla Ubuntu or any other Linux distro will cover it so use whatever you like.</li>
	<li>Mac installation is about the exact same.</li>
	<li>Windows will need some trickery to get <a href="http://ant.apache.org/manual/install.html" target="_blank">Apache Ant</a> built.</li>
</ul>

<h2>Install the FloodLight OpenFlow SDN Controller</h2>

The following is from the <a href="http://www.openflowhub.org/display/floodlightcontroller/Installation+Guide" target="_blank">FloodLight Wiki Installation Guide</a>. It's perfect so no need to rewrite it.
<pre class="brush: bash; gutter: true">sudo apt-get install build-essential default-jdk ant python-dev eclipse
git clone git://github.com/floodlight/floodlight.git
cd floodlight
ant eclipse</pre>
<em>Open eclipse and create a new workspace (i<strong>nside Eclipse)</strong> :</em>

<ul>
	<li><strong>./eclipse &amp;</strong> &lt;-Non-root from the command line or find the icon to launch it Eclipse.</li>
	<li>File -&gt; Import -&gt; General -&gt; Existing Projects into Workspace. Then click “Next”.</li>
	<li>From “Select root directory” click “Browse”. Select the parent directory where you placed floodlight earlier.</li>
	<li>Check the box for “Floodlight”. No other Projects should be present and none should be selected.</li>
	<li>Click Finish.</li>
</ul>

<strong>Create the FloodlightLaunch target (inside Eclipse):</strong>

<ul>
	<li>Click Run-&gt;Run Configurations</li>
	<li>Right Click Java Application-&gt;New</li>
	<li>For Name use FloodlightLaunch</li>
	<li>For Project use Floodlight</li>
	<li>For Main use net.floodlightcontroller.core.Main</li>
	<li>Click Apply</li>
</ul>



<h2>Add a Class In Eclipse</h2>

I am naming this class HeaderExtract. A package is normally lower case "headerextract" while the class inside the package is named with some upper cases "HeaderExtract"
<ol class="legacy-numbers">
<ul>
<ol>
	<li>Expand the “floodlight” item in the Package Explorer and find the “src/main/java” folder.</li>
	<li>Right-click on the “src/main/java” folder and choose “New/Class.”</li>
	<li>Enter “net.floodlightcontroller.headerextract” in the “Package” box.</li>
	<li>Enter “HeaderExtract” in the “name” box.</li>
	<li>Next to the “Interfaces” box, choose “Add…”</li>
	<li>Type “IOFMessageListener” into the search box, and choose “OK.”</li>
	<li>Type “IFloodlightModule” into the search box, and choose “OK.”</li>
	<li>Click “Finish” in the dialog.</li>
</ol>
</ul>
</ol>

<ul>
	<li>Next add net.floodlightcontroller.headerextract.HeaderExtract to the default startup modules in:</li>
</ul>

<pre class="brush: text; gutter: false">src/main/resources/floodlightdefault.properties
src/main/resources/META-INF/services/net.floodlight.core.module.IFloodlightModule</pre>
floodlightdefault.properties should look something like this:
<pre class="brush: text; gutter: true">floodlight.modules = net.floodlightcontroller.storage.memory.MemoryStorageSource,\
net.floodlightcontroller.core.FloodlightProvider,\
net.floodlightcontroller.threadpool.ThreadPool,\
net.floodlightcontroller.devicemanager.internal.DeviceManagerImpl,\
net.floodlightcontroller.devicemanager.internal.DefaultEntityClassifier,\
net.floodlightcontroller.staticflowentry.StaticFlowEntryPusher,\
net.floodlightcontroller.firewall.Firewall,\
net.floodlightcontroller.forwarding.Forwarding,\
net.floodlightcontroller.linkdiscovery.internal.LinkDiscoveryManager, \
net.floodlightcontroller.topology.TopologyManager, \
net.floodlightcontroller.flowcache.FlowCache, \
net.floodlightcontroller.flowcache.FlowReconcileManager, \
net.floodlightcontroller.jython.JythonDebugInterface,\
net.floodlightcontroller.counter.CounterStore,\
net.floodlightcontroller.perfmon.PktInProcessingTime,\
net.floodlightcontroller.ui.web.StaticWebRoutable,\
net.floodlightcontroller.headerextract.HeaderExtract
net.floodlightcontroller.restserver.RestApiServer.port = 8080
net.floodlightcontroller.core.FloodlightProvider.openflowport = 6633
net.floodlightcontroller.jython.JythonDebugInterface.port = 6655
net.floodlightcontroller.forwarding.Forwarding.idletimeout = 5
net.floodlightcontroller.forwarding.Forwarding.hardtimeout = 0</pre>
<pre class="brush: text; gutter: false">src/main/resources/META-INF/services/net.floodlight.core.module.IFloodlightModule</pre>
net.floodlight.core.module.IFloodlightModule should look something like this:
<pre class="brush: text; gutter: true">net.floodlightcontroller.core.FloodlightProvider
net.floodlightcontroller.storage.memory.MemoryStorageSource
net.floodlightcontroller.devicemanager.internal.DeviceManagerImpl
net.floodlightcontroller.linkdiscovery.internal.LinkDiscoveryManager
net.floodlightcontroller.topology.TopologyManager
net.floodlightcontroller.forwarding.Forwarding
net.floodlightcontroller.flowcache.FlowCache
net.floodlightcontroller.flowcache.FlowReconcileManager
net.floodlightcontroller.core.OFMessageFilterManager
net.floodlightcontroller.staticflowentry.StaticFlowEntryPusher
net.floodlightcontroller.perfmon.PktInProcessingTime
net.floodlightcontroller.perfmon.NullPktInProcessingTime
net.floodlightcontroller.restserver.RestApiServer
net.floodlightcontroller.learningswitch.LearningSwitch
net.floodlightcontroller.hub.Hub
net.floodlightcontroller.jython.JythonDebugInterface
net.floodlightcontroller.counter.CounterStore
net.floodlightcontroller.counter.NullCounterStore
net.floodlightcontroller.threadpool.ThreadPool
net.floodlightcontroller.ui.web.StaticWebRoutable
net.floodlightcontroller.virtualnetwork.VirtualNetworkFilter
net.floodlightcontroller.devicemanager.internal.DefaultEntityClassifier
net.floodlightcontroller.devicemanager.test.MockDeviceManager
net.floodlightcontroller.core.test.MockFloodlightProvider
net.floodlightcontroller.core.test.MockThreadPoolService
net.floodlightcontroller.firewall.Firewall
net.floodlightcontroller.headerextract.HeaderExtract</pre>
Keep in mind those modules are subject to change as new modules are added into the FloodLight trunk. The main reason I pasted it is in case it is confusing on where to paste the module you want to add.

<h2>Add code to your new Class</h2>

This is once you created your class you will have a skeleton configuration. You can delete what is in "HeaderExtract.java" and replace it with the code below. The only difference from the MacTracker tutorial is some of the imports and the initialization method. We are capturing the packet-in the same way but just pulling a couple of different fields than the MacTracker class.
<pre class="brush: java; gutter: true">package net.floodlightcontroller.headerextract;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.openflow.protocol.OFMatch;
import org.openflow.protocol.OFMessage;
import org.openflow.protocol.OFPacketIn;
import org.openflow.protocol.OFType;
import org.openflow.util.HexString;
import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.packet.BasePacket;
import net.floodlightcontroller.packet.Ethernet;
import net.floodlightcontroller.packet.IPv4;
import net.floodlightcontroller.staticflowentry.IStaticFlowEntryPusherService;
public class HeaderExtract implements IFloodlightModule, IOFMessageListener {
public final int DEFAULT_CACHE_SIZE = 10;
 protected IFloodlightProviderService floodlightProvider;
 private IStaticFlowEntryPusherService flowPusher;
@Override
 public String getName() {
 return &quot;Names&quot;;
 }
 @Override
 public boolean isCallbackOrderingPrereq(OFType type, String name) {
 return false;
 }
 @Override
 public boolean isCallbackOrderingPostreq(OFType type, String name) {
 return false;
 }
//This is where we pull fields from the packet-in
 @Override
 public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
 BasePacket pkt = (BasePacket) IFloodlightProviderService.bcStore.get(cntx, IFloodlightProviderService.CONTEXT_PI_PAYLOAD);
 //Instantiate two objects for OFMatch and OFPacketIn
 OFPacketIn pin = (OFPacketIn) msg;
 OFMatch match = new OFMatch();
 match.loadFromPacket(pin.getPacketData(), pin.getInPort());
//Destination IP Address for each packet-in
System.out.println(&quot;$$$$$-Get the Desitnation IP Address-$$$$$&quot;);
System.out.println(IPv4.fromIPv4Address(match.getNetworkDestination()));
// Source Mac Address for each packet-in
System.out.println(&quot;$$$$$-Mac Address Destination-$$$$$$&quot;);
Long sourceMACHash = Ethernet.toLong(match.getDataLayerDestination());
System.out.println(HexString.toHexString(sourceMACHash));
//Here we print the entire packet-in array which has all matchable fields
System.out.println(&quot;$$$$$-PacketIn ARRAY-$$$$$&quot;);
System.out.println(Arrays.asList(match));

return Command.CONTINUE;
}
@Override
public Collection&lt;Class&lt;? extends IFloodlightService&gt;&gt; getModuleServices() {
// TODO Auto-generated method stub
return null;
}
@Override
public Map&lt;Class&lt;? extends IFloodlightService&gt;, IFloodlightService&gt; getServiceImpls() {
// TODO Auto-generated method stub
return null;
}
@Override
public Collection&lt;Class&lt;? extends IFloodlightService&gt;&gt; getModuleDependencies() {
Collection&lt;Class&lt;? extends IFloodlightService&gt;&gt; l = new ArrayList&lt;Class&lt;? extends IFloodlightService&gt;&gt;();
l.add(IFloodlightProviderService.class);
return l;
}

@Override
public void init(FloodlightModuleContext context)
throws FloodlightModuleException {
floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
}
@Override
public void startUp(FloodlightModuleContext context) {
floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
}
}</pre>

<ul>
	<li>Paste the above code into HeaderExtract.java and save it. Then run configuration and hopefully you don't get too many errors. Refer to the video to see if you missed a step.</li>
</ul>

<h2>PacketIn Extract</h2>

The guts of this class is capturing the packet-in and extracting the L2-L4 headers, convert them from binary using various modules. The snippet below extracts the packet-in fields and displays them as a string. I am just using "println" function to spit out STDOUT. MacTracker uses a logging module that is sexier. The key is getting all of the various fields and then having the flexibility to instantiate whatever you want into the fields and even further down the road whatever meta-data you want to inject. This extensibility is easier in software switching today, but presumably will improve in hardware in the future.
<ul>
	<li>Quick look at a snippet:</li>
</ul>
<pre class="brush: text; gutter: true">System.out.println(&quot;$$$$-PacketIn ARRAY-$$$$&quot;); &lt;--Just a string denoting the beginning of the next line.
System.out.println(Arrays.asList(match)); &lt;-Print the packet-in OFMatch object elements packed in an array</pre>
<ul>
	<li>The output in your console will look like this:</li>
</ul>
<pre class="brush: text; gutter: true">$$$$$$$$$$$$-PacketIn ARRAY-$$$$$$$$$$$$
[OFMatch[in_port=1,dl_dst=ff:ff:ff:ff:ff:ff,dl_src=e6:69:06:a0:98:0b,dl_type=0x806,dl_vlan=0xffff,dl_vlan_pcp=0,nw_dst=10.0.0.3,nw_src=10.0.0.2,nw_proto=1,nw_tos=0,tp_dst=1,tp_src=0]]</pre>
<h2>Download Install Mininet that acts as an OpenFlow enabled vSwitch</h3>
</h2>
<ul>
	<li>Download Mininet from <a href="http://yuba.stanford.edu/foswiki/bin/view/OpenFlow/MininetGettingStarted" target="_blank">here</a>.</li>
	<li>Installation instructions are <a href="http://yuba.stanford.edu/foswiki/bin/view/OpenFlow/MininetVMSetupNotes" target="_blank">here</a>.</li>
</ul>

Essentially its pretty easy peasy, just download and extract the image and start it in your hypervisor (VM Fusion, VirtualBox). You will now have two VMs if you are nesting both your Linux image and Mininet or just one if you are running Eclipse on your Mac/Linux/Windows native OS.

Once installed and booted the following should get you going.
<pre class="brush: bash; gutter: true">ifconfig eth0 &lt;-grab the IP address of the device.
sudo passwd root &lt;- Optional but I do everything as root in this.
apt-get install ssh</pre>

<h2>TRealtime OpenFlow SDN Magic on the FloodLight Controller</h2>

ssh to your Mininet instance with the following:
<pre class="brush: bash; gutter: true">ssh -YC root@&lt;insert ip address of the Mininet host from ifconfig eth0&gt; 
mn --controller=remote --ip=&lt;Eclipse Floodlight IP&gt; --port=6633</pre>
Start FloodLight in Eclipse and you should see Mininet attach to the controller.

From your ssh window some commands to get started are:

<ul>
	<li>pingall &lt;-H2 (host2) and H3 (host3) will ping one another.</li>
	<li>dump &lt;-Displays the configuration and IPs</li>
	<li>Help &lt;- Well you get this one.</li>
	<li>xterm h2 &lt;- Will spawn an Xterm window that gives you the console on h2.</li>
	<li>(In Xterm) tcpdump -XX -n &lt;-Will run tcpdump from the host perspective.</li>
	<li>You can also run Wireshark over the SSH session and capture any of the interfaces with 'wireshark' from the command line.</li>
</ul>


<h2>ScreenCast of the Build</h2>
<p><a href="http://www.youtube.com/watch?v=v-64jQnTDsY&hd=1">Watch video on YouTube</a></p>
<hr>

If interested, get involved in the <a href="http://openvswitch.org" target="_blank">OpevSwitch</a> and <a href="http://www.openflowhub.org/display/Home/OpenFlowHub" target="_blank">Openflow</a> communities. Anyone can be part of shaping the industry in the coming years. I can attest that folks from <a href="http://bigswitch.com" target="_blank">BigSwitch</a> like Paul Lappas, Nick Bastin, Alex Riemers and (KC) Wang and everyone else I have meet or spoken with online are all super helpful in fostering the FloodLight dev community. They have amazing tutorials on their wiki and OpenFlow hub found <a href="http://floodlight.openflowhub.org" target="_blank">here</a>.
<hr>
<aside class="legacy-callout"><strong>Building OpenFlow Applications</strong>The second part of this tutorial can be found at <a href="{{< relurl "/floodlight-openflow-controller-using-the-static-flow-entry-pusher/" >}}" target="_blank">Floodlight OpenFlow Controller: Using the Static Flow Entry </a></aside>

Thanks for stopping by!
<hr />