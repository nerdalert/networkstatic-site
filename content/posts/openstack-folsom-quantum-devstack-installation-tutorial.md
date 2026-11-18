+++
title = "OpenStack Folsom Quantum Devstack Installation Tutorial"
date = "2012-10-06T06:45:35+00:00"
lastmod = "2013-10-19T02:58:02+00:00"
author = "Brent Salisbury"
wp_id = 2919
categories = ["In the Lab", "Tools"]
tags = ["DevStack", "Open vSwitch", "OpenStack", "Tutorials"]
description = ""
url = "/openstack-folsom-quantum-devstack-installation-tutorial/"
image = "/wp-content/uploads/2012/11/devops-openstack-lab.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8c627c0c58ecb1ac0cbb132494d7f72c06171c3eae1752faf5a0f324a2bca605"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>OpenStack Folsom Quantum Devstack Installation Tutorial and Screencast</h2>
<aside class="legacy-callout">
<ul>
	<li><a href="{{< relurl "/installing-openstack-grizzly-with-devstack/" >}}" target="_blank">Installing OpenStack Grizzly with DevStack</a> : Here is an updated Grizzly DevStack tutorial since Folsom is coming to an end.</li>
</ul>
</aside>

This is a quick guide that includes a diagram of a working reference architecture for installation of the OpenStack Folsom release using which includes the Quantum networking component using the <a href="http://devstack.org" target="_blank">DevStack</a> installation bash script.

With the OpenStack Essex release, I was writing installers with Python for Linux bridging and the Quantum plugin. So far the OpenStack Folsom install is more complex due to the added options mainly from the Quantum networking plugin. A big feature of Quantum out of the box using this build with OpenvSwitch is it adds features such as layer2 multi-tenancy for path isolation with GRE tunnels and/or Vlan IDs.

This tutorial will install the packages as listed under Folsom below. Trying to keep the Python installer up to date is too much maintenance for me so switching to DevStack for people who get paid to do it. While installing by hand is good for initial builds, this release mainly due to the complexity of Quantum is trickier than Essex in my opinion. I think that's some ironic commentary on SDN for those who track developments and try and separate reality, fear and myth on that front.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2012/10/opestack-releases.jpg" >}}" alt="OpenStack Releases"></figure>
<em><strong>Figure 1</strong>.</em> OpenStack Releases (Note Quantum is still in development and not stable until 'Grizzly' Q2Y2013.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/openstack-contributions1.jpg" >}}"><img class="aligncenter  wp-image-2923" title="openstack-contributions-folsom" alt="openstack-contributions-folsom" src="{{< relurl "/wp-content/uploads/2012/10/openstack-contributions1.jpg" >}}" width="561" height="432" /></a>
<strong><em>Figure 2.</em></strong> Vendor contributions and how they have differed from Essex to Folsom.</p>

<h2>OpenStack Folsom Installation Pre-Requisites</h2>
I am using Ubuntu 12.04. Never hurts to patch and update but not required. Then we will download Devstack project from GitHub. Since the hooks for OpenvSwitch are coupled with KVM you will need physical hardware that supports hardware virtualization. <a href="{{< relurl "/nested-kvm-hypervisor-support/" >}}" target="_blank">Nested</a> support is road-mapped and may already be integrated with <a href="http://wiki.openstack.org/Heat" target="_blank">HEAT</a> in OpenStack for hypervisor hooks into the public <a href="{{< relurl "/public-cloud-network-as-a-service/" >}}" target="_blank">cloud</a>.

Check for hardware virtualization on Intel (Intel-VT) with:
<pre class="code-sample"><code>grep --color vmx /proc/cpuinfo</code></pre>
Check for hardware virtualizationon AMD (AMD-V) with:
<pre class="code-sample"><code>grep --color svm /proc/cpuinfo</code></pre>
You should see VMX or SVM highlighted in red from the commands above if HW virtualization is supported.

Download and install git. Then clone the devstack repo on github.
<pre class="code-sample"><code>sudo apt-get install git
git clone git://github.com/openstack-dev/devstack.git
cd devstack</code></pre>
Here is what my network NIC configurations look like in /etc/network/interfaces. We want the port to be up in promiscuous mode. Think of <a href="http://wiki.aanval.com/wiki/Community:Snort_2.9.2.3_Installation_Guide_for_Ubuntu_12.04,_with_Barnyard2,_Pulledpork,_and_Aanval" target="_blank">Snort</a> or OpenVPN interface configuration :)
<pre class="code-sample"><code># The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet static
address 172.31.246.7
netmask 255.255.254.0
network 172.31.246.0
broadcast 172.31.247.255
gateway 172.31.246.1
# dns-* options are implemented by the resolvconf package, if installed
dns-nameservers 8.8.8.8

auto eth1
iface eth1 inet manual
up ifconfig $IFACE 0.0.0.0 up
up ip link set $IFACE promisc on
down ip link set $IFACE promisc off
down ifconfig $IFACE down</code></pre>
Above is the /etc/network/interfaces file that determines the "ifconfig" output. Other handy binaries ethtool "apt-get install ethtool" to determine if you have link to a NIC, e.g. "ethtool eth0" would return a Boolean on link detected: yes|no and tcpdump is installed by default, "tcpdump host 172.16.1.100 -i eth0" would promiscuously listen for the host specified on interface eth0.
<h2>DevStack Localrc File</h2>
Add the following in the devstack directory and name it "localrc". It is the same directory that contains the "stack.sh" shell script. The localrc file contains all of your build parameters to pass to the script. Finding the right combination took way too many hours but here is what is used in the screencast at the bottom of the post.

Be sure to read the script and understand what other parameters are available. This will create unique Vlan IDs between the host and Hypervisor. If for example you wanted to use GRE tunnels instead you would add the line "ENABLE_TENANT_TUNNELS=True" to the configuration. This is the key to the install. If you have two NICs on a host this should work for you.

<pre class="code-sample"><code>
ENABLED_SERVICES=q-meta,q-lbaas,n-obj,n-cpu,n-sch,n-cauth,horizon,mysql,rabbit,sysstat,cinder,c-api,c-vol,c-sch,n-cond,quantum,q-svc,q-agt,q-dhcp,q-l3,n-novnc,n-xvnc,q-lbaas,g-api,g-reg,key,n-api,n-crt
ADMIN_PASSWORD=openstack
MYSQL_PASSWORD=openstack
RABBIT_PASSWORD=openstack
SERVICE_PASSWORD=openstack
SERVICE_TOKEN=openstack
MYSQL_PASSWORD=password
LOG=True
</code></pre>
If you downloaded devstack git source a a few days or even hours before you execute it you may consider updating the installer. Assuming you allowed devstack to install into the default /opt/stack/ directory, running this will update the latest code merge.

<pre class="code-sample"><code>cd /opt/stack/quantum && sudo git pull
cd /opt/stack/nova && sudo git pull
cd /opt/stack/horizon && sudo git pull
cd /opt/stack/glance && sudo git pull
cd /opt/stack/keystone && sudo git pull</code></pre>

<h2>Run ./stack.sh to Install OpenStack Folsom</h2>
With your localrc file in the same directory run ./stack.sh. Once the installation is done run the following to pull-down and import the Amazon EC2 Ubuntu Cloud Image. I had a terrible time with what gets pulled down with the script and you will notice at the end I actually get errors on tokens from Glance but everything still works fine EXCEPT for the Cirros image. You can always test if your image is working by looking at it in the Dashboard through VNC. Nova will report a host up even if it is sitting their with a broken image trying to pxi boot.

<hr />

Your shell environmentals need to have similar values to the following. This is service authentication. Merely pasting it into your bash shell or adding it to localrc for persistency will give you CLI permissions.
<pre class="code-sample"><code>export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0</code></pre>

<hr />
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/folsom-glance.jpg" >}}"><img class="wp-image-2926 aligncenter" title="folsom-glance" alt="folsom-glance-openstack" src="{{< relurl "/wp-content/uploads/2012/10/folsom-glance.jpg" >}}" width="486" height="470" /></a>
<strong>Figure 3</strong>. Check the VM if you are troubleshooting. Nova still reports it up even if it is in this state.
<aside class="legacy-callout"><strong>Glance Errors </strong>If you get "You must provide a username via either --os-username or env[OS_USERNAME]" Verify you added proper environmental variables to match what is in localrc and then try another CLI command like "glance index".</p>
export SERVICE_TOKEN=openstack
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL=http://localhost:5000/v2.0/
export SERVICE_ENDPOINT=http://localhost:35357/v2.0</aside>

The Glance error looks something like this. It's like the SERVICE_TOKEN variable isnt getting passed even though it is defined in keystone somewhere. Did not spend any time on it since I want Ubuntu Precise Cloud Image. You can build windows images with this <a href="{{< relurl "/building-a-windows-image-for-openstack/" >}}" target="_blank">tutorial.</a>
<pre class="code-sample"><code>wget https://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img
glance add name=Ubuntu-12.04 is_public=true container_format=ovf disk_format=qcow2 &lt; precise-server-cloudimg-amd64-disk1.img
#You can then view the imported image with:
glance index</code></pre>
Before you boot a host you need to do one thing that is not automated. You have to add your fixed_range or back-end NIC to the br-int OpenvSwitch bridge. You are taking that physical interface eth1 and binding it to br-int. Think of it as a locally significant Vlan with no tags being inserted (Probably worst explanation ever). That physical host still does not have any addresses on it.

<h2>Folsom Quantum L3-agent</h2>
The L3-agent will take care of arp-proxying the hosts. The eth1 host is up promiscuously. That is how if two hosts in the same tenant/bridge/subnet would always show the same arp entry for neighboring VMs. Example, VM Host1 at 192.168.1.10/24 and VM Host2 at 192.168.1.11/24 and a gateway of 192.168.1.1. Pinging 192.168.1.1 from Host1 would give you the same mac address in the arp entry of the gateway as you would see if your pinged Host2. This is because all traffic is funneled through the L3-agent. The datapaths (Layer2 path) is kept isolated by two mechanisms, one being Vlan tagging from the VM to the Physical host and the other option being GRE tunnels from a VM to Physical. This was not possible prior to the OpenStack Folsom release OpenStack Essex. Essex used default Linux bridging.

Folsom leverages advanced vSwitch features in the case OpenvSwitch in conjunction with IPTables filtering and DNSMASQ to deliver self provisioning L2/L3/L4 header for policy application from flow based forwarding. Elegant solution and more on networking in the next section with some drawings.

<em>Note that when you spawn VM from the DevStack install as shown in the video. I use the "demo" group and in the networking tab select "private".</em>
<pre class="code-sample"><code>#look at the current vSwitch and routing table configuration
sudo ovs-vsctl show
route -n
#add eth1 to br-ex
sudo ovs-vsctl add-port br-ex eth1
route -n</code></pre>
&nbsp;

<hr />

<p><a href="http://www.youtube.com/watch?v=WiwOc5-gYLU&hd=1">Watch video on YouTube</a></p>

Video 1. Quick walk through of post script operations.
<h2>OpenStack Quantum Networking</h2>
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/openstack.folsom.isolation.jpg" >}}"><img class="size-full wp-image-2930 aligncenter" title="openstack.folsom.isolation" alt="openstack.folsom.isolation" src="{{< relurl "/wp-content/uploads/2012/10/openstack.folsom.isolation.jpg" >}}" width="461" height="348" /></a>
<strong>Figure 4</strong>. Data Path (Layer 2) isolation is achieved between hypervisor and VM host with Vlans a GRE tunnels. Those encapsulations break out at the hypervisor or could be picked up by emerging SDN/Data Center orchestration networking.</p>
The concepts are pretty cool. Our future is apparently going to be reliant on DNSMASQ, IPTables or plug-ins like NVP to build state and forwarding policy, see Cisco VSG and Nexus 1k, its all the same concepts, forwarding instantiation. Remember that Quantum won't be released as stable until Grizzle in spring of 2013. There are quite a few pieces that are not baked into Horizon (Dashboard) since Horizon development froze for Folsom release. Take a look at the <a href="https://blueprints.launchpad.net/quantum/folsom/+assignments" target="_blank">blueprint</a> if interested in seeing upcoming features. Floating addresses is not supported via Horizon so you need to add those via the API or CLI.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/10/openstack.tenant.vlans_1.jpg" >}}"><img class="size-full wp-image-2941 aligncenter" title="openstack.tenant.vlans" alt="openstack.tenant.vlans" src="{{< relurl "/wp-content/uploads/2012/10/openstack.tenant.vlans_1.jpg" >}}" width="429" height="394" /></a>
<strong>Figure 5</strong>. Here are where some of the DevStack parameters fit into the topology and how OpenStack networking from Hypervisor down looks.</p>

<div><a href="{{< relurl "/wp-content/uploads/2012/10/route.table_.openstack.quantum.jpg" >}}"><img class="wp-image-2931 aligncenter" title="route.table.openstack.quantum" alt="route.table.openstack.quantum" src="{{< relurl "/wp-content/uploads/2012/10/route.table_.openstack.quantum.jpg" >}}" width="546" height="149" /></a></div>
<div><strong>Figure 6</strong>. Routing table of the physical host. br-ex is rather confusing at first. Think of it as a NAT bridge between frontend and backend. br-ex will be attached to the public bridge eth0 (public facing) while VMs reside on br-int bridge in OVS.</div>
<div><a href="{{< relurl "/wp-content/uploads/2012/10/netns.quantum.jpg" >}}"><img class="wp-image-2932 aligncenter" title="netns.quantum" alt="netns.quantum.exec" src="{{< relurl "/wp-content/uploads/2012/10/netns.quantum.jpg" >}}" width="528" height="168" /></a></div>
<strong>Figure 7.</strong> Quantum Namespaces are the path isolation components. Getting familiar with 'ip netns exec' commands will be part of a deep dive.
<h2>Uninstall or Reinstall the Devstack OpenStack Environment</h2>
Depending on if I ran into problems or not I will often delete installed packages and directories to get as vanilla an install as I can get. Since this will be physical hosts the snapshot image isn't available. Something along the following will delete some main packages and delete some directories that will get reinstalled as soon as you run the ./stack.sh script again. Remember to just unload the Devstack script and processes like quantum, nova, glance etc run ./unstack.sh. That will not stop dependencies like your hypervisor or vSwtich which in this case is KVM/libvirt-bin and OpenvSwitch.
<pre class="code-sample"><code>./unstack &amp;&amp; sudo apt-get purge libvirt-bin qemu-kvm qemu bridge-utils dkms openvswitch-switch openvswitch-datapath-dkms rabbitmq-server  dnsmasq iptables tgt
#Delete some directories with configuration files if hitting problems to start from scratch.
sudo rm -rf /etc/quantum
sudo rm -rf /etc/nova
sudo rm -rf /etc/glance
sudo rm -rf /var/lib/nova
sudo rm -rf /etc/libvirt/
sudo rm -rf /var/lib/libvirt/</code></pre>
&nbsp;
<h2>Potential DevStack Folsom Errors to Troubleshoot</h2>
<strong>Horizon Error</strong>: Template error Dashboard with slug "nova" is not registered. Just delete /opt/stack/horizon/ and pull it done again and the error will clean up. I didn't troubleshoot Django to try and see why since just rebuilding the directory fixes it up.
<pre class="code-sample"><code>In template /opt/stack/horizon/horizon/templates/horizon/common/_sidebar.html, error at
 Dashboard with slug "nova" is not registered.
 {% load branding horizon i18n %}</code></pre>

<div class="sidebar">
<p class="brand clearfix">{% site_branding %}
{% horizon_main_nav %}</p>

</div>
<div class="sidebar">
<h2>Summary</h2>
Check out the admin <a href="http://docs.openstack.org/trunk/openstack-network/admin/content/ch_preface.html" target="_blank">guide</a> to learn more and tweak your setup. DevStack tears down the config on reboot and unstack so it is not a permanent install. You could easily take your install configurations from here and make them your permanent build. Before I end I want to point out what a machine Dan Wendlandt from Nicira is. He is a small army of patching and documentation both formal and on boards. Nice guy who even answers a nobody like me. I was skeptical that he and his team would be allowed to continue as he was after the VMware <a href="{{< relurl "/nicira-acquisition-by-vmware-winners-and-losers/" >}}" target="_blank">acquisition</a> but Dan is still around the clock and quite frankly, where are the other vendors? I realize they are there somewhere but go read the boards, they speak for themselves.

That said I am still completely skeptical of VMware on the OpenStack board, if that isn't the fox in the hen house what is? I don't blame them, it is a direct competition, its commoditization of not just the Hypervisor but the management of them also at the very least. It's open source vCloud Director, but whatever they all make lots more money than me so don't really care. It's competition, and thats good for the consumer either way.

Hope this helps a bit, there isn't much documentation on this yet and the network bridging components are conceptually pretty new in some cases so some pictures might help.
<h2>Additional DevStack Resources</h2>
<aside class="legacy-callout">
<ul>
	<li><a href="{{< relurl "/openstack-multi-node-devstack-nova-network-tutorial/" >}}" target="_blank">OpenStack Multi-Node DevStack Nova Network Tutorial</a>: If just starting out with OpenStack or DevStack, it may be easier getting to know the services using nova-network for starters.</li>
	<li><a href="http://www.slideshare.net/mestery/openstack-development-using-devstack" target="_blank">OpenStack Development Using DevStack</a>: For a nice presentation on DevStack from <a href="http://www.siliconloons.com" target="_blank">Kyle Mestery</a> <a href="https://twitter.com/mestery" target="_blank">@mestery</a></li>
	<li><a href="http://devstack.org/stack.sh.html" target="_blank">DevStack Code</a>: Reviewing the code is a really great way to get to understanding the script. DevStack Website</li>
	<li><a href="http://docs.openstack.org" target="_blank">OpenStack Documentation</a>: This has remarkably improved.</li>
</ul>
</aside>

<hr />

Thanks for stopping by. If you have problems I will do my best to help out, just give me a couple days to reply. the #openstack irc channels on irc.freenode.org have some brilliant folks that can give you a hand also. Cheers!

<hr />

</div>