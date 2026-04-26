import subprocess
import re
import struct
import os

def get_gateway():
    out = subprocess.check_output('ipconfig', shell=True).decode()
    for line in out.splitlines():
        if 'Default Gateway' in line:
            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            if match:
                return match.group(1)
    return '192.168.0.1'

def ping(target_ip, count=4):
    print(f"\n── PING ────────────────────────────────────────")
    print(f"Target : {target_ip}")
    print(f"What's inside every packet: 'jaswanth-netwatch'")
    print(f"Protocol: ICMP — no ports, no TCP, no encryption")
    print(f"────────────────────────────────────────────────\n")

    out = subprocess.check_output(
        f'ping -n {count} {target_ip}',
        shell=True
    ).decode()

    times = []
    for line in out.splitlines():
        line = line.strip()
        if 'time=' in line.lower():
            match = re.search(r'time[=<](\d+)ms', line)
            if match:
                times.append(int(match.group(1)))
            print(line)

    if times:
        print(f"\nmin={min(times)}ms  avg={sum(times)//len(times)}ms  max={max(times)}ms")
        print(f"\nThose milliseconds = radio wave from your WiFi card")
        print(f"→ router antenna → router CPU → reply → back to you.")
        print(f"'jaswanth-netwatch' traveled that path {len(times)} times.")
        print(f"Unencrypted. Wireshark on your WiFi would show it in plain text.")
    else:
        print("No replies received.")

    print(f"\n── WHAT ICMP PACKET LOOKS LIKE IN MEMORY ───────")
    pid = os.getpid() & 0xFFFF
    seq = 0
    header = struct.pack('bbHHh', 8, 0, 0, pid, seq)
    payload = b'jaswanth-netwatch'
    packet = header + payload
    print(f"Bytes : {packet.hex()}")
    print(f"type=8 (echo request) | code=0 | checksum | pid | seq | payload")
    print(f"Total : {len(packet)} bytes physically sent per ping")

gateway = get_gateway()
print(f"Router found: {gateway}")
ping(gateway)