import psutil
import socket

def get_open_ports():
    print("\n── OPEN PORTS ─────────────────────────────────────────")
    print(f"{'PORT':<8} {'PROTO':<6} {'BINDING':<22} {'PROCESS':<20} {'EXPOSED?'}")
    print("─" * 70)

    connections = psutil.net_connections(kind='inet')

    for conn in sorted(connections, key=lambda c: c.laddr.port if c.laddr else 0):
        if conn.status != 'LISTEN':
            continue

        port = conn.laddr.port
        ip   = conn.laddr.ip
        proto = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'

        try:
            proc = psutil.Process(conn.pid)
            name = proc.name()
        except Exception:
            name = 'unknown'

        exposed = 'YES ← exposed' if ip == '0.0.0.0' or ip == '::' else 'local only'
        print(f"{port:<8} {proto:<6} {ip:<22} {name:<20} {exposed}")

get_open_ports()
