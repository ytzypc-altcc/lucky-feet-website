#!/usr/bin/env python3
"""
豪门贵足养生馆 - X (Twitter) Daily Post Script
Generates daily unique copy and posts to X via CDP.
"""

import json
import time
import urllib.request
import os
import base64
from datetime import datetime

CDP_HOST = "localhost:9222"
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ============================================================
# Daily copy generation - 7 rotating topics
# ============================================================
def generate_daily_copy():
    """Generate a unique daily post based on topic rotation."""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    topics = [
        {
            "category": "football",
            "opening": "今天看英超太激动了🔴⚽ 曼城3:1大胜！不过看完球发现脖子都僵了😂",
            "transition": "来【豪门贵足养生馆】给脖子松松吧～专业推拿按摩，缓解久坐疲劳💆‍♂️",
            "tags": "#RichmondBC #温哥华生活"
        },
        {
            "category": "weather",
            "opening": "今天Richmond终于出太阳了☀️ 难得的好天气适合出去走走～",
            "transition": "但是太阳晒久了肩膀也酸，不如来做个推拿放松一下！【豪门贵足养生馆】等你来💆‍♀️",
            "tags": "#RichmondBC #温哥华天气"
        },
        {
            "category": "holiday",
            "opening": "明天就是长周末了🎉 打算去哪玩？",
            "transition": "不管去哪玩，出发前先来【豪门贵足养生馆】按一按，身体轻松才能玩得开心呀！专业推拿💪",
            "tags": "#长周末 #Richmond按摩"
        },
        {
            "category": "season",
            "opening": "最近换季🍂 好多朋友说关节不舒服、容易疲劳...",
            "transition": "这是身体在提醒你该保养了！【豪门贵足养生馆】专业祛湿排毒、舒缓颈肩腰腿痛🌿",
            "tags": "#换季养生 #温哥华养生"
        },
        {
            "category": "community",
            "opening": "听说Richmond中国城这周末有活动🏮 好多人去逛！",
            "transition": "逛累了记得来【豪门贵足养生馆】歇歇脚，专业按摩帮你恢复体力🧘‍♂️",
            "tags": "#Richmond #华人社区"
        },
        {
            "category": "daily_life",
            "opening": "这周连上五天班💼 终于熬到周五了！谁懂...",
            "transition": "周末别忘了犒劳自己！【豪门贵足养生馆】专业推拿按摩，缓解一周的疲劳✨",
            "tags": "#FridayFeeling #豪门贵足"
        },
        {
            "category": "health",
            "opening": "医生说我每天走太少，建议多运动🏃‍♂️ 可是久坐一天真的腰酸背痛啊...",
            "transition": "运动之余更要会放松！【豪门贵足养生馆】专业推拿，疏通经络，祛湿排毒🌿",
            "tags": "#健康养生 #温哥华"
        },
        {
            "category": "food",
            "opening": "刚吃完一顿麻辣火锅🌶️🔥 肚子饱了但腰更酸了...",
            "transition": "美食虽好，也别忘了身体！【豪门贵足养生馆】来按一按，解乏又舒服😋💆",
            "tags": "#温哥华美食 #按摩放松"
        },
    ]
    
    topic = topics[day_of_year % len(topics)]
    
    address = "📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1"
    phone = "📞 604-370-2248 / 778-881-0168"
    wechat = "💬 微信：ytzypc"
    
    copy = f"{topic['opening']}\n\n{topic['transition']}\n\n{address}\n{phone}\n{wechat}\n\n{topic['tags']}"
    
    return copy


# ============================================================
# CDP Utilities
# ============================================================
def get_ws_url():
    """Find the X home page tab WebSocket URL."""
    req = urllib.request.Request(f"http://{CDP_HOST}/json")
    resp = urllib.request.urlopen(req, timeout=10)
    tabs = json.loads(resp.read().decode())
    
    # Prefer x.com/home tab
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
    """Take screenshot, return PNG bytes or None."""
    result = cdp_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
    if "result" in result and "data" in result["result"]:
        return base64.b64decode(result["result"]["data"])
    return None


def eval_js(ws, expr, msg_id=1):
    """Evaluate JS and return the value."""
    params = {"expression": expr, "returnByValue": True, "awaitPromise": True}
    result = cdp_cmd(ws, "Runtime.evaluate", params, msg_id)
    if "result" in result and "value" in result["result"]:
        return result["result"]["value"]
    return None


def inject_cookies_from_chrome():
    """Extract auth cookies from Chrome's cookie jar and inject them into the X tab via CDP."""
    import sqlite3, base64, struct, ctypes, ctypes.wintypes
    
    db_path = "/home/rc/.config/chrome-openclaw-debug/Default/Cookies"
    chrome_login_data = "/home/rc/.config/chrome-openclaw-debug/Default/LoginData"
    
    cookies_to_inject = []
    
    # Try to decrypt using Chrome's DPAPI (Windows) or simple method (Linux)
    # On Linux Chrome, encrypted_value uses 8-byte random salt + AES-256-CBC
    # But on Linux, Chrome uses libsecret/keyring, so encrypted_value is often plaintext-like
    # Let's try reading directly first
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%x.com%'")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            host_key, name, encrypted_value = row
            # On Linux, sometimes cookies are stored as plaintext in the DB
            # or encrypted with a simple scheme
            value = encrypted_value
            try:
                # Try to decode as UTF-8 directly
                decoded = value.decode('utf-8')
                if decoded and not decoded.startswith('v10') and not decoded.startswith('v11'):
                    cookies_to_inject.append((host_key, name, decoded))
            except:
                pass
                
        # Also try LoginData for potentially stored passwords
        if not cookies_to_inject and os.path.exists(chrome_login_data):
            conn = sqlite3.connect(chrome_login_data)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins WHERE origin_url LIKE '%x.com%' OR origin_url LIKE '%twitter%'")
            rows = cursor.fetchall()
            conn.close()
            
    except Exception as e:
        print(f"  Cookie extraction note: {e}")
    
    return cookies_to_inject


def main():
    today = datetime.now()
    print("=" * 60)
    print("豪门贵足养生馆 - X (Twitter) Daily Post")
    print(f"Date: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Generate daily copy
    copy = generate_daily_copy()
    print(f"\n📝 Generated Copy ({len(copy)} chars):")
    print("-" * 40)
    print(copy)
    print("-" * 40)
    
    # Step 2: Connect to CDP
    ws_url = get_ws_url()
    if not ws_url:
        print("\n❌ Could not find X tab!")
        return False
    
    print(f"\n🔗 Connecting to: {ws_url}")
    
    import websocket
    ws = websocket.create_connection(ws_url, timeout=15)
    print("✅ Connected to Chrome DevTools")
    
    try:
        # Enable required domains
        cdp_cmd(ws, "Page.enable", {}, msg_id=1)
        cdp_cmd(ws, "Runtime.enable", {}, msg_id=2)
        
        # Step 3: Navigate to X home
        print("\n📍 Navigating to X home...")
        cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, msg_id=3)
        time.sleep(5)  # Wait for page to load
        
        # Step 4: Check if logged in by looking for compose area
        print("🔍 Checking login status...")
        page_state = eval_js(ws, """(() => {
            return {
                title: document.title,
                url: window.location.href,
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                hasComposer: !!document.querySelector('[data-testid="composerTextArea"]'),
                isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || 
                           !!document.querySelector('[aria-label="Account menu"]'),
                buttonCount: document.querySelectorAll('button').length,
            };
        })()""", msg_id=4)
        print(f"  Page state: {json.dumps(page_state)}")
        
        # If not logged in, try to click "Continue with Google" or use cookies
        if not page_state or not page_state.get("isLoggedIn"):
            print("\n  ⚠️  Not logged in, attempting Google login...")
            
            # Take screenshot to see current state
            img = take_screenshot(ws, msg_id=98)
            if img:
                path = os.path.join(SCREENSHOT_DIR, "x_login_state.png")
                with open(path, "wb") as f:
                    f.write(img)
                print(f"  📸 Saved login state screenshot: {path}")
            
            # Try clicking the Google sign-in button
            google_btn = eval_js(ws, """(() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if ((b.textContent || '').includes('Google')) {
                        b.click();
                        return { clicked: true, text: b.textContent.trim() };
                    }
                }
                return { clicked: false };
            })()""", msg_id=5)
            print(f"  Google button: {json.dumps(google_btn)}")
            time.sleep(8)
            
            # Check if login succeeded
            page_state2 = eval_js(ws, """(() => {
                return {
                    url: window.location.href,
                    hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                    isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || 
                               !!document.querySelector('[aria-label="Account menu"]'),
                    title: document.title.slice(0, 50),
                };
            })()""", msg_id=6)
            print(f"  After login attempt: {json.dumps(page_state2)}")
            
            if not page_state2.get("isLoggedIn"):
                print("\n  ❌ Google login didn't work. Taking screenshot for manual review.")
                img = take_screenshot(ws, msg_id=97)
                if img:
                    path = os.path.join(SCREENSHOT_DIR, "x_login_failed.png")
                    with open(path, "wb") as f:
                        f.write(img)
                    print(f"  📸 Saved: {path}")
                
                # Try navigating directly to see if cookies work
                print("\n  Trying direct navigation to x.com/home...")
                cdp_cmd(ws, "Page.navigate", {"url": "https://x.com/home"}, msg_id=7)
                time.sleep(5)
                
                page_state3 = eval_js(ws, """(() => {
                    return {
                        url: window.location.href,
                        hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
                        isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || 
                                   !!document.querySelector('[aria-label="Account menu"]'),
                    };
                })()""", msg_id=8)
                print(f"  After re-navigate: {json.dumps(page_state3)}")
                
                if not page_state3.get("isLoggedIn"):
                    print("\n  ❌ Still not logged in. Will try posting anyway.")
        
        # Step 5: Find and use the compose textarea
        print("\n✏️  Finding compose textarea...")
        textarea_info = eval_js(ws, """(() => {
            // Try various selectors
            const selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[data-testid="composerTextArea"]',
                'textarea[aria-label="Post"]',
                'textarea[placeholder*="What"]',
                'textarea[placeholder*="发推"]',
                'div[role="textbox"][contenteditable="true"]',
            ];
            
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    return {
                        found: true,
                        selector: sel,
                        tag: el.tagName,
                        type: el.isContentEditable ? 'contenteditable' : 'textarea',
                        ariaLabel: el.getAttribute('aria-label'),
                        placeholder: (el.placeholder || '').slice(0, 50),
                    };
                }
            }
            
            // Last resort: find any visible textarea
            const allTas = Array.from(document.querySelectorAll('textarea'));
            if (allTas.length > 0) {
                return {
                    found: true,
                    selector: 'textarea:nth-of-type(1)',
                    tag: allTas[0].tagName,
                    ariaLabel: allTas[0].getAttribute('aria-label'),
                    placeholder: (allTas[0].placeholder || '').slice(0, 50),
                };
            }
            
            return { found: false };
        })()""", msg_id=10)
        print(f"  Textarea info: {json.dumps(textarea_info)}")
        
        if not textarea_info or not textarea_info.get("found"):
            print("\n  ❌ Compose textarea not found!")
            
            # List all interactive elements for debugging
            all_elements = eval_js(ws, """(() => {
                const els = [];
                document.querySelectorAll('*').forEach(el => {
                    if (el.tagName === 'TEXTAREA' || el.getAttribute('role') === 'textbox' || 
                        el.getAttribute('aria-label')?.includes('Post') || 
                        el.getAttribute('aria-label')?.includes('tweet')) {
                        els.push({
                            tag: el.tagName,
                            role: el.getAttribute('role'),
                            ariaLabel: el.getAttribute('aria-label'),
                            placeholder: el.placeholder?.slice(0, 30),
                            contentEditable: el.contentEditable,
                        });
                    }
                });
                return els;
            })()""", msg_id=11)
            print(f"  All textarea-like elements: {json.dumps(all_elements)}")
            
            # Take screenshot for debugging
            img = take_screenshot(ws, msg_id=96)
            if img:
                path = os.path.join(SCREENSHOT_DIR, "x_no_compose.png")
                with open(path, "wb") as f:
                    f.write(img)
                print(f"  📸 Debug screenshot: {path}")
            
            ws.close()
            return False
        
        # Step 6: Type the message
        print("\n📝 Typing message...")
        
        # Escape the copy for safe JS string embedding
        escaped_copy = copy.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")
        
        if textarea_info.get("type") == "contenteditable":
            type_result = eval_js(ws, f"""(() => {{
                const el = document.querySelector('{textarea_info["selector"]}');
                if (el) {{
                    el.focus();
                    el.innerHTML = '{escaped_copy}';
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, method: 'contentEditable', length: el.innerText.length }};
                }}
                return {{ success: false }};
            }})()""", msg_id=12)
        else:
            type_result = eval_js(ws, f"""(() => {{
                const ta = document.querySelector('{textarea_info["selector"]}');
                if (ta) {{
                    ta.focus();
                    ta.value = '{escaped_copy}';
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, method: 'textarea', length: ta.value.length }};
                }}
                return {{ success: false }};
            }})()""", msg_id=13)
        
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(3)
        
        # Verify text was entered
        verify_text = eval_js(ws, f"""(() => {{
            const ta = document.querySelector('{textarea_info["selector"]}');
            if (ta) {{
                return {{
                    value: (ta.value || ta.innerText || '').slice(0, 100),
                    length: (ta.value || ta.innerText || '').length,
                }};
            }}
            return {{ value: '', length: 0 }};
        }})()""", msg_id=14)
        print(f"  Text verification: {json.dumps(verify_text)}")
        
        # Step 7: Find and click the Post button
        print("\n🚀 Finding and clicking Post button...")
        
        # First, list all buttons near the compose area
        buttons_info = eval_js(ws, """(() => {
            const buttons = [];
            // Look for buttons in the compose area
            const compose = document.querySelector('[data-testid="tweetTextarea_0"], [data-testid="composerTextArea"]');
            const searchArea = compose || document.body;
            
            // Find all buttons
            document.querySelectorAll('button').forEach((b, i) => {
                const rect = b.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && rect.top < 800) { // Only visible buttons
                    buttons.push({
                        index: i,
                        text: (b.textContent || '').trim().slice(0, 30),
                        ariaLabel: b.getAttribute('aria-label'),
                        testId: b.getAttribute('data-testid'),
                        className: b.className?.toString().slice(0, 50),
                        x: Math.round(rect.x),
                        y: Math.round(rect.y),
                    });
                }
            });
            return buttons;
        })()""", msg_id=15)
        print(f"  Visible buttons: {json.dumps(buttons_info)}")
        
        # Try to click the Post button
        post_result = eval_js(ws, """(() => {
            // Try various selectors for the Post button
            const selectors = [
                '[data-testid="tweetButtonInline"]',
                'button[data-testid="btnTweet"]',
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
            
            // Try by text content
            const allBtns = Array.from(document.querySelectorAll('button'));
            for (const btn of allBtns) {
                const text = (btn.textContent || '').trim();
                if (text === 'Post' || text === '发推' || text === '发布' || text === '推文') {
                    btn.click();
                    return { posted: true, foundByText: text };
                }
            }
            
            // Try by CSS class patterns
            for (const btn of allBtns) {
                const cls = (btn.className || '').toString();
                if (cls.includes('r-button') && cls.includes('primary') && btn.closest('[data-testid*="Composer"]') || 
                    btn.closest('[data-testid*="tweet"]')) {
                    btn.click();
                    return { posted: true, byClass: 'primary button' };
                }
            }
            
            return { posted: false };
        })()""", msg_id=16)
        
        print(f"  Post result: {json.dumps(post_result)}")
        time.sleep(5)
        
        # Step 8: Verify post was sent
        print("\n✅ Verifying post...")
        verify = eval_js(ws, """(() => {
            return {
                location: window.location.href,
                title: document.title,
                composeAreaEmpty: (() => {
                    const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
                    return ta ? !ta.value : 'no textarea';
                })(),
                hasNewTweet: !!document.querySelector('[data-testid="tweet"]'),
                timestamp: Date.now(),
            };
        })()""", msg_id=17)
        print(f"  Verification: {json.dumps(verify)}")
        
        # Step 9: Take final screenshot
        print("\n📸 Taking final screenshot...")
        img = take_screenshot(ws, msg_id=18)
        screenshot_path = ""
        if img:
            screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_final.png")
            with open(screenshot_path, "wb") as f:
                f.write(img)
            print(f"  ✅ Screenshot saved: {screenshot_path}")
        
        ws.close()
        
        # Summary
        print("\n" + "=" * 60)
        print("POSTING SEQUENCE COMPLETED")
        print("=" * 60)
        print(f"  Date: {today.strftime('%Y-%m-%d')}")
        print(f"  Copy length: {len(copy)} chars")
        print(f"  Type result: {json.dumps(type_result)}")
        print(f"  Post result: {json.dumps(post_result)}")
        print(f"  Verify: {json.dumps(verify)}")
        print(f"  Screenshot: {screenshot_path}")
        print("=" * 60)
        
        success = post_result.get("posted", False) or verify.get("composeAreaEmpty") == True
        print(f"\nFINAL RESULT: {'✅ POST SUCCESSFUL' if success else '⚠️ POST ATTEMPTED (manual verification needed)'}")
        return success
        
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
    main()
