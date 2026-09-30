#!/usr/bin/env python3
"""Deep debug CDP interaction."""

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
        if tab.get("type") == "page" and "x.com" in tab.get("url", "") and "home" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    return None

ws_url = get_ws_for_x()
print(f"WS URL: {ws_url}")

ws = websocket.create_connection(ws_url, timeout=15)

def recv_filtered(ws, expected_id):
    """Receive messages until we get the expected response id."""
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == expected_id:
            return data
        # Skip events

# Enable domains
print("Enabling Page...")
recv_filtered(ws, 1)
ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
r = recv_filtered(ws, 1)
print(f"  Page.enable: {json.dumps(r)[:100]}")

print("Enabling Runtime...")
ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
r = recv_filtered(ws, 2)
print(f"  Runtime.enable: {json.dumps(r)[:100]}")

# Simple evaluation
print("\nTrying: document.title")
ws.send(json.dumps({
    "id": 3,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True
    }
}))

# Collect all messages for 5 seconds
start = time.time()
results = []
while time.time() - start < 5 and len(results) < 10:
    try:
        raw = ws.recv()
        data = json.loads(raw)
        results.append(data)
        print(f"  Got message type={data.get('id', 'event')}: {json.dumps(data)[:200]}")
    except:
        break

print(f"\nTotal messages received: {len(results)}")

# Check if we got the response
for r in results:
    if r.get("id") == 3:
        print(f"  Response for id=3: {json.dumps(r, indent=2)[:500]}")

# Try with contextId
print("\nTrying with ExecutionContextId...")
ws.send(json.dumps({
    "id": 4,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True,
        "contextId": 1
    }
}))

start = time.time()
while time.time() - start < 3:
    try:
        raw = ws.recv()
        data = json.loads(raw)
        print(f"  Message: {json.dumps(data)[:300]}")
    except:
        break

ws.close()
