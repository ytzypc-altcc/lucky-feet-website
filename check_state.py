#!/usr/bin/env python3
"""Check current state and verify post."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    current_url = page.evaluate("window.location.href")
    print(f"Current URL: {current_url}")
    print(f"Title: {page.title()}")
    
    # Check if logged in
    is_logged_in = page.evaluate("""(() => {
        return {
            isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]'),
            hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            title: document.title,
        };
    })()""")
    print(f"Login status: {json.dumps(is_logged_in)}")
    
    # Take screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_current_state.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
