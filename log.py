# log.py
import time

def log(event, src=None, extra=None):
    ts = time.time()
    print(f"[{ts}] {event} {src or ''} {extra or ''}")
    
    with open("log.txt", "a") as f:
        f.write(f"[{ts}] {event} {src or ''} {extra or ''}\n")