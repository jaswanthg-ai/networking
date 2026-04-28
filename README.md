# netwatch

Raw networking experiments in Python — no frameworks, 
no libraries beyond stdlib and psutil.

## modules

**netwatch.py** — reads the kernel's socket table directly 
via psutil. Shows every open port, the process that owns it, 
and whether it's exposed (0.0.0.0) or local only (127.0.0.1). 
Equivalent to netstat -ano but written from scratch.

**server.py / server_threaded.py** — raw HTTP server built 
on BSD sockets. No Flask, no Django. socket() → bind() → 
listen() → accept() → send(). This is what every web 
framework does underneath. Threaded version spawns one 
thread per connection — how Tomcat worked before NIO.

**raw_icmp_ping.py** — constructs ICMP Echo Request packets 
using struct.pack(), sends to local router, parses reply. 
Shows TTL, round trip time, and the raw packet bytes in hex. 
The string 'jaswanth-netwatch' is embedded in every packet 
payload — unencrypted, readable by Wireshark on the same WiFi.

**http_client.py** — opens a raw TCP socket to httpbin.org:80, 
constructs an HTTP GET request as bytes, reads the response. 
Then does the same to :443 wrapped in TLS — reads the 
certificate issuer, expiry, and cipher suite. Shows the 
exact point where HTTP becomes HTTPS — one wrap_socket() call.

## what I actually understood building this

- A socket is a file descriptor the kernel gives you
- Ports are numbers in a TCP packet header — kernel routes them
- HTTP is plain text over a TCP socket — headers, blank line, body
- ICMP has no ports — raw packet at IP layer, below TCP
- TLS sits on top of TCP — Diffie-Hellman key exchange means 
  session key is never transmitted, both sides derive it independently
- Firewalls are stateful rules engines inside the kernel — 
  not separate hardware
- Every framework from Spring Boot to Express is 
  socket → bind → listen → accept at the bottom.
