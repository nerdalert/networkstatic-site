+++
title = "Docker Machine Provisioning on AWS"
date = "2015-04-30T07:46:02+00:00"
lastmod = "2015-05-30T10:10:20+00:00"
author = "Brent Salisbury"
wp_id = 7559
categories = ["In the Lab"]
tags = ["AWS", "Docker", "Docker-Machine", "EC2"]
description = ""
url = "/docker-machine-provisioning-on-aws/"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "091135e2859f611837e6d495a27f61a2c53c2adad3a391592692da337c1e6622"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3> Docker Machine Provisioning on AWS</h3>
Next up in the docker machine <a href="http://normalizing-the-cloud-with-docker-machine" target="_blank">series</a> of integration posts is spinning up some cloud resources on Amazon EC2. The model is the same as previous docker machine posts, boot a VM running as a Docker host, add your cloud credentials for the provider and use your regular docker client commands on the remote Docker host in Amazon.

The docker machine docs are excellent at <a href="https://docs.docker.com/machine/" target="_blank">docs.docker.com</a>. These posts are just my notes as I am getting to know the docker machine provisioning harness.

<a href="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif"><img src="https://cloud.githubusercontent.com/assets/1711674/7408653/ffad6dbe-eeec-11e4-85b2-9fef61d02818.gif" alt="Docker Machine" width="645" height="675" class="aligncenter size-full wp-image-7574" /></a>
<hr>

<ul>
	<li>access-id and secret-key and VPC ID.</li>
	<li>First if you haven't before, sign up for the <a href="http://aws.amazon.com/free/" target="_blank">free tier at AWS</a> valid for a year. </li>
	<li>Next retrieve your VPC ID from the Services -&gt; '<a href="http://aws.amazon.com" target="_blank">VPC Dashboard</a>' -&gt; 'Your VPCs'</li>
	<li>Next, grab your access-id and secret-key for AWS. If you have never setup a user account before, simply do so from
<a href="https://console.aws.amazon.com/iam/home?#users" target="_blank">IAM Console</a> -&gt; Users  It will display the one time secret and ID.</li>
	<li> Lastly attach a policy to the new user account to enable API calls for resources. For simplicity sake, you can add "AdministratorAccess"</li>
</ul>


The `docker-machine create` examples were verified. Thanks to <a href="https://twitter.com/botchagalupe" target="_blank">@botchagalupe</a> for verifying them with me.

<h3> Export your account ENV variables: </h3>

This isn't required but it can be easier/cleaner to keep your credentials in the shell's environmental variables.
<pre class="code-sample"><code>
export AWS_ACCESS_KEY_ID=<Secret>
export AWS_SECRET_ACCESS_KEY=<Super_Top_Secret>
export AWS_VPC_ID=vpc-8752d5e2
</code></pre>

Verify that the AWS credentials are exported into your shell (these will need to be re-added if you switch to a new tab or terminal):

<pre class="code-sample"><code>
env | grep AWS
</code></pre>

<h3> Lets get Cloud Bursty </h3>

The region ID by default is: `us-east-1`
Inside of the of region is the `zone`. The zone will be only a letter. Look closely at the options in the <a href="https://docs.docker.com/machine/#amazon-web-services" target="_blank">Docker Machine docs</a> as there are a lot of moving parts. A default subnet is also used. Later in the post is an example of provisioning with a subnet argument passed. Container service zones can be viewed from Amazon <a href="http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region" target="_blank">here</a>.

<strong>!!Note!!</strong>- if you delete the default subnet for the VPC you will be required to provide a subnet per AWS SOP. The only way to restore the default subnet is to contact AWS support and have them create a new VPC for you.

Next create the machine like so:

<pre class="code-sample"><code>
docker-machine -D create \
    --driver amazonec2 \
    --amazonec2-access-key $AWS_ACCESS_KEY_ID \
    --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY \
    --amazonec2-vpc-id vpc-a8e5cfcd \
    --amazonec2-zone b \
    test-instance1
</code></pre>

It will take about 30-60 seconds for the VM to boot up and then return a successful create message.

<h3> Now Run Some Containers! </h3>
Now you have an excellent interface to all of your clouds.

For testing lets spin up a bash shell so you can poke around in the container:

<pre class="code-sample"><code>
docker run -it ubuntu /bin/bash
# Unable to find image 'ubuntu:latest' locally
# latest: Pulling from ubuntu
# ...
# ...
root@dc7264161d79:/#
</code></pre>

Verify we are in fact on our cloud instance for funzies:

<pre class="code-sample"><code>
apt-get install -y curl
curl ifconfig.me
#  52.5.11.81 </code></pre>

To remove the container, you use the normal docker commands:

<pre class="code-sample"><code>
# Grab the container ID
docker ps -lq
# Stop and Delete the container docker stop/rm
# or a one liner to stop and delte the most recent image etc.
docker ps -l -q | xargs docker stop | xargs docker rm
</code></pre>

To switch between docker machines you are manageing, notice the astericks '*' by 'test-instance' when you list the populated machines. That means that any 'docker' commands like spinning up a new container with 'docker run' will be performed on the active docker host/machine.

<pre class="code-sample"><code>
docker-machine ls

NAME ACTIVE DRIVER STATE URL SWARM
dev virtualbox Running tcp://192.168.99.102:2376
test-instance * amazonec2 Running tcp://52.5.11.81:2376
</code></pre>

To switch the active host, simply use the active command

<pre class="code-sample"><code>
docker-machine active dev
# [01:01:25] (='o'=) [~]docker-machine ls
# NAME ACTIVE DRIVER STATE URL SWARM
# dev * virtualbox Running tcp://192.168.99.102:2376
# test-instance6 amazonec2 Running tcp://52.5.11.81:2376
</code></pre>

To remove the Docker host/VM running the docker daemon with your containers simply run:
<pre class="code-sample"><code>
docker-machine rm test-instance
</code></pre>




<h3> Booting a Docker Machine with a Subnet Specified </h3>

The only difference when adding a specified subnet is you are adding a `--amazonec2-subnet-id` argument. The subnet must be added by you via API or the VPC web UI.

1) In order to specify a subnet ID you need to first create a subnet in the VPC.

<a href="{{< relurl "/wp-content/uploads/2015/04/Subnet-VPC.jpg" >}}"><img src="{{< relurl "/wp-content/uploads/2015/04/Subnet-VPC-660x500.jpg" >}}" alt="AWS VPC Subnet Creation" width="660" height="500" class="aligncenter size-large wp-image-7680" /></a>

2) Record the subnet-id and pass it into the `docker-machine create`. Since docker-machine will default to us-east-1 and zone a, if you create the subnet there, you can leave those parameters out. If the subnet was in say region `b` you would need to specify it in the create.

3) In this case I created a subnet in the region `us-east-1` and the zone `a`, those concatenated are `us-east-1a`. (which is the default in the docker-machine default parameters). 

If you were to pass that region and zone via the docker-machine API it would be:

`--amazonec2-region us-east-1`
`--amazonec2-zone a`

I am emphasizing the zones because its going to be what trips folks up if anything.



<pre class="code-sample"><code>

docker-machine create \
   --driver amazonec2 \
   --amazonec2-access-key $AWS_ACCESS_KEY_ID \
   --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY \
   --amazonec2-vpc-id $AWS_VPC_ID \
   --amazonec2-subnet-id subnet-209c260b \
   --amazonec2-zone a 
   test-aws-instance-2

# Launching instance...
# To see how to connect Docker to this machine, run: docker-machine env aws-instance-1
</code></pre>

Then view the new machine.
<pre class="code-sample"><code>
docker-machine ls
NAME                   ACTIVE   DRIVER         STATE     URL                                         SWARM
aws-instance-1                  amazonec2      Running   tcp://52.6.214.218:2376
</code></pre>

Here is output from another instance but with the `-D` debug flag with more details of the create:
<pre class="code-sample"><code>
# INFO[0000] Launching instance...
# DEBU[0001] creating key pair: test-instance
# DEBU[0001] configuring security group in vpc-42dffc27
# DEBU[0001] found existing security group (docker-machine) in vpc-42dffc27
# DEBU[0001] configuring security group authorization for 0.0.0.0/0
# DEBU[0001] launching instance in subnet subnet-209c260b
# DEBU[0002] waiting for ip address to become available
# DEBU[0021] Got the IP Address, it's "52.5.11.81"
# DEBU[0021] created instance ID i-efc00f39, IP address 52.5.11.81, Private IP address 172.31.50.167
# DEBU[0021] Settings tags for instance
# DEBU[0021] Getting to WaitForSSH function...
# DEBU[0177] generating server cert: /Users/brent/.docker/machine/machines/test-instance/server.pem ca-key=/Users/brent/.docker/machine/certs/ca.pem private-key=/Users/# brent/.docker/machine/certs/ca-key.pem org=test-instance
# INFO[0184] "test-instance" has been created and is now the active machine.
# INFO[0184] To point your Docker client at it, run this in your shell: eval "$(docker-machine env test-instance)"
</code></pre>




<h3> Troubleshooting </h3>

If you want to test your AWS permissions prior to getting started with machine you can download the client tool with (This is totally optional, it is only another way to troubleshoot AWS):

<pre class="code-sample"><code>
# Install easy_install
curl https://bootstrap.pypa.io/ez_setup.py -o - | python
sudo easy_install awscli
complete -C aws_completer aws
aws configure

# Answer the questions:
# AWS Access Key ID [None]: ...
# etc.
</code></pre>

You can also modify those key/values in '~/aws/credentials' and '~/aws/config'

<pre class="code-sample"><code>
~/.aws/config
~/.aws/credentials
$ cat ~/.aws/config
# [default]
# output = json
# region = us-east-1a
</code></pre>

Next verify the AWS permissions for the client account by querying AWS for the user list.

<pre class="code-sample"><code>
$ aws iam list-users
{
"Users": [
{
"UserName": "brent",
"Path": "/",
"CreateDate": "2015-04-27T06:51:28Z",
"UserId": "-----------",
"Arn": "arn:aws:iam::---------"
}
]
}
</code></pre>


It is probably safe to say most of the issues you will encounter are going to be related to your AWS ENVs. I listed a couple of examples and the resulting err messages for reference.

If you specify the wrong VPC (which I did the first go around, doh), you will see something like this:
<pre class="code-sample"><code>
docker-machine -v
#docker-machine version 0.2.0 (HEAD)

docker-machine -D create \
--driver amazonec2 \
--amazonec2-access-key $AWS_ACCESS_KEY_ID \
--amazonec2-secret-key $AWS_SECRET_ACCESS_KEY \
--amazonec2-vpc-id $AWS_VPC_ID \
--amazonec2-subnet-id $AWS_SUBNET_EAST1 \
test-instance
#INFO[0000] Launching instance...
#DEBU[0001] creating key pair: test-instance
#DEBU[0001] configuring security group in vpc-8752d5e2
#DEBU[0001] creating security group (docker-machine) in vpc-8752d5e2
#ERRO[0001] Error creating machine: Error decoding error response: Error decoding error response: http: read on closed response body
#WARN[0001] You will want to check the provider to make sure the machine and associated resources were properly removed.
#FATA[0001] Error creating machine
</code></pre>

Another potential issue is if you specify a subnet ID in the wrong availability region.

<pre class="code-sample"><code>
docker-machine create \
--driver amazonec2 \
--amazonec2-access-key $AWS_ACCESS_KEY_ID \
--amazonec2-secret-key $AWS_SECRET_ACCESS_KEY \
--amazonec2-vpc-id $AWS_VPC_ID \
--amazonec2-subnet-id subnet-209c260b \
--amazonec2-zone us-east-1 \
test-instance
</code></pre>
The resulting AWS API reply

<pre class="code-sample"><code>
## ERRO[0000] Error creating machine: unable to find a subnet in the zone: us-east-1a
## WARN[0000] You will want to check the provider to make sure the machine and associated # resources were properly removed.
## FATA[0000] Error creating machine
</code></pre>


The aws API client can list all of the resources that you may prefer over the web-ui. For example:

<pre class="code-sample"><code>
$ aws ec2 describe-subnets
</code></pre>
Returns:
<pre class="code-sample"><code>
{
"Subnets": [
{
"VpcId": "vpc-42dffc27",
"CidrBlock": "172.31.0.0/20",
"MapPublicIpOnLaunch": true,
"DefaultForAz": true,
"State": "available",
"AvailabilityZone": "us-east-1b",
"SubnetId": "subnet-60542817",
"AvailableIpAddressCount": 4091
},
{
"VpcId": "vpc-42dffc27",
"CidrBlock": "172.31.16.0/20",
"MapPublicIpOnLaunch": true,
"DefaultForAz": true,
"State": "available",
"AvailabilityZone": "us-east-1c",
"SubnetId": "subnet-58b72401",
"AvailableIpAddressCount": 4091
},
{
"VpcId": "vpc-42dffc27",
"CidrBlock": "172.31.48.0/20",
"MapPublicIpOnLaunch": true,
"DefaultForAz": true,
"State": "available",
"AvailabilityZone": "us-east-1a",
"SubnetId": "subnet-209c260b",
"AvailableIpAddressCount": 4091
},
{
"VpcId": "vpc-42dffc27",
"CidrBlock": "172.31.32.0/20",
"MapPublicIpOnLaunch": true,
"DefaultForAz": true,
"State": "available",
"AvailabilityZone": "us-east-1e",
"SubnetId": "subnet-a7567a9d",
"AvailableIpAddressCount": 4091
}
]
}
</code></pre>


Thats it! Easy peasy. Its pretty cool seeing the efficiencies in the cloud that you can get from one single EC2 instance. That OpEx efficiency of application virtualization is profound and few are starting to scratch the surface outside of the Google's of the world and some crafty web-scales that were ahead of their time. Next couple over next couple of nights I will dig into Google GCE, RackSpace (and anywhere else offering trials)  with docker machine and then dig into network use cases. To be clear, Im using CSPs that have a free trial so anyone can hack along with me.

<a href="{{< relurl "/running-docker-machine-on-rackspace-public-cloud/" >}}" target="_blank" rel="noopener noreferrer">Next up is Docker Machine on Rackspace Pub Cloud</a>