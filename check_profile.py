#!/usr/bin/env python3
"""Check user profile to verify post."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    # Get current state
    current_url = page.evaluate("window.location.href")
    print(f"Current URL: {current_url}")
    
    # Check what's on the page
    page_state = page.evaluate("""(() => {
        return {
            title: document.title,
            bodyText: document.body?.innerText?.slice(0, 200),
            buttonCount: document.querySelectorAll('button').length,
            hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            hasUserSwitcher: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]'),
        };
    })()""")
    print(f"Page state: {json.dumps(page_state, ensure_ascii=False)}")
    
    # Try to find the user's profile
    print("\nLooking for user profile...")
    user_info = page.evaluate("""(() => {
        const userBtn = document.querySelector('[data-testid="SideNav.UserSwitcher"]');
        if (userBtn) {
            const text = userBtn.textContent || '';
            return { found: true, text: text.slice(0, 50) };
        }
        // Check for account menu
        const accountMenu = document.querySelector('[aria-label="Account menu"]');
        if (accountMenu) {
            return { found: true, text: 'account menu found' };
        }
        return { found: false };
    })()""")
    print(f"User info: {json.dumps(user_info)}")
    
    # Take screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_state_check.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
