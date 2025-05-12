import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_end_to_end():
    async with async_playwright() as p:
        # Launch browser in headless mode for testing
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Step 1: Visit the website
        await page.goto('https://mohanshil.vercel.app/')
        
        # Step 2: Verify the page title
        title = await page.title()
        assert title == "Mohan Shil Portfolio", f"Expected title 'Mohan Shil Portfolio', but got '{title}'"
        
        # Step 3: Ensure the page has loaded by waiting for a key element (e.g., the navigation bar)
        await page.wait_for_selector("nav", timeout=10000)  # Wait for navigation bar
        
        # Step 4: Test navigation to 'About' section
        await page.click('text=About')  # Click on the About section in the navigation
        await page.wait_for_selector("text=About Me", timeout=10000)  # Wait for 'About Me' header in the About section
        assert "About" in await page.title(), "Navigation to 'About' failed!"
        
        # Step 5: Test navigation to 'Projects' section
        await page.click('text=Projects')
        await page.wait_for_selector("text=Projects", timeout=10000)  # Wait for Projects section
        assert "Projects" in await page.title(), "Navigation to 'Projects' failed!"
        
        # Step 6: Test external link (GitHub link)
        github_link = "a[href='https://github.com/mohan-shil']"
        
        # Wait for the GitHub link to be visible
        await page.wait_for_selector(github_link, timeout=15000)
        # Click on GitHub link and check if it opens in a new tab
        new_tab_promise = context.expect_page()
        await page.locator(github_link).click()
        
        # Step 7: Verify that the new tab contains the correct GitHub URL
        github_page = await new_tab_promise
        await github_page.wait_for_load_state("domcontentloaded")
        assert "github.com" in github_page.url, f"Expected GitHub page, but got {github_page.url}"



        # Close the browser
        await browser.close()
