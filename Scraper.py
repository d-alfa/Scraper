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
    for data in html_data:
        title = data.find("h2")
        h2 = title.string.strip()
        titles.append([h2])
    return titles

async def collect_price(soup):
    prices = []
    html_data = soup.find_all(class_="products__item")
    for data in html_data:
        price = data.find("ins")
        ins = price.string.replace("\xa0€","").replace(",",".").replace("€","")
        prices.append([ins])
    return prices

async def main():
    url = "https://www.skonis-kvapas.lt/arbata/juodoji-arbata"
    soup = await collect_html(url)
    title = await collect_title(soup)
    price = await collect_price(soup)
    print(price)

if __name__ == "__main__":
    asyncio.run(main())