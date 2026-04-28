import socket
import ssl

def raw_http(host, path='/'):
    print(f"\n── HTTP (port 80) ──────────────────────────────")
    print(f"Target: {host}{path}")
    print(f"────────────────────────────────────────────────\n")

    # 1. create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. connect — DNS + TCP handshake happens here
    sock.connect((host, 80))
    print(f"TCP handshake complete — connected to {host}:80")

    # 3. build raw HTTP request by hand
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    print(f"Sending:\n{request}")

    # 4. send it — just bytes over the socket
    sock.sendall(request.encode())

    # 5. read response
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    sock.close()

    # 6. split headers and body
    raw = response.decode(errors='replace')
    if '\r\n\r\n' in raw:
        headers, body = raw.split('\r\n\r\n', 1)
    else:
        headers, body = raw, ''

    print(f"── RESPONSE HEADERS ────────────────────────────")
    print(headers)
    print(f"\n── RESPONSE BODY ───────────────────────────────")
    print(body[:500])

    return response


def raw_https(host, path='/get'):
    print(f"\n── HTTPS (port 443 + TLS) ──────────────────────")
    print(f"Target: {host}{path}")
    print(f"────────────────────────────────────────────────\n")

    # 1. plain TCP socket — same as before
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 443))
    print(f"TCP handshake complete")

    # 2. wrap in TLS — this triggers the TLS handshake
    context = ssl.create_default_context()
    sock = context.wrap_socket(sock, server_hostname=host)
    print(f"TLS handshake complete — cipher: {sock.cipher()[0]}")

    # 3. inspect the certificate
    cert = sock.getpeercert()
    subject = dict(x[0] for x in cert['subject'])
    print(f"Certificate issued to: {subject.get('commonName')}")
    print(f"Valid until: {cert['notAfter']}")
    issuer = dict(x[0] for x in cert['issuer'])
    print(f"Issued by: {issuer.get('organizationName')}")

    # 4. exact same HTTP request as before
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    print(f"\nSending (encrypted — hacker sees noise):\n{request}")
    sock.sendall(request.encode())

    # 5. read response
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    sock.close()

    raw = response.decode(errors='replace')
    if '\r\n\r\n' in raw:
        headers, body = raw.split('\r\n\r\n', 1)
    else:
        headers, body = raw, ''

    print(f"\n── RESPONSE HEADERS ────────────────────────────")
    print(headers)
    print(f"\n── RESPONSE BODY ───────────────────────────────")
    print(body[:500])


# ── run both ─────────────────────────────────────
raw_http('httpbin.org')
raw_https('httpbin.org')
