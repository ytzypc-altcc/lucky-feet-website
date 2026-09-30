#!/usr/bin/env python3
"""Post to X using proper event dispatching."""
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
        print(f"\n🔗 Connecting to CDP...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
        
        # Go to home
        print("\n📍 Going to X home...")
        page.goto("https://x.com/home", timeout=15000, wait_until="domcontentloaded")
        time.sleep(3)
        
        # Check login and account
        account_info = page.evaluate("""() => {
            const accountBtn = document.querySelector('[aria-label="Account menu"]');
            const userSwitcher = document.querySelector('[data-testid="SideNav.UserSwitcher"]');
            return {
                isLoggedIn: !!accountBtn || !!userSwitcher,
                accountText: accountBtn?.textContent?.trim().slice(0, 30) || userSwitcher?.textContent?.trim().slice(0, 30) || 'none',
                url: window.location.href,
            };
        }""")
        print(f"  Account: {json.dumps(account_info)}")
        
        if not account_info.get("isLoggedIn"):
            print("  ❌ Not logged in")
            browser.close()
            return False
        
        # Click the compose area to open editor
        print("\n✏️  Opening compose editor...")
        page.click('[data-testid="tweetTextarea_0"]')
        time.sleep(2)
        
        # Type text using proper event dispatching
        print("\n📝 Typing message...")
        type_result = page.evaluate(f"""() => {{
            const el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return {{ success: false }};
            
            el.focus();
            el.innerText = `{copy}`;
            
            // Dispatch all relevant events that X listens to
            const events = ['input', 'change', 'keydown', 'keyup', 'blur'];
            events.forEach(eventName => {{
                el.dispatchEvent(new Event(eventName, {{ bubbles: true }}));
            }});
            
            // Also try dispatching on the parent
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('paste', {{ bubbles: true }}));
            
            // Check if Post button is now enabled
            const postBtn = document.querySelector('button[data-testid="tweetButton"]');
            const postBtnInline = document.querySelector('button[data-testid="tweetButtonInline"]');
            
            return {{
                success: true,
                length: el.innerText.length,
                postBtnEnabled: postBtn ? !postBtn.disabled : 'not found',
                postBtnInlineDisabled: postBtnInline ? postBtnInline.disabled : 'not found',
            }};
        }}""")
        print(f"  Type result: {json.dumps(type_result)}")
        time.sleep(2)
        
        # Try to click Post button
        print("\n🚀 Clicking Post...")
        post_result = page.evaluate("""() => {
            // Try different post button selectors
            const selectors = [
                'button[data-testid="tweetButton"]',
                'button[data-testid="tweetButtonInline"]',
            ];
            
            for (const sel of selectors) {
                const btn = document.querySelector(sel);
                if (btn && btn.offsetParent !== null) {
                    btn.click();
                    return { clicked: true, selector: sel, disabled: btn.disabled };
                }
            }
            
            // Try by text
            const allBtns = Array.from(document.querySelectorAll('button'));
            for (const btn of allBtns) {
                const text = (btn.textContent || '').trim();
                if (text === 'Post' && btn.offsetParent !== null) {
                    btn.click();
                    return { clicked: true, byText: text, disabled: btn.disabled };
                }
            }
            
            return { clicked: false };
        }""")
        print(f"  Post result: {json.dumps(post_result)}")
        
        # Wait for post
        print("  Waiting...")
        time.sleep(8)
        
        # Verify
        verify = page.evaluate("""() => {
            const url = window.location.href;
            const hasTweetUrl = url.includes('/status/');
            const composeEmpty = !document.querySelector('[data-testid="tweetTextarea_0"]')?.innerText;
            
            // Check for post confirmation
            const confirmEl = document.querySelector('[data-testid="backButton"]');
            
            return {
                url: url,
                hasTweetUrl: hasTweetUrl,
                composeEmpty: composeEmpty,
                hasBackButton: !!confirmEl,
            };
        }""")
        print(f"  Verify: {json.dumps(verify)}")
        
        # Screenshot
        screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_v6.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"\n📸 Screenshot: {screenshot_path}")
        
        browser.close()
        
        success = verify.get("composeEmpty") or verify.get("hasTweetUrl") or verify.get("hasBackButton")
        print(f"\n{'='*50}")
        print(f"RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"Copy: {copy[:120]}...")
        print(f"Screenshot: {screenshot_path}")
        print(f"{'='*50}")
        return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
