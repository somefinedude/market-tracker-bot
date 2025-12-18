from playwright.sync_api import sync_playwright

def scrape_site():
    with sync_playwright() as p:
        IN_STOCK_CHECKBOX_SELECTOR = 'span[title="В наличии"]'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://moba.ru/catalog/chekhly/", timeout=60000)

        page.wait_for_load_state("load")
        page.click(IN_STOCK_CHECKBOX_SELECTOR, timeout=60000)
        print("Filter clicked")
        page.wait_for_timeout(1000)

        element1 = page.query_selector("CSS_SELECTOR_1").inner_text() if page.query_selector("CSS_SELECTOR_1") else None
        element2 = page.query_selector("CSS_SELECTOR_2").inner_text() if page.query_selector("CSS_SELECTOR_2") else None
        element3 = page.query_selector("CSS_SELECTOR_3").inner_text() if page.query_selector("CSS_SELECTOR_3") else None
        element4 = page.query_selector("CSS_SELECTOR_4").inner_text() if page.query_selector("CSS_SELECTOR_4") else None
        element5 = page.query_selector("CSS_SELECTOR_5").inner_text() if page.query_selector("CSS_SELECTOR_5") else None

        results = {
            "field1": element1,
            "field2": element2,
            "field3": element3,
            "field4": element4,
            "field5": element5
        }
        browser.close()
        return results

if __name__ == "__main__":
    data = scrape_site()

    print(data)