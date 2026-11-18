+++
title = "Measuring Network Bandwidth using Iperf and Docker"
date = "2018-01-02T23:38:59+00:00"
lastmod = "2019-12-11T00:51:35+00:00"
author = "Brent Salisbury"
wp_id = 7878
categories = ["In the Lab"]
tags = ["Docker", "Network", "Tools"]
description = ""
url = "/measuring-network-bandwidth-using-iperf-and-docker/"
image = "/wp-content/uploads/2016/03/docker_networking-banner1.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "3984fa26990111fbcf83e5b1022411798bcfa5d4326887db1c0c25b878778ed4"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>Measuring Network Bandwidth using Iperf and Docker</h3>


At the heart of any network engineer's toolkit, are applications that let you peer into the network for performance, congestion and capacity planning. One of the thoroughbreds in the open source network tools collection is iperf. Iperf has been around for a long time. The good folks at <a href="https://www.es.net" target="_blank">ESnet</a> updated the original iperf with new features and what not and released it as iperf3.

This tutorial assumes no working knowledge of Docker or Iperf3. If you don't have Docker installed you can get it from <a href="https://docs.docker.com/engine/installation/" rel="noopener" target="_blank">here</a>. More on Docker commands can be found <a href="http://training.play-with-docker.com" target="_blank">here</a>.

<h3>Run the Iperf Server Side Docker Container</h3>


Start a listener service on port 5201 and name the container "iperf3-server" (if the image is not yet downloaded, the run command will pull it down for you). This is bound to the host machine/node IP address via NAT thanks to the -p 5201:5201 mapping. This means there is a container with a private IP address, along with the host machine's IP listening on 5201. 

<pre class="code-sample"><code>
(='o'=) [~]$  docker run  -it --rm --name=iperf3-server -p 5201:5201 networkstatic/iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
</code></pre>

That returns an iperf3 process bound to a socket waiting for new connections on port 5201.

From a new console, you can view the running container with the following Docker command. 

<pre class="code-sample"><code>
(='o'=) [~]$ docker ps
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS                    NAMES
43c6f69371ce        networkstatic/iperf3   "iperf3 -s"         2 minutes ago       Up 2 minutes        0.0.0.0:5201->5201/tcp   iperf3-server
</code></pre>

You can view the image you downloaded with the following Docker command. 

<pre class="code-sample"><code>
(='o'=) [~]$ docker image ls
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
networkstatic/iperf3   latest              6ea158fee1a7        22 months ago       126MB
</code></pre>

<h3> Run the Iperf Client Side Docker Container</h3>


Since we started the server, we now want to a client from another host/node at the server to measure the bandwidth between the two endpoints. This can be the same host you are on it you are First, get the IP address of the new Iperf3 server container you just started. If you are testing in the real world against two seperate machines, you would point at the host's IP that is reachable between the two endpoints

The following will run the client side command from the same host, the server container is running on:


<pre class="code-sample"><code>
docker inspect --format "{{ .NetworkSettings.IPAddress }}" iperf3-server

(Returned) 172.17.0.163
</code></pre>

Next, initiate a client connection from another container, to measure the bandwidth between the two endpoints.

Do this by running a client container pointing at the server service IP address.


<pre class="code-sample"><code>
docker run  -it --rm networkstatic/iperf3 -c 172.17.0.163
</code></pre>

And the output is the following:

<pre class="code-sample"><code>
Connecting to host 172.17.0.163, port 5201
[  4] local 172.17.0.191 port 51148 connected to 172.17.0.163 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec  4.16 GBytes  35.7 Gbits/sec    0    468 KBytes
[  4]   1.00-2.00   sec  4.10 GBytes  35.2 Gbits/sec    0    632 KBytes
[  4]   2.00-3.00   sec  4.28 GBytes  36.8 Gbits/sec    0   1.02 MBytes
[  4]   3.00-4.00   sec  4.25 GBytes  36.5 Gbits/sec    0   1.28 MBytes
[  4]   4.00-5.00   sec  4.20 GBytes  36.0 Gbits/sec    0   1.37 MBytes
[  4]   5.00-6.00   sec  4.23 GBytes  36.3 Gbits/sec    0   1.40 MBytes
[  4]   6.00-7.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.40 MBytes
[  4]   7.00-8.00   sec  4.14 GBytes  35.6 Gbits/sec    0   1.40 MBytes
[  4]   8.00-9.00   sec  4.29 GBytes  36.8 Gbits/sec    0   1.64 MBytes
[  4]   9.00-10.00  sec  4.15 GBytes  35.7 Gbits/sec    0   1.68 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  42.0 GBytes  36.1 Gbits/sec    0             sender
[  4]   0.00-10.00  sec  42.0 GBytes  36.0 Gbits/sec                  receiver

iperf Done.
</code></pre>

Note: if you are new to Docker, the --rm flag will destroy the container after the test runs. I also left out explicitly naming the container. It's totally optional. I typically explicitly name containers for organization and to maintain a consistent pattern but since the client container is run once and then detroyed until I am ready to take the next measurement, it is treated as a disposable container (e.g. pets vs. cattle).

You can do something fancier in a one liner like so (docker ps -ql returns the CID e.g. container ID of the last container started which would be the server we want in this case)

<pre class="code-sample"><code>
docker run  -it --rm networkstatic/iperf3 -c $(docker inspect --format "{{ .NetworkSettings.IPAddress }}" $(docker ps -ql))
Connecting to host 172.17.0.193, port 5201
[  4] local 172.17.0.194 port 60922 connected to 172.17.0.193 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec  4.32 GBytes  37.1 Gbits/sec    0    877 KBytes
[  4]   1.00-2.00   sec  4.28 GBytes  36.7 Gbits/sec    0   1.01 MBytes
[  4]   2.00-3.00   sec  4.18 GBytes  35.9 Gbits/sec    0   1.01 MBytes
[  4]   3.00-4.00   sec  4.23 GBytes  36.3 Gbits/sec    0   1.13 MBytes
[  4]   4.00-5.00   sec  4.20 GBytes  36.1 Gbits/sec    0   1.27 MBytes
[  4]   5.00-6.00   sec  4.19 GBytes  36.0 Gbits/sec    0   1.29 MBytes
[  4]   6.00-7.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   7.00-8.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   8.00-9.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   9.00-10.00  sec  4.22 GBytes  36.3 Gbits/sec    0   1.29 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  42.1 GBytes  36.2 Gbits/sec    0             sender
[  4]   0.00-10.00  sec  42.1 GBytes  36.2 Gbits/sec                  receiver

iperf Done.
</code></pre>

You can do lots of cool things by regularly measuring bandwidth with Iperf3 and doing so in containers makes it easy to run on any platform, anywhere. You can take those measurements and pump them into TSDBs or any other applications designed to collect metrics for trending, capacity planning or simply proactively monitoring for potential bottlenecks in your network.

That's it for now. Hope everyone had a happy new year. As a resolution I plan to pry myself away from other projects and start blogging again regularly (hopefully). Cheers!