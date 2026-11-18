+++
title = "Python Tutorial: Classes, Objects, Methods, init and Simple Examples"
date = "2012-09-06T23:09:40+00:00"
lastmod = "2013-03-27T02:03:36+00:00"
author = "Brent Salisbury"
wp_id = 2452
categories = ["Programming"]
tags = ["Programming", "Python", "Tutorials"]
description = ""
url = "/python-tutorial-classes-objects-methods-init-and-simple-examples/"
image = "/wp-content/uploads/2012/09/python1.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "05c70cb08e2254f7346e5ede4b2b3a80ee7ee7de5ee0dff8bb5127a068dad5e1"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Python Tutorial: Classes, Objects, Methods, init and Simple Examples</h2>
Python Tutorial on Classes, Objects, Methods: In this post we will dive into Python classes, methods, objects and using the init constructer to initialize classes. Object oriented programming has gone well past being a fad (sorry punchcards) like it or not encapsulation and inheritance is winning out. The idea is to make modules and procedures abstracted, modifiable and reusable without needing to worry about reinventing the wheel. All interesting stuff, but this is just to give some examples as I am knocking off years of rust and having some fun with Python. These are just simple examples that might help folks out as they start learning programming. Most attempts Python tutorials on classes object methods etc, are more advanced than are appropriate for beginners.
<hr>
If you want a quick review on basic functions check this tutorial.

<ul>
	<li>More Python tutorials: <a href="{{< relurl "/python-tutorial-functions-and-passing-lists-and-dictionaries-with-simple-examples/" >}}" target="_blank">Functions and Passing Lists and Dictionaries with Simple Examples</a></li>
</ul>

<hr />


<h2>Python Classes and Object Oriented Programming OOB</h2>
<a href="{{< relurl "/wp-content/uploads/2012/09/Kitty-Coder.jpg" >}}"><img class="alignright size-full wp-image-2478" title="Kitty-Coder" alt="Kitty writing code" src="{{< relurl "/wp-content/uploads/2012/09/Kitty-Coder.jpg" >}}" width="247" height="247" /></a>
If you look at python.org <a href="http://docs.python.org/py3k/tutorial/classes.html">docs</a> the definition is about as clear as mud. No offense intended, programming concepts in general can fairly nacient and wide open to interpretation regardless of language since it is as much style and theory. I tend to explain classes and methods (think function in a class) as a blueprint for what to pass and object data with attributes being applied through a framework. I can pass an object (examples to follow) into a class and it modifies the object based on the <strong>blueprint</strong>.
<h2>Python Methods</h2>
In the simplest term a <a href="http://docs.python.org/py3k/tutorial/classes.html#method-objects" target="_blank">method</a> is a function inside of an object. You can pass attributes (variable inside a method) to the class and method that will get processed inside of the method and independently for each object. Variables or attributes defined or initialized at the beginning of the class are inherited to the methods inside that class. We will see in the examples.
<h2>Python Self for OOB</h2>
This can be rather confusing starting out. In a method which is a function inside of a class the first parameter is always <strong>self</strong>. <a href="http://www.tutorialspoint.com/python/python_classes_objects.htm" target="_blank">Self</a> is just referring to the object you passed into the method. Clear as mud? One other thing is a class object can be called or instantiated using __init__ (self). Using init will save you a couple lines of code. I learn through example so enough chit chat.
<h4>Practical Application (ever so loosely o_O)</h4>
A practical application of this could be calling a process that would spawn a VM to spin up. Here we will just print the name but you could execute a shell command that would spawn a widget.
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">subprocess.Popen(&quot;&quot;&quot; nova boot --flavor 1 --image &lt;insert image ID here&gt; --key_name \
 ssh_key&quot;&quot;&quot; VMnameFromPython &quot;&quot;&quot;, shell=True, stdin=None, executable=&quot;/bin/bash&quot;&quot;&quot;)</pre>
<h2>Class and Method Examples</h2>
So here are a couple of easy peasy examples that should help you get a kickstart, think of code reusability and as why you would add this extra complexity. Also you notice what happens when we try and print from the method, it returns 'none', in the next example we will change that to return which can be useful to break out of methods and also return parameters back from the method while pass would be indicate and empty block statement:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">#!/usr/bin/python
class VMname:
    def createVM(self, name):
        #Remember Self just refers to the object you are passing firstHot or secondHost
        self.name=name
        #Initialize the argument we passed with the object
    def stateVM(self):
        print(self.name)

#Create your first object
firstHost = VMname()
firstHost.createVM(&#039;email.foo.org&#039;)
Hname1 = firstHost.stateVM()
print(&#039;You named your VM &#039; + str(Hname1))

#Create your second object
secondHost = VMname()
secondHost.createVM(&#039;ldap.bar.org&#039;)
Hname2 = secondHost.stateVM()
print(&#039;You named your VM &#039; + str(Hname2))

#Notice what gets printed when we call the method stateVM, it prints &#039;None&quot;
#If we replace print(self.name) with return(self.name) 
#it will pass the attribute back outside of the class.
#Next we call a method directly using the variable assigned to the object and class &quot;firstHost&quot; with a &quot;.statVM() calling the method. 
#It will not pass back data from the class without us using return.
#Notice it says none.

print(firstHost.stateVM())
print(Hname2)</pre>
The output looks like this:
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">email.foo.org
You named your VM None
ldap.bar.org
You named your VM None
email.foo.org
None
None</pre>
<h2>Return Statement from a Function or Method in a Class</h2>
Let's add the '<strong>return</strong>' statement and add a bit of formatting. Return allows us to use the method data from the class outside of the class. I also added a couple of different ways to print strings in there for reference:
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">#!/usr/bin/python
class VMname:
    def createVM(self, name):
        self.name=name
    def stateVM(self):
        print(&#039;Your VMname is %s&#039; % self.name)
        print(&#039;Another Way to print the string from the method &#039; + self.name)
        return(self.name)

firstHost = VMname()
firstHost.createVM(&#039;email.foo.org&#039;)
Hname1 = firstHost.stateVM()
print(&#039;A third way to print your 1st VM &#039; + str(Hname1))

secondHost = VMname()
secondHost.createVM(&#039;ldap.bar.org&#039;)
Hname2 = secondHost.stateVM()
print(&#039;A third way to print your 2nd VM &#039; + str(Hname2))</pre>
The output looks like this:
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">Your VMname is email.foo.org
Another Way to print the string from the method email.foo.org
A third way to print your 1st VM email.foo.org
Your VMname is ldap.bar.org
Another Way to print the string from the method ldap.bar.org
A third way to print your 2nd VM ldap.bar.org</pre>
<h2>Constructors the Magical Method __init__ Example</h2>
When a instance of a class is created the initializer is called with <strong>__init__</strong>, this can set default values and can save you from explicitly initializing a class with something like "firstHost = VMname()" in our previous example. C+ <a href="http://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)" target="_blank">constructors</a> are a similar concept. Clear as mud!
<pre class="brush: python; gutter: false; first-line: 1; highlight: []; html-script: false">#Example #1 Class

class VMname:
    def createVM(self, name):
        self.name=name
    def stateVM(self):
        print(&#039;Printing from the 1st Class Example &#039; + self.name)
        print() #Adding Whitespace   

#Explicitly initializing the Class
example1 = VMname()
example1.createVM(&#039;classEx.foo.org&#039;)
example1.stateVM()

#Example #3 What the heck is this __init__?
class VMname1:
    def __init__(self, name):
        self.name=name
    def stateVM1(self):
        print(&#039;Printing from the 2nd Class Example &#039; + self.name)
        print() #Adding Whitespace

#__init__ initializes the Class
example2 = VMname1(&#039;constructorEx.foo.org&#039;)
example2.stateVM1()

#Example #3 Predefined Data
class VMname2:
    def __init__(self, name=&#039;predefinedvarsEx.foo.org&#039;):
        self.name=name
    def stateVM2(self):
        print(&#039;Printing from the 3rd Class Example &#039; + self.name)
        print() #Adding Whitespace

#__init__ initializes the Class and a predefined value for name
example3 = VMname2()
example3.stateVM2()</pre>
Here is the exciting output and names of our hosts!
<pre class="brush: text; gutter: true; first-line: 1; highlight: []; html-script: false">Printing from the 1st Class Example classEx.foo.org

Printing from the 2nd Class Example constructorEx.foo.org

Printing from the 3rd Class Example predefinedvarsEx.foo.org</pre>
That does it for this one. Excuse mistakes and bad concepts, a lot of this can be open to interpretation or just flat wrong but the examples are what I need mostly so hopefully those will help those visiting Python or knocking off the rust. More <strong>Tutorials</strong> in the <a href="{{< relurl "/category/programming/" >}}" target="_blank">Programming</a> section.
<hr>

<ul>
	<li>More Python tutorials: <a href="{{< relurl "/python-tutorial-functions-and-passing-lists-and-dictionaries-with-simple-examples/" >}}" target="_blank">Functions and Passing Lists and Dictionaries with Simple Examples</a></li>
</ul>

<hr />
Thanks for stopping by.
<hr />