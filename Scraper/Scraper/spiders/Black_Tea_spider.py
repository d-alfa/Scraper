import scrapy
from Scraper.items import Black_Tea_Item

class Black_Tea_Spider(scrapy.Spider):
    name = "Black_Tea_Spider"
    allowed_domains = ["www.skonis-kvapas.lt", "https://proxy.scrapeops.io/v1/"]
    start_urls = ["https://www.skonis-kvapas.lt/arbata/juodoji-arbata"]

    def parse(self, response):
        black_teas = response.css("div.products__item")
        black_tea_item = Black_Tea_Item()

        for tea in black_teas:
            black_tea_item["name"] = tea.css("h2::text").get().strip(),
            black_tea_item["price"] = tea.css("ins::text").get(),
            black_tea_item["url"] = tea.css("a.products__item-link").attrib["href"]
            yield black_tea_item

        next_page = response.css("a[rel='next']").attrib.get("href")

        if next_page is not None:
            yield scrapy.Request(url=next_page, callback = self.parse)