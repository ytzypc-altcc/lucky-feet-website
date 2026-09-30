#!/usr/bin/env python3
"""Check if post is in drafts or timeline."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Go to home
    print("Going to home...")
    page.goto("https://x.com/home", timeout=15000, wait_until="domcontentloaded")
    time.sleep(3)
    
    # Check for drafts or compose area
    drafts_check = page.evaluate("""() => {
        // Check for draft indicator
        const draftEl = document.querySelector('[data-testid="draftIndicator"]');
        const composeEl = document.querySelector('[data-testid="tweetTextarea_0"]');
        
        // Check all articles for our post
        const articles = document.querySelectorAll('article');
        const ourPost = Array.from(articles).some(art => {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            return textEl && textEl.textContent.includes('Richmond') && textEl.textContent.includes('太阳');
        });
        
        // Check URL for post confirmation
        const url = window.location.href;
        
        return {
            hasDraft: !!draftEl,
            hasCompose: !!composeEl,
            composeText: composeEl?.innerText?.slice(0, 50) || '',
            ourPostInTimeline: ourPost,
            url: url,
            articleCount: articles.length,
        };
    }""")
    print(f"Page state: {json.dumps(drafts_check)}")
    
    # Scroll through timeline to find our post
    print("\nScrolling through timeline...")
    our_post_found = False
    for i in range(5):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1)
        
        check = page.evaluate("""() => {
            const articles = document.querySelectorAll('article');
            let found = false;
            articles.forEach(art => {
                const textEl = art.querySelector('[data-testid="tweetText"]');
                if (textEl && textEl.textContent.includes('Richmond') && textEl.textContent.includes('太阳')) {
                    found = true;
                }
            });
            return found;
        }""")
        if check:
            our_post_found = True
            print("  Found our post in timeline!")
            break
    
    if not our_post_found:
        print("  Post not found in timeline after scrolling")
    
    # Check profile again with more tweets
    print("\nChecking profile with more detail...")
    page.goto("https://x.com/Luckyfeet_168", timeout=15000, wait_until="domcontentloaded")
    time.sleep(5)
    
    # Get ALL tweets including older ones
    all_tweets = page.evaluate("""() => {
        const articles = document.querySelectorAll('article');
        const results = [];
        for (const art of articles) {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            const dateEl = art.querySelector('[data-testid="tweetDate"]');
            if (textEl) {
                results.push({
                    text: textEl.textContent,
                    date: dateEl ? dateEl.textContent : '',
                });
            }
        }
        return results;
    }""")
    print(f"Profile tweets ({len(all_tweets)}):")
    for i, t in enumerate(all_tweets):
        print(f"  [{i}] [{t['date']}] {t['text'][:80]}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_check.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
    
    print(f"\n{'='*50}")
    if our_post_found or any('Richmond' in t['text'] and '太阳' in t['text'] for t in all_tweets):
        print("✅ POST CONFIRMED")
    else:
        print("⚠️ POST NOT FOUND - may need to check again later")
    print(f"{'='*50}")
