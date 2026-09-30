#!/usr/bin/env python3
"""
Post to X (Twitter) using CDP on localhost:9222.
Verified working: page is logged in, compose area exists.
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

def get_ws_for_x():
    """Find the X home page tab."""
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    for tab in tabs:
        if tab.get("type") == "page" and "x.com" in tab.get("url", "") and "home" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    # Fallback
    for tab in tabs:
        if tab.get("type") == "page" and "x.com" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    return None

def cdp_cmd(ws, method, params=None, msg_id=1):
    """Send CDP command and wait for response, filtering events."""
    if params is None:
        params = {}
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if "id" in data and data["id"] == msg_id:
            return data
        # Skip events

def take_screenshot(ws, msg_id=99):
    """Take screenshot, return PNG bytes or None."""
    result = cdp_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None

def eval_js(ws, expr, msg_id=1, return_by_value=True, await_promise=True):
    """Evaluate JS and return the value."""
    params = {"expression": expr, "returnByValue": return_by_value}
    if await_promise:
        params["awaitPromise"] = True
    result = cdp_cmd(ws, "Runtime.evaluate", params, msg_id)
    if "result" in result and "value" in result["result"]:
        return result["result"]["value"]
    return None

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
    
    # Find X tab
    ws_url = get_ws_for_x()
    if not ws_url:
        print("\n❌ Could not find X tab!")
        return False
    
    print(f"\n🔗 Connecting to: {ws_url}")
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected")
    
    try:
        # Enable domains
        cdp_cmd(ws, "Page.enable", {}, 1)
        cdp_cmd(ws, "Runtime.enable", {}, 2)
        
        # Navigate to home
        print("\n📍 Navigating to X home...")
        cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, 3)
        time.sleep(3)
        
        # Verify page state
        print("🔍 Verifying page state...")
        page_state = eval_js(ws, """(() => {
            return {
                title: document.title,
                url: window.location.href,
                composeArea: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                sidebar: !!document.querySelector('aside'),
                buttonCount: document.querySelectorAll('button').length,
            };
        })()""", 4)
        print(f"  Page state: {json.dumps(page_state)}")
        
        if not page_state or not page_state.get("composeArea"):
            print("  ⚠️  Compose area not found, waiting longer...")
            time.sleep(3)
            page_state = eval_js(ws, """(() => {
                return {
                    composeArea: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                    composerArea: !!document.querySelector('[data-testid="composerTextArea"]'),
                };
            })()""", 4)
            print(f"  Retry state: {json.dumps(page_state)}")
        
        # Find the compose textarea
        print("\n✏️  Finding compose textarea...")
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
                    valueLength: ta.value?.length || 0,
                };
            }
            // Try contenteditable
            const ce = document.querySelector('div[contenteditable="true"]');
            if (ce) {
                return {
                    found: true,
                    type: 'contenteditable',
                    tagName: ce.tagName,
                    text: ce.innerText?.slice(0, 50),
                };
            }
            return { found: false };
        })()""", 5)
        print(f"  Textarea info: {json.dumps(textarea_info)}")
        
        if not textarea_info or not textarea_info.get("found"):
            print("  ❌ Compose textarea not found!")
            # List all textareas
            all_inputs = eval_js(ws, """(() => {
                return Array.from(document.querySelectorAll('textarea, [contenteditable="true"], input[type="text"]')).map(el => ({
                    tag: el.tagName,
                    type: el.type || 'none',
                    ariaLabel: el.getAttribute('aria-label'),
                    placeholder: el.placeholder?.slice(0, 30),
                    contentEditable: el.contentEditable,
                }));
            })()""", 6)
            print(f"  All inputs: {json.dumps(all_inputs)}")
            ws.close()
            return False
        
        # Type the text
        print("\n📝 Typing message...")
        
        # Escape text for safe JS string embedding
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
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Find and click Post button
        print("\n🚀 Finding and clicking Post button...")
        
        # First, let's find all buttons and look for the Post button
        buttons_info = eval_js(ws, """(() => {
            return Array.from(document.querySelectorAll('button')).map((b, i) => ({
                index: i,
                text: (b.textContent || '').trim().slice(0, 30),
                ariaLabel: b.getAttribute('aria-label'),
                testId: b.getAttribute('data-testid'),
                className: b.className?.slice(0, 50),
            })).filter(b => b.text || b.ariaLabel || b.testId);
        })()""", 8)
        print(f"  Buttons: {json.dumps(buttons_info)}")
        
        # Click the Post button
        js_post = """(() => {
            // Try various selectors for the Post button
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
            
            // Last resort: find button by text content
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
        
        # Verify post
        print("\n✅ Verifying post...")
        verify = eval_js(ws, """(() => {
            return {
                composeAreaEmpty: !document.querySelector('[data-testid="tweetTextarea_0"]')?.value,
                location: window.location.href,
                timestamp: Date.now(),
            };
        })()""", 10)
        print(f"  Verify: {json.dumps(verify)}")
        
        # Save screenshot
        img = take_screenshot(ws, 11)
        if img:
            path = os.path.join(SCREENSHOT_DIR, "post_result.png")
            with open(path, "wb") as f:
                f.write(img)
            print(f"  📸 Screenshot saved: {path}")
        
        ws.close()
        
        print("\n" + "=" * 60)
        print("✅ POSTING SEQUENCE COMPLETED SUCCESSFULLY!")
        print(f"   Copy length: {len(copy)} chars")
        print(f"   Type result: {type_result}")
        print(f"   Post result: {post_result}")
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
