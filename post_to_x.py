#!/usr/bin/env python3
"""Post to X (Twitter) using CDP connection to logged-in Chrome on localhost:9222."""

import json
import time
import websocket
import urllib.request
import os
import base64
from datetime import datetime

CDP_HOST = "localhost:9222"
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def cdp_request(method, params, ws_url, msg_id=1):
    """Send a CDP command and return response."""
    ws = websocket.create_connection(ws_url, timeout=15)
    cmd = {"id": msg_id, "method": method, "params": params}
    ws.send(json.dumps(cmd))
    
    # Collect response
    while True:
        msg = ws.recv()
        data = json.loads(msg)
        if "id" in data and data["id"] == msg_id:
            ws.close()
            return data
        elif "method" in data:
            # Event notification, skip
            continue

def get_x_tab_url():
    """Find the X/Twitter tab in Chrome."""
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    
    # Look for X home page
    for tab in tabs:
        if tab.get("type") == "page":
            url = tab.get("url", "")
            if "x.com" in url and "home" in url:
                return tab["webSocketDebuggerUrl"]
            if "twitter.com" in url and "home" in url:
                return tab["webSocketDebuggerUrl"]
    
    # Fallback: any x.com or twitter.com page
    for tab in tabs:
        if tab.get("type") == "page":
            url = tab.get("url", "")
            if "x.com" in url or "twitter.com" in url:
                return tab["webSocketDebuggerUrl"]
    
    return None

def generate_daily_copy():
    """Generate daily promotional copy."""
    today = datetime.now()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_idx = today.weekday()
    date_str = today.strftime("%Y-%m-%d")
    
    copies = [
        # Monday
        f"新的一周开始啦！💪\n\n忙碌的工作从周一开始，你的身体还好吗？颈肩酸痛、腰背僵硬？来【豪门贵足养生馆】给身体充个电吧！⚡\n\n🧖‍♂️ 专业推拿按摩\n🌿 祛湿排毒\n💆 舒缓颈肩腰腿痛\n\n📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#RichmondBC #豪门贵足 #温哥华养生 #MondayMotivation",
        
        # Tuesday
        f"周二养生小课堂来了！📚\n\n久坐办公室的你，是不是经常觉得脖子僵硬、肩膀酸痛？😩\n\n别硬扛了！【豪门贵足养生馆】专业推拿，精准定位痛点，层层放松肌肉，让你从头到脚都轻松！✨\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#Vancouver #按摩推荐 #Richmond养生 #TuesdayVibes",
        
        # Wednesday
        f"周三啦！一周过半，给自己一个奖励吧 🎁\n\n工作再忙也要照顾好自己的身体哦～【豪门贵足养生馆】等你来放松！\n\n✅ 专业手法，力度适中\n✅ 环境舒适，安静私密\n✅ 祛湿排毒，焕发活力\n\n📍 161-5951 Minoru Blvd, Richmond\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#WednesdayWellness #豪门贵足 #BC省按摩 #Richmond",
        
        # Thursday
        f"周四倒计时！马上周末啦 🎉\n\n但在那之前，先让【豪门贵足养生馆】帮你卸下这一周的疲惫吧～💆‍♂️\n\n🌟 专业推拿｜🌟 祛湿排毒｜🌟 舒缓疼痛\n\n周末元气满满地度过，从一次深度放松开始！\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#ThursdayThoughts #温哥华按摩 #养生保健 #豪门贵足养生馆",
        
        # Friday
        f"周五到啦！周末模式准备开启 🚀\n\n辛苦了一周，是时候好好犒劳自己了！【豪门贵足养生馆】专业推拿按摩，帮你缓解颈肩腰腿痛，祛湿排毒，焕然一新！🧖‍♀️\n\n📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n快来预约你的周末放松时光吧！🎊\n\n#FridayFeeling #RichmondBC #按摩放松 #温哥华生活",
        
        # Saturday
        f"周末愉快！🌈 来【豪门贵足养生馆】享受专属放松时刻～\n\n不用去远方，家门口就有最专业的推拿按摩！💆\n\n✨ 舒缓颈肩腰腿痛\n✨ 祛湿排毒养颜\n✨ 专业技师手法到位\n\n带上家人朋友一起来吧！👨‍👩‍👧‍👦\n\n📍 161-5951 Minoru Blvd, Richmond V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#SaturdayVibes #周末放松 #豪门贵足 #Richmond按摩",
        
        # Sunday
        f"周日自我关怀日 💕\n\n一周即将结束，给身体一个温柔的拥抱吧～\n\n【豪门贵足养生馆】专业推拿按摩，帮你：\n🔹 缓解一周积累的疲劳\n🔹 疏通经络，祛湿排毒\n🔹 舒缓颈肩腰腿不适\n\n为新的一周蓄满能量！⚡\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#SundaySelfCare #养生日常 #温哥华养生 #豪门贵足养生馆"
    ]
    
    return copies[day_idx]

def take_screenshot(ws_url, filename):
    """Take a screenshot using CDP."""
    ws = websocket.create_connection(ws_url, timeout=15)
    # Enable page domain
    ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
    # Wait for response
    ws.recv()
    # Capture screenshot
    ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
    result = json.loads(ws.recv())
    ws.close()
    
    if "result" in result and "data" in result["result"]:
        img_data = base64.b64decode(result["result"]["data"])
        path = os.path.join(SCREENSHOT_DIR, filename)
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"📸 Screenshot saved: {path}")
        return path
    return None

def post_via_cdp(ws_url, text):
    """Post text to X using CDP Runtime.evaluate."""
    print(f"  Attempting to post: {text[:50]}...")
    
    # Step 1: Navigate to X home
    print("  Step 1: Navigating to X home...")
    r = cdp_request("Page.navigate", {"url": "https://x.com/home"}, ws_url, msg_id=1)
    print(f"    Response: {json.dumps(r)[:100]}")
    time.sleep(3)
    
    # Step 2: Take screenshot to check state
    print("  Step 2: Taking screenshot to check state...")
    take_screenshot(ws_url, "step2_check.png")
    time.sleep(1)
    
    # Step 3: Find and interact with compose area
    print("  Step 3: Looking for compose element...")
    
    # Try to find the compose textarea
    result = cdp_request("Runtime.evaluate", {
        "expression": """(() => {
            const selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[data-testid="composerTextArea"]',
                'textarea[aria-label="Post"]',
                'div[contenteditable="true"][data-testid="tweetBoxTextArea"]',
            ];
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el) return { found: true, selector: s, tagName: el.tagName, ariaLabel: el.getAttribute("aria-label") };
            }
            return { found: false };
        })()"""
    }, ws_url, msg_id=3)
    print(f"    Compose check: {json.dumps(result)}")
    
    # Step 4: If textarea found, type into it
    textarea_result = result.get("result", {}).get("value", {})
    
    if textarea_result.get("found"):
        print("  Step 4: Found compose textarea, typing...")
        # Escape the text for JavaScript
        escaped_text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        
        type_result = cdp_request("Runtime.evaluate", {
            "expression": f"""(() => {{
                const ta = document.querySelector('[data-testid="tweetTextarea_0"]') || document.querySelector('[data-testid="composerTextArea"]');
                if (ta) {{
                    ta.focus();
                    ta.value = '{escaped_text}';
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, length: ta.value.length }};
                }}
                return {{ success: false }};
            }})()"""
        }, ws_url, msg_id=4)
        print(f"    Type result: {json.dumps(type_result)[:200]}")
        time.sleep(2)
    else:
        # Try clicking compose button first
        print("  Step 4: No textarea found, trying to click compose button...")
        click_result = cdp_request("Runtime.evaluate", {
            "expression": """(() => {
                const btn = document.querySelector('[data-testid="SideNav_Tweet_Button"]')
                    || document.querySelector('[data-testid="composeTweet"]')
                    || document.querySelector('button[aria-label="Post"]');
                if (btn) {
                    btn.click();
                    return { clicked: true };
                }
                return { clicked: false };
            })()"""
        }, ws_url, msg_id=5)
        print(f"    Click result: {json.dumps(click_result)}")
        time.sleep(3)
        
        # Take screenshot after clicking
        take_screenshot(ws_url, "step4_after_click.png")
        time.sleep(1)
        
        # Try again to find textarea
        result2 = cdp_request("Runtime.evaluate", {
            "expression": """(() => {
                const ta = document.querySelector('[data-testid="tweetTextarea_0"]') || document.querySelector('[data-testid="composerTextArea"]');
                if (ta) return { found: true };
                return { found: false };
            })()"""
        }, ws_url, msg_id=6)
        print(f"    Retried textarea check: {json.dumps(result2)}")
        
        if result2.get("result", {}).get("value", {}).get("found"):
            escaped_text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            type_result = cdp_request("Runtime.evaluate", {
                "expression": f"""(() => {{
                    const ta = document.querySelector('[data-testid="tweetTextarea_0"]') || document.querySelector('[data-testid="composerTextArea"]');
                    if (ta) {{
                        ta.focus();
                        ta.value = '{escaped_text}';
                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        return {{ success: true }};
                    }}
                    return {{ success: false }};
                }})()"""
            }, ws_url, msg_id=7)
            print(f"    Type result (retry): {json.dumps(type_result)[:200]}")
            time.sleep(2)
    
    # Step 5: Click Post button
    print("  Step 5: Clicking Post button...")
    post_result = cdp_request("Runtime.evaluate", {
        "expression": """(() => {
            const btn = document.querySelector('[data-testid="tweetButtonInline"]')
                || document.querySelector('button[data-testid="tweetButtonInline"]');
            if (btn) {
                btn.click();
                return { posted: true };
            }
            return { posted: false };
        })()"""
    }, ws_url, msg_id=8)
    print(f"    Post result: {json.dumps(post_result)}")
    time.sleep(5)
    
    # Step 6: Final screenshot
    print("  Step 6: Taking final screenshot...")
    take_screenshot(ws_url, "final_screenshot.png")
    time.sleep(1)
    
    return True

def main():
    print("=" * 60)
    print("豪门贵足养生馆 - X (Twitter) Daily Post")
    today = datetime.now()
    print(f"Date: {today.strftime('%Y-%m-%d')} ({today.strftime('%A')})")
    print("=" * 60)
    
    # Generate copy
    copy = generate_daily_copy()
    print(f"\n📝 Generated copy ({len(copy)} chars):\n{copy}")
    print(f"\n📏 Character count: {len(copy)}")
    
    if len(copy) > 280:
        print(f"⚠️  WARNING: Text exceeds 280 chars! Truncating...")
        copy = copy[:277] + "..."
        print(f"📝 Truncated copy:\n{copy}")
    
    # Find X tab
    ws_url = get_x_tab_url()
    if not ws_url:
        print("\n❌ Could not find X/Twitter tab in Chrome on localhost:9222")
        print("Available tabs:")
        req = urllib.request.Request(f"http://{CDP_HOST}/json")
        resp = urllib.request.urlopen(req, timeout=10)
        tabs = json.loads(resp.read().decode())
        for tab in tabs:
            if tab.get("type") == "page":
                print(f"  - {tab.get('title', 'N/A')}: {tab.get('url', 'N/A')}")
        return False
    
    print(f"\n🔗 Using tab: {ws_url}")
    
    try:
        print("\n🚀 Starting post sequence...")
        success = post_via_cdp(ws_url, copy)
        
        if success:
            print("\n✅ Post sequence completed!")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error during posting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'=' * 60}")
    print(f"FINAL RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"{'=' * 60}")
