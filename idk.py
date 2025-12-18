import time
from playwright.sync_api import sync_playwright

def smth():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="profile_ig",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1536, "height": 864},
            locale="en-US"
        )

        page = context.pages[0] if context.pages else context.new_page()

        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """)


        page.goto("https://www.instagram.com/")
        time.sleep(5.3)
        page.locator('a[href^="/accounts/login"]').click()
        time.sleep(10)

        context.close()

smth()
