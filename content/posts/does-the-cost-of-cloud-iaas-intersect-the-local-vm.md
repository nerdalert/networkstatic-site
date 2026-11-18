+++
title = "Does the Cost of Cloud IaaS Intersect the Local VM?"
date = "2012-09-19T04:02:36+00:00"
lastmod = "2015-05-26T06:14:46+00:00"
author = "Brent Salisbury"
wp_id = 2799
categories = ["Speculative"]
tags = ["Enterprise", "Public Cloud", "Service Provider"]
description = ""
url = "/does-the-cost-of-cloud-iaas-intersect-the-local-vm/"
image = "/wp-content/uploads/2012/09/unicorn-accountant.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ff73a602a301f9ea90116e6d4d64eea10c2454b5aaeab0dbdb38c41e66250943"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Does the Cost of Cloud IaaS Intersect the Local VM?</h2>
Does the Cost of Cloud IaaS Intersect the Local VM? In the 90's if you were to recommend hosting your corporate email from a provider for cost savings you would probably get laughed out of a job. Today depending on the sensitivity of your data and levels of FUD in your organization suggesting keeping email long term on your premise you may get just as bizarre of looks from your colleagues. Hard to beat free. The ability to monetize things like 3Gb of storage from DropBox or free email to an Enterprise from Google is fascinating. Last I saw %97 of Googles income was from advertising.


<ul>
	<li>SaaS - Well, we all have a Gmail account.</li>
	<li>PaaS - Some examples-Wordpress <a href="http://wordpress.com" target="_blank">Wordpress.org</a>, Drupal <a href="http://www.drupalgardens.com" target="_blank">Drupalgardens</a>, (insert_prefix_names)Cloud(insert_suffix_names) doing pretty cool stuff, Ruby on Rails <a href="http://www.heroku.com" target="_blank">Heroku</a>.</li>
	<li>IaaS - Can it be monetized? Why not. Mine it? Add value like amazon does with extra services, features, availability etc. First hit is free. More PaaS integration? Wtf do I care about an OS again? Is it the wrong place to abstract? Probably</li>
</ul>

<hr />
If<strong> Google </strong>can be<strong> worth $200 Billion</strong> US and derive <strong>%97</strong> of it's revenue from <strong>advertising</strong>, anything is doable and leads me to never rule anything out.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Q1-2012.jpg" >}}"><img class="aligncenter  wp-image-2800" title="Q1 Q2 2012 Google Microsoft Apple" src="{{< relurl "/wp-content/uploads/2012/09/Q1-2012.jpg" >}}" alt="Q1 Q2 2012 Google Microsoft Apple" width="580" height="420" /></a></p>
<strong>Figure 1.</strong> Where does their money come from? Q1-Q2 2012 source: ZDNet
<h2>Competition Is The Key Amazon vs. Everyone Else in a Race to Free?</h2>
<hr />
We now have HP, IBM, PistonCloud to name a few in the pool with both feet betting on public cloud and new ecosystems like <a href="http://www.openstack.org" target="_blank">OpenStack</a> enabling some ubiquity to the provider offerings. Each have their own story to differentiate themselves from their competitors wether heavy on the platform support or geared towards hybrid cloud deployments. What will competition do? Certainly not raise the price, it will do what it always does and be a win for the consumer by forcing vendors to sacrifice margins to compete. Thats ok because guess what, there is a LOT of margin left.

<blockquote class="pullquote">"[Amazon's] margins for selling compute and storage are absurd," Brooks says. He notes that a basic EC2 unit — the workhorse of the AWS cloud — is around one half of one modern CPU (<a href="http://aws.amazon.com/ec2/instance-types/" target="_blank">a single EC2 unit</a>is roughly equivalent to a 1.0-1.2GHz AMD Opteron or Intel Xeon processor from 2007, according to Amazon). Amazon charges between $70 and $80 per month for these VMs, each of which has an operating price of $2-$4 per month, Brooks says. <footer><a href="http://www.zdnet.com/aws-can-anyone-catch-amazons-cloud-3040155322/">ZDNet</a></footer></blockquote>

Pretty ridiculous profit margins there. That said there is lots of cost that goes into running that operation plenty of room to drop significantly. While dominating the market share AWS prices have still been reduced <a href="http://gigaom.com/cloud/amazon-cuts-prices-again-on-key-web-services/" target="_blank">19 times</a> in the past 6 years. It would be safe to assume that the dramatic increase in public cloud providers this year, competition will speed up the decline in IaaS pricing significantly in the race to the bottom. 

The significant potential disrupters will be the network service providers (NSP). The cloud hypers can never address the fact that most of the carriers that make up the Internet take massive profit and will not invest the CapEx required to improve a customers network unless there is a business case. The Internet is far from the LAN of today. NSPs own the last mile into organizations. Traditional LECs have huge hardened buildings that formerly held giant phone switching banks that are now empty. If a carrier has not executed any cloud plans it is mainly because they are incredibly slow to change and innovate. Not too mention there are few architects within small to medium NSPs that can design cloud products. AT&T is basically giving away circuits to win above the net services. That will continue to put pressure on the incumbent AWS in the race to the bottom. 

<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/AWS.jpg" >}}"><img class="aligncenter  wp-image-2803" title="AWS" src="{{< relurl "/wp-content/uploads/2012/09/AWS.jpg" >}}" alt="aws vs local VM" width="599" height="362" /></a></p>
<strong>Figure 2.</strong> Amazon's own explanation. This is the basics of Cloud Economics and why AWS sees the end game as cloud. Don't buy what you dont use and the average shop cannot cannot manage to stay at 90% capacity at all times and either have too much or too little. While I agree with the problem I think it is the perfect rational for hybrid cloud to make the cost model work. Burst when you need to and keep the rest local. But what happens when 500 cloud instances are cheaper than 500 local instances? Hard not to think someone will monetize that cough *Google*. Google and GCE is the biggest threat. As details around GCE continue to emerge it will be the one to watch.
<hr />
<h2>Innovation Leads to Efficiency</h2>


This can get cheaper. Efficiency and innovation will continue to drive the operational cost to providers down. The more compute and storage you buy and operate  Power consumption which is arguably one of the bigger costs at scale alone in chips appears to be on the verge of extraordinary breakthrough with speculation of the 2013 Intel chip "Haswell" to be as low as 10 watts TDP (GPU included), that is a %41 decrease from the 2012 "Ivy Bridge" chip at 10 watts TDP. For those who scoff that Moore's law slowing an gates becoming too small to grow, tend to discount innovation.
<blockquote class="pullquote">"Intel often uses the Intel Developer Forum (IDF) as a platform to discuss its long-term vision for computing as well as more practical business initiatives. This year, the company has discussed the shrinking energy cost of computation as well as a point when it believes the energy required for 'meaningful computing' will approach zero and become ubiquitous by the year 2020. The idea that we could push the energy cost of computing down to nearly immeasurable levels is exciting.<footer><a href="http://www.extremetech.com/computing/136043-intel-predicts-ubiquitous-almost-zero-energy-computing-by-2020">ExtremeTech</a></footer></blockquote>
<hr />
<h2>Cloud Economics Operations at Scale</h2>

The economies of scale in CapEx, OpEx and operational efficiencies are what makes this work. The more compute and storage one has the cheaper that should be. Sidenote: Urs Hoezzle of Google had a great <a href="http://www.youtube.com/watch?v=VLHJUfgxEO4" target="_blank">talk</a> at the Open Networking Summit put on by the <a href="https://www.opennetworking.org/?option=com_wordpress&Itemid=72" target="_blank">ONF</a> pointing out when it comes to networking it is a much more linear and inefficient path.

I have been taking a position lately that the price of a local on premise VM in an average medium size Enterprise will at some point inflect or intersect with the cost of a cloud hosted VM. Cloud IaaS providers are use exactly what they buy and scale out and up to perfection. There is no such thing as overage and underage. The Average enterprises are not so good at making sure they are using exactly what they buy. Odds are there are some boxes, cycles, spindles, ports sitting around that never quite made it into production or was not quite forecasted properly in capacity planning. It is process, really really good process and mastering the human element which is a discipline beyond most organizations not in the business of delivering IT. Just as there are accountants that love their jobs, there are process people that really exist.
<p style="text-align: center;"><a href="{{< relurl "/wp-content/uploads/2012/09/Cloud-Cost.jpg" >}}"><img class="wp-image-2801 aligncenter" title="cloud vs local cost vm" src="{{< relurl "/wp-content/uploads/2012/09/Cloud-Cost.jpg" >}}" alt="cloud vs local cost vm" width="468" height="323" /></a></p>
<strong>Figure 3.</strong> These are hypothetical numbers but a visual representation of the potential intersection. My question is when?

Someone will make money off IaaS just as they have with giving away Gigs of storage or free office sweets. Free VMs is likely a bit harder than most, if the margins are as high as they appear and the Cap and OpEx are as low as they are at Hyper-Scale then I fully expect it to become cheaper than a half hearted DIY approach.

Until the early twentieth century, the amount of knowledge accumulated by mankind was doubling every 100 years. Now, the total amount of human knowledge is doubling every two to three years, likely reflected from the growth of the Internet and collective information. As we hurdle towards Singularity and the neuron and transistor becoming one in the same, to rule out innovation and the industries ability to turn a profit anywhere seems like a losing bet. Free is never free, but most "frees" are good enough for many organizations looking to focus on their organizations business objectives, rather than how to build bigger IT.

<hr>
Thanks for stopping by.