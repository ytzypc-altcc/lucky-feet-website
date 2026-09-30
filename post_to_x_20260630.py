#!/usr/bin/env python3
"""
豪门贵足养生馆 - X (Twitter) Daily Post Script
Date: 2026-06-30 (Tuesday)
Generates unique daily copy and posts to X via CDP
"""

import json
import time
import os
import base64
import urllib.request
from datetime import datetime

CDP_HOST = "localhost:9222"
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def get_ws_for_x():
    """Find the X home page tab via CDP."""
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    for tab in tabs:
        if tab.get("type") == "page" and "x.com" in tab.get("url", "") and "home" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    for tab in tabs:
        if tab.get("type") == "page" and "x.com" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    return None

def cdp_cmd(ws, method, params=None, msg_id=1):
    """Send CDP command and wait for response."""
    import websocket
    if params is None:
        params = {}
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == msg_id:
            return data

def take_screenshot(ws, msg_id=99):
    """Take screenshot, return PNG bytes."""
    import websocket
    result = cdp_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None

def eval_js(ws, expr, msg_id=1, return_by_value=True, await_promise=True):
    """Evaluate JS and return the value."""
    import websocket
    params = {"expression": expr, "returnByValue": return_by_value}
    if await_promise:
        params["awaitPromise"] = True
    result = cdp_cmd(ws, "Runtime.evaluate", params, msg_id)
    if "result" in result and "value" in result["result"]:
        return result["result"]["value"]
    return None

def generate_daily_copy():
    """Generate today's unique promotional copy.
    
    Today is Tuesday, June 30, 2026.
    Topic: Summer solstice / long daylight hours (Topic #2 - Weather/Seasonal)
    """
    today = datetime.now()
    copy = (
        "今天是夏至过后第一天☀️ 白天越来越长，太阳到晚上10点多还不落，"
        "出门溜达一圈回来肩膀酸得不行😅\n\n"
        "来【豪门贵足养生馆】按一按，瞬间回血！💪\n"
        "🧖‍♂️ 专业推拿按摩\n"
        "🌿 祛湿排毒\n"
        "💆 舒缓颈肩腰腿痛\n\n"
        "📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n"
        "📞 604-370-2248 / 778-881-0168\n"
        "💬 微信：ytzypc\n\n"
        "#RichmondBC #夏至 #按摩养生 #豪门贵足"
    )
    return copy

def main():
    copy = generate_daily_copy()
    
    print("=" * 60)
    print("豪门贵足养生馆 - X (Twitter) Daily Post")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    print(f"\n📝 Generated Copy ({len(copy)} chars):")
    print(copy)
    print()
    
    # Find X tab
    ws_url = get_ws_for_x()
    if not ws_url:
        print("❌ Could not find X tab! Make sure Chrome is running with --remote-debugging-port=9222 and X is open.")
        return False
    
    print(f"🔗 Connecting to: {ws_url}")
    import websocket
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected")
    
    try:
        # Enable domains
        cdp_cmd(ws, "Page.enable", {}, 1)
        cdp_cmd(ws, "Runtime.enable", {}, 2)
        
        # Navigate to home
        print("\n📍 Navigating to X home...")
        cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, 3)
        time.sleep(5)
        
        # Verify login state
        print("🔍 Checking login state...")
        page_state = eval_js(ws, """(() => {
            return {
                url: window.location.href,
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                hasComposer: !!document.querySelector('[data-testid="composerTextArea"]'),
                hasSidebar: !!document.querySelector('aside nav'),
                buttonCount: document.querySelectorAll('button').length,
            };
        })()""", 4)
        print(f"  State: {json.dumps(page_state)}")
        
        if not page_state or not (page_state.get("hasCompose") or page_state.get("hasComposer")):
            print("  ⚠️ Not logged in or compose area not found!")
            print("  Please log in to X first, then re-run this script.")
            ws.close()
            return False
        
        # Find compose textarea
        print("\n✏️ Finding compose textarea...")
        textarea_info = eval_js(ws, """(() => {
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]') 
                    || document.querySelector('[data-testid="composerTextArea"]')
                    || document.querySelector('textarea[aria-label="Post"]');
            if (ta) {
                return {
                    found: true,
                    tagName: ta.tagName,
                    ariaLabel: ta.getAttribute('aria-label'),
                    placeholder: ta.placeholder?.slice(0, 50),
                };
            }
            const ce = document.querySelector('div[contenteditable="true"]');
            if (ce) {
                return { found: true, type: 'contenteditable' };
            }
            return { found: false };
        })()""", 5)
        print(f"  Info: {json.dumps(textarea_info)}")
        
        if not textarea_info or not textarea_info.get("found"):
            print("  ❌ Compose textarea not found!")
            ws.close()
            return False
        
        # Type the text
        print("\n📝 Typing message...")
        escaped = copy.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
        
        if textarea_info.get("type") == "contenteditable":
            js_type = f"""(() => {{
                const ce = document.querySelector('div[contenteditable="true"]');
                if (ce) {{
                    ce.focus();
                    ce.innerText = '{escaped}';
                    ce.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return {{ success: true, method: 'contentEditable' }};
                }}
                return {{ success: false }};
            }})()"""
        else:
            js_type = f"""(() => {{
                const ta = document.querySelector('[data-testid="tweetTextarea_0"]') 
                    || document.querySelector('[data-testid="composerTextArea"]')
                    || document.querySelector('textarea');
                if (ta) {{
                    ta.focus();
                    ta.value = '{escaped}';
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, length: ta.value.length }};
                }}
                return {{ success: false }};
            }})()"""
        
        type_result = eval_js(ws, js_type, 7)
        print(f"  Result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Click Post button
        print("\n🚀 Clicking Post button...")
        js_post = """(() => {
            const selectors = [
                '[data-testid="tweetButtonInline"]',
                'button[aria-label="Post"]',
                'button[data-testid="tweetButton"]',
            ];
            for (const sel of selectors) {
                const btn = document.querySelector(sel);
                if (btn) {
                    btn.click();
                    return { posted: true, selector: sel };
                }
            }
            const allBtns = Array.from(document.querySelectorAll('button'));
            for (const btn of allBtns) {
                const text = (btn.textContent || '').trim();
                if (text === 'Post' || text === '发推' || text === '发布') {
                    btn.click();
                    return { posted: true, foundByText: text };
                }
            }
            return { posted: false };
        })()"""
        
        post_result = eval_js(ws, js_post, 9)
        print(f"  Post result: {json.dumps(post_result)}")
        time.sleep(5)
        
        # Take screenshot
        print("\n📸 Taking screenshot...")
        img = take_screenshot(ws, 11)
        if img:
            path = os.path.join(SCREENSHOT_DIR, "post_result_20260630.png")
            with open(path, "wb") as f:
                f.write(img)
            print(f"  Saved: {path}")
        
        ws.close()
        
        print("\n" + "=" * 60)
        print("✅ POSTING SEQUENCE COMPLETED!")
        print(f"   Copy length: {len(copy)} chars")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            ws.close()
        except:
            pass
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nFINAL RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
