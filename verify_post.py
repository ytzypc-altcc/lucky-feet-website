#!/usr/bin/env python3
"""Verify the post appeared on X timeline."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Scroll to top to see latest posts
    print("Scrolling to top...")
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)
    
    # Check for the new post
    tweets = page.evaluate("""(() => {
        const articles = document.querySelectorAll('article');
        const results = [];
        for (const art of articles) {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            if (textEl) {
                const text = textEl.textContent;
                if (text.includes('豪门贵足') || text.includes('养生馆') || text.includes('推拿')) {
                    results.push({
                        text: text.substring(0, 120),
                        hasDataTestid: art.getAttribute('data-testid'),
                    });
                }
            }
        }
        return results;
    })()""")
    print(f"\nFound posts with keyword: {json.dumps(tweets, ensure_ascii=False)}")
    
    # Also get all recent tweets
    all_tweets = page.evaluate("""(() => {
        const articles = document.querySelectorAll('article');
        return Array.from(articles).slice(0, 5).map(art => {
            const textEl = art.querySelector('[data-testid="tweetText"]');
            return textEl ? textEl.textContent.substring(0, 80) : 'no text';
        });
    })()""")
    print(f"\nAll recent tweets: {json.dumps(all_tweets, ensure_ascii=False)}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_post_verified.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
