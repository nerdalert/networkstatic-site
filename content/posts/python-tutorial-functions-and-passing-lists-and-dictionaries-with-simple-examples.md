+++
title = "Python Tutorial: Functions and Passing Lists and Dictionaries with Simple Examples"
date = "2012-09-04T06:54:38+00:00"
lastmod = "2013-05-26T21:48:57+00:00"
author = "Brent Salisbury"
wp_id = 2410
categories = ["Programming"]
tags = ["Programming", "Python", "Tutorials"]
description = ""
url = "/python-tutorial-functions-and-passing-lists-and-dictionaries-with-simple-examples/"
image = "/wp-content/uploads/2012/09/Python-Header.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "2aa6c9538d7bdc0c5d3049697a90eb2e6da3d421b99ce200e74995704732261b"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Python Tutorial: Functions, Passing Lists, Dictionaries with Simple Examples</h2>

In Python the differences between functions, classes and methods is often best explained with examples of code. It is also the best way to learn syntax and languages for some of us. We will start off with Functions and work into Classes which is the Object Oriented Programming (OOP) in Python over the next few posts. These are merely blueprints to run data through often times in an iterated fashion. Python is much like C in syntax minus declarations, in fact it, is written in C and interpreted in a C binary. This will be the first of a series of post that are a primer to the programming language Python. This Python tutorial will focus on functions with a refresher or start learning Python for beginners to look at lists, dictionaries / associative arrays.

<h2>Python Tutorial: Python Functions</h2>

A <a href="http://docs.python.org/py3k/tutorial/controlflow.html#defining-functions" target="_blank">function</a> is a start of code reusability in Python that we will later expand on with OOP concepts. We can call a function and pass or not pass arguments to the function.For anyone totally new to programming an example of an argument would be "ping 8.8.8.8", 8.8.8.8 was an argument we passed to the program ping.
<h2>Python Tutorial: Function without any Arguments Example</h2>

Lets make a function and call it.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def sld():
    print(&#039;Slowest Common Denominator&#039;)    
sld()
#Run that and your output will be:
&gt;&gt;&gt;Slowest Common Denominator</pre>

<h2>Python Tutorial: Function with a single Argument Example</h2>
<a href="{{< relurl "/wp-content/uploads/2012/09/Kitten-PC1.jpg" >}}"><img class="alignright  wp-image-2439" title="Nerd Kitten" src="{{< relurl "/wp-content/uploads/2012/09/Kitten-PC1-334x350.jpg" >}}" alt="" width="288" height="302" /></a>

Ok, that was easy enough. We made a function and called it with "sld()", that executed "def sld()" or "called" it for execution. Next lets pass an argument to be executed in the function. This begins hitting on the reusability factor of function. We are setting up a framework or routine that can be called many times and pass different data values to it each time.

We will pass an argument to a variable in the function, in this case "name" will get the string "brent is the" as it's value. We will then print the string in the function along with the argument we passed that is represented with the variable "name". When you define arguments in this fashion, you have to pass as many as you define to the function or you will get a syntax error.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def sld(name):
    print(name +&#039;Slowest Common Denominator&#039;)    
sld(&#039;Brent is the &#039;)
#This time we added a placeholder &quot;name&quot; in the function parentheses and passed it a string.
&gt;&gt;Brent is the Slowest Common Denominator</pre>
If you had not passed an argument to the definition but defined one you would get this type of error.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def sld(name):
    print(name +&#039;Slowest Common Denominator&#039;)    
sld(&#039;Brent is the &#039;)
&gt;&gt;    sld()
TypeError: sld() takes exactly 1 argument (0 given)</pre>

<h2>Python Tutorial: Function with Multiple Arguments Example</h2>
Now let's pass more than one variable.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def sld(name, tail):
    print(name +&#039; Slowest Common Denominator &#039;+ tail)    
sld(&#039;Brent is the&#039;, &#039;in the World&#039; )
#We passed two arguments and wrapped them around the string in the function.
&gt;&gt;Brent is the Slowest Common Denominator in the World</pre>

<h2>Python Tutorial: Python List Examples</h2>

Lets get a bit more flexible, lets pass a <a href="http://docs.python.org/tutorial/datastructures.html" target="_blank">list</a>. We will pass variable length arguments meaning, you can pass as many lists as you want. Quick refresher on lists, a list holds a number of objects inside of a sequence. A tuple is similar but the difference is a tuple cannot be modified while a list can. Example of a list.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
BadSocialMedia = [&#039;Facebook&#039;, &#039;MySpace&#039;]
#Print the List
print(BadSocialMedia)
#Print just one object in the list
print(BadSocialMedia[0])
#Remember counts start at 0 in Python
print(BadSocialMedia[1])
#Replace an Object in the 2nd place [1]. Note: Lists are mutable eg. we can change values.
BadSocialMedia[1] = &#039;Pinterest&#039;
print(BadSocialMedia)
#Create or append a new value in slot [2] the 3rd slot
BadSocialMedia.append(&#039;Twitter&#039;)
print(BadSocialMedia)</pre>
The output would look like this:
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">[&#039;Facebook&#039;, &#039;MySpace&#039;]
Facebook
MySpace
[&#039;Facebook&#039;, &#039;Pinterest&#039;]
[&#039;Facebook&#039;, &#039;Pinterest&#039;, &#039;Twitter&#039;]</pre>

<h2>Python Tutorial: Example Passing Variable Length Argument to a List in a Function</h2>
Now lets pass a list to a function notice I am using the built-in 'str' function to convert the list to a string in order to print the whole thing in the function.
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def socfun(args):
    print(&#039;Here is the whole list passed &#039; +str(args))
    print(&#039;Here is just one value parsed w/str &#039; +str(args[0])) 
    print(&#039;Here is just one value parsed w/o str &#039; + args[0]) 
#Define the List  
BadSocialMedia = [&#039;Facebook&#039;, &#039;MySpace&#039;, &#039;Pinterest&#039;]
#Call the function passing the List
socfun(BadSocialMedia)</pre>
Output:
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">Here is the whole list passed [&#039;Facebook&#039;, &#039;MySpace&#039;, &#039;Pinterest&#039;]
Here is just one value parsed w/str Facebook
Here is just one value parsed w/out str Facebook</pre>

<h2>Python Tutorial: Python Dictionaries</h2>
A Dictionary is like it sounds. It can take a keyword and associate it to a value or object. This is often referred to as an Associative Array. Since most reading this would be interested in infrastrcuture and/or networks a good example would be a mac address table entry. A <a href="http://www.sdncentral.com/products-technologies/sdn-openflow-tcam-need-to-know/2012/07/" target="_blank">BCAM</a> (Binary Content Addressable Memory) lookup or search index would be an associative array. If we had two fields one being a port and the other being the MAC address learned on that port are associated with a dictionary entry could look like this:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">Gig2/10 --&gt; 1cdf.0f95.08ba
Gig4/22 --&gt; 000c.2997.23dd</pre>
In Python that would look like this:
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
macAddrTable = {&#039;Gig2/10&#039;:&#039;1cdf.0f95.08ba&#039;, &#039;Gig4/22&#039;:&#039;000c.2997.23dd&#039;}
print(macAddrTable)
print(&#039;Who is on port gig2/10? &#039; + macAddrTable[&#039;Gig2/10&#039;])
Output:
{&#039;Gig4/22&#039;: &#039;000c.2997.23dd&#039;, &#039;Gig2/10&#039;: &#039;1cdf.0f95.08ba&#039;}
Who is on port gig2/10? 1cdf.0f95.08ba</pre>


<h2>Python Tutorial: Python Dictionaries and Functions</h2>

<ul>
	<li>Let's add a few functions. One will be a new MAC address was flooded on port Gigabit 3/2. We will pass the current state of the MAC addr tables and update it with the new entry on Gig3/2.</li>
	<li>The next function will replace a MAC an existing association on Gig4/22 with the new one heard from flooding.</li>
</ul>
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">#!/user/bin/python
def macAdd(macAddrTable):
    #new MAC address was learned on port Gig3/2 Update the tables
    print(&#039;We heard a new MAC address flood, lets update the MAC tables&#039;)
    macAddrTable[&#039;Gig3/2&#039;] = &#039;d067.e5e5.1354&#039;
    print(macAddrTable)
    print()

def macUpdate(macAddrTable):
    #A new MAC address was learned on port Gig3/2 Update the tables
    print(&#039;We heard a defferent MAC address flood on 4/22, lets replace the MAC entry&#039;)
    macAddrTable[&#039;Gig4/22&#039;] = &#039;0004.009d.039e&#039;
    print(macAddrTable)

macAddrTable = {&#039;Gig2/10&#039;:&#039;1cdf.0f95.08ba&#039;,
                &#039;Gig4/22&#039;:&#039;000c.2997.23dd&#039;}

print(&#039;The original MAC address table is:&#039;)
print(macAddrTable)
print()
print(&#039;Who is on port gig2/10 ??? --&gt; &#039; + macAddrTable[&#039;Gig2/10&#039;])
print()
#Call the macAdd function and pass the current state of the tables
macAdd(macAddrTable)
#Call the macUpdate function and pass the current state of the tables
macUpdate(macAddrTable)</pre>
The output looks like this:
<pre class="brush: python; gutter: true; first-line: 1; highlight: []; html-script: false">The original MAC address table is:
{&#039;Gig4/22&#039;: &#039;000c.2997.23dd&#039;, &#039;Gig2/10&#039;: &#039;1cdf.0f95.08ba&#039;}

Who is on port gig2/10 ??? --&gt; 1cdf.0f95.08ba

We heard a new MAC address flood, lets update the MAC tables
{&#039;Gig4/22&#039;: &#039;000c.2997.23dd&#039;, &#039;Gig2/10&#039;: &#039;1cdf.0f95.08ba&#039;, &#039;Gig3/2&#039;: &#039;d067.e5e5.1354&#039;}

We heard a defferent MAC address flood on 4/22, lets replace the MAC entry
{&#039;Gig4/22&#039;: &#039;0004.009d.039e&#039;, &#039;Gig2/10&#039;: &#039;1cdf.0f95.08ba&#039;, &#039;Gig3/2&#039;: &#039;d067.e5e5.1354&#039;}</pre>
Going to wrap up there for this review of Lists, Dictionaries and how they interact with Functions. We will get into some <a href="http://docs.python.org/py3k/tutorial/classes.html#a-first-look-at-classes" target="_blank">Object Oriented Programming</a> (OOP) in the next post.
<hr>

<ul>
	<li>More Python tutorials: <a href="{{< relurl "/python-tutorial-classes-objects-methods-init-and-simple-examples/" >}}" target="_blank">Python Tutorial: Classes, Objects, Methods, init and Simple Examples</a></li>
</ul>

<hr>
Thanks for stopping by.
<hr>