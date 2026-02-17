# dns.py
import socket

AP_IP = "192.168.4.1"

def startDNS():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 53))

    print("DNS hijack running")

    while True:
        try:
            data, addr = s.recvfrom(512)

            # Transaction ID (first 2 bytes)
            tid = data[:2]

            # DNS flags: standard response, no error
            flags = b"\x81\x80"

            # Question count = 1, Answer count = 1
            qdcount = b"\x00\x01"
            ancount = b"\x00\x01"
            nscount = b"\x00\x00"
            arcount = b"\x00\x00"

            header = tid + flags + qdcount + ancount + nscount + arcount

            # Question section (copy from request)
            question = data[12:]

            # Answer section
            answer = (
                b"\xc0\x0c"         # pointer to domain name
                b"\x00\x01"         # Type A
                b"\x00\x01"         # Class IN
                b"\x00\x00\x00\x3c" # TTL = 60s
                b"\x00\x04"         # IPv4 length
                + bytes(map(int, AP_IP.split(".")))
            )

            s.sendto(header + question + answer, addr)

        except Exception as e:
            print("DNS error:", e)

