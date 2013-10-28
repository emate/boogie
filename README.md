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
python boogie.py [-p PORT] [-l BIND_ADDRESS]
</pre>

There are plenty of parameters, that you can use to simulate desired response. Parameters are send in query string of request, after ? (question mark) line in regular HTTP GET request.

<pre>
[address_of_server]:[port]/?par1name=par1value&par2name=par2value...
</pre>

##### Available parameters:
* code - return code for response
* sleep - send response afrer N seconds of sleep
* slowconn - set slowconnection mode
    * size - size of data to send in response in KB
    * rate - transfer rate from server while sending response in KB/s


Examples
======
To simulate 500 error after 10 seconds delay, send request like:
<pre>
curl localhost:8080/?code=500&sleep=10
</pre>

To simulate transfering of 10MB data through slow connection (e.g. 10KB/s), send request like:
<pre>
curl localhost:8080/?code=200&slowconn=True&size=10240&rate=10
</pre>

