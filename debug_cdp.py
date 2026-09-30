#!/usr/bin/env python3
"""Debug script to understand the CDP interaction with X."""

import json
import time
import websocket
import urllib.request
import os
import base64

CDP_HOST = "localhost:9222"

def get_ws_for_x():
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    for tab in tabs:
        if tab.get("type") == "page" and "x.com" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    return None

ws_url = get_ws_for_x()
print(f"WS URL: {ws_url}")

ws = websocket.create_connection(ws_url, timeout=15)

# Enable domains
for method, params, mid in [
    ("Page.enable", {}, 1),
    ("Runtime.enable", {}, 2),
]:
    ws.send(json.dumps({"id": mid, "method": method, "params": params}))
    resp = ws.recv()
    data = json.loads(resp)
    print(f"Enable {method}: {json.dumps(data)}")

# Navigate to X home
ws.send(json.dumps({"id": 3, "method": "Page.navigate", "params": {"url": "https://x.com/home"}}))
resp = ws.recv()
data = json.loads(resp)
print(f"\nNavigate: {json.dumps(data)[:200]}")
time.sleep(5)

# Take screenshot
ws.send(json.dumps({"id": 4, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
resp = ws.recv()
data = json.loads(resp)
if "result" in data and "data" in data["result"]:
    img = base64.b64decode(data["result"]["data"])
    with open("/home/rc/lucky-feet-website/assets/debug_screenshot.png", "wb") as f:
        f.write(img)
    print(f"\n📸 Screenshot saved ({len(img)} bytes)")

# Try simple JS evaluation
print("\n--- Testing Runtime.evaluate ---")
ws.send(json.dumps({
    "id": 5,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True,
        "awaitPromise": True
    }
}))

# Read all pending messages
messages_read = 0
while messages_read < 5:
    try:
        raw = ws.recv()
        data = json.loads(raw)
        print(f"Message {messages_read}: {json.dumps(data)[:300]}")
        messages_read += 1
    except:
        break

# Try a more complex JS evaluation
print("\n--- Complex JS evaluation ---")
ws.send(json.dumps({
    "id": 6,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "(() => { return { title: document.title, url: window.location.href, buttons: document.querySelectorAll('button').length }; })()",
        "returnByValue": True,
        "awaitPromise": True
    }
}))

messages_read = 0
while messages_read < 5:
    try:
        raw = ws.recv()
        data = json.loads(raw)
        print(f"Message {messages_read}: {json.dumps(data)[:500]}")
        messages_read += 1
    except:
        break

ws.close()
