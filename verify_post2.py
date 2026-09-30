#!/usr/bin/env python3
"""Verify the post appeared on X timeline - retry."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Refresh the page
    print("Refreshing page...")
    page.reload(timeout=20000, wait_until="domcontentloaded")
    time.sleep(5)
    
    # Check login
    is_logged_in = page.evaluate("""(() => {
        return {
            url: window.location.href,
            isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]'),
        };
    })()""")
    print(f"  Logged in: {is_logged_in.get('isLoggedIn')}")
    
    # Scroll to top
    print("Scrolling to top...")
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)
    
    # Get all tweets
    tweets = page.evaluate("""(() => {
        const articles = document.querySelectorAll('article');
        const results = [];
        for (const art of articles) {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            if (textEl) {
                results.push({
                    text: textEl.textContent.substring(0, 100),
                    author: art.querySelector('[data-testid="User-Name"]')?.textContent?.trim().split('\n')[0] || 'unknown',
                });
            }
        }
        return results;
    })()""")
    print(f"\nTweets found ({len(tweets)}):")
    for t in tweets:
        print(f"  - {t['author']}: {t['text'][:60]}...")
    
    # Check if our post is there
    our_post = any('豪门贵足' in t['text'] or '养生馆' in t['text'] for t in tweets)
    print(f"\nOur post found: {our_post}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_verified2.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
