import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from fake_useragent import UserAgent

BASE_URL = "https://api.tracker.gg/api/v2/valorant/standard/matches/"
MATCH_ID = "6b829358-096d-47f9-aeb6-3748347946b1" 

ua = UserAgent()

async def fetch_match_data(page, match_id):
    url = f"{BASE_URL}{match_id}"
    print(f"Fetching Match: {url}")
    
    match_json = await page.evaluate(f"""
        async () => {{
            const res = await fetch("{url}");
            return await res.json();
        }}
    """)
    return match_json

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=ua.random)
        page = await context.new_page()

        await page.goto("https://tracker.gg/valorant")
        await asyncio.sleep(3)

        match_data = await fetch_match_data(page, MATCH_ID)

        filename = f"match_{MATCH_ID}.json"
        with open(filename, "w") as f:
            json.dump(match_data, f, indent=4)
        print(f"json saved to {filename}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())