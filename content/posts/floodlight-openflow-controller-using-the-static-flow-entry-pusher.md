+++
title = "Floodlight OpenFlow Controller: Using the Static Flow Entry Pusher"
date = "2012-12-10T04:22:04+00:00"
lastmod = "2014-02-18T02:53:55+00:00"
author = "Brent Salisbury"
wp_id = 4974
categories = ["In the Lab", "Programming"]
tags = ["Java", "OpenFlow", "Programming", "Software Defined Networking", "Tutorials"]
description = ""
url = "/floodlight-openflow-controller-using-the-static-flow-entry-pusher/"
image = "/wp-content/uploads/2013/04/Openflow-Programming-header-sm.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "79fada2cbd27faa17ad192db2ae635ef76660adfc2461eb773b356bc7ae719cc"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Floodlight OpenFlow Controller: Using the Static Flow Entry Pusher</h2>
Floodlight OpenFlow Controller: Using the Static Flow Entry Pusher: The first post in this tutorial can be found at <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">Tutorial to Build a FloodLight SDN OpenFlow Controller </a>.

<hr />

For those looking to do things with early SDN / OpenFlow controllers this post may be of some use to kickstart your efforts. I am posting a Java class below that Cory Fowler and I put together. There are lots of good guides out there but what exactly I was looking for was unavaialble at the time.
<h2>Packet-in Logic</h2>
The goal was to get the framework together for this <a href="{{< relurl "/sdn-using-dns-naming-for-classification/" >}}" target="_blank">project</a>, but I didn't see anything out there that did it from within Floodlight with a Java module. Fortunately, the guys from BigSwitch built a nice module that abstracted some of the nuances of doing a FlowMod like OFAction fields, setting lengths, flushing between flows and the dozens of other little gotchas that need layers of abstraction to simplify.
<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/12/FowMod-OpenFlow.jpg" >}}" alt="OpenFlow FlowMod"></figure>
<h2>Using the Floodlight Static Flow Entry Pusher Service</h2>
What this allows for is to proactively instantiate a static flow to define a predetermined path based on a match and then the corresponding action.
<aside class="legacy-callout"><strong>Simple OpenFlow workflow</strong>The flow logic looks like the following minus lots of details:</aside>
<ol class="legacy-numbers">
<ol>
	<li>Flow comes into the OpenFlow enabled switch.</li>
	<li>Switch looks in its forwarding table to see if there is a match. If there is a match the switch forwards that packet per the forwarding table instruction. The matches can either be a coarse match like anything destined to IPv4 10.0.0.0/8 ---&gt; do this action, or as fine as anything matching {port 80, mac addr 0000.1111.2222, dest_ipv4 10.1.1.1/32, (any other tuple in the header) etc}. Think traditional _access-lists_.</li>
	<li>If there is not a matching flow in the switch an event is triggered creating a packet-in packet to the controller where the logic in the code below could be processed.</li>
	<li>After the controller determines an action it then creates a packet-out packet that tells the switch what action to take with that flow and subsequent packets in that same flow.</li>
</ol>
<div></ol></div>
<aside class="legacy-callout"><strong>Note on a FlowMod for IPv4 destination prefix matching</strong>If you are matching on a IPv4 destination you need to set the ethertype per the OpenFlow spec. In the next section code, that looks like: .setDataLayerType(Ethernet.TYPE_IPv4) </aside>

The method to add a flow requires three parameters addFlow(String name, OFFlowMod fm, String swDpid);

<ol class="legacy-numbers">
<ol>
	<li><em>String name:</em> The name variable is an arbitrary name, but it must be unique to the static flow. If you use the same name it will be overwritten. Very similar to access list line numbers.</li>
	<li><em>OFFlowMod fm:</em> fm is the flow to push.</li>
	<li>S<em>tring swDpid:</em> Is the switch datapath ID (DPID) to push it to. The Mininet default DPID is 00:00:00:00:00:00:00:01.</li>
</ol>
</ol>
<aside class="legacy-callout"><strong>Floodlight package net.floodlightcontroller.staticflowentry Javadoc</strong>The package net.floodlightcontroller.staticflowentry is documented at the <a href="http://floodlight.openflowhub.org/files/javadoc/net/floodlightcontroller/staticflowentry/package-summary.html" target="_blank">OpenFlow Hub</a>.</aside>
Below is a module that I threw together for this post but mainly as part of another project, ehem* disclaimer if completely inefficient :-)
<pre class="brush: java; gutter: true">//net.floodlightcontroller.names is a created package for something else, not part of FloodLight to make sure there isn&#039;t any confusion.
 package net.floodlightcontroller.names;
import java.util.ArrayList;
 import java.util.Collection;
 import java.util.List;
 import java.util.Map;
import org.openflow.protocol.OFFlowMod;
 import org.openflow.protocol.OFMatch;
 import org.openflow.protocol.OFMessage;
 import org.openflow.protocol.OFPacketIn;
 import org.openflow.protocol.OFType;
 import org.openflow.protocol.action.OFAction;
 import org.openflow.protocol.action.OFActionOutput;
import net.floodlightcontroller.core.FloodlightContext;
 import net.floodlightcontroller.core.IFloodlightProviderService;
 import net.floodlightcontroller.core.IOFMessageListener;
 import net.floodlightcontroller.core.IOFSwitch;
 import net.floodlightcontroller.core.module.FloodlightModuleContext;
 import net.floodlightcontroller.core.module.FloodlightModuleException;
 import net.floodlightcontroller.core.module.IFloodlightModule;
 import net.floodlightcontroller.core.module.IFloodlightService;
 import net.floodlightcontroller.packet.Ethernet;
 import net.floodlightcontroller.packet.IPv4;
 import net.floodlightcontroller.staticflowentry.IStaticFlowEntryPusherService;
 //import net.floodlightcontroller.staticflowentry.StaticFlowEntryPusher;
public class Names implements IFloodlightModule, IOFMessageListener {
protected IFloodlightProviderService floodlightProvider;
 protected IStaticFlowEntryPusherService staticFlowEntryPusher;
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
@Override
 public net.floodlightcontroller.core.IListener.Command receive(
 IOFSwitch sw, OFMessage msg, FloodlightContext cntx ) {
String dp = &quot;00:00:00:00:00:00:00:01&quot;;
 OFPacketIn pi = (OFPacketIn) msg;
 OFMatch match = new OFMatch();
 match.loadFromPacket(pi.getPacketData(), (short) 0);
 System.out.println(&quot;$$$$$$$$$OFMATCH$$$$$$$$$$$&quot;);
 System.out.println(match);
 System.out.println(&quot;$$$$$$$$$IP-Destination$$$$$$$$$$$&quot;);
 System.out.println(&quot;$$$$$$$$$IP-Destination$$$$$$$$$$$&quot;);
 System.out.println(IPv4.fromIPv4Address(match.getNetworkDestination()));
//IPv4-To
 List actionsTo = new ArrayList();
 // Declare the flow
 OFFlowMod fmTo = new OFFlowMod();
 fmTo.setType(OFType.FLOW_MOD);
 // Declare the action
 OFAction outputTo = new OFActionOutput((short) 2);
 actionsTo.add(outputTo);
 // Declare the match
 OFMatch mTo = new OFMatch();
 mTo.setNetworkDestination(IPv4.toIPv4Address(&quot;10.0.0.3&quot;));
 mTo.setDataLayerType(Ethernet.TYPE_IPv4);
 fmTo.setActions(actionsTo);
 fmTo.setMatch(mTo);
 // Push the flow
 staticFlowEntryPusher.addFlow(&quot;FlowTo&quot;, fmTo, dp);
//IPv4-From
 List actionsFrom = new ArrayList();
 // Declare the flow
 OFFlowMod fmFrom = new OFFlowMod();
 fmFrom.setType(OFType.FLOW_MOD);
 // Declare the action
 OFAction outputFrom = new OFActionOutput((short) 1);
 actionsFrom.add(outputFrom);
 // Declare the match
 OFMatch mFrom = new OFMatch();
 mFrom.setNetworkDestination(IPv4.toIPv4Address(&quot;10.0.0.2&quot;));
 mFrom.setDataLayerType(Ethernet.TYPE_IPv4);
 fmFrom.setActions(actionsFrom);
 fmFrom.setMatch(mFrom);
 // Push the flow
 staticFlowEntryPusher.addFlow(&quot;FlowFrom&quot;, fmFrom, dp);
//ToArp
 List actionsToArp = new ArrayList();
 // Declare the flow
 OFFlowMod fmToArp = new OFFlowMod();
 fmToArp.setType(OFType.FLOW_MOD);
 // Declare the action
 OFAction outputToArp = new OFActionOutput((short) 2);
 actionsToArp.add(outputToArp);
 // Declare the match
 OFMatch mToArp = new OFMatch();
 mToArp.setNetworkDestination(IPv4.toIPv4Address(&quot;10.0.0.3&quot;));
 mToArp.setDataLayerType(Ethernet.TYPE_ARP);
 fmToArp.setActions(actionsToArp);
 fmToArp.setMatch(mToArp);
 // Push the flow
 staticFlowEntryPusher.addFlow(&quot;FlowToArp&quot;, fmToArp, dp);
//ArpFrom
 List actionsFromArp = new ArrayList();
 // Declare the flow
 OFFlowMod fmFromArp = new OFFlowMod();
 fmFromArp.setType(OFType.FLOW_MOD);
 // Declare the action
 OFAction outputFromArp = new OFActionOutput((short) 1);
 actionsFromArp.add(outputFromArp);
 // Declare the match
 OFMatch mFromArp = new OFMatch();
 mFromArp.setNetworkDestination(IPv4.toIPv4Address(&quot;10.0.0.2&quot;));
 mFromArp.setDataLayerType(Ethernet.TYPE_ARP);
 fmFromArp.setActions(actionsFromArp);
 fmFromArp.setMatch(mFromArp);
 // Push the flow
 staticFlowEntryPusher.addFlow(&quot;FlowFromArp&quot;, fmFromArp, dp);
System.out.println(&quot;$$$$$$$$$OFMATCH$$$$$$$$$$$&quot;);
 System.out.println(mTo);
return Command.CONTINUE;
 }
@Override
 public Collection&lt;Class&gt; getModuleServices() {
 // TODO Auto-generated method stub
 return null;
 }
@Override
 public Map&lt;Class, IFloodlightService&gt; getServiceImpls() {
 // TODO Auto-generated method stub
 return null;
 }
 //Service Class l.add(IStaticFlowEntryPusherService.class);
 @Override
 public Collection&lt;Class&gt; getModuleDependencies() {
 Collection&lt;Class&gt; l = new ArrayList&lt;Class&gt;();
 l.add(IFloodlightProviderService.class);
 l.add(IStaticFlowEntryPusherService.class);
 return l;
 }
// Context object SFP Class
 @Override
 public void init(FloodlightModuleContext context)
 throws FloodlightModuleException {
 floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
 staticFlowEntryPusher = context.getServiceImpl(IStaticFlowEntryPusherService.class);
 }
@Override
 public void startUp(FloodlightModuleContext context) {
 floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
 }
 }</pre>
<h2>Testing the Class with Mininet</h2>
For testing I normally use <a href="http://yuba.stanford.edu/foswiki/bin/view/OpenFlow/Mininet" target="_blank">Mininet</a>. If you look at the first <a href="{{< relurl "/tutorial-to-build-a-floodlight-sdn-openflow-controller-module/" >}}" target="_blank">post</a> you can see the video and how to attach mininet switches to the controller running in Eclipse and use Xterm to source traffic from your simulated hosts.
<h2>Additional OpenFlow SDN Development Resources</h2>
Here are some open source OpenFlow controller projects and links to their documentation tutorials and guides.

<ul>
	<li><span style="text-decoration: underline;"><a href="http://www.openflowhub.org/display/floodlightcontroller/Floodlight+Documentation" target="_blank">Floodlight</a></span> - Lots of nice documents for developers to understand how to get started. The Floodlight <span style="text-decoration: underline;"><a href="https://groups.google.com/a/openflowhub.org/forum/?fromgroups#!forum/floodlight-dev" target="_blank">listserv</a> </span>is very helpful also.</li>
	<li><span style="text-decoration: underline;"><a href="https://openflow.stanford.edu/display/Beacon/" target="_blank">Beacon</a></span> - David has lots of good <span style="text-decoration: underline;"><a href="https://openflow.stanford.edu/display/Beacon/Guides" target="_blank">tutorials</a></span> at the Beacon OpenFlow homepage. FloodLight was built on top of Ericksons controller Beacon. David is a nice guy that does an amazing job answering questions on the Beacon forum. Pretty neat to have the chance to ask questions directly from a pioneer like him. He has just updated his development tutorial so take a look at <span style="text-decoration: underline;"><a href="http://www.openflow.org/wk/index.php/OpenFlow_Tutorial#Create_Learning_Switch" target="_blank">Creating a Learning Switch</a></span> and help with feedback on the <span style="text-decoration: underline;"><a href="https://openflow.stanford.edu/forums/topic/243-looking-for-beta-testers/" target="_blank">Beacon forum</a></span> if interested.</li>
	<li><span style="text-decoration: underline;"><a href="http://www.noxrepo.org/pox/about-pox/" target="_blank">POX</a> </span>- For those more comfortable with programming with <span style="text-decoration: underline;"><a href="{{< relurl "/tag/python/" >}}" target="_blank">Python</a></span> have a look at Murphy McCauley's project POX. Murphy is another very accessible community oriented researcher.</li>
	<li>For those wanting to just get a basic understanding of OpenFlow or even just watch a video of it and  don't care about the nitty gritty programming details, this <span style="text-decoration: underline;"><a href="{{< relurl "/openflow-openvswitch-lab/" >}}" target="_blank">tutorial</a></span> I did a while back. It needs a makeover but its probably enough to get the point. I need to update it but its just basic usage of the <span style="text-decoration: underline;"><a href="http://www.openflowhub.org/display/floodlightcontroller/REST+API" target="_blank">RESTful Floodlight API</a></span>.</li>
</ul>


Programming applications directly into OpenFlow primitives is likely not the path for any semblance of DevOps networking gets in to. There will be additional layers that will enable :<em>Policy in -&gt; Flows out</em>. These additional layers are cropping up in the form of APIs and additional languages that are creating the SDN policy wood chipper to create flows. I discussed a couple of those projects in this post: <a href="{{< relurl "/software-defined-network-sdn-looking-toward-2013-part-1/" >}}" target="_blank">Software Defined Network (SDN) -Looking Toward 2013</a>
<hr />

Here are some additional reading on networking APIs from some friends:

<ul>
	<li><span style="text-decoration: underline;"><a href="http://nerdtwilight.wordpress.com/2012/09/18/northbound-api-the-standardization-debate/" target="_blank"><em>Brad Casemore</em></a></span></li>
	<li><span style="text-decoration: underline;"><a href="http://etherealmind.com/northbound-api-southbound-api-eastnorth-lan-navigation-in-an-openflow-world-and-an-sdn-compass/" target="_blank"><em>Greg Ferro</em></a></span></li>
	<li><span style="text-decoration: underline;"><a href="http://blog.ioshints.info/2012/09/sdn-controller-northbound-api-is.html" target="_blank"><em>Ivan Pepelnjak</em></a></span></li>
	<li><span style="text-decoration: underline;"><a href="http://www.sdncentral.com/sdn-blog/openflow-northbound-api-olympics/2012/07/" target="_blank"><em>Roy Chua</em></a></span></li>
	<li><span style="text-decoration: underline;"><a href="http://wiki.openstack.org/Quantum" target="_blank"><em>OpenStack Quantum</em></a></span>: Take a look at a real life networking API in production today in the OpenStack project.</li>
</ul>

Learn more about Floodlight development on the <a href="https://groups.google.com/a/openflowhub.org/forum/?fromgroups#!forum/floodlight-dev" target="_blank">Floodlight-Dev Listserv</a>
<hr />
[http://networkstatic.net/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf]({{% relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" %}})

Hope this helps add some documentation for those looking to dig under the hood a bit and create their own networking applications for research or a network that fits their needs. Thanks for stopping by.
<hr>
<a href="{{< relurl "/wp-content/uploads/2013/02/openflow-spec-v1.3.0.pdf" >}}" target="_blank" rel="noopener noreferrer">Download OpenFlow v1.3</a>
<hr />