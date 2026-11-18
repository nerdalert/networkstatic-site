+++
title = "GoBGP - A Control Plane Evolving Software Networking"
date = "2016-03-29T05:15:17+00:00"
lastmod = "2016-04-12T22:29:38+00:00"
author = "Brent Salisbury"
wp_id = 7852
categories = ["In the Lab", "Programming"]
tags = ["BGP", "Go", "Programming", "Routing", "Software Defined Networking"]
description = ""
url = "/gobgp-control-plane-evolving-software-networking/"
image = "/wp-content/uploads/2016/03/gobgp-purple.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "82dfc819b6d51285360996291139b32178443c2d778b7e4a810667b5a8b4b369"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>GoBGP - A Control Plane Evolving Software Networking</h3>
If I have talked to you over the past year or two about networking, odds are I have mentioned a project to you called <a href="http://osrg.github.io/gobgp/" target="_blank">GoBGP</a>. If we have spoken a lot, you are probably sick of me talking to you about GoBGP :) There is a reason, it's because GoBGP is a missing link in networking that has been for a long time. GoBGP is a project from some really smart and just as importantly friendly, community minded folks at NTT Communications (largest telco in Japan). The software group that does the software is <a href="https://github.com/osrg/gobgp" target="_blank">OSRG</a> and the same organization that did RYU the SDN controller that was popular in OpenStack deployments. <a href="http://osrg.github.io/gobgp/" target="_blank">GoBGP</a> is a BGP focused routing daemon that is incredibly flexible, written in Go and perfect for those both looking for practical control plane SDN solutions or network engineers looking to figure out what the hell their future will look like and where to start evolving in a software driven age. The tutorial will also instruct you how to install the Go programming language and environment in order to pull down and build the GoBGP binaries.

There are a few software router implementations, all useful in their own right. The first reason I prefer GoBGP is its written in Go, which gives you many of the benefits of C with a lower barrier to entry then C along with great concurrency support along with great native tooling. More on reasons to use Go <a href="https://www.youtube.com/watch?v=FTl0tl9BGdc" target="_blank">here</a>. GoBGP is also completely cross platform and does not have any hardware specific dependencies. Secondly, its architecture is outstanding and very modular unlike the monolithic alternatives. As an example, they implemented a draft I am huge fan of from <a href="https://twitter.com/petrlapu" target="_blank">Petr Lapukhov</a> of Facebook named <a href="https://tools.ietf.org/html/draft-lapukhov-bgp-opaque-signaling-00" target="_blank">BGP for opaque signaling</a> in a couple of days without needing to change anything internally. I see this level of modularity at work and recognize the level of experience required to design such nice architectures like the OSRG team have put together to seamlessly support EVPN, Opaque Flowspec, RRs, RPKI, BMP to name a few.

<h3>Download and Install GoBGP </h3>

The team does a great job with documentation so anything I write will duplicitous but I will dump my quick notes to get up and running. There is not a binary download for Mac/Linux/Windows explicitly so its a great chance for you to learn something new by installing the Go compiler if you haven't before. Its fast and easy. If on a Mac or Linux box it is the same.

Pre-Requisites:


<ul>
	<li>Windows or Mac there are installers found at <a href="https://golang.org/dl/" target="_blank">Go Downloads</a>.</li>
	<li>Also Install <a href="https://help.github.com/articles/set-up-git/" target="_blank">git</a> if you want to compile from source at the end of the post.</li>
</ul>


To install on Linux, paste the following or follow these <a href="https://golang.org/doc/install" target="_blank">instructions</a>:

<pre class="code-sample"><code>
cd /usr/local
sudo wget https://storage.googleapis.com/golang/go1.6.linux-amd64.tar.gz
# Untar into /usr/local/go That is the generally excepted location.
sudo tar xvzf go1.6.linux-amd64.tar.gz
# Add the go bin directory to your executable path.
export PATH=$PATH:/usr/local/go/bin
</code></pre>

The next part of a Go install is the part that trips people up the most. Go uses a file structure for libraries that has to follow a convention because libraries are statically linked. The rational for this is because the compile time is incredibly fast because there is not any dynamic linking that eats up compile time searching for libraries.

Wherever you are going to store your Go project need to be contained in the exported to the $GOPATH directory. The docs use this example:

<pre class="code-sample"><code>
export GOPATH=$HOME/work
</code></pre>

I store all of my Go projects in a directory in my home directory named, you guessed it, go. Im going to spell out full file paths to keep it as simple as possible. You want to add the export GOPATH=<Path> to your ~/.bash_profile startup file. If one doesn't exist just create it in your home ~/ directory.

<pre class="code-sample"><code>
# Set the Mac OS X GOPATH with:
$ export GOPATH=/Users/brent/code/go

# Now your env should contain that path
$ env | grep GO
GOPATH=/Users/brent/code/go

# Echo it to your .bashrc so it will be persistent
$ echo GOPATH=/Users/brent/code/go >> ~/.bash_profile

# Reread your bashrc and verify with `env` again
$ source ~/.bash_profile
</code></pre>

On a Linux box I use /home/brent/go:

<pre class="code-sample"><code>
# My Linux Hosts
$ export GOPATH=/home/brent/go

# Verify the Linux exports with
$ env | grep GO
GOPATH=/home/brent/go

# Echo it to your .bashrc so it will be persistent
$ echo GOPATH=/home/brent/go >> ~/.bashrc

# Reread your bashrc and verify with `env` again
$ source ~/.bashrc
</code></pre>

All of your libraries are going to be installed into the $GOPATH directory path.

Now you should be ready to download GoBGP:

<pre class="code-sample"><code>
$ go get github.com/osrg/gobgp/gobgpd
$ go get github.com/osrg/gobgp/gobgp
</code></pre>

There are two binaries that should be in your file path now, gobgp (client cli) and gobgpd (daemon).

<pre class="code-sample"><code>
gobgp --help
gobgpd --help
</code></pre>

<h3>GoBGP Download and Run </h3>

Now run gobgp with an example config. The following toml formatted config points to another BGP instance both using AS: 65000. The source IP is 192.168.1.103 and the remote BGP peer is 192.168.1.249. Simply create a text file containing that config with your IP address swapped in.

<pre class="code-sample"><code>
[global.config]
    as = 65000
    router-id = "192.168.1.103"

[[neighbors]]
  [neighbors.config]
      neighbor-address = "192.168.1.249"
      peer-as = 65000
</code></pre>

Now start the daemon using the config file I saved as gobgp-conf-151.toml and using -l debug for debug logging so you can see the sausage factory go:

<pre class="code-sample"><code>
# 
$ gobgpd -l debug --config-file=gobgp-conf-151.toml
</code></pre>

Assuming you have a router, another gobgp, quagga etc looking to peer with the the host you start gobgpd on view the neighbor adjacency with:

<pre class="code-sample"><code>
# gobgp neighbor
Peer                AS  Up/Down State       |#Advertised Received Accepted
192.168.1.249    65000 07:27:46 Establ      |          2        1        1
</code></pre>

From there, the options are massive. Some of the highlights for example is, I want to monitor a route and do something when the route appears. It is super easy to integrate code with this project. A simple example is something I did just reading CLI output <a href="https://github.com/nerdalert/bgp-ipvlan-docker/blob/master/plugin/routing/rib_updates.go" target="_blank">here</a> to monitor when a container prefix appears to plumb routes. Note, that project currently is defunct but we have some cool stuff coming up.  

<h3>GoBGP Example Commands </h3>

Here is my CLI cheatsheet. The OSRG folks have amazing docs so please use those but figured I would dump them here anyways to help you get an overview of how versatile this project is.

<pre class="code-sample"><code>
############> Neighbor Options <############

# Disable a BGP neighbor
gobgp neighbor 192.168.1.248 disable

# Enable a BGP neighbor
gobgp neighbor 192.168.1.248 enable

# List BGP neighbors
gobgp neighbor

############> Custom Neighbor Ops <############

gobgp neighbor 192.168.1.248 adj-in
gobgp neighbor 192.168.1.248 adj-out
gobgp neighbor 192.168.1.248 local -a ipv4

#################> BGP Neighbor Resets <###############
gobgp neighbor 192.168.1.248 disable
gobgp neighbor 192.168.1.248 enable
gobgp neighbor 192.168.1.248 softreset
gobgp neighbor 192.168.1.248 softresetin
gobgp neighbor 192.168.1.248 softresetout
gobgp neighbor 192.168.1.248  reset

############> Extended Community <############

# Add Policy
gobgp policy extcommunity add ecs1 RT:65100:10

# Del Policy
gobgp policy neighbor del ecs1

############> Add/Del VRF  <############

# Add a VRF
gobgp vrf add <vrf name> rd <rd> rt {import|export|both} <rt>...

# Del a VRF
gobgp vrf del <vrf name>

# Show VRFs
gobgp vrf

##########> Add Del Routes to a VRF <############

# Add routes to a VRF
gobgp vrf <vrf name> rib add <prefix> -a <address family>

# Del routes from a VRF
gobgp vrf <vrf name> rib del <prefix> -a <address family>

# Show routes in vrf
gobgp vrf <vrf name>

# Example:
gobgp vrf FOO rib add 251.1.1.10/32 -a ipv4

##############> Global RIB Ops <################

# Add a global rib route
gobgp global rib add <prefix> [-a <address family>]

# Delete a specific Route
 gobgp global rib del <prefix> [-a <address family>]

# show all Route information
gobgp global rib [-a <address family>]

# show a specific route information
gobgp global rib [<prefix>|<host>] [-a <address family>]

# Del v6 RIB entry
gobgp global rib del 2001:123:123:1::/64 -a ipv6

# Add v4 RIB entry
gobgp global rib add 251.1.1.100/32 -a ipv4

gobgp global rib add <prefix> [-a <address family>]
gobgp global rib del <prefix> [-a <address family>]

gobgp global rib [-a <address family>]
gobgp global rib [<prefix>|<host>] [-a <address family>]

gobgp global rib del 2001:123:123:1::/64 -a ipv6
gobgp global rib add 251.1.1.100/32 -a ipv4

################> Monitor Neighbors <#############

# monitor neighbor status
gobgp monitor neighbor

# monitor specific neighbor status
gobgp monitor neighbor <neighbor address>

#############> Monitor Rib Entries <#############

gobgp monitor global rib
# Example Output
# [ROUTE] 10.0.0.0/24 via 0.0.0.0 aspath [] attrs [{Origin: i}]

# monitor command blocks. add routes from another terminal
gobgp global rib add 10.0.0.0/24

# monitor global rib changes
gobgp monitor global rib

</code></pre>

<h3>GoBGP Build from Source</h3>


For those new to Go, I figured I could add a bit of value for the OSRG project by explaining a bit more on pulling the Go source code and building a binary from them. The binaries for Go are stored in $GOPATH/bin which in my case is /home/brent/go/bin on a Linux OS. If you want to pull the GoBGP source code and build it locally do the following.

<pre class="code-sample"><code>
# cd $GOPATH is the same as cd /home/brent/go for me
$ cd $GOPATH

# Create a src/github directory so the source files are stored in a static location the compiler knows where to look for.
$ mkdir -p src/github.com
$ cd src/github.com
# or 
$ cd $GOPATH/src/github.com
# or :)
$ cd /home/<username>/go/src/github.com

# Clone the github.com/osrg/gobgp source repo
$ git clone https://github.com/osrg/gobgp.git
$ cd osrg/gobgp

# Now we need to pull down the libraries that are used by gobgp. 
# Go makes this very easy. go get ./... will recursively look for
# any dependencies below /home/<username>/go/src/github.com/osrg/gobgp
$ go get ./..

# Then build the src code using or install the binary using go install ./...
$ go build ./...

# Now you will see binaries in the $GOPATH/bin/ directory
ls $GOPATH/bin/
</code></pre>


<h3>More Resources</h3>

This doesn't even scratch the surface. There is plenty of valid reasons where a control plane belongs. L3 obviously scales further and is more reliable then large L2 domains. If you are looking to push routing closer to the edge, eventually you will consider where the L3 control belongs. Containers using Ipvlan L3 will require routes to be injected into the network. That could be a vendor HW integration installing routes or it could be the edge host signaling new routes. Either way, instead of announcing MAC addresses into a ToR, its just as reasonable to expect folks to want to announce routes into ToRs. If you want to eliminate L2, it requires pushing L3 further to the edge where the density is and will rapidly grow.

Thanks to the OSRG folks for being such good stewards in open source and the support from their parent company NTT in supporting them. Explore the <a href="https://github.com/osrg/gobgp" target="_blank">github.com/osrg/gobgp</a> project, there is a lot to learn there. The APIs for development are cutting edge with tons of opportunity for users, devs, vendors and those looking to evolve their skills in both NetOps and development, or both. They have a massive BGP network, they know it well, there is a lot everyone of all levels can learn there. Pretty reasonable to start expecting containerized control planes to bolt on top of any <a href="{{< relurl "/configuring-macvlan-ipvlan-linux-networking/" >}}" target="_blank">datapath</a> sooner rather then later so why not get ahead of the curve. If you have any troubles use the project's repo issues to get assistance as I am regrettably slow replying to comments here as time is not my friend atm :)