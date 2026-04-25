import socket, threading

def handle(conn, addr):
    request = conn.recv(1024).decode()
    print(f"Connection from {addr}")
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n<h1>Jaswanth was here</h1>")
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9999))
server.listen(100)

print("Multi-threaded server on port 9999...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle, args=(conn, addr))
    thread.start()
