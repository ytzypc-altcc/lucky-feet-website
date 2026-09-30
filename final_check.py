#!/usr/bin/env python3
"""Final verification of the post."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Go to profile
    print("Checking profile...")
    page.goto("https://x.com/Luckyfeet_168", timeout=20000, wait_until="domcontentloaded")
    time.sleep(5)
    
    # Get all tweets
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
    print(f"\nAll tweets on profile ({len(all_tweets)}):")
    for i, t in enumerate(all_tweets):
        print(f"  [{i}] {t['text'][:100]}")
    
    # Check for our post
    our_post = any('Richmond' in t['text'] and '太阳' in t['text'] for t in all_tweets)
    print(f"\nOur post found: {our_post}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_final_verify.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    # Also check timeline
    print("\nChecking timeline...")
    page.goto("https://x.com/home", timeout=15000, wait_until="domcontentloaded")
    time.sleep(3)
    
    timeline_tweets = page.evaluate("""() => {
        const articles = document.querySelectorAll('article');
        return Array.from(articles).slice(0, 5).map(art => {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            return textEl ? textEl.textContent.substring(0, 80) : '';
        });
    }""")
    print(f"Timeline tweets: {json.dumps(timeline_tweets, ensure_ascii=False)}")
    
    browser.close()
    
    if our_post:
        print(f"\n✅ POST VERIFIED on profile!")
    else:
        print(f"\n⚠️ Post not found on profile yet (may take a moment to appear)")
