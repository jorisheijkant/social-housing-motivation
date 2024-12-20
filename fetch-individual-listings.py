import os 
from bs4 import BeautifulSoup
import requests
import time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio

headless = False
listing_folder = "output/listings"
links_to_listings = []

async def scrape(headless=headless):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        print("Opened the browser...")

        for (folder, labels, files) in os.walk(listing_folder):
            for file in files:
                file_path = f"{listing_folder}/{file}"
                file_city = file.split('.')[0]
                print(f"Now getting listings from file {file} ({file_city})")
                with open(file_path, "r") as html_file:
                    soup = BeautifulSoup(html_file, 'html.parser')

                    job_list = soup.find("div", {"class": "list", "disable-virtualization": True})

                    if job_list:
                        jobs = job_list.find_all("div", {"data-container": ""})
                        print(f"{len(jobs)} jobs found")

                        for job in jobs:
                            job_id = ""
                            job_classes = job.get("class")
                            if job_classes is not None:
                                job_id = job_classes[0]
                            
                            job_link_item = job.find("a")
                            if job_link_item is None:
                                continue
                            
                            job_link = job_link_item.get("href")
                            print(f"{job_id}, {job_link}")

                            await page.goto(job_link)
                            await page.wait_for_timeout(2000)

                            html_content = await page.content()
                            bestand_map = f"output/listing"
                            bestand_naam = f"output/listing/{job_id}.html"
                            os.makedirs(bestand_map, exist_ok=True)

                            with open(bestand_naam, "w", encoding="utf-8") as f:
                                f.write(html_content)

async def main():
    while True:
        try:
            await scrape()
        except Exception as e:
            print(f"An error occurred: {e}. Restarting the scrape...")

if __name__ == "__main__":
    asyncio.run(main())
