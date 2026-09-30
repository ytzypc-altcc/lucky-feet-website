#!/usr/bin/env python3
"""Post to X using CDP with chrome-openclaw-debug profile."""
import json, time, urllib.request, os, base64, websocket
from datetime import datetime

CDP = "http://localhost:9222"
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def cdp_req(method, params=None, id=1):
    data = json.dumps({"id": id, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(f"{CDP}/json/new", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  cdp_req error: {e}")
        return None

def get_ws_for_x():
    req = urllib.request.Request(f"{CDP}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    for t in tabs:
        if t.get("type") == "page" and "x.com" in t.get("url", ""):
            return t["webSocketDebuggerUrl"], t["id"]
    return None, None

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
    return None

def take_screenshot(ws, msg_id=99):
    result = cdp_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None

def generate_daily_copy():
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    topics = [
        {"opening": "今天看英超太激动了🔴⚽ 曼城3:1大胜！不过看完球发现脖子都僵了😂", "transition": "来【豪门贵足养生馆】给脖子松松吧～专业推拿按摩，缓解久坐疲劳💆‍♂️", "tags": "#RichmondBC #温哥华生活"},
        {"opening": "今天Richmond终于出太阳了☀️ 难得的好天气适合出去走走～", "transition": "但是太阳晒久了肩膀也酸，不如来做个推拿放松一下！【豪门贵足养生馆】等你来💆‍♀️", "tags": "#RichmondBC #温哥华天气"},
        {"opening": "明天就是长周末了🎉 打算去哪玩？", "transition": "不管去哪玩，出发前先来【豪门贵足养生馆】按一按，身体轻松才能玩得开心呀！专业推拿💪", "tags": "#长周末 #Richmond按摩"},
        {"opening": "最近换季🍂 好多朋友说关节不舒服、容易疲劳...", "transition": "这是身体在提醒你该保养了！【豪门贵足养生馆】专业祛湿排毒、舒缓颈肩腰腿痛🌿", "tags": "#换季养生 #温哥华养生"},
        {"opening": "听说Richmond中国城这周末有活动🏮 好多人去逛！", "transition": "逛累了记得来【豪门贵足养生馆】歇歇脚，专业按摩帮你恢复体力🧘‍♂️", "tags": "#Richmond #华人社区"},
        {"opening": "这周连上五天班💼 终于熬到周五了！谁懂...", "transition": "周末别忘了犒劳自己！【豪门贵足养生馆】专业推拿按摩，缓解一周的疲劳✨", "tags": "#FridayFeeling #豪门贵足"},
        {"opening": "医生说我每天走太少，建议多运动🏃‍♂️ 可是久坐一天真的腰酸背痛啊...", "transition": "运动之余更要会放松！【豪门贵足养生馆】专业推拿，疏通经络，祛湿排毒🌿", "tags": "#健康养生 #温哥华"},
        {"opening": "刚吃完一顿麻辣火锅🌶️🔥 肚子饱了但腰更酸了...", "transition": "美食虽好，也别忘了身体！【豪门贵足养生馆】来按一按，解乏又舒服😋💆", "tags": "#温哥华美食 #按摩放松"},
    ]
    topic = topics[day_of_year % len(topics)]
    address = "📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1"
    phone = "📞 604-370-2248 / 778-881-0168"
    wechat = "💬 微信：ytzypc"
    return f"{topic['opening']}\n\n{topic['transition']}\n\n{address}\n{phone}\n{wechat}\n\n{topic['tags']}"

def main():
    today = datetime.now()
    print(f"=== 豪门贵足养生馆 X Post - {today.strftime('%Y-%m-%d')} ===")
    
    copy = generate_daily_copy()
    print(f"\n📝 Copy ({len(copy)} chars):\n{copy}")
    
    # Get all tabs first
    req = urllib.request.Request(f"{CDP}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    print(f"\n📋 Available tabs ({len(tabs)}):")
    for t in tabs:
        print(f"  [{t.get('id','')}] {t.get('url','')[:80]} ({t.get('type','')})")
    
    # Find X tab or create one
    ws_url, tab_id = get_ws_for_x()
    
    if not ws_url:
        print("\n📌 No X tab found, creating new tab...")
        result = cdp_req("create", {"url": "https://x.com"})
        if result:
            ws_url = result.get("webSocketDebuggerUrl")
            print(f"  Created: {result.get('id')} - {result.get('url','')[:60]}")
        else:
            print("  ❌ Failed to create tab")
            return False
    
    print(f"\n🔗 Connecting: {ws_url}")
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected")
    
    try:
        cdp_cmd(ws, "Runtime.enable", {}, 1)
        cdp_cmd(ws, "Page.enable", {}, 2)
        
        # Navigate to X home
        print("\n📍 Navigating to X home...")
        cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, 3)
        time.sleep(5)
        
        # Check login status
        print("🔍 Checking login status...")
        state = eval_js(ws, """(() => {
            return {
                url: window.location.href,
                title: document.title,
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                hasComposer: !!document.querySelector('[data-testid="composerTextArea"]'),
                isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
                buttonCount: document.querySelectorAll('button').length,
            };
        })()""", 4)
        print(f"  State: {json.dumps(state)}")
        
        if not state or not state.get("isLoggedIn"):
            print("\n  ⚠️  Not logged in!")
            img = take_screenshot(ws, 98)
            if img:
                p = os.path.join(SCREENSHOT_DIR, "x_login_state.png")
                with open(p, "wb") as f:
                    f.write(img)
                print(f"  📸 Screenshot: {p}")
            
            # Try clicking Google sign-in
            google_click = eval_js(ws, """(() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    const text = (b.textContent || '').toLowerCase();
                    if (text.includes('google')) {
                        b.click();
                        return { clicked: true, text: b.textContent.trim() };
                    }
                }
                return { clicked: false };
            })()""", 5)
            print(f"  Google click: {json.dumps(google_click)}")
            time.sleep(10)
            
            state2 = eval_js(ws, """(() => {
                return {
                    url: window.location.href,
                    isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
                    hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                    title: document.title.slice(0, 50),
                };
            })()""", 6)
            print(f"  After login attempt: {json.dumps(state2)}")
            
            if not state2.get("isLoggedIn"):
                print("\n  ❌ Login failed. Cannot post without authentication.")
                img = take_screenshot(ws, 97)
                if img:
                    p = os.path.join(SCREENSHOT_DIR, "x_not_logged_in.png")
                    with open(p, "wb") as f:
                        f.write(img)
                    print(f"  📸 Screenshot: {p}")
                ws.close()
                return False
        
        # Find compose area
        print("\n✏️  Finding compose area...")
        ta_info = eval_js(ws, """(() => {
            const selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[data-testid="composerTextArea"]',
                'textarea[aria-label="Post"]',
                'div[role="textbox"][contenteditable="true"]',
            ];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    return { found: true, selector: sel, type: el.isContentEditable ? 'contenteditable' : 'textarea', tag: el.tagName };
                }
            }
            return { found: false };
        })()""", 10)
        print(f"  Info: {json.dumps(ta_info)}")
        
        if not ta_info or not ta_info.get("found"):
            print("  ❌ Compose area not found!")
            img = take_screenshot(ws, 96)
            if img:
                p = os.path.join(SCREENSHOT_DIR, "x_no_compose.png")
                with open(p, "wb") as f:
                    f.write(img)
            ws.close()
            return False
        
        # Type the message
        print("\n📝 Typing message...")
        escaped = copy.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
        
        if ta_info.get("type") == "contenteditable":
            type_result = eval_js(ws, f"""(() => {{
                const el = document.querySelector('{ta_info['selector']}');
                if (el) {{
                    el.focus();
                    el.innerHTML = '{escaped}';
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return {{ success: true, length: el.innerText.length }};
                }}
                return {{ success: false }};
            }})()""", 11)
        else:
            type_result = eval_js(ws, f"""(() => {{
                const ta = document.querySelector('{ta_info['selector']}');
                if (ta) {{
                    ta.focus();
                    ta.value = '{escaped}';
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, length: ta.value.length }};
                }}
                return {{ success: false }};
            }})()""", 12)
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Click Post
        print("\n🚀 Clicking Post...")
        post_result = eval_js(ws, """(() => {
            const selectors = [
                '[data-testid="tweetButtonInline"]',
                'button[aria-label="Post"]',
                'button[data-testid="tweetButton"]',
            ];
            for (const sel of selectors) {
                const btn = document.querySelector(sel);
                if (btn) { btn.click(); return { posted: true, selector: sel }; }
            }
            const allBtns = Array.from(document.querySelectorAll('button'));
            for (const btn of allBtns) {
                const text = (btn.textContent || '').trim();
                if (text === 'Post' || text === '发推' || text === '发布') { btn.click(); return { posted: true, text }; }
            }
            return { posted: false };
        })()""", 13)
        print(f"  Post result: {json.dumps(post_result)}")
        time.sleep(5)
        
        # Verify
        print("\n✅ Verifying...")
        verify = eval_js(ws, """(() => {
            return {
                url: window.location.href,
                composeEmpty: !document.querySelector('[data-testid="tweetTextarea_0"]')?.value,
                timestamp: Date.now(),
            };
        })()""", 14)
        print(f"  Verify: {json.dumps(verify)}")
        
        # Screenshot
        img = take_screenshot(ws, 15)
        screenshot_path = ""
        if img:
            screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_result.png")
            with open(screenshot_path, "wb") as f:
                f.write(img)
            print(f"  📸 Screenshot: {screenshot_path}")
        
        ws.close()
        
        success = post_result.get("posted", False)
        print(f"\n{'='*50}")
        print(f"RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"Copy ({len(copy)} chars): {copy[:120]}...")
        print(f"Screenshot: {screenshot_path}")
        print(f"{'='*50}")
        return success
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try: ws.close()
        except: pass
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
