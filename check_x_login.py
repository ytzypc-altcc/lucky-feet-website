#!/usr/bin/env python3
"""Navigate to X and check login status via CDP."""
import json, time, urllib.request, os, base64, websocket
from datetime import datetime

CDP = "http://localhost:9222"
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def cdp_cmd(ws, method, params=None, msg_id=1):
    if params is None:
        params = {}
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == msg_id:
            return data

def eval_js(ws, expr, msg_id=1):
    result = cdp_cmd(ws, "Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True}, msg_id)
    if "result" in result and "value" in result["result"]:
        return result["result"]["value"]
    exc = result.get("result", {}).get("exceptionDetails")
    if exc:
        print(f"  JS Exception: {exc.get('text', '')}")
    return None

def take_screenshot(ws, msg_id=99):
    result = cdp_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None

def main():
    print("Connecting to Chrome on port 9222...")
    
    # Get browser WS URL
    req = urllib.request.Request(f"{CDP}/json/version")
    resp = urllib.request.urlopen(req, timeout=5)
    info = json.loads(resp.read())
    ws_url = info.get("webSocketDebuggerUrl")
    print(f"Browser WS: {ws_url}")
    
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected to browser")
    
    try:
        # Enable domains
        cdp_cmd(ws, "Target.enable", {}, 1)
        cdp_cmd(ws, "Runtime.enable", {}, 2)
        cdp_cmd(ws, "Page.enable", {}, 3)
        
        # Create a new target/tab
        print("\n📌 Creating new tab...")
        result = cdp_cmd(ws, "Target.createTarget", {"url": "about:blank"}, 10)
        target_id = result.get("result", {}).get("targetId")
        print(f"  Target ID: {target_id}")
        
        if not target_id:
            print("  ❌ Failed to create target")
            ws.close()
            return False
        
        # Connect to the new target
        time.sleep(1)
        req = urllib.request.Request(f"{CDP}/json")
        resp = urllib.request.urlopen(req, timeout=5)
        tabs = json.loads(resp.read())
        
        x_tab = None
        for t in tabs:
            if t.get("id") == target_id or t.get("type") == "page":
                x_tab = t
                break
        
        if not x_tab:
            print(f"  ❌ Could not find new tab. Tabs: {[(t.get('id'), t.get('url','')[:40]) for t in tabs]}")
            ws.close()
            return False
        
        print(f"  Found tab: {x_tab.get('url','')[:60]}")
        
        # Connect to the page
        page_ws_url = x_tab["webSocketDebuggerUrl"]
        ws.close()
        ws = websocket.create_connection(page_ws_url, timeout=15)
        print(f"✅ Connected to page: {page_ws_url[:60]}")
        
        cdp_cmd(ws, "Runtime.enable", {}, 20)
        cdp_cmd(ws, "Page.enable", {}, 21)
        
        # Navigate to X
        print("\n📍 Navigating to X...")
        cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, 22)
        time.sleep(5)
        
        # Check status
        print("🔍 Checking login status...")
        state = eval_js(ws, """(() => {
            return {
                url: window.location.href,
                title: document.title,
                isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                buttonCount: document.querySelectorAll('button').length,
            };
        })()""", 23)
        print(f"  State: {json.dumps(state)}")
        
        if not state or not state.get("isLoggedIn"):
            print("\n  ⚠️  Not logged in")
            img = take_screenshot(ws, 99)
            if img:
                p = os.path.join(SCREENSHOT_DIR, "x_login_check.png")
                with open(p, "wb") as f:
                    f.write(img)
                print(f"  📸 Screenshot: {p}")
            
            # Try to find sign-in button
            signin = eval_js(ws, """(() => {
                const btns = document.querySelectorAll('button');
                const results = [];
                for (const b of btns) {
                    const text = (b.textContent || '').trim();
                    if (text.includes('Sign in') || text.includes('登录') || text.includes('Google')) {
                        results.push({ text, ariaLabel: b.getAttribute('aria-label') });
                    }
                }
                return results;
            })()""", 24)
            print(f"  Sign-in buttons: {json.dumps(signin)}")
        
        ws.close()
        print("\nDone checking login status")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try: ws.close()
        except: pass

if __name__ == "__main__":
    main()
