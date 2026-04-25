import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9999))
server.listen(5)

print("Server running on port 9999...")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()        # actually read what browser sent
    print(f"\nConnection from {addr}")
    print(f"Request:\n{request[:200]}")       # print the raw HTTP request
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n<h1>Jaswanth was here</h1>")
    time.sleep(0.1)
    conn.close()