+++
title = "Golang for Network Ops"
date = "2015-01-16T06:03:49+00:00"
lastmod = "2015-05-24T11:44:15+00:00"
author = "Brent Salisbury"
wp_id = 7441
categories = ["Programming"]
tags = ["Docker", "Go", "Socketplane"]
description = ""
url = "/golang-network-ops/"
image = "/wp-content/uploads/2015/01/twitter-gopher-banner-small.jpg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "ec43597e90b8a8352b0147a0ad99cfe30270fc2e2af3de1273e10d5518903287"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Golang for Network Ops</h2>

I get asked quite often where the traditional network engineer / network ops should start if they want to broaden their horizons with better code hacking skills or they have spent the last 20 years using Perl scripts or more recently Python and need a change. The answer is easy, Golang. At <a href="https://github.com/socketplane" target="_blank">Socketplane</a>, we all ditched the past couple of years of Java or C and now all code almost exclusively in Go. Go allows us to rapidly develop network solutions around <a href="https://www.docker.com/tryit/" target="_blank">Docker</a> which is written in Go, not to mention incredibly fun to develop in. We have a technology preview up and some really cool new things in development. Now there are many that could care less about the language they use and argue that is merely an implementation detail, the difference to me is if it takes you 3x the time in another language, or there is a performance penalty it is very relevant. That coupled with natively integrated tools, (go fmt, go run -race, go get, go test; etc) puts the productivity through the roof.

One of the creators, Rob Pike (who goes all the way back to Plan 9 at Bell labs) sums up what the goals were when they set out developing Go:

<blockquote class="pullquote">"I've said a lot about this since Go came out. In a nutshell, we wanted a language with the safety and performance of statically compiled languages such as C++ and Java, but the lightness and fun of dynamically typed interpreted languages such as Python. It was also important that the result be suitable for large systems software development on modern, networked, multicore hardware. To achieve these goals, we tried to design a language in which the various elements - the type system, the package system, the syntax, concurrency, and so on - were completely "orthogonal", by which I mean that they never interact in surprising ways, making the language easy to understand but also easy to implement."<footer>-Rob Pike</footer></blockquote>

Python like interfaces with similar performance as statically typed/linked languages is exactly what most network hackers I know would like. Just as important, is what is left out of the spec and how well if a program compiles it often will result in what you expected and test driven development is lightning fast in Go thanks to the static linking (which also leaves you with a tidy little binary to run or distribute). 

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2015/01/go-docker.png" >}}" alt=""></figure>

The orthogonal nature of go is at the heart of its appropriateness for infra projects. Go doesn't include the kitchen sink by design. It is intended to be readable, not magical. One of my favorite coding guidelines comes from Docker CTO Solomon Hykes in the <a href="https://github.com/docker/docker/blob/master/project/PRINCIPLES.md" title="Docker principles" target="_blank">Docker Principles</a> that makes Go such a perfect language for platforms. Some criticize go for not having generics. I am actually happy it doesn't because large collaborative projects with overlay confusing code bases are painful to say the least. Code/Peer reviews are the scalable paths to maintaining code quality, not complexity for the sake of complexity to exclude less then seasoned devs. The following quote is spot on to maintain code coherency (not to mention fun) in large OSS projects and it is reflected in the projects language of choice.

<blockquote class="pullquote">"50 lines of straightforward, readable code is better than 10 lines of magic that nobody can understand."<footer>-Solomon Hykes</footer></blockquote>

Many of my friends in the network community use Python, but often hit the wall when it comes down to multi-threading due to the global interpreter locking native to Python. You can spin up as many threads as you want but only one is being processed at any given time in order to stay safe. Go uses channels that are basically a sender and receiver that can share data between concurrent threads or "go routines". This is so much easier then concurrent programming of any other language I have used and not to mention extremely powerful as you can type a channel just as you would any other structure and this includes structs. 


<a href="http://dtucker.co.uk/" target="_blank">Dave Tucker</a> and more of our friends from the networking community will be doing some podcasts, hangouts and eventually meetups for those in NetOps interested in learning more about Go and how it applies to managing infra with a focus on Docker since it is natively written in Go, and well.. awesome. I titled this 'Golang for Network Ops' because I think as Rob Pike said, a Python like interface that is compiled to machine code and the associated performance, while still offering convenience of GC (zero latency at that) is perfect for both new and old network hackers alike. I networking performance is king, the same should apply to our tools. So I threw together some simple snippets for those like me who learn by breaking :)

<h2>Install Go</h2>






<ul>
	<li>For more assistance getting go installed here is a quick video tutorial <a href="https://www.youtube.com/watch?v=XCsL89YtqCs" target="_blank">Writing, building, installing, and testing Go code </a></li>
	<li> And the official <a href="http://golang.org/doc/install" target="_blank">getting started guide</a> (more resources at the bottom of the post)</li> 
</ul>





Download Go from <a href="http://golang.org/dl/" target="_blank">http://golang.org/dl/</a> and unzip the directory into /usr/local/ on Mac, Fedora or Ubuntu or use installers w/Mac and Windows. The most confusing thing for most is defining a $GOPATH env that points to where your libraries are stored. Instead of requiring a Makefile, you simply keep your libs/code in that path and the Go compiler takes care of the rest when linking.

<pre class="code-sample"><code>
#Can also be .profile or ~/.bash_profile for a Mac.
mkdir $HOME/go
echo "GOPATH=$HOME/go" >> ~/.bashrc
source ~/.bashrc
cd $HOME/go/src
</code></pre>

Install <a href="https://help.github.com/articles/set-up-git/" target="_blank">git</a>. yum install git /apt-get install git
Lastly clone a starter project to use:

<pre class="code-sample"><code>
cd $HOME/go/src
# The following will clone a starter repo and place it in your $GOPATH so the libraries can be referenced.
git clone https://github.com/nerdalert/go-netops-tutorials.git github.com/nerdalert/go-tutorial-examples
# Next go into the cloned directory and run any of the go files using 'go run <insert filename>.go' 
cd github.com/nerdalert/go-tutorial-examples
go run hello_world.go
</code></pre>

If the go compiler is not found, make sure it appears in your shells ENV path and the go binary is found like the following from a Mac.
<pre class="code-sample"><code>
go-tutorial-examples # echo $GOPATH
/Users/brent/code/go
go-tutorial-examples # which go
/usr/local/go/bin/go
</code></pre>
Each of the files have a main() declaration so they can each run standalone for ease for the first timer.



<ul>
<li>Run it on <a href="https://play.golang.org/" target="_blank">Go Playground</a></li>
</ul>


<pre class="code-sample"><code>
package main

import "fmt"

func main() {
fmt.Println("Hello World")
}
</code></pre>

<h2>Go Example for Python Devs</h2>
Lets do some exec calls. Execs are pretty similar to Python. If you want to perform sysadmin scripts using go it is as easy as Python for doing so.

Package <a href="http://golang.org/pkg/os/exec/" target="_blank">exec</a> runs external commands. It wraps os.StartProcess to make it easier to remap stdin and stdout, connect I/O with pipes, and do other adjustments.

<pre class="code-sample"><code>
package main

import "os/exec"
import "log"

func main() {

	// send two pings and send the ouput to STDOUT
	output1, err := exec.Command("ping", "-c", "2", "8.8.8.8").Output()
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("The results are -->  %s\n", output1)

	// run the date command and store the output
	output2, err := exec.Command("date").Output()
	if err != nil {
		log.Print(err)
	}
	// another wat to print
	log.Printf("The date is --> %s ", output2)
}
</code></pre>

Next lets attempt to resolve some DNS names.

<pre class="code-sample"><code>
package main

import (
	"fmt"
	"log"
	"net"
)

func main() {

	ip := "docker.io"
	ip2, _ := dnsLookup(ip)
	fmt.Println("docker.io resolves to --> ", ip2)

	// print a blank line for a space in output
	fmt.Println()

	// now lookup a fake hostname
	l33t := "badH0stN@me.c0m"
	dnsResp, _ := dnsLookup(l33t)
	fmt.Println("badH0stN@me.c0m doesnt resolve and prints a nil pointer, thats uglies --> ", dnsResp)

	// print a blank line for a space in output using print line
	fmt.Printf("\n")

	// now properly handle the nil response from the failed DNS lookup
	dnsResp2, err := dnsLookup(l33t)
	if err != nil {
		log.Printf("lookup failed for [ %s ]", l33t)
	} else {
		fmt.Println("g00gl3.c0m resolves to --> ", dnsResp2)
	}

	// print a blank line for a space in output using print format
	fmt.Printf("\n")
	// now properly handle a good response from a successful lookup
	ovs := "openvswitch.org"
	dnsResp3, err1 := dnsLookup(ovs)
	if err1 != nil {
		log.Println("lookup failed")
	} else {
		fmt.Println("openvswitch.org resolves to --> ", dnsResp3)
	}
}

func dnsLookup(ipStr string) (string, error) {
	ipAddr, err := net.ResolveIPAddr("ip", ipStr)
	return ipAddr.String(), err
}

</code></pre>


<h2>3 Different ways to Define Structs in Go</h2>
Structs and Pointers makes Go quite familiar for C programmers. A primary difference in how Go implements pointers is the built in garbage collection native to Go. This means pointers are dynamically dereferenced with zero latency. Zero latency is quite interesting for those who have ever seen a JVM do a massive GC with latency.

The following are three different ways to use structs. This can be familiar for both those coming from both OOP and C style data structures.




<ul>
<li>Run it on <a href="https://play.golang.org/p/YZn4hHXYdw" target="_blank">Go Playground</a></li>
</ul>


<pre class="code-sample"><code>

package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type Prefix struct {
	Network string
	Mask    int
}

func main() {

	valueStruct()
	time.Sleep(time.Second * 1)
	literalStruct()
	time.Sleep(time.Second * 1)
	pointerStruct()
}

func valueStruct() {
	// struct as a value
	var nw Prefix
	nw.Network = "10.1.1.0"
	nw.Mask = 24
	fmt.Println("### struct as a pointer ###")
	PrettyPrint(&nw)
}

func literalStruct() {
	// literal structs are the shortest LOC
	nw2 := &Prefix{"10.1.2.0", 30}
	fmt.Println("### struct as a literal ###")
	PrettyPrint(nw2)
}

func pointerStruct() {
	// struct as a pointer
	nw3 := new(Prefix)
	// very similar to setters/getters in OOP
	nw3.Network = "10.1.1.0"
	// or even like so
	(*nw3).Mask = 28
	fmt.Println("### struct as a pointer ###")
	PrettyPrint(nw3)
}

// print the contents of the network obj
func PrettyPrint(data interface{}) {
	var p []byte
	//    var err := error
	p, err := json.MarshalIndent(data, "", "\t")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("%s \n", p)
}

</code></pre>


<h2>Random Pointers</h2>
Access control to between packages is like most things in Go, simple yet effective. To export a function, method, interface from a package, you just start the name of it with a capital letter.

The following would be exported and accessible by any package in the project:
<pre class="code-sample"><code> func Foo() </code></pre>

While the following is only exported and accessible by the package it resides in only:
<pre class="code-sample"><code> func foo() </code></pre>

At any time you can run go files independant of the directory structure by calling them explicitly as long as there is a main() function and they are in the same package. For example, if you have a struct or function in one file (foo.go) and it is being called from another file that contains a main() execution in (bar.go) you can simply call them both with:

<pre class="code-sample"><code> go run foo.go bar.go </code></pre>

That will avoid any undefined errors from structs/methods/funcs/const etc not located in the same file being explicitly run.

<h2>Go Resources</h2>

So take a peek and keep an eye out for stuff we will be doing around NetOps, Docker and Go. It will be fun stuff.

<ul>
	<li> <a href="https://www.youtube.com/watch?v=2KmHtgtEZ1s" target="_blank">Get Started with Go</a> (Youtube)</li>
	<li> <a href="https://play.golang.org/" target="_blank">Go Playground</a> </li>
<li> <a href="http://golangtutorials.blogspot.com/" target="_blank">Go Lang Tutorials</a> </li>
<li> <a href="https://tour.golang.org/welcome/1" target="_blank">Tour of Go</a> (exercises) </li>
<li> <a href="https://www.softcover.io/downloads/88e295ad/GoBootcamp" target="_blank">Go Bootcamp</a> (free book) </li>
	<li> <a href="http://dave.cheney.net/resources-for-new-go-programmers" target="_blank">Resources for new Go programmers</a> via Dave Cheney's blog</li>
	<li> <a href="http://www.golang-book.com/" target="_blank">An Introduction to Programming in Go</a> (free book)</li>
	<li> <a href="https://www.youtube.com/watch?v=ytEkHepK08c" target="_blank">A Tour of Go</a> (Youtube)</li>
<li>  If you are new to Git, check out my friend Scott Lowe's recent blog posts on using Git. <a href="http://blog.scottlowe.org/2015/01/26/using-git-with-github/" target="_blank">Using Git with GitHub</a>. I also added an example of a pull request in the example project <a href="https://github.com/nerdalert/go-netops-tutorials" target="_blank"> README </a></li>

</ul>


Thanks for stopping by, checkout what we are up to at Socketplane and for those in networking, my top three recommendations for learning at the moment are Docker, OVS and Go!