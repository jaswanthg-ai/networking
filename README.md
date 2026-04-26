# netwatch

Raw networking experiments in Python — no frameworks, no libraries beyond stdlib + psutil.

## What's here

**netwatch.py** — reads the kernel's socket table directly. Shows every 
open port, the process that owns it, and whether it's exposed to the 
network (0.0.0.0) or local only (127.0.0.1).

**server.py** — a raw HTTP server built on BSD sockets. No Flask, no 
Django. socket() → bind() → listen() → accept() → send(). 
This is what every web framework does underneath.

**server_threaded.py** — same server, one thread per connection. 
This is how Tomcat handled concurrency before NIO.

## What I actually understood building this

- A socket is a file descriptor the kernel gives you
- Ports are just numbers in a TCP packet header — the kernel routes 
  them to the right process
- HTTP is plain text over a TCP socket — headers, blank line, body
- Every framework from Spring Boot to Express is this loop at the bottom:
  while True: conn = accept(); thread(handle, conn)
