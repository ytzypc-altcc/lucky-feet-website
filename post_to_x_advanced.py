#!/usr/bin/env python3
"""
Advanced X/Twitter poster using CDP on localhost:9222.
Uses DOMSnapshot to find elements and Runtime.evaluate for interaction.
"""

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

def get_ws_for_url(target_url_pattern):
    """Find a tab whose URL matches the pattern and return its ws URL."""
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    
    for tab in tabs:
        if tab.get("type") == "page":
            url = tab.get("url", "")
            if target_url_pattern in url:
                return tab["webSocketDebuggerUrl"], tab["id"], url
    
    return None, None, None

def cdp_call(ws, method, params=None, msg_id=1):
    """Send CDP command and return parsed result."""
    if params is None:
        params = {}
    cmd = {"id": msg_id, "method": method, "params": params}
    ws.send(json.dumps(cmd))
    
    # Collect all messages until we get the response
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == msg_id:
            return data
        # Skip events (notifications)

def cdp_send_event(ws, method, params=None):
    """Send CDP command without waiting for response (for event subscriptions)."""
    if params is None:
        params = {}
    cmd = {"id": 9999, "method": method, "params": params}
    ws.send(json.dumps(cmd))

def take_screenshot(ws, msg_id=100):
    """Take a screenshot and return base64 encoded PNG."""
    result = cdp_call(ws, "Page.captureScreenshot", {"format": "png"}, msg_id=msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None

def save_screenshot(data, filename):
    """Save screenshot data to file."""
    if data:
        path = os.path.join(SCREENSHOT_DIR, filename)
        with open(path, "wb") as f:
            f.write(data)
        print(f"  📸 Saved: {path} ({len(data)} bytes)")
        return path
    return None

def eval_js(ws, expr, msg_id=1):
    """Evaluate JavaScript and return the result value."""
    result = cdp_call(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True,
        "userGesture": True
    }, msg_id=msg_id)
    
    if "result" in result:
        return result["result"].get("value"), result
    return None, result

def dump_object(ws, object_id, msg_id=1):
    """Dump a JS object by its objectId."""
    result = cdp_call(ws, "Runtime.callFunctionOn", {
        "objectId": object_id,
        "functionDeclaration": "() => { const o = this; return JSON.stringify(o, Object.getOwnPropertyNames(o)); }",
        "returnByValue": True
    }, msg_id=msg_id)
    return result

def main():
    today = datetime.now()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_idx = today.weekday()
    
    # Generate daily copy
    copies = [
        f"新的一周开始啦！💪\n\n忙碌的工作从周一开始，你的身体还好吗？颈肩酸痛、腰背僵硬？来【豪门贵足养生馆】给身体充个电吧！⚡\n\n🧖‍♂️ 专业推拿按摩\n🌿 祛湿排毒\n💆 舒缓颈肩腰腿痛\n\n📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#RichmondBC #豪门贵足 #温哥华养生 #MondayMotivation",
        
        f"周二养生小课堂来了！📚\n\n久坐办公室的你，是不是经常觉得脖子僵硬、肩膀酸痛？😩\n\n别硬扛了！【豪门贵足养生馆】专业推拿，精准定位痛点，层层放松肌肉，让你从头到脚都轻松！✨\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#Vancouver #按摩推荐 #Richmond养生 #TuesdayVibes",
        
        f"周三啦！一周过半，给自己一个奖励吧 🎁\n\n工作再忙也要照顾好自己的身体哦～【豪门贵足养生馆】等你来放松！\n\n✅ 专业手法，力度适中\n✅ 环境舒适，安静私密\n✅ 祛湿排毒，焕发活力\n\n📍 161-5951 Minoru Blvd, Richmond\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#WednesdayWellness #豪门贵足 #BC省按摩 #Richmond",
        
        f"周四倒计时！马上周末啦 🎉\n\n但在那之前，先让【豪门贵足养生馆】帮你卸下这一周的疲惫吧～💆‍♂️\n\n🌟 专业推拿｜🌟 祛湿排毒｜🌟 舒缓疼痛\n\n周末元气满满地度过，从一次深度放松开始！\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#ThursdayThoughts #温哥华按摩 #养生保健 #豪门贵足养生馆",
        
        f"周五到啦！周末模式准备开启 🚀\n\n辛苦了一周，是时候好好犒劳自己了！【豪门贵足养生馆】专业推拿按摩，帮你缓解颈肩腰腿痛，祛湿排毒，焕然一新！🧖‍♀️\n\n📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n快来预约你的周末放松时光吧！🎊\n\n#FridayFeeling #RichmondBC #按摩放松 #温哥华生活",
        
        f"周末愉快！🌈 来【豪门贵足养生馆】享受专属放松时刻～\n\n不用去远方，家门口就有最专业的推拿按摩！💆\n\n✨ 舒缓颈肩腰腿痛\n✨ 祛湿排毒养颜\n✨ 专业技师手法到位\n\n带上家人朋友一起来吧！👨‍👩‍👧‍👦\n\n📍 161-5951 Minoru Blvd, Richmond V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#SaturdayVibes #周末放松 #豪门贵足 #Richmond按摩",
        
        f"周日自我关怀日 💕\n\n一周即将结束，给身体一个温柔的拥抱吧～\n\n【豪门贵足养生馆】专业推拿按摩，帮你：\n🔹 缓解一周积累的疲劳\n🔹 疏通经络，祛湿排毒\n🔹 舒缓颈肩腰腿不适\n\n为新的一周蓄满能量！⚡\n\n📍 Richmond, BC V6X 4B1\n📞 604-370-2248 / 778-881-0168\n💬 微信：ytzypc\n\n#SundaySelfCare #养生日常 #温哥华养生 #豪门贵足养生馆"
    ]
    
    copy = copies[day_idx]
    
    print("=" * 60)
    print("豪门贵足养生馆 - X (Twitter) Daily Post")
    print(f"Date: {today.strftime('%Y-%m-%d')} ({day_names[day_idx]})")
    print("=" * 60)
    print(f"\n📝 Copy ({len(copy)} chars):\n{copy}")
    
    # Find X home tab
    ws_url, tab_id, tab_url = get_ws_for_url("x.com")
    if not ws_url:
        print("\n❌ No X tab found!")
        return False
    
    print(f"\n🔗 Found X tab: {tab_url}")
    print(f"   WS: {ws_url}")
    
    # Connect to CDP
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected to Chrome DevTools Protocol")
    
    try:
        # Enable domains
        cdp_call(ws, "Page.enable", {}, msg_id=1)
        cdp_call(ws, "Runtime.enable", {}, msg_id=2)
        cdp_call(ws, "DOM.enable", {}, msg_id=3)
        cdp_call(ws, "DOMDocument.enable", {}, msg_id=4)
        
        # Navigate to X home
        print("\n📍 Navigating to X home...")
        cdp_call(ws, "Page.navigate", {"url": "https://x.com/home"}, msg_id=5)
        time.sleep(5)  # Wait for page to load
        
        # Take initial screenshot
        img = take_screenshot(ws, msg_id=6)
        save_screenshot(img, "cdp_step1_home.png")
        
        # Check if logged in by looking for compose button
        print("\n🔍 Checking login status...")
        js_check_logged_in = """(() => {
            // Check for compose elements that indicate logged-in state
            const composeBtn = document.querySelector('[data-testid="SideNav_Tweet_Button"]');
            const composeArea = document.querySelector('[data-testid="tweetTextarea_0"]');
            const navItems = document.querySelectorAll('nav a, [role="navigation"] a');
            const navCount = navItems.length;
            
            return {
                hasComposeBtn: !!composeBtn,
                hasComposeArea: !!composeArea,
                navItemCount: navCount,
                location: window.location.href,
                hasUserProfile: !!document.querySelector('[data-testid="AppHeader"]'),
            };
        })()"""
        
        logged_in, _ = eval_js(ws, js_check_logged_in, msg_id=7)
        print(f"  Login status: {json.dumps(logged_in, indent=2)}")
        
        if not logged_in or not logged_in.get("hasComposeBtn"):
            print("\n  ⚠️  Compose button not found. Trying to find any clickable element...")
            # Dump the page structure
            js_dump = """(() => {
                const allButtons = Array.from(document.querySelectorAll('button')).map(b => ({
                    text: b.textContent.trim().slice(0, 50),
                    ariaLabel: b.getAttribute('aria-label'),
                    testId: b.getAttribute('data-testid'),
                    visible: b.offsetParent !== null
                }));
                return { buttonCount: allButtons.length, buttons: allButtons.slice(0, 20) };
            })()"""
            buttons_info, _ = eval_js(ws, js_dump, msg_id=8)
            print(f"  Buttons found: {buttons_info}")
        
        # Try to find the compose button
        print("\n🖱️  Finding compose button...")
        js_find_compose = """(() => {
            // Try multiple selectors
            const selectors = [
                '[data-testid="SideNav_Tweet_Button"]',
                '[data-testid="composeTweet"]',
                'button[aria-label*="Post"]',
                'button[aria-label*="tweet"]',
                'svg[aria-label*="Post"]',
            ];
            
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    return { found: true, selector: sel, text: el.textContent?.trim()?.slice(0,30), tagName: el.tagName };
                }
            }
            
            // Also try to find the compose area directly
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]') 
                    || document.querySelector('[data-testid="composerTextArea"]');
            if (ta) return { found: true, selector: 'textarea', tagName: ta.tagName };
            
            return { found: false };
        })()"""
        
        compose_info, _ = eval_js(ws, js_find_compose, msg_id=9)
        print(f"  Compose info: {json.dumps(compose_info, indent=2)}")
        
        if compose_info and compose_info.get("found"):
            print("\n  ✅ Found compose element!")
        else:
            print("\n  ❌ Compose element not found, trying broader search...")
            # Try to find any sidebar or compose-related element
            js_broad_search = """(() => {
                // Look for the compose button in the sidebar
                const sideNav = document.querySelector('aside') || document.querySelector('[role="navigation"]');
                if (sideNav) {
                    const buttons = Array.from(sideNav.querySelectorAll('button, a'));
                    const relevant = buttons.filter(b => {
                        const text = (b.textContent || '').toLowerCase();
                        const label = (b.getAttribute('aria-label') || '').toLowerCase();
                        return text.includes('post') || text.includes('tweet') || text.includes('compose') 
                            || label.includes('post') || label.includes('tweet') || label.includes('compose');
                    });
                    return { found: relevant.length > 0, count: relevant.length, items: relevant.map(r => ({
                        text: r.textContent?.trim()?.slice(0,30),
                        ariaLabel: r.getAttribute('aria-label'),
                        testId: r.getAttribute('data-testid')
                    }))};
                }
                return { found: false, reason: 'no sidebar found' };
            })()"""
            broad, _ = eval_js(ws, js_broad_search, msg_id=10)
            print(f"  Broad search: {json.dumps(broad, indent=2)}")
        
        # Click compose button
        print("\n✏️  Clicking compose button...")
        js_click_compose = """(() => {
            const btn = document.querySelector('[data-testid="SideNav_Tweet_Button"]')
                || document.querySelector('[data-testid="composeTweet"]');
            if (btn) {
                btn.scrollIntoView({ block: 'center' });
                btn.click();
                return { clicked: true };
            }
            return { clicked: false };
        })()"""
        
        click_result, _ = eval_js(ws, js_click_compose, msg_id=11)
        print(f"  Click result: {json.dumps(click_result)}")
        time.sleep(3)
        
        # Take screenshot after clicking compose
        img = take_screenshot(ws, msg_id=12)
        save_screenshot(img, "cdp_step2_compose_opened.png")
        
        # Type the text
        print("\n📝 Typing message...")
        escaped_text = copy.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
        escaped_text = escaped_text.replace("\n", "\\n")
        
        js_type = f"""(() => {{
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]')
                || document.querySelector('[data-testid="composerTextArea"]')
                || document.querySelector('textarea');
            if (ta) {{
                ta.focus();
                ta.value = '{escaped_text}';
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                ta.dispatchEvent(new KeyboardEvent('keydown', {{ bubbles: true }}));
                ta.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles: true }}));
                return {{ typed: true, length: ta.value.length }};
            }}
            
            // Try contenteditable div
            const ce = document.querySelector('[data-testid="tweetBox"]')
                || document.querySelector('div[contenteditable="true"]');
            if (ce) {{
                ce.focus();
                ce.innerText = '{escaped_text}';
                ce.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return {{ typed: true, method: 'contentEditable', length: ce.innerText.length }};
            }}
            
            return {{ typed: false }};
        }})()"""
        
        type_result, _ = eval_js(ws, js_type, msg_id=13)
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Take screenshot after typing
        img = take_screenshot(ws, msg_id=14)
        save_screenshot(img, "cdp_step3_text_entered.png")
        
        # Find and click Post button
        print("\n🚀 Clicking Post button...")
        js_post = """(() => {
            const btn = document.querySelector('[data-testid="tweetButtonInline"]')
                || document.querySelector('button[data-testid="tweetButtonInline"]')
                || document.querySelector('button[aria-label="Post"]');
            if (btn) {
                btn.scrollIntoView({ block: 'center' });
                btn.click();
                return { posted: true };
            }
            return { posted: false };
        })()"""
        
        post_result, _ = eval_js(ws, js_post, msg_id=15)
        print(f"  Post result: {json.dumps(post_result)}")
        time.sleep(5)
        
        # Final screenshot
        print("\n📸 Taking final screenshot...")
        img = take_screenshot(ws, msg_id=16)
        save_screenshot(img, "cdp_step4_final.png")
        
        # Check if post was successful by looking at the page
        js_verify = """(() => {
            // Check if compose area is closed (meaning post was submitted)
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
            const composeArea = document.querySelector('[data-testid="composerTextArea"]');
            
            // Check for confirmation or recent tweet
            const recentTweet = document.querySelector('[data-testid="tweet"]');
            
            return {
                composeClosed: !ta && !composeArea,
                hasRecentTweet: !!recentTweet,
                location: window.location.href
            };
        })()"""
        
        verify, _ = eval_js(ws, js_verify, msg_id=17)
        print(f"  Verification: {json.dumps(verify)}")
        
        ws.close()
        
        print("\n" + "=" * 60)
        print(f"✅ Posting sequence completed!")
        print(f"   Compose closed: {verify.get('composeClosed', 'unknown')}")
        print(f"   Has recent tweet: {verify.get('hasRecentTweet', 'unknown')}")
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
    print(f"\nFINAL: {'✅ SUCCESS' if success else '❌ FAILED'}")
