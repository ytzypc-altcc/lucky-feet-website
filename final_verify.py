#!/usr/bin/env python3
"""Detailed verification of post."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Go to profile
    print("Going to profile...")
    page.goto("https://x.com/Luckyfeet_168", timeout=20000, wait_until="domcontentloaded")
    time.sleep(5)
    
    # Get ALL tweets on profile
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
    
    # Check if our post is there
    our_post = any('Richmond' in t['text'] and '太阳' in t['text'] for t in all_tweets)
    print(f"\nOur post (today's weather topic) found: {our_post}")
    
    # Also check the compose area
    compose_check = page.evaluate("""() => {
        const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
        if (ta) {
            return {
                found: true,
                text: (ta.innerText || ta.value || '').slice(0, 100),
                length: (ta.innerText || ta.value || '').length,
            };
        }
        return { found: false };
    }""")
    print(f"\nCompose area: {json.dumps(compose_check)}")
    
    # Go to home timeline
    print("\nGoing to home timeline...")
    page.goto("https://x.com/home", timeout=15000, wait_until="domcontentloaded")
    time.sleep(3)
    
    # Get timeline tweets
    timeline_tweets = page.evaluate("""() => {
        const articles = document.querySelectorAll('article');
        const results = [];
        for (const art of articles) {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            if (textEl) {
                results.push(textEl.textContent.substring(0, 100));
            }
        }
        return results.slice(0, 10);
    }""")
    print(f"\nTimeline tweets ({len(timeline_tweets)}):")
    for i, t in enumerate(timeline_tweets):
        print(f"  [{i}] {t}")
    
    # Check for our post in timeline
    timeline_has_post = any('Richmond' in t and '太阳' in t for t in timeline_tweets)
    print(f"\nOur post in timeline: {timeline_has_post}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_final_verify.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
    
    if our_post:
        print(f"\n{'='*50}")
        print("✅ POST CONFIRMED - Post appears on profile!")
        print(f"{'='*50}")
    else:
        print(f"\n{'='*50}")
        print("⚠️ POST NOT FOUND on profile - may have failed silently")
        print(f"{'='*50}")
