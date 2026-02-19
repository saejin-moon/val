import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from fake_useragent import UserAgent

BASE_URL = "https://api.tracker.gg/api/v2/valorant/standard/matches/"
TARGET_URL = f"{BASE_URL}riot/ski%23lgnd?platform=pc&season=3ea2b318-423b-cf86-25da-7cbb0eefbe2d&type=competitive"

ua = UserAgent()

async def get_json(page, url):
    await asyncio.sleep(random.uniform(3, 7))
    
    print(f"req {url}")
    
    response_data = await page.evaluate(f"""
        async () => {{
            try {{
                const res = await fetch("{url}");
                if (res.status === 429) return {{ error: 429 }};
                if (!res.ok) return {{ error: res.status }};
                return await res.json();
            }} catch (e) {{
                return {{ error: 'fetch_failed' }};
            }}
        }}
    """)

    if isinstance(response_data, dict) and response_data.get("error") == 429:
        print("429 error, 30s sleep.")
        await asyncio.sleep(30)
        return None
        
    return response_data

async def get_match_ids(page, page_num):
    url = TARGET_URL + (f"&next={page_num}" if page_num > 0 else "")
    json_data = await get_json(page, url)
    
    if json_data and 'data' in json_data and 'matches' in json_data['data']:
        return [m['attributes']['id'] for m in json_data['data']['matches']]
    return []

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)
        
        context = await browser.new_context(
            user_agent=ua.random,
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()

        print("init.")
        await page.goto("https://tracker.gg/valorant")
        await asyncio.sleep(5) 

        all_match_ids = []
        page_num = 0
        
        while True:
            batch = await get_match_ids(page, page_num)
            
            if not batch or len(batch) == 0:
                print("end.")
                break
                
            all_match_ids.extend(batch)
            print(f"page no. {page_num}: got {len(batch)} matches (total: {len(all_match_ids)})")
            
            page_num += 1
            
            if page_num > 20: 
                break

        with open("match_ids.txt", "w") as f:
            f.write("\n".join(all_match_ids))

        print(f"saved {len(all_match_ids)} ids to match_ids.txt.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())