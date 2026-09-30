#!/usr/bin/env python3
"""Debug X page structure."""
import json, time, os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/home/rc/lucky-feet-website/assets"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0] if browser.contexts else browser.new_page()
    
    print(f"Current URL: {page.url}")
    print(f"Title: {page.title()}")
    
    # Check login
    is_logged_in = page.evaluate("""(() => {
        return {
            url: window.location.href,
            isLoggedIn: !!document.querySelector('[data-testid="SideNav.UserSwitcher"]') || !!document.querySelector('[aria-label="Account menu"]'),
            hasCompose: !!document.querySelector('[data-testid="tweetTextarea_0"]'),
            buttonCount: document.querySelectorAll('button').length,
        };
    })()""")
    print(f"Login: {json.dumps(is_logged_in)}")
    
    # List all buttons
    buttons = page.evaluate("""(() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => ({
            index: i,
            text: (b.textContent || '').trim().slice(0, 30),
            ariaLabel: b.getAttribute('aria-label'),
            testId: b.getAttribute('data-testid'),
            visible: b.offsetWidth > 0 && b.offsetHeight > 0,
        })).filter(b => b.text || b.ariaLabel || b.testId).slice(0, 30);
    })()""")
    print(f"\nButtons ({len(buttons)}):")
    for b in buttons:
        print(f"  [{b['index']}] text='{b['text']}' aria='{b['ariaLabel']}' testid='{b['testId']}' visible={b['visible']}")
    
    # List all textareas and contenteditables
    inputs = page.evaluate("""(() => {
        return Array.from(document.querySelectorAll('textarea, [contenteditable="true"], [role="textbox"]')).map(el => ({
            tag: el.tagName,
            type: el.isContentEditable ? 'contenteditable' : (el.tagName === 'TEXTAREA' ? 'textarea' : 'div'),
            ariaLabel: el.getAttribute('aria-label'),
            placeholder: (el.placeholder || '').slice(0, 40),
            testId: el.getAttribute('data-testid'),
            role: el.getAttribute('role'),
            visible: el.offsetWidth > 0 && el.offsetHeight > 0,
        }));
    })()""")
    print(f"\nInputs ({len(inputs)}):")
    for inp in inputs:
        print(f"  tag={inp['tag']} type={inp['type']} aria={inp['ariaLabel']} testid={inp['testId']} placeholder='{inp['placeholder']}' visible={inp['visible']}")
    
    # Check sidebar
    sidebar = page.evaluate("""(() => {
        const aside = document.querySelector('aside');
        if (!aside) return { noAside: true };
        const buttons = Array.from(aside.querySelectorAll('button')).map(b => ({
            text: (b.textContent || '').trim().slice(0, 30),
            ariaLabel: b.getAttribute('aria-label'),
            testId: b.getAttribute('data-testid'),
        }));
        const inputs = Array.from(aside.querySelectorAll('textarea, [contenteditable="true"], [role="textbox"]')).map(el => ({
            tag: el.tagName,
            ariaLabel: el.getAttribute('aria-label'),
            testId: el.getAttribute('data-testid'),
            role: el.getAttribute('role'),
            contentEditable: el.contentEditable,
        }));
        return { buttons, inputs };
    })()""")
    print(f"\nSidebar buttons: {json.dumps(sidebar.get('buttons', []))}")
    print(f"Sidebar inputs: {json.dumps(sidebar.get('inputs', []))}")
    
    # Take screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "x_debug.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"\n📸 Screenshot: {screenshot_path}")
    
    browser.close()
