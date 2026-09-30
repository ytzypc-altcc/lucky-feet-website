#!/usr/bin/env python3
"""Post to X using Playwright with CDP - fixed version."""
import json, time, os
from datetime import datetime
from playwright.sync_api import sync_playwright

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

def main():
    today = datetime.now()
    print(f"=== 豪门贵足养生馆 X Post - {today.strftime('%Y-%m-%d')} ===")
    
    copy = generate_daily_copy()
    print(f"\n📝 Copy ({len(copy)} chars):\n{copy}")
    
    with sync_playwright() as p:
        print(f"\n🔗 Connecting to CDP on port 9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # Use existing context or create one
        if browser.contexts:
            ctx = browser.contexts[0]
        else:
            ctx = browser.new_context()
        
        # Find existing page or create new one
        pages = ctx.pages
        if pages:
            page = pages[0]
            print(f"  Using existing page: {page.url[:60]}")
        else:
            page = ctx.new_page()
            print("  Created new page")
        
        # Navigate to X home
        print("\n📍 Navigating to X home...")
        page.goto("https://x.com/home", timeout=30000, wait_until="networkidle")
        time.sleep(5)
        
        # Check login
        is_logged_in = page.evaluate("""(() => {
            return {
                url: window.location.href,
                title: document.title,
                isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
                hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            };
        })()""")
        print(f"  Login: {json.dumps(is_logged_in)}")
        
        if not is_logged_in.get("isLoggedIn"):
            print("  ❌ Not logged in!")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "x_login_failed.png")
            page.screenshot(path=screenshot_path)
            print(f"  📸 {screenshot_path}")
            browser.close()
            return False
        
        print("\n✅ Logged in!")
        
        # Find and click the compose area to open the tweet composer
        print("\n✏️  Clicking compose area...")
        
        # Try clicking on the compose area or the Post button in sidebar
        click_result = page.evaluate("""(() => {
            // Try clicking the compose textarea
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (ta && ta.offsetParent !== null) {
                ta.click();
                return { clicked: 'textarea', text: ta.innerText?.slice(0, 50) };
            }
            // Try clicking the Post button in sidebar
            const postBtn = document.querySelector('button[data-testid="tweetButtonInline"]');
            if (postBtn && postBtn.offsetParent !== null) {
                postBtn.click();
                return { clicked: 'post_button' };
            }
            return { clicked: 'nothing' };
        })()""")
        print(f"  Click result: {json.dumps(click_result)}")
        time.sleep(3)
        
        # Find compose area after clicking
        ta_info = page.evaluate("""(() => {
            const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (ta) {
                return { found: true, type: ta.isContentEditable ? 'contenteditable' : 'textarea', visible: ta.offsetParent !== null };
            }
            // Try composer textarea
            const composer = document.querySelector('[data-testid="composerTextArea"]');
            if (composer) {
                return { found: true, type: 'composerTextArea', visible: composer.offsetParent !== null };
            }
            // Try any contenteditable
            const ce = document.querySelector('div[contenteditable="true"]');
            if (ce && ce.offsetParent !== null) {
                return { found: true, type: 'contenteditable', visible: true };
            }
            return { found: false };
        })()""")
        print(f"  Compose info: {json.dumps(ta_info)}")
        
        if not ta_info.get("found"):
            print("  ❌ Compose area not found after click!")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "x_no_compose.png")
            page.screenshot(path=screenshot_path)
            print(f"  📸 {screenshot_path}")
            browser.close()
            return False
        
        # Type the message
        print("\n📝 Typing message...")
        type_result = page.evaluate(f"""(() => {{
            // Try tweetTextarea_0 first
            let el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) el = document.querySelector('[data-testid="composerTextArea"]');
            if (!el) el = document.querySelector('div[contenteditable="true"]');
            
            if (el) {{
                el.focus();
                if (el.isContentEditable) {{
                    el.innerText = `{copy}`;
                }} else {{
                    el.value = `{copy}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return {{ success: true, length: (el.innerText || el.value || '').length }};
            }}
            return {{ success: false }};
        }})()""")
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Verify text
        text_check = page.evaluate("""(() => {
            const el = document.querySelector('[data-testid="tweetTextarea_0"]') 
                || document.querySelector('[data-testid="composerTextArea"]')
                || document.querySelector('div[contenteditable="true"]');
            return { 
                text: (el?.innerText || el?.value || '').slice(0, 100),
                length: (el?.innerText || el?.value || '').length 
            };
        })()""")
        print(f"  Text check: {json.dumps(text_check)}")
        
        # Click Post
        print("\n🚀 Clicking Post...")
        post_result = page.evaluate("""(() => {
            // Try various selectors
            const selectors = [
                '[data-testid="tweetButtonInline"]',
                'button[aria-label="Post"]',
                'button[data-testid="tweetButton"]',
            ];
            for (const sel of selectors) {
                const btn = document.querySelector(sel);
                if (btn && btn.offsetParent !== null) {
                    btn.click();
                    return { posted: true, selector: sel };
                }
            }
            // Find by text
            const allBtns = Array.from(document.querySelectorAll('button'));
            for (const btn of allBtns) {
                const text = (btn.textContent || '').trim();
                if (text === 'Post' || text === '发推' || text === '发布') {
                    btn.click();
                    return { posted: true, text };
                }
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
                composeEmpty: !document.querySelector('[data-testid="tweetTextarea_0"]')?.innerText,
            };
        })()""")
        print(f"  Verify: {json.dumps(verify)}")
        
        # Screenshot
        screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_result.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"  📸 Screenshot: {screenshot_path}")
        
        # Check timeline
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
