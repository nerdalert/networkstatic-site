+++
title = "Open Source Flow Monitoring and Visualization"
date = "2019-12-11T00:46:48+00:00"
lastmod = "2020-01-02T05:12:24+00:00"
author = "Brent Salisbury"
wp_id = 7902
categories = ["In the Lab", "Tools"]
tags = ["DevOps", "Flows", "Monitoring", "NetOps"]
description = ""
url = "/open-source-flow-monitoring-and-visualization/"
image = "/wp-content/uploads/2019/12/elastiflow-header.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "8b4f29c1b40af2bf0f444de7fab56601b4f078a2642ea939ddbede1841052f7f"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>Open Source Flow Monitoring and Visualization</h3>
At the heart of any reasonably sized network, should be a solid strategy around flow collection, querying and visualization. Proper use of flow logs are crucial to SecOps/NetOps from triaging attacks to capacity planning and traffic trending. I remember some 20 years ago, the first time I saw flow logs being visualized in rrdtools it was pretty close to magic. I wanted to recreate that <a href="https://github.com/nerdalert/nfsen-dockerized" target="_blank" rel="noopener noreferrer">environment</a> a few years back and it felt pretty dated.

Recently, I decided to poke around and see what’s new in the open source monitoring space of sFlow/NetFlow/IPFIX and ran across a couple of interesting projects, <a href="https://github.com/cloudflare/goflow" target="_blank" rel="noopener noreferrer">cloudflare/goflow</a> (CloudFlare OSS), <a href="https://github.com/VerizonDigital/vflow" target="_blank" rel="noopener noreferrer">VerizonDigital/vflow</a> (Verizon OSS) and <a href="https://github.com/robcowart/elastiflow" target="_blank" rel="noopener noreferrer">robcowart/elastiflow</a> (also deserving of a mention here is <a href="https://github.com/pmacct/pmacct" target="_blank" rel="noopener noreferrer">pmacct</a>). GoFlow and vFlow are both written in Go which I like and both appear to be highly scalable collectors. What they don’t have are built-in front ends so will require a bit more work to extract interesting data.

Since most ops are already have a workload that doesn’t allow for weeks of development that a Verizon or CloudFlare would staff would have, I thought it would make sense to highlight Elastiflow, since it’s a nice end to end out of the box OSS solution, that’s easy to get up and running.
<h3>Installation and Testing</h3>
The order of setup and validation is as follows:


<ul>
 	<li>Prep the target system (Linux) with a couple of dependencies. The Linux VM is 4-core and 8GB of mem on a laptop. ELK stack is not trivial on the resources and was sluggish on a laptop VM.</li>
 	<li>Bring up the classic <a href="https://www.elastic.co/what-is/elk-stack" target="_blank" rel="noopener noreferrer">ELK</a> stack consisting of Elasticsearch, Logstash and Kibana.</li>
 	<li>Provision the Elistiflow Java component.</li>
 	<li>Validate the flow collection and visualization with a tool I wrote to generate Netflow data <a href="https://github.com/nerdalert/nflow-generator" target="_blank" rel="noopener noreferrer">nerdalert/nflow-generator</a> or if you have some switches with traffic, point them to the collector</li>
 	<li>Quick crash course in Kabana.</li>
</ul>


The install is pretty simple since it is containerized. Depending on the size of your network (i.e. flows generated and exported) and the various moving parts here, the easiest scenario for you to troubleshoot should determine how you deploy, whether inside or outside of containers. For the easy setup and demo we will use the `docker-compose.yml` file included in the project. There were a few things unclear in the docs so I am jotting down what worked for me in setting it up.
<h3>ElastiFlow Installation</h3>
On a Linux host, install Docker and Docker Compose if it’s not already on the system:
<pre class="lang:sh decode:true "># Docker install
sudo apt-get install docker.io
# Docker Compose install
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
</pre>
Download the latest release tarball or zip. Using the master branch image doesn’t build. I’m assuming by design as opposed to neglect while its under development ¯\_(ツ)_/¯. The following is documented in the project <a href="https://github.com/robcowart/elastiflow/blob/master/DOCKER.md" target="_blank" rel="noopener noreferrer">here</a>.
<pre class="lang:sh decode:true "># Download the latest release (currently):
# https://github.com/robcowart/elastiflow/archive/v3.5.1.zip
# All releases: https://github.com/robcowart/elastiflow/releases
unzip v3.5.1.zip
cd elastiflow-3.5.1
</pre>
The compose file mounts the local fs for writing data out. Run the following to prep the filesystem.
<pre class="lang:sh decode:true ">sudo mkdir /var/lib/elastiflow_es
sudo chown -R 1000:1000 /var/lib/elastiflow_es
</pre>
Start the compose stack with:
<pre class="lang:sh decode:true ">sudo docker-compose up -d
Creating elastiflow-elasticsearch-oss ... done
Creating elastiflow-logstash-oss      ... done
Creating elastiflow-kibana-oss        ... done
</pre>
The collector ports listen on the following ports:
<pre class="lang:sh decode:true ">ELASTIFLOW_NETFLOW_IPV4_PORT: 2055
ELASTIFLOW_SFLOW_IPV4_PORT: 6343
ELASTIFLOW_IPFIX_TCP_IPV4_PORT: 4739
</pre>
<h3>Validate the Installation</h3>
The project uses `—net=host` so the ports will get bound to the systems IP address. This is all configurable in the compose file if you fork it. Assuming you don’t get any errors, you should see some new listening ports bound to `0.0.0.0`. Below is a dump from my host as a reference.
<pre class="lang:sh decode:true ">netstat -pln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:34547         0.0.0.0:*               LISTEN      1401/containerd
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      415/systemd-resolve
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      546/sshd
tcp        0      0 0.0.0.0:5601            0.0.0.0:*               LISTEN      6131/node
udp        0      0 0.0.0.0:2055            0.0.0.0:*                           6115/java
udp        0      0 0.0.0.0:6343            0.0.0.0:*                           6115/java
udp        0      0 127.0.0.53:53           0.0.0.0:*                           415/systemd-resolve
udp        0      0 192.168.1.17:68         0.0.0.0:*                           391/systemd-network
udp        0      0 0.0.0.0:4739            0.0.0.0:*                           6115/java
</pre>
Next start pushing some flows into the collector so we can start populating so flows to view running the following container. You can also grab binaries or build it yourself here <a href="https://github.com/nerdalert/nflow-generator" target="_blank" rel="noopener noreferrer">nerdalert/nflow-generator</a>
<pre class="lang:sh decode:true "># HOST_IP is the IP of the host running the collector
sudo docker run -it --rm networkstatic/nflow-generator -t HOST_IP -p 2055
</pre>
While that runs in the background, validate the installation by making sure we can reach the Kibana UI by pointing your browser to `http://HOST_IP:5601/app/kibana` where HOST_IP is the machine running the ELK stack.


<ul>
 	<li>Once the page loads, go to Management -&gt; Index Patterns -&gt; Create Index Pattern. Just pop a star/wildcard in the box and hit next step until done like so:</li>
</ul>


<img class="aligncenter size-large wp-image-7908" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-1-1-660x301.png" >}}" alt="elastiflow-1" width="660" height="301" /></a>

Now we need to import some dashboards, which is one of the things I really like about this project is that it has a nice collection ready for import. Download one of the dashboard templates from <a href="https://github.com/robcowart/elastiflow/tree/master/kibana" target="_blank" rel="noopener noreferrer">github.com/robcowart/elastiflow/tree/master/kibana</a>. I used `elastiflow.kibana.7.3.x.ndjson` for this to match the v3.5.1. release timeframe.


<ul>
 	<li>Go to Management -&gt; Saved Objects and click import and upload the elastiflow.kibana.7.y.x.ndjson file you downloaded.</li>
</ul>


<a href="{{< relurl "/wp-content/uploads/2019/12/elastiflow-2.png" >}}"><img class="aligncenter size-large wp-image-7910" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-2-660x188.png" >}}" alt="elastiflow-2" width="660" height="188" /></a>


<ul>
 	<li>Once those import, you should now have a 300+ imported dashboards.</li>
</ul>


<a href="{{< relurl "/wp-content/uploads/2019/12/elastiflow-3.png" >}}"><img class="aligncenter size-large wp-image-7911" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-3-660x639.png" >}}" alt="elastiflow-3" width="660" height="639" /></a>

<hr />

Now you can bedazzle your colleagues with the glorious Kibana visualizations by simply clicking on any of the saved objects in the list. The flow data is in the following examples is just random Netflow flows injected from <a href="https://github.com/nerdalert/nflow-generator" target="_blank" rel="noopener noreferrer">nerdalert/nflow-generator</a>.


<ul>
 	<li>Dashboard Name - ElastiFlow: Top Talkers</li>
</ul>


<a href="{{< relurl "/wp-content/uploads/2019/12/elastiflow-4-1.png" >}}"><img class="aligncenter size-large wp-image-7913" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-4-1-660x558.png" >}}" alt="elastiflow-4" width="660" height="558" /></a>


<ul>
 	<li>Dashboard Name - ElastiFlow: Flows (src/dst)</li>
</ul>


<a href="{{< relurl "/wp-content/uploads/2019/12/elastiflow-5.png" >}}"><img class="aligncenter size-large wp-image-7914" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-5-660x620.png" >}}" alt="elastiflow-5" width="660" height="620" /></a>


<ul>
 	<li>Dashboard Name - ElastiFlow: Geo Location (src/dst)</li>
</ul>


<a href="{{< relurl "/wp-content/uploads/2019/12/elastiflow-6.png" >}}"><img class="aligncenter size-large wp-image-7915" src="{{< relurl "/wp-content/uploads/2019/12/elastiflow-6-660x723.png" >}}" alt="elastiflow-6" width="660" height="723" /></a>
<h3>Wrap Up</h3>
That’s all for now. Thanks to <a href="https://github.com/robcowart" target="_blank" rel="noopener noreferrer">github.com/robcowart</a> for the work in putting together and open sourcing this nice end to end flow management project. If you run into issues or improvements, I am sure he is open to accepting PRs. I know I will open a couple to help contribute.

If you have any networking projects you would like highlighted or looking for contributors, I am always interested. Ping me at <a href="https://twitter.com/networkstatic" target="_blank" rel="noopener noreferrer">@networkstatic</a> and let me know what you’re working on!