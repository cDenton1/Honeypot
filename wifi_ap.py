# wifi_ap.py
import network

def startAP(ssid, sec_lvl):
    ap = network.WLAN(network.AP_IF)            # create WLAN network interface object - access point 
    ap.config(essid=ssid, security=sec_lvl)     # configure ssid and set security to 0 so it's open
    ap.active(True)                             # set the AP to active
    
    print("AP active:", ap.config('ssid'), "at", ap.ifconfig()[0])  # print out the ssid of the AP
    return ap