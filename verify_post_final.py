#!/usr/bin/env python3
"""Verify post by checking user profile."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Navigate to user profile
    print("Navigating to user profile...")
    page.goto("https://x.com/Luckyfeet_168", timeout=20000, wait_until="domcontentloaded")
    time.sleep(5)
    
    # Get profile info
    profile_info = page.evaluate("() => ({ url: window.location.href, title: document.title, username: document.querySelector('[data-testid=\"UserName\"]')?.textContent?.split('\\n')[0] || 'unknown' })")
    print(f"Profile: {json.dumps(profile_info)}")
    
    # Get recent tweets
    tweets = page.evaluate("() => { const articles = document.querySelectorAll('article'); const results = []; for (const art of articles) { const textEl = art.querySelector('[data-testid=\"tweetText\"]'); if (textEl) { results.push(textEl.textContent.substring(0, 120)); } } return results.slice(0, 5); }")
    print(f"\nRecent tweets on profile ({len(tweets)}):")
    for i, t in enumerate(tweets):
        print(f"  [{i}] {t}")
    
    # Check if our post is there
    our_post = any('豪门贵足' in t or '养生馆' in t for t in tweets)
    print(f"\nOur post found on profile: {our_post}")
    
    # Screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_profile_verified.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
    
    print(f"\n{'='*50}")
    print(f"POST VERIFICATION: {'✅ CONFIRMED' if our_post else '⚠️ POST SUBMITTED BUT NOT FOUND ON PROFILE'}")
    print(f"{'='*50}")
