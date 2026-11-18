+++
title = "Getting Started With OVSDB"
date = "2013-10-01T01:57:09+00:00"
lastmod = "2014-05-06T21:20:24+00:00"
author = "Brent Salisbury"
wp_id = 6911
categories = ["Programming", "Tools"]
tags = ["Open vSwitch", "Programming", "Software Defined Networking"]
description = ""
url = "/getting-started-ovsdb/"
image = "/wp-content/uploads/2013/10/Open-Source.jpeg"
source_status = "publish"
source_password_protected = false
migration_generated = true
source_content_sha256 = "2f662162270cf387e76a62f25cb42e90aaf68b8087d7a923cb8779770909b6e2"
conversion_version = "0.11.0"
review_only = false
draft = false
+++

<h2>Getting Started With OVSDB</h2>

OVSDB (Open vSwtich Database) is a management protocol used to manipulate the configuration of <a href="http://openvswitch.org" target="_blank">Open vSwitches</a> and more recently vendors have begun implementing OVSDB in their Ethernet switches firmware. Some of those vendor data plane implementations are already running OVS under the hood so the implementation should be relatively painless. A project I am involved in developing is the OVSDB implementation in the OpenDaylight SDN platform. I will disclaim this post is relatively self-serving to act as a reference for anyone interested in being part of the Daylight implementation and a little bit about how we are going about coding it. But it is also for anyone interested in getting started with OVSDB. I see OVSDB as a keystone protocol for enabling programmatic networks in the future. Adoption is high underway from <em>almost</em> all networking software and hardware vendors.

The OVSDB schema consists of 13 tables with a database schema schema or blueprint defined in the OVSDB Schema document:

<a href="http://openvswitch.org/ovs-vswitchd.conf.db.5.pdf" target="_blank" rel="noopener noreferrer">OVSDB Schema</a>

If you are unfamiliar with Open vSwitch I highly cant recommend enough that you get familiar with it if involved in anything data center related. It is the reference SDN data plane implementation.

<a href="{{< relurl "/configuring-vxlan-and-gre-tunnels-on-openvswitch/" >}}" target="_blank" rel="noopener noreferrer">Compiling Open vSwitch from Source</a>


Or download the <a href="http://mininet.org" target="_blank">Mininet</a> image now managed by the <a href="http://onlab.us" target="_blank">On.lab</a>. I personally prefer Mininet for dev/test.

<a href="http://mininet.org" target="_blank" rel="noopener noreferrer">Download Mininet</a>

Once in Mininet you can download the daily OpenDaylight build from OpenDaylight Jenkins server.

<a href="https://jenkins.opendaylight.org/controller/job/controller-merge/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/" target="_blank" rel="noopener noreferrer">Download the OpenDaylight Daily Build</a>

<em>From Mininet run the following</em>:
<pre class="code-sample"><code>
apt-get update
apt-get install maven git openjdk-7-jre openjdk-7-jdk unzip
wget https://jenkins.opendaylight.org/controller/job/controller-merge/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/distribution.opendaylight-osgipackage.zip
unzip distribution.opendaylight-osgipackage.zip
cd opendaylight
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64
./run.sh
### Then go to http://<ip>:8080 ###
### On Mininet ###
mn --controller=remote,ip=<IP of Controller> --topo=linear,2 --listenport=6633</code></pre>

For more on building OpenDaylight from source and other tutorials see <a href="{{< relurl "/opendaylight-openflow-tutorial/" >}}" target="_blank">here</a> and <a href="https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation" target="_blank">here</a>.

<h2>OpenDaylight OVSDB Implementation</h2>
If you have interest in joining some of us in coding OVSDB into <a href="https://wiki.opendaylight.org/view/Main_Page#Work_Streams_.26_Committees" target="_blank">OpenDaylight</a> project all are welcome. The following is an architectural overview of the OVSDB project:

<a href="https://wiki.opendaylight.org/view/OVSDB_Integration:Design" target="_blank" rel="noopener noreferrer">OVSDB Architectural Implementation Overview</a>

We can be found on <a href="https://kiwiirc.com/client/irc.freenode.net" target="_blank">irc.freenode.net</a> in <strong>#opendaylight-ovsdb</strong> at all bizarre hours of the night and day.

<h2>JSON-RPC Transport</h2>


OVSDB is a uses JSON-RPC v1.0 to transport the messages.

JSON-RPC is an object that consists of three properties that are serialized into an object to be sent on the wire:
<ol class="legacy-numbers">
<ol>
	<li><em>Method</em> - A String containing the name of the method to be invoked.</li>
	<li><em>Params</em> - An Array of objects to pass as arguments to the method.</li>
	<li><em>ID</em> - The request id. This can be of any type. It is used to match the response with the request that it is replying to.</li>
</ol>
</ol>
<hr>
<h2>OVSDB Schema</h2>


The OVSDB manager can programs the OVSDB server daemon which resides in a persistent file on the data path vSwtich filesystem.

This is created during the build using the ovsdb-tool. For example:

<pre class="code-sample"><code>ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema</code></pre>

 The OVSDB manager programs the ovsdb-server process which implments the configuration in OVS. This is separate from the control plane forwarding instantiation by the OpenFlow protocol with the ovs-vswitchd daemon.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/09/ovsdb-vswitchd.png" >}}" alt="OVSDB Manager"></figure>

The OVSDB tables can be viewed with the following command:
<pre class="code-sample"><code>ovsdb-client dump</code></pre>
The command can be called remotely also:
<pre class="code-sample"><code>ovsdb-client dump tcp:172.16.58.131:6640</code></pre>

Like any database tables it the output contains rows and columns. The relations between the tables are listed in the OSDB schema document. Table rows key on on UUIDs for each object in the tables. For example a new port would have a new row uniquely identified with a UUID in the _uuid column. If that port is part of a particular bridge, that UUID would be listed in the "ports" column of the bridge it is a member of in the bridge table. A snippet of the output of the ovsdb-client dump command is below.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/09/ovsdb-tables.png" >}}" alt="OVSDB Dump"></figure>

In the following example the UUID c513db7b-ab35-4cf1-9e44-2d5ff2cabe86 is mapped to the name vif0 in a row in the port table. The name is in the "name" column of the row.

<pre class="code-sample"><code>
Port table
_uuid                                bond_downdelay bond_fake_iface bond_mode bond_updelay external_ids fake_bridge interfaces                             lacp mac name   other_config qos statistics status tag trunks vlan_mode
------------------------------------ -------------- --------------- --------- ------------ ------------ ----------- -------------------------------------- ---- --- ------ ------------ --- ---------- ------ --- ------ ---------
10563d98-6d2c-4ee5-9897-6a259c766195 0              false           []        0            {}           false       [fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf] []   []  "br0"  {}           []  {}         {}     []  []     []       
c513db7b-ab35-4cf1-9e44-2d5ff2cabe86 0              false           []        0            {}           false       [404b5777-8021-48d7-a223-c5b8c4cb9314] []   []  "vif0" {}           []  {}         {}     []  []     []       
</code></pre>

For the port to be added to the bridge br0, it is added to the array in the "ports" column in the row keyed on the UUID 3409f223-4a8c-4920-b227-c418cf338c4b that corresponds to name br0.

<pre class="code-sample"><code>
Bridge table
_uuid                                controller datapath_id datapath_type external_ids fail_mode flood_vlans mirrors name  netflow other_config ports                                                                        sflow status stp_enable
------------------------------------ ---------- ----------- ------------- ------------ --------- ----------- ------- ----- ------- ------------ ---------------------------------------------------------------------------- ----- ------ ----------
3409f223-4a8c-4920-b227-c418cf338c4b []         []          ""            {}           []        []          []      "br0" []      {}           [10563d98-6d2c-4ee5-9897-6a259c766195, c513db7b-ab35-4cf1-9e44-2d5ff2cabe86] []    {}     false     
</code></pre>


Using ovs-vsctl you can send commands with the vjsonrpc parameter to show the JSON requests you are sending.
<pre class="code-sample"><code>ovs-vsctl -vjsonrpc  --db=tcp:172.16.58.131:6640 add-br br0</code></pre>

An example output of the vjsonrpc parameter is as follows:

<pre class="code-sample"><code>root@mininet-vm:~# ovs-vsctl -vjsonrpc  --db=tcp:172.16.58.131:6640 show
Sep 30 15:14:40|00001|jsonrpc|DBG|tcp:172.16.58.131:6640: send request, method="monitor", params=["Open_vSwitch",null,{"Port":{"columns":["interfaces","name","tag","trunks"]},"Controller":{"columns":["is_connected","target"]},"Interface":{"columns":["name","options","type"]},"Open_vSwitch":{"columns":["bridges","cur_cfg","manager_options","ovs_version"]},"Manager":{"columns":["is_connected","target"]},"Bridge":{"columns":["controller","fail_mode","name","ports"]}}], id=0
Sep 30 15:14:40|00002|jsonrpc|DBG|tcp:172.16.58.131:6640: received reply, result={"Port":{"10563d98-6d2c-4ee5-9897-6a259c766195":{"new":{"name":"br0","trunks":["set",[]],"interfaces":["uuid","fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf"],"tag":["set",[]]}},"c513db7b-ab35-4cf1-9e44-2d5ff2cabe86":{"new":{"name":"vif0","trunks":["set",[]],"interfaces":["uuid","404b5777-8021-48d7-a223-c5b8c4cb9314"],"tag":["set",[]]}}},"Interface":{"fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf":{"new":{"name":"br0","type":"internal","options":["map",[]]}},"404b5777-8021-48d7-a223-c5b8c4cb9314":{"new":{"name":"vif0","type":"","options":["map",[]]}}},"Open_vSwitch":{"987c42d0-eab0-43d9-a32b-4246973706c2":{"new":{"ovs_version":"1.4.3","cur_cfg":53,"manager_options":["set",[]],"bridges":["uuid","3409f223-4a8c-4920-b227-c418cf338c4b"]}}},"Bridge":{"3409f223-4a8c-4920-b227-c418cf338c4b":{"new":{"name":"br0","ports":["set",[["uuid","10563d98-6d2c-4ee5-9897-6a259c766195"],["uuid","c513db7b-ab35-4cf1-9e44-2d5ff2cabe86"]]],"fail_mode":["set",[]],"controller":["set",[]]}}}}, id=0
987c42d0-eab0-43d9-a32b-4246973706c2
    Bridge "br0"
        Port "br0"
            Interface "br0"
                type: internal
        Port "vif0"
            Interface "vif0"
    ovs_version: "1.4.3"</code></pre>

You could start ovs-server with the following to have the JSON-RPC ID, Method and send Parameters be sent to STDOUT with the following:

<pre class="code-sample"><code>ovsdb-server /var/lib/openvswitch/conf.db -v --remote=ptcp:6640:172.16.58.131 --remote=db:Open_vSwitch,manager_options</code></pre>

The ovsdb-client can send raw JSON requests for provisioning to debug or help figure out formatting such as:

<pre class="code-sample"><code>ovsdb-client -v transact  tcp:172.16.58.128:6640 '["Open_vSwitch",{your JSON transact here}]'</code></pre>


<h2>Deserializing the JSON data with the Jackson Library</h2>

In order to receive the JSON name value pairs and do something meaningful with them, we need to deserialize and serialize the OVSDB JSON into meaningful objects. For this we are using the library called <a href="https://github.com/FasterXML/jackson" target="_blank">Jackson</a>.

A tiny snippet (1 bridge and 1 port) of raw OVSDB JSON looks like this:

<pre class="code-sample"><code>
{"Port":{"d97ecd2f-a0f9-495d-8637-e0849f7de291":{"new":{"trunks":["set",[]],"interfaces":["uuid","f3b84c90-a85b-4d97-9ddd-cd710a5490ce"],"name":"br0","tag":["set",[]]}},"8be80f67-f27a-4822-8130-76aa43e8d292":{"new":{"trunks":["set",[]],"interfaces":["uuid","181a8348-5a0b-4e34-bc7a-786901c61493"],"name":"tap2","tag":["set",[]]}},"7c1b9f41-8222-4c78-ad90-244e1a66baac":{"new":{"trunks":["set",[]],"interfaces":["uuid","eb43c2ae-0e49-4ac1-b249-18d493f11422"],"name":"tap1","tag":["set",[]]}},"7eb5508f-b2d9-4343-b7f3-b109bcd0ae86":{"new":{"trunks":["set",[]],"interfaces":["uuid","79b2d0ba-9ead-4149-9e4c-428dd14dc987"],"name":"JUNIT_BRIDGE_TEST","tag":["set",[]]}},"303d6f72-340b-468e-8bb7-7e44f15b77af":{"new":{"trunks":["set",[]],"interfaces":["uuid","e63cbe6f-ec12-4972-9170-079097e85c3d"],"name":"tap3","tag":["set",[]]}}},"Interface":{"181a8348-5a0b-4e34-bc7a-786901c61493":{"new":{"name":"tap2","type":"","options":["map",[]]}},"f3b84c90-a85b-4d97-9ddd-cd710a5490ce":{"new":{"name":"br0","type":"internal","options":["map",[]]}},"e63cbe6f-ec12-4972-9170-079097e85c3d":{"new":{"name":"tap3","type":"","options":["map",[]]}},"eb43c2ae-0e49-4ac1-b249-18d493f11422":{"new":{"name":"tap1","type":"","options":["map",[]]}},"79b2d0ba-9ead-4149-9e4c-428dd14dc987":{"new":{"name":"JUNIT_BRIDGE_TEST","type":"internal","options":["map",[]]}}},"Open_vSwitch":{"2cfdf9dd-e2a3-46b9-b09d-fbc68f23bc5d":{"new":{"ovs_version":"1.4.3","cur_cfg":301,"bridges":["set",[["uuid","3732d17d-339f-4f9d-a553-4396e1158df7"],["uuid","be7403fe-e124-4c29-931b-139cf060d021"]]],"manager_options":["uuid","fc37548a-aa08-427f-bf8d-cd88d81ae099"]}}},"Bridge":{"3732d17d-339f-4f9d-a553-4396e1158df7":{"new":{"name":"br0","ports":["set",[["uuid","303d6f72-340b-468e-8bb7-7e44f15b77af"],["uuid","7c1b9f41-8222-4c78-ad90-244e1a66baac"],["uuid","8be80f67-f27a-4822-8130-76aa43e8d292"],["uuid","d97ecd2f-a0f9-495d-8637-e0849f7de291"]]],"controller":["set",[]],"fail_mode":["set",[]]}},"be7403fe-e124-4c29-931b-139cf060d021":{"new":{"name":"JUNIT_BRIDGE_TEST","ports":["uuid","7eb5508f-b2d9-4343-b7f3-b109bcd0ae86"],"controller":["set",[]],"fail_mode":["set",[]]}}},"Manager":{"fc37548a-aa08-427f-bf8d-cd88d81ae099":{"new":{"target":"ptcp:6634:172.16.58.128","is_connected":false}}}}</code></pre>

To view the schema for your OVS server you can run the following. Pretty will print the output in a hierarchical format.

<pre class="code-sample"><code>ovsdb-client get-schema --pretty</code></pre>
Or remote
<pre class="code-sample"><code>ovsdb-client get-schema tcp:172.16.58.131:6640 --pretty</code></pre>

A snippet in a "pretty" print is the following using a JSON editor. Note, there are lots of online JSON editors <a href="http://goo.gl/BEsyZO" target="_blank">http://goo.gl/BEsyZO</a>

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/10/ovsdb-json.png" >}}" alt="JSON Output"></figure>


<h2>Super Simple Jackson Deserialization Example</h2>

A completely basic example of Jackson deserialization is the following. 
<pre class="code-sample"><code>{
  "Foo": "Bar",
  "NumberFoo": 100,
  "IsaFoo": true
}</code></pre>

Taking that JSON data, we will add it to a driver class as a string. We will map that String to a POJO (Plain Old Java Object). This will let us break out the names or values. 

<pre class="code-sample"><code>import com.fasterxml.jackson.databind.*;
import java.io.IOException;

public class Driver {

    public static void main(String[] args) {

        String msg = "{\"Foo\":\"Bar\",\"NumberFoo\":100,\"IsaFoo\":true}";

        ObjectMapper mapper = new ObjectMapper();
        try {
            ExamplePojo foo = mapper.readValue(msg, ExamplePojo.class);
            System.out.println("All of the values are:");
            System.out.println(foo.toString());
            System.out.println("=========================");
            System.out.println("Or retrieve individual value of Foo is ==> " + foo.getNumberFoo());
        } catch (JsonMappingException e) {
            System.err.println(e);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}</code></pre>

Next is the POJO.

<pre class="code-sample"><code>import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ExamplePojo {

    @JsonProperty("Foo")
    private String Foo;
    @JsonProperty("NumberFoo")
    private Integer NumberFoo;
    @JsonProperty("IsaFoo")
    private Boolean IsaFoo;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("Foo")
    public String getFoo() {
        return Foo;
    }

    @JsonProperty("Foo")
    public void setFoo(String Foo) {
        this.Foo = Foo;
    }

    @JsonProperty("NumberFoo")
    public Integer getNumberFoo() {
        return NumberFoo;
    }

    @JsonProperty("NumberFoo")
    public void setNumberFoo(Integer NumberFoo) {
        this.NumberFoo = NumberFoo;
    }

    @JsonProperty("IsaFoo")
    public Boolean getIsaFoo() {
        return IsaFoo;
    }

    @JsonProperty("IsaFoo")
    public void setIsaFoo(Boolean IsaFoo) {
        this.IsaFoo = IsaFoo;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return "ExamplePojo{\n" +
                "Foo='" + Foo + '\'' + ",\n" +
                "NumberFoo=" + NumberFoo + ",\n" +
                "IsaFoo=" + IsaFoo + ",\n" +
                "additionalProperties=" + additionalProperties + '}';
    }
}</code></pre>

The little sysout is the following:

<pre class="code-sample"><code>All of the values are:
ExamplePojo{
Foo='Bar',
NumberFoo=100,
IsaFoo=true,
additionalProperties={}}
=========================
Or retrieve individual value of Foo is ==> 100</code></pre>

This can get very tricky when demarshalling complex JSON such as OVSDB messages. Keys are polymorphic meaning they cannot be defined as an expected name value. The JsonProperty annotations (conceptually the same as <a href="http://docs.oracle.com/javase/tutorial/jaxb/intro/arch.html" target="_blank">JAXB</a> annotations but for JSON) are not required but merely helpers to help define the type. The are helpful when a name or value is an operator in the language. For example, the name "new" is significant to not only the OVSDB schema but also Java. In such a case annotations are very helpful to avoid gross coding tricks in order to get successful bindings.
<hr>
Simplistically, when dealing with tables only, you want to demarshall the elements within the JSON replies and associate those to meaningful identifiers.

<figure class="legacy-figure"><img src="{{< relurl "/wp-content/uploads/2013/10/unmarshall.png" >}}" alt="JSON Demarshalling OVSDB"></figure>

This approach and OVSDB in general are incredibly flexible and extensible. To add new elements it can easily be extended rather then replaced, thus extensibility == good.

<h2>OVSDB Monitor Method</h2>

There are various <a href="http://tools.ietf.org/html/draft-pfaff-ovsdb-proto-02#section-4.1" target="_blank">methods</a> in the OVSDB specification. One we will touch on in this is the monitor method. A monitor method will pull the requested tables and columns and return the associated configuration from OVSDB.

<blockquote class="pullquote">Subsequently, when changes to the specified tables are committed, the changes are automatically sent to the client using the "update" monitor notification (see Section 4.1.6).  This monitoring persists until the JSON-RPC session terminates or until the client sends a "monitor_cancel" JSON-RPC request.</blockquote>

After you send your initial monitor request, OVSDB will send you diffs as notifications over the open channel. The keys for the reply are "new" and "old". This means as the manager you now need to update your cache of the configuration for the element. This is vital for maintaining good state and amazing when talking about a realtime view of the state of network and compute elements. This is a million miles away from SNMP.

An example of an "update" method notification is the following:

<pre class="code-sample"><code>{
  id=10,
  error=null,
  result={
    Port={
      10563d98-6d2c-4ee5-9897-6a259c766195={
        new={
          trunks=[
            set,
            [
            ]
          ],
          external_ids=[
            map,
            [
            ]
          ],
          interfaces=[
            uuid,
            fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf
          ],
          name=br0,
          tag=[
            set,
            [
            ]
          ]
        }
      }
    },
    Interface={
      fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf={
        new={
          name=br0,
          type=internal,
          options=[
            map,
            [
            ]
          ]
        }
      }
    },
    Open_vSwitch={
      987c42d0-eab0-43d9-a32b-4246973706c2={
        new={
          ovs_version=1.4.3,
          cur_cfg=53,
          bridges=[
            uuid,
            3409f223-4a8c-4920-b227-c418cf338c4b
          ],
          manager_options=[
            set,
            [
            ]
          ]
        }
      }
    },
    Bridge={
      3409f223-4a8c-4920-b227-c418cf338c4b={
        new={
          name=br0,
          ports=[
            uuid,
            10563d98-6d2c-4ee5-9897-6a259c766195
          ],
          controller=[
            set,
            [
            ]
          ]
        }
      }
    }
  }
}</code></pre>

Or raw logs from our ODL module:

<pre class="code-sample"><code>[nioEventLoopGroup-2-1] INFO  o.o.ovsdb.internal.MessageHandler - {id=10,error=null,result={Port={10563d98-6d2c-4ee5-9897-6a259c766195={new={trunks=[set,[]],external_ids=[map,[]],interfaces=[uuid,fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf],name=br0,tag=[set,[]]}}},Interface={fe6a1fbc-dec3-43d9-b9fc-8ab74e84a3cf={new={name=br0,type=internal,options=[map,[]]}}},Open_vSwitch={987c42d0-eab0-43d9-a32b-4246973706c2={new={ovs_version=1.4.3,cur_cfg=53,bridges=[uuid,3409f223-4a8c-4920-b227-c418cf338c4b],manager_options=[set,[]]}}},Bridge={3409f223-4a8c-4920-b227-c418cf338c4b={new={name=br0,ports=[uuid,10563d98-6d2c-4ee5-9897-6a259c766195],controller=[set,[]]}}}}}</code></pre>

More on the Monitor method <a href="http://tools.ietf.org/html/draft-pfaff-ovsdb-proto-02#section-4.1.5" target="_blank">here</a>. The draft is great, Pfaff and Davie did a fantastic job on it. It is why we have not had to ping him once on the #OpenvSwitch irc channel (join that too :-). Course it helps to be working with developers like Madhu, Giovanni, Kyle to name a few.

<h2>OpenDaylight Nightly Build</h2>
If none of this made any sense, thats ok! There is lots of time to learn new things, this is a long funnel. Take a look at the nightly OpenDaylight build.
<a href="https://jenkins.opendaylight.org/controller/job/controller-nightly/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/" target="_blank" rel="noopener noreferrer">Download the Nightly OpenDaylight Build from the ODL Jenkins Server</a>

On a Mac run the following:

<pre class="code-sample"><code>wget https://jenkins.opendaylight.org/controller/job/controller-nightly/lastSuccessfulBuild/artifact/opendaylight/distribution/opendaylight/target/distribution.opendaylight-build133-2013-08-01_01-36-07-osgipackage.zip
unzip distribution.opendaylight-build133-2013-08-01_01-36-07-osgipackage.zip
cd opendaylight/
./run.sh</code></pre>
Once the JVM is started, point a browser at <a href="http://127.0.0.1:8080" target="_blank">http://127.0.0.1:8080</a>
<h2>Speak Now or forever Hold Your Peice</h2>



There is a books worth of material that could be covered here but only a short blogs worth of time. I am going to get into the <a href="http://netty.io" target="_blank">Netty</a> I/O socket abstraction library in the next post that is pretty geeky network programming and very important to the OpenDylight controller for non-blocking asynch socket messaging. If interested in exploring the amazing world of OVSDB and SDN with me and the ODL team, check out the <a href="https://wiki.opendaylight.org/view/Main_Page" target="_blank">OpenDaylight wiki</a> and jump on irc.freenode.net #opendaylight and #opendaylight-ovsdb. There are some brilliant folks who try and find time to help out community which is the core of OSS projects. If there ever was a time to get involved in some form or fashion, this is it. Whether it is coding, blogging, labbing, learning, tweeting it all goes on record as contributing to the community. More soon, cheers!