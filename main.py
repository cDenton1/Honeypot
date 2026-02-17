# main.py
def run():
    from Honeypot.wifi_ap import startAP
    from Honeypot.config import SSID, SECURITY
    from Honeypot.portal import startServer
#     from Honeypot.connections import monitorConnect
#     from Honeypot.dns import startDNS
    from Honeypot.background import backgroundTask
    import time
    import _thread
    
    with open("log.txt", "w") as f:
        f.write("")
    
    ap = startAP(SSID, SECURITY)     # call for the ap to start
#     _thread.start_new_thread(startDNS, ())
#     _thread.start_new_thread(monitorConnect, (ap,))
    _thread.start_new_thread(backgroundTask, (ap,))
    startServer()