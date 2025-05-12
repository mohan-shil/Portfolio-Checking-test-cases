from playwright.sync_api import sync_playwright

def test_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0.5)
        page = browser.new_page()
        page.goto("https://mohanshil.vercel.app")

        # Assert page title
        assert page.title() == "Mohan's Portfolio"

        # Assert main header contains expected name
        main_heading = page.locator("h1").inner_text()
        assert "Mohan Shil" in main_heading

        assert page.pause()

        browser.close()