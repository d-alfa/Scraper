import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def collect_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()

    soup = BeautifulSoup(response_text, "html.parser")
    return soup

async def collect_title(soup):
    titles = []
    html_data = soup.find_all(class_="products__item")
    for h in html_data:
        title = h.find("h2")
        h2 = title.string.strip()
        titles.append([h2])
    return titles

async def main():
    url = "https://www.skonis-kvapas.lt/arbata/juodoji-arbata"
    soup = await collect_html(url)
    title = await collect_title(soup)
    print(title)

if __name__ == "__main__":
    asyncio.run(main())