boogie
======

Boogie, pure Python HTTP error server.


But... what for?
======

Modern applications often depend on remote resources, but sometimes there is one unknown. What's gonna happen when remote-site misbehaves?
Using Boogie server, you can test how your application behaves when some HTTP connection trouble appears.

Usage
======
<pre>
python boogie.py [-p PORT] [-l BIND_ADDRESS] [-c CONFIGFILE [-o]] 
</pre>

Boogie can operate in one of the two modes: Config mode or QueryString mode.


###### Config mode
In config mode, you can pre-define response parameters in config file. Config file should be valid JSON format. Using this mode, you can specify different parameters for different URI (see `Parameters->Config mode` section in this document).

###### QueryString mode
Using QueryString mode, you can specify response paraeters directly in query string, after ? (question mark) of URI (see `Parmaters->QueryString mode` section in this document). 

Parameters
======

##### Available parameters:
* code - return code for response
* sleep - send response afrer N seconds of sleep
* slowconn - set slowconnection mode
    * size - size of data to send in response in KB
    * rate - transfer rate from server while sending response in KB/s

You can pass parameters either in config mode, or QueryString mode:

Config mode
<pre>
{
    "/admin":  { 
        "code": 301,
        "sleep": 1
    },
    "default":  { 
        "code": 200
    }
}
</pre>


QueryString mode
<pre>
&lt;address_of_server&gt;:&lt;port&gt;/?par1name=par1value&par2name=par2value...
</pre>



Examples
======

##### Example 1
Imagine, you want to simulate some errors on www.my-fancy-remote-resource.com website. All you have to do, is to simply edit /etc/hosts file, and add line like this:
<pre>
127.0.0.1 www.my-fancy-remote-resource.com
</pre>

Then add some rules to config.json file
<pre>
{
    "/badresource/*":  { 
        "code": 500,
        "sleep": 20
    },
    "/longresource/*":  { 
        "code": 200,
        "sleep": 20
    },
    "default":  { 
        "code": 200,
        "sleep": 1
    }

}
</pre>
And start boogie on 80 port:
<pre>
sudo python boogie.py -p 80 -c /path/to/congig.json
</pre>
After that, you can check how your application will act without any changes in the code!

##### Example 2
To simulate 500 error after 10 seconds delay, send request like:
<pre>
curl localhost:8080/?code=500&sleep=10
</pre>
Similar example, but with pre-defined config:

config.json
<pre>
{
    "/app/*":  { 
        "code": 301,
        "sleep": 2
    },
    "default":  { 
        "code": 500,
        "sleep": 10
    }

}
</pre>
For every request on /app/* boogie will return 301 status code after 2 secons sleep. For any other request, there will be 10 second delayed response with 500 status code.


##### Example 3
To simulate transfering of 10MB data through slow connection (e.g. 10KB/s), send request like:
<pre>
curl localhost:8080/?code=200&slowconn=True&size=10240&rate=10
</pre>


TODO
======
* Extend config mode with capability to specify response headers/cookies etc.
* Unify POST and GET handlers
