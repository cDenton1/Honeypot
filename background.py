import time
import socket

AP_IP = "192.168.4.1"

def backgroundTask(ap):
    dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns.bind(("0.0.0.0", 53))
    dns.settimeout(0.1)

    print("DNS hijack running")

    known = set()
    last_station_check = 0

    while True:
        # ---------------- DNS hijack ----------------
        try:
            data, addr = dns.recvfrom(512)

            tid = data[:2]
            flags = b"\x81\x80"
            counts = b"\x00\x01\x00\x01\x00\x00\x00\x00"
            header = tid + flags + counts

            question = data[12:]

            answer = (
                b"\xc0\x0c"
                b"\x00\x01"
                b"\x00\x01"
                b"\x00\x00\x00\x3c"
                b"\x00\x04"
                + bytes(map(int, AP_IP.split(".")))
            )

            dns.sendto(header + question + answer, addr)

        except OSError:
            pass  # no DNS packet received

        # ------------- station monitoring -------------
        now = time.time()
        if now - last_station_check > 5:
            last_station_check = now
            try:
                stations = ap.status("stations")
            except:
                stations = None

            if isinstance(stations, dict):
                macs = stations.keys()
            elif isinstance(stations, list):
                macs = [s[0] if isinstance(s, tuple) else s for s in stations]
            else:
                macs = []

            for mac in macs:
                if mac not in known:
                    known.add(mac)
                    mac_str = ":".join("{:02x}".format(b) for b in mac)
                    print("New device connected:", mac_str)

        time.sleep(0.01)
