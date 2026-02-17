import time
import network
import _thread

known = set()

def monitorConnect(ap):
    global known
    while True:
        try:
            stations = ap.status('stations')
        except:
            stations = None
            
        if not stations:
            time.sleep(2)
            continue
        
        if isinstance(stations, dict):
            macs = stations.keys()
        elif isinstance(stations, list):
            macs = []
            for s in stations:
                if isinstance(s, tuple):
                    macs.append(s[0])
                else:
                    macs.append(s)
        else:
            macs = []
        
        for mac in macs:
            if mac not in known:
                known.add(mac)
                mac_str = ":".join("{:02x}".format(x) for x in mac)
                
                ts = time.time()
                print(f"[{ts}] New device connected: {mac_str}")
                
                with open("log.txt", "a") as f:
                    f.write(f"[{ts}] New device connected: {mac_str}\n")
        time.sleep(2)
    _thread.exit()