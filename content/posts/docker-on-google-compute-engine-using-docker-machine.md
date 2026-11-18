+++
title = "Docker on Google Compute Engine Using Docker Machine"
date = "2015-06-13T01:26:59+00:00"
lastmod = "2015-06-17T21:45:14+00:00"
author = "Brent Salisbury"
wp_id = 7747
categories = ["In the Lab"]
tags = ["Docker", "Docker-Machine", "Google"]
description = ""
url = "/docker-on-google-compute-engine-using-docker-machine/"
image = "/wp-content/uploads/2015/06/build_ship_run-banner.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "66c3dceabc23b75e2ea328ad5bb5cad70711c3272289e50aba674052c77873c8"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> Docker on Google Compute Engine Using Docker Machine</h3>
Next up in Using Docker Machine across <a href="{{< relurl "/normalizing-the-cloud-with-docker-machine/" >}}" target="_blank">private and public clouds</a>, is Google Compute Engine (GCE).

<hr />

As with the other posts, a diagram of how I view the importance of a Docker Machine abstraction.

<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img class="aligncenter size-full wp-image-7574" src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" /></a>


First, if you don't already have an account you can get $300 credit expiring after 60-days towards Google GCE that we will use as Docker hosts in this setup.

<a href="https://cloud.google.com">Setup your $300 in credit on GCE</a>
<h3> Configure Google Compute Engine to Enable Docker Containers and API Calls </h3>
Check this link for some of the pre-requisites to get your GCE account <a href="https://cloud.google.com/deployment-manager/create-container-deployment" target="_blank">enabled for containers</a>.

Once you have signed up, you will get dropped into a page with a project. Record the Project ID (api-project-xxxxxxxxxxxxx).

As a n00b to GCE it wasn't clear in a couple of areas what the pre-reqs to get started were but I think there are at least two steps after signing up to start running Docker containers. Log into your <a href="https://console.developers.google.com" target="_blank">Google Developers Console</a>

<hr>
<ol class="legacy-numbers">
<ol>
	<li>Head to the Developers Console and enable the "Google Container Engine API" from [APIs &amp; Auth]-> [APIs] -> [Container Engine API] -> [Enable the API]</li>
	<li>Also inside the Google Developers Console, you need to enable billing for the Container Engine. [Compute]-> [Container Engine] -> [Enable Billing]</li>
</ol>
</ol>


<h3> Create Docker Machines on GCE </h3>
See the <a href="https://docs.docker.com/machine/#google-compute-engine" target="_blank">Docker Machine docs</a> for detailed descriptions and defaults of all of the Docker Machine flags.

The following is just the bare minimum for provisioning a machine:

<pre class="code-sample"><code>
docker-machine create \
--driver google \
--google-project api-project-xxxxxxxx \
google-machine
</code></pre>

If you haven't seen GCE before you will get prompted for an OAUTH authentication which will spring a web page where you accept and auth with your gmail account.

I ran into a bit of an issue here only on setting up a new project. Once the project was good to go then the docker machine CRUD was perfect. It almost seemed like there was some delay in the project propagating after I enabled billing. After an error on billing not being enabled (listed below in troubleshooting) I got the following API response:

<pre class="code-sample"><code>
Error creating machine: googleapi: Error 404: The resource 'projects/api-project-xxxxxxxxxx' was not found, notFound
You will want to check the provider to make sure the machine and associated resources were properly removed.
</code></pre>

I poked around for about 30 minutes, created a new project, got the same errors and proceeded to install the `gcloud` client listed in Troubleshooting. Then things just started working,(of course ;_). I don't think it was from doing anything with the `gcloud` client but its possible. I also listed my steps with that in case it was related. I haven't had time to recreate the steps to validate the issue or if it was just someone giving the gremlins water after midnight.

This is all normal stuff and to be expected when getting setup, which is another reason I'm excited about moving towards some ubiquity in container API interfaces because there is no value to me as a consumer using different but same abstractions and implementations when the end goal is all the same. It seems trivial but it is part of the commodities recipe that containerization will drive compute towards and ultimately a <a href="{{< relurl "/does-the-cost-of-cloud-iaas-intersect-the-local-vm/" >}}" target="_blank">race to zero</a>. Moving on!

To delete the machine or if something wasn't enabled properly on the Google side of your account you can delete the machine with the following (Note: force is used if there was an issue at provisioning and the instance is essentially orphaned meaning it exists on your docker machine side but not in GCE):

<pre class="code-sample"><code>
docker-machine rm -f google-machine
# Deleting disk.
# Successfully removed google-machine
</code></pre>

So here are two instances along with the rest of my free trial account stable of container ready docker host ponies in the cloud.

<pre class="code-sample"><code>
docker-machine ls
# NAME ACTIVE DRIVER STATE URL SWARM
# aws-machine amazonec2 Stopped
# dev virtualbox Saved
# digitalocean-machine digitalocean Running tcp://45.55.146.243:2376
# google-machine google Running tcp://130.211.137.13:2376
# google-machine2 google Running tcp://23.236.48.13:2376
# microsfot-unique-azure-unique azure Stopped tcp://microsfot-unique-azure-unique.cloudapp.net:2376
# metal-machine none tcp://172.16.86.133:2375
# racker-test-instance * rackspace Running tcp://162.209.126.37:2376
# virtualbox-machine * virtualbox Running tcp://192.168.99.100:2376
</code></pre>

Seriously, that sexy.
<h3> Run Docker on GCE Machines </h3>
From here on it it's smooth docker UI sailing.

<pre class="code-sample"><code>
docker run -d -p 80:80 nginx
</code></pre>

Next verify the service you started. First by getting the IP address of the VM you started with `docker-machine create`.

<pre class="code-sample"><code>
docker-machine ip test-machine
</code></pre>

Next curl the public port you started the service on using the IP address you just retreived:

<pre class="code-sample"><code>
curl 45.55.146.243:8000

# You can also nest the 'docker-machine ip' command in the curl requested
curl $(docker-machine ip test-machine):80
</code></pre>

The API supports stopping and starting, it does return `/creating/deleting` when `/start/stop/` are called from the Google API but other then semantics the operations look good.

<pre class="code-sample"><code>
docker-machine start google-machine
# Creating instance.
# Waiting for Instance...
# Uploading SSH Key
# Waiting for SSH Key
</code></pre>

And a `docker-machine stop`:
<pre class="code-sample"><code>
$ docker-machine stop google-machine
# Deleting instance.
# Waiting for instance to delete.
</code></pre>
<h3>Troubleshooting GCE Container Process</h3>
When you setup your GCE account, you have to enable billing as described above. If you don't enable billing you will get an error like so:

<pre class="code-sample"><code>
docker-machine create --driver google --google-project api-project-272576371661 google-machine
# Opening auth URL in browser.
# https://accounts.google.com/o/oauth2/auth?client_id=zzzzzzzzzzzzzzzz.apps.googleusercontent.com&amp;redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&amp;response_type=code&amp;scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute&amp;state=yyyyyyyyyyyyyyyy
# If the URL doesn't open please open it manually and copy the code here.
# Enter code: 4/LONG_CODE_BLAH
# Got code: 4/LONG_CODE_BLAH
# Saving token in /Users/brent/.docker/machine/machines/google-machine/gce_token
# Creating host...
# Generating SSH Key
# Creating instance.
# Creating firewall rule.
# Error creating machine: googleapi: Error 403: Project projects/api-project-xxxxxxxxxx cannot accept requests to insert while in an inactive billing state. Billing state may take several minutes to update., inactiveBillingState
# You will want to check the provider to make sure the machine and associated resources were properly removed.

</code></pre>

This bit is optional but I was having issues with the project not being found so gave the client API a shot to see if it resolved anything. I dont think it did but it was helpful to validate information and API requests.

(Optional)Install `gcloud` client..

<pre class="code-sample"><code>
curl https://sdk.cloud.google.com | bash
</code></pre>

Then Auth.. Which will pop open a web browser to get a token.
<pre class="code-sample"><code>
gcloud auth login
</code></pre>

Set the project name in your terminal to the project ID in the dev console

<pre class="code-sample"><code>
gcloud config set project planar-flux-xxxxx
</code></pre>

Thats it! Hopefully you are seeing the pattern of a common interface between dev/private/public virtual machines and provisioning containers within. Couple that with the ease of provisioning and de-provisioning services has both interesting Ops opportunities along with some serious potentials to reduce your cloud bills per workload by tearing down idle infra.
<hr>

Thanks for stopping by!