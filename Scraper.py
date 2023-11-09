import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def collect_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()

    soup = BeautifulSoup(response_text, "html.parser")
    return soup

async def main():
    url = "https://www.skonis-kvapas.lt/arbata/juodoji-arbata"
    parsed_data = await collect_html(url)
    print(parsed_data)

if __name__ == "__main__":
    asyncio.run(main())