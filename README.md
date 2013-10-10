boogie
======

Boogie, pure Python HTTP error server.


Usage
======
<pre>
python boogie.py [-p PORT] [-l BIND_ADDRESS]
</pre>

To simulate 500 error after 10 seconds delay, send request like:
<pre>
curl localhost:8080/?code=500&sleep=10
</pre>
