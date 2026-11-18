+++
title = "Getting Started with the Rust Programming Language"
date = "2020-01-02T15:58:54+00:00"
lastmod = "2020-01-07T02:25:49+00:00"
author = "Brent Salisbury"
wp_id = 7949
categories = ["Programming"]
tags = ["Programming", "Rust"]
description = ""
url = "/getting-started-with-the-rust-programming-language/"
image = "/wp-content/uploads/2020/01/rustacean-banner.png"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "4a9a1e3900b97f805361fd539152bfca6257d3298a66d36fb84f64bcb69d32a7"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h3>Getting Started with the Rust Programming Language</h3>

A programming language that has begun picking up momentum in the community lately is Rust. This is a guide aimed at helping folks get started with the Rust Programming Language. Rust has been around for a while with a stable v1.0 shipping in 2015. Rust initially came from Mozilla who maintain the multi-million line C++ codebase in Firefox that has bugs that Mozilla devs speak openly about being unfixable due to the unintended consequences up and down stream as a result. Rust does an amazing job via memory ownership and strict compilation rules, that address the massive problem of memory safety bugs and CVEs. In short, Rust is the overbearing parent you need in your life. 

In my (fairly new to Rust) opinion, Rust opens up lower level systems programming with performance on par with C/C++ to a wider audience. As a card carrying networking community member, I think there is potential for those who have been exploring Python, Java, Go to go a bit deeper into the breach with Rust. Be forewarned, it is a lower level language and thus is inherently more complex due to less abstractions. 

Oh, did I mention it actually has a dependance and build management system built in! I love <a href="{{< relurl "/golang-network-ops/" >}}" rel="noopener noreferrer" target="_blank">Go</a> but it's dependency management is a dumpster fire, at last count there are 16 separate project build/dependency management. Pip/virtualenv is well, Python being Python and I still suffer nightmares of 45 minute Maven builds from my Java days.


<h3>Rust Language Highlights</h3>

If you learn like I do, here are the highlights and then skip to the bottom of the page for resource links that I have been using the past few weeks to start learning Rust. These are my general impressions of the language after a few weeks of hacking:


<ul>
<li>Performance on par with C/C++ but much safer due to the unique cornerstone of Rust memory ownership and borrowing for safety guarantees without implementing a garbage collector.</li>
<li>An amazing (and simple to use) built in dependency and build management system.</li>
<li>Lots of examples in the std library API docs. The syntax can get a bit harry here and there so having examples in the docs are great</li>
<li>There is no concept of nil values. Since nil/null can result in null pointer exceptions or worse, a dev never doing null checks, in Rust output can have either (Some) value or no value (None) and for results either success (Ok) or failure (Err). This is similar to Haskell with match statements. This has probably been the hardest thing for me to get used to. Some(T) is the closest you get to a null value in Rust.</li>
<li>Compiles to a binary.</li>
<li>String vs str is kind of clunky. A <code>String</code> is essentially heap allocated and growable that you generally would use if you need to modify the data (same as Vec). A str is a fixed length view of the data that you would borrow using a reference <code>&str</code>.</li>
<li>Functions only return one value (denoted with a -> operator). They do not require a return statement but can perform early returns with a return statement. Get used to the enum <code>Result< T, E ></code>.</li>
<li>Conveniences of a high level language in a low level language that lowers the barrier to entry of this type of systems programming (Rust supports methods!).</li>
<li>Built-in support for multi-threading</li>
<li>Strict compiler and rules in general (memory ownership) that protect you from yourself.</li>
<li>Rust is positioned to be the leader in WebAssembly apps due to its extremely small runtime footprint like C/C++ but with tooling that makes it attractive (imo).</li>
<li>You get to watch C++ programmer heads explode when you ask them about Rust.</li>
</ul>



<h3>Dealing with Memory in Rust</h3>

One of the biggest difference from other languages is there is no garbage collector, nor is there explicit memory management. Rust doesn't let you run with scissors and in turn makes it pretty easy produce stable code due to the strict nature of ownership. In lieu of garbage collection is the concept of ownership.


The following are the <a href="https://doc.rust-lang.org/1.30.0/book/second-edition/ch04-01-what-is-ownership.html" rel="noopener noreferrer" target="_blank">three rules of ownership</a> as defined by the Rust Book distributed with the Rust releases. I added a couple of thoughts to them (not in bold) below.


<ul>
<li><strong>Each value in Rust has a variable that’s called its owner.</strong> - the borrow checker can be painfully consistent (but that's a good thing). The alternative is a 10,000 line method where nothing transfers since you borrowed everything at once.</li>
<li><strong>There can only be one owner at a time.</strong> - If there were two owners at once, and changes the ptr the other has no idea. This prevents the double-free scenario in C or C++. </li>
<li><strong>When the owner goes out of scope, the value will be dropped.</strong> - The easiest example is passing a variables to a function. The variable gets moved into a new stack frame and the old one is destroyed in the stack. You can work around this by referencing immutable borrowed references (e.g. `&x`). </li>
</ul>


<img src="{{< relurl "/wp-content/uploads/2020/01/memory-vulns-linux-660x513.png" >}}" alt="" width="660" height="513" class="aligncenter size-large wp-image-7946" /></a>

Source - <a href="https://phil-opp.github.io/talk-konstanz-may-2018/#14" rel="noopener noreferrer" target="_blank">The Rust Way of OS Development </a>
<hr>
<img src="{{< relurl "/wp-content/uploads/2020/01/image-660x257.png" >}}" alt="" width="660" height="257" class="aligncenter size-large wp-image-7945" /></a>
Source - <a href="https://msrc-blog.microsoft.com/2019/07/16/a-proactive-approach-to-more-secure-code/" rel="noopener noreferrer" target="_blank">A proactive approach to more secure code</a>

<h3>Rust Concurrency</h3>

Like any new language built by the community is like a big boat, it can be hard to steer. Concurrency is one of the harder problems in computing, so it's no surprise there are a number of various runtimes to deal with concurrency. Since most people reading this care about networking, a concurrency implementation will be relevant for async network i/o. The majority Rust projects I have run across use <a href="https://docs.rs/tokio" rel="noopener noreferrer" target="_blank">tokio</a> but as of November, 2019 <a href="https://docs.rs/async-std/" rel="noopener noreferrer" target="_blank">async-std</a> v1.0 stable which future APIs will be built on this initial release. Rust natively uses OS threads. Rust had a green thread implementation prior to v1.0 that was removed. Tokio and possibly the newer async-std look to address the c10k issue of spawning a million threads for the OS to manage. I'm guessing futures/async will be a choose your own adventure area for a while. 

<h3>Getting Started Hacking with Rust</h3>

I think the basic getting started exemplifies the extent the creators went to in empathizing with a user in making an incredibly easy starter project.

Current installation instruction for Rust and it's toolchain can be found at <a href="https://www.rust-lang.org/tools/install" rel="noopener noreferrer" target="_blank">rust-lang.org</a>

Currently, you can use:
<em>curl</em> https://sh.rustup.rs -sSf | sh

Next, you can create a quick project to validate the installation and run your first project:

<pre class="lang:sh decode:true ">
source ~/.cargo/env 
cargo new hello-rust --bin
cd hello-rust/
cargo run ./
</pre>

This will create a hello world sample in `src/main.rs` that contains a main function with a print statement.

<pre class="lang:rust decode:true ">
fn main() {
    println!("Hello, world!");
}
</pre>

To compile your app to a binary, you can do something like this:

<pre class="lang:sh decode:true ">
# Install the target platform you are compiling on or cross compiling to:
rustup target add x86_64-unknown-linux-gnu
cargo build --release --target=x86_64-unknown-linux-gnu

# or for Mac OSX
rustup target add x86_64-apple-darwin
cargo build --release --target=x86_64-apple-darwin

# Then look in the build target platform directory for the binary:
ls target/x86_64-apple-darwin/release/
</pre>


<h3>Install an IDE for Rust</h3>

For an IDE, there are two main ones. VSCode and the Jetbrains <a href="https://intellij-rust.github.io" rel="noopener noreferrer" target="_blank">Rust plugin</a>. Jetbrains tends to open source a new language for development and bug testing and then discontinue the project when they commercialize the platform, e.g. Goland. I've tried both and prefer <a href="https://code.visualstudio.com" rel="noopener noreferrer" target="_blank">VSCode</a>. If you choose VScode, once it is installed, go to preferences -> extensions and install <a href="https://github.com/rust-lang/rls-vscode" rel="noopener noreferrer" target="_blank">Rust Language Server (rls)</a>. As a consumer of Jetbrains products for a long time, this has converted me to VSCode for Rust dev. I still love Intellij for Java fwiw.


<h3>Rust Learning Resources</h3>

Lastly, below are the resources I found helpful for getting started.



<ul>
<li><a href="https://doc.rust-lang.org/1.30.0/book/2018-edition/index.html" rel="noopener noreferrer" target="_blank">Rust Programming Language</a> The canonical Rust book that is free.</li>
<li><a href="https://www.youtube.com/watch?v=EYqceb2AnkU&list=PLJbE2Yu2zumDF6BX6_RdPisRVHgzV02NW" rel="noopener noreferrer" target="_blank">Intro to Rustlang - Tensor Programming</a> A fantastic web series by  on Youtube. While youtube is generally a toxic dumpster fire, it can be great for learning new languages for those who respond well to video follow alongs like myself. I have found this better than some of the paid videos I previewed.</li>
<li><a href="https://www.youtube.com/watch?v=vOMJlQ5B-M0&list=PLVvjrrRCBy2JSHf9tGxGKJ-bYAN_uDCUL" rel="noopener noreferrer" target="_blank">Rust Programming Tutorial (beginners)</a> If you learn via code snippets, this Youtube series from will be right up your ally. 
<li><a href="https://www.youtube.com/watch?v=lJ3NC-R3gSI" rel="noopener noreferrer" target="_blank">Rust's Journey to Async/Await</a> or any talk by Steve Klabnik.</li>

<li>As one that learns via snippets, I have been pushing my Rust pieces and parts as I have been going here: <a href="https://github.com/nerdalert/rust-examples" rel="noopener noreferrer" target="_blank">nerdalert/rust-examples</a> and a quick project for latency monitoring and graphing in Rust here: <a href="https://github.com/nerdalert/cloud-latency" rel="noopener noreferrer" target="_blank">nerdalert/cloud-latency</a>
<li>What would a language be without a web interface playground - <a href="https://play.rust-lang.org" rel="noopener noreferrer" target="_blank">play.rust-lang</a></li>
<li><a href="https://github.com/ctjhoa/rust-learning" rel="noopener noreferrer" target="_blank">ctjhoa/rust-learning</a> is an exceptional list of curated Rust resources </li> 
</ul>

That's it for now. Thanks for reading. I will be posting more in coming weeks including how Rust can impact the networking landscape we have today.