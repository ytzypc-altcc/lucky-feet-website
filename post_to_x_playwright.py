#!/usr/bin/env python3
"""
Post to X using Playwright with CDP.
Injects cookies from chrome-openclaw-debug profile.
"""
import json, time, os, base64, sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright

CDP_PORT = 9222
SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

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

def decrypt_chrome_cookie(encrypted_value):
    """Try to decrypt Chrome v10 cookie on Linux."""
    # Chrome v10 on Linux: encrypted_value = 'v10' + salt(8 bytes) + encrypted(256 bytes) + tag(16 bytes)
    # Uses AES-256-GCM with key from Secret Service
    if not encrypted_value or len(encrypted_value) < 13:
        return None
    if encrypted_value.startswith(b'v10') or encrypted_value.startswith(b'v11'):
        return None  # Encrypted, can't decrypt without keyring
    try:
        return encrypted_value.decode('utf-8')
    except:
        return None

def get_cookies_from_chrome():
    """Extract cookies from chrome-openclaw-debug profile."""
    cookies = []
    db_paths = [
        '/home/rc/.config/chrome-openclaw-debug/Default/Cookies',
        '/home/rc/.config/chrome-openclaw-debug/Profile 1/Cookies',
    ]
    for db_path in db_paths:
        if not os.path.exists(db_path):
            continue
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT host_key, name, value, encrypted_value, path, expires_utc, is_secure, is_http_only
                FROM cookies
                WHERE host_key LIKE '%x.com%' OR host_key LIKE '%twitter.com%'
                AND (name = 'auth_token' OR name = 'ct0' OR name = 'guest_id' OR name = 'session_id')
            """)
            for row in cursor.fetchall():
                host_key, name, value, encrypted_value, path, expires, secure, http_only = row
                # Try decrypted value first, then plaintext
                cookie_val = decrypt_chrome_cookie(encrypted_value)
                if cookie_val is None and value:
                    cookie_val = value
                if cookie_val:
                    cookies.append({
                        'name': name,
                        'value': cookie_val,
                        'domain': host_key.lstrip('.'),
                        'path': path or '/',
                        'secure': bool(secure),
                        'httpOnly': bool(http_only),
                    })
            conn.close()
        except Exception as e:
            print(f"  Cookie DB error: {e}")
    return cookies

def main():
    today = datetime.now()
    print(f"=== 豪门贵足养生馆 X Post - {today.strftime('%Y-%m-%d')} ===")
    
    copy = generate_daily_copy()
    print(f"\n📝 Copy ({len(copy)} chars):\n{copy}")
    
    # Get cookies from Chrome
    print("\n🔑 Extracting cookies...")
    cookies = get_cookies_from_chrome()
    print(f"  Found {len(cookies)} cookies")
    for c in cookies:
        print(f"    {c['domain']} {c['name']}={c['value'][:20] if len(c['value']) > 20 else c['value']}...")
    
    with sync_playwright() as p:
        # Connect to existing Chrome on port 9222
        print(f"\n🔗 Connecting to CDP on port {CDP_PORT}...")
        browser = p.chromium.connect_over_cdp(f"http://localhost:{CDP_PORT}")
        
        # Get or create a page
        pages = browser.contexts[0].pages if browser.contexts else []
        print(f"  Existing pages: {len(pages)}")
        
        if pages:
            page = pages[0]
        else:
            page = browser.contexts[0].new_page() if browser.contexts else None
        
        if not page:
            print("  ❌ No page available")
            browser.close()
            return False
        
        print(f"  Using page: {page.url[:60] if page.url else 'about:blank'}")
        
        # Navigate to X
        print("\n📍 Navigating to X...")
        page.goto("https://x.com/home", timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Check login status
        is_logged_in = page.evaluate("""(() => {
            return {
                url: window.location.href,
                title: document.title,
                isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            };
        })()""")
        print(f"  Login status: {json.dumps(is_logged_in)}")
        
        if not is_logged_in.get("isLoggedIn"):
            print("\n  ⚠️  Not logged in!")
            # Try Google sign-in
            print("  Trying Google sign-in...")
            google_btn = page.locator('button:has-text("Google")').first
            if google_btn.is_visible(timeout=3000):
                google_btn.click()
                time.sleep(8)
                is_logged_in = page.evaluate("""(() => {
                    return {
                        url: window.location.href,
                        isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]'),
                    };
                })()""")
                print(f"  After Google: {json.dumps(is_logged_in)}")
            
            if not is_logged_in.get("isLoggedIn"):
                print("  ❌ Login failed. Taking screenshot...")
                screenshot_path = os.path.join(SCREENSHOT_DIR, "x_login_failed.png")
                page.screenshot(path=screenshot_path)
                print(f"  📸 {screenshot_path}")
                browser.close()
                return False
        
        print("\n✅ Logged in!")
        
        # Find compose area
        print("\n✏️  Finding compose area...")
        ta_info = page.evaluate("""(() => {
            const selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[data-testid="composerTextArea"]',
                'textarea[aria-label="Post"]',
                'div[role="textbox"][contenteditable="true"]',
            ];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    return { found: true, type: el.isContentEditable ? 'contenteditable' : 'textarea' };
                }
            }
            return { found: false };
        })()""")
        print(f"  Info: {json.dumps(ta_info)}")
        
        if not ta_info.get("found"):
            print("  ❌ Compose area not found!")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "x_no_compose.png")
            page.screenshot(path=screenshot_path)
            browser.close()
            return False
        
        # Type the message
        print("\n📝 Typing message...")
        if ta_info.get("type") == "contenteditable":
            page.evaluate(f"""(() => {{
                const el = document.querySelector('div[role="textbox"][contenteditable="true"]') 
                    || document.querySelector('[data-testid="tweetTextarea_0"]')
                    || document.querySelector('[data-testid="composerTextArea"]');
                if (el) {{
                    el.focus();
                    el.innerText = `{copy}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return {{ success: true, length: el.innerText.length }};
                }}
                return {{ success: false }};
            }})()""")
        else:
            page.evaluate(f"""(() => {{
                const ta = document.querySelector('[data-testid="tweetTextarea_0"]')
                    || document.querySelector('[data-testid="composerTextArea"]')
                    || document.querySelector('textarea[aria-label="Post"]');
                if (ta) {{
                    ta.focus();
                    ta.value = `{copy}`;
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{ success: true, length: ta.value.length }};
                }}
                return {{ success: false }};
            }})()""")
        time.sleep(2)
        
        # Verify text
        text_check = page.evaluate("""(() => {
            const el = document.querySelector('[data-testid="tweetTextarea_0"]') 
                || document.querySelector('[data-testid="composerTextArea"]')
                || document.querySelector('div[role="textbox"][contenteditable="true"]');
            return { text: (el?.innerText || el?.value || '').slice(0, 80), length: (el?.innerText || el?.value || '').length };
        })()""")
        print(f"  Text check: {json.dumps(text_check)}")
        
        # Click Post
        print("\n🚀 Clicking Post...")
        post_result = page.evaluate("""(() => {
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
        })()""")
        print(f"  Post result: {json.dumps(post_result)}")
        time.sleep(5)
        
        # Verify post
        print("\n✅ Verifying...")
        verify = page.evaluate("""(() => {
            return {
                url: window.location.href,
                composeEmpty: !document.querySelector('[data-testid="tweetTextarea_0"]')?.value,
            };
        })()""")
        print(f"  Verify: {json.dumps(verify)}")
        
        # Screenshot
        screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_result.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"  📸 Screenshot: {screenshot_path}")
        
        # Also check timeline for the new post
        tweets = page.evaluate("""(() => {
            const articles = document.querySelectorAll('article');
            const results = [];
            for (const art of articles) {
                const textEl = art.querySelector('[data-testid="tweetText"]');
                if (textEl) {
                    results.push(textEl.textContent.substring(0, 80));
                }
            }
            return results.slice(0, 3);
        })()""")
        print(f"  Recent tweets: {tweets}")
        
        browser.close()
        
        success = post_result.get("posted", False)
        print(f"\n{'='*50}")
        print(f"RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"Copy ({len(copy)} chars): {copy[:120]}...")
        print(f"Screenshot: {screenshot_path}")
        print(f"{'='*50}")
        return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
