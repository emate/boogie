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

To simulate 500 error after 10 seconds delay, send request like:
<pre>
curl localhost:8080/?code=500&sleep=10
</pre>
