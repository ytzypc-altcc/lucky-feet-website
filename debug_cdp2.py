#!/usr/bin/env python3
"""Debug script - properly handle CDP events vs responses."""

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

def cdp_cmd(method, params=None, msg_id=1):
    """Send a CDP command and wait for its response, filtering out events."""
    if params is None:
        params = {}
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == msg_id:
            return data
        # Skip events (they have "method" but no "id")

# Enable domains
print("Enabling domains...")
cdp_cmd("Page.enable", {}, 1)
cdp_cmd("Runtime.enable", {}, 2)

# Navigate
print("Navigating to X home...")
cdp_cmd("Page.navigate", {"url": "https://x.com/home"}, 3)
time.sleep(5)

# Screenshot
print("Taking screenshot...")
result = cdp_cmd("Page.captureScreenshot", {"format": "png"}, 4)
if "result" in result and "data" in result["result"]:
    img = base64.b64decode(result["result"]["data"])
    with open("/home/rc/lucky-feet-website/assets/debug_screenshot2.png", "wb") as f:
        f.write(img)
    print(f"  Screenshot saved ({len(img)} bytes)")

# Test JS evaluation - simple
print("\nTesting JS: document.title")
result = cdp_cmd("Runtime.evaluate", {
    "expression": "document.title",
    "returnByValue": True
}, 5)
print(f"  Result: {json.dumps(result, indent=2)[:500]}")

# Test JS evaluation - complex
print("\nTesting JS: page structure")
result = cdp_cmd("Runtime.evaluate", {
    "expression": """(() => {
        return {
            title: document.title,
            url: window.location.href,
            buttonCount: document.querySelectorAll('button').length,
            composeBtn: !!document.querySelector('[data-testid="SideNav_Tweet_Button"]'),
            composeArea: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            sidebar: !!document.querySelector('aside'),
            navItems: document.querySelectorAll('nav a, [role="navigation"] a').length,
        };
    })()""",
    "returnByValue": True,
    "awaitPromise": True
}, 6)
print(f"  Result: {json.dumps(result, indent=2)[:1000]}")

# Take another screenshot
print("\nTaking screenshot after JS check...")
result = cdp_cmd("Page.captureScreenshot", {"format": "png"}, 7)
if "result" in result and "data" in result["result"]:
    img = base64.b64decode(result["result"]["data"])
    with open("/home/rc/lucky-feet-website/assets/debug_screenshot3.png", "wb") as f:
        f.write(img)
    print(f"  Screenshot saved ({len(img)} bytes)")

# Try to find and click compose button
print("\nFinding compose button...")
result = cdp_cmd("Runtime.evaluate", {
    "expression": """(() => {
        const btn = document.querySelector('[data-testid="SideNav_Tweet_Button"]');
        if (btn) {
            return { found: true, text: btn.textContent?.trim(), ariaLabel: btn.getAttribute('aria-label'), testId: btn.getAttribute('data-testid') };
        }
        return { found: false };
    })()""",
    "returnByValue": True,
    "awaitPromise": True
}, 8)
print(f"  Compose button: {json.dumps(result, indent=2)[:500]}")

ws.close()
print("\nDone!")
