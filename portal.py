# portal.py
import socket
from Honeypot.config import ALERT_RATE_LIMIT
from Honeypot.log import log

def loadHTML(file):
    with open(file, "r") as f:
        return(f.read())

formHTML = loadHTML("Honeypot/portalForm.html")
successHTML = loadHTML("Honeypot/portalSuccess.html")

def respond(HTML):
    return (
       "HTTP/1.1 200 OK\r\n"
       "Content-Type: text/html\r\n"
       "Connection: close\r\n\r\n"
        + HTML
    ).encode()

def parseHTTP(data, con):
    text = data.decode()
    
    headers, _, rest = text.partition("\r\n\r\n")
    lines = headers.split("\r\n")
    
    method, path, _ = lines[0].split(" ")

    content_length = 0
    for h in lines[1:]:
        if h.lower().startswith("content-length"):
            content_length = int(h.split(":")[1].strip())
    
    body = rest
    while len(body) < content_length:
        body += con.recv(512).decode()
    return method, path, body

def parseForm(body):
    fields = {}
    for pair in body.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            fields[k] = v.replace("+", " ")
    return fields

def receive(con):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = con.recv(512)
        if not chunk:
            break
        data += chunk
    return data

def startServer():
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(1)
    
    print("Portal running")
    
    while True:
        con, addr = s.accept()
        src_ip = addr[0]
        
        data = receive(con)
        method, path, body = parseHTTP(data, con)
        
        if method:
            log("HTTP", src_ip, f"{method} {path}")
        
        if method == "POST":
            if body:
                form = parseForm(body)
                log("FORM_SUBMIT", src_ip, form)
            con.send(respond(successHTML))
        else:
            con.send(respond(formHTML))
            
        con.close()