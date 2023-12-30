import scrapy
from Scraper.items import Green_Tea_Item

class Green_Tea_Spider(scrapy.Spider):
    name = "Green_Tea_Spider"
    allowed_domains = ["www.skonis-kvapas.lt", "https://proxy.scrapeops.io/v1/"]
    start_urls = ["https://www.skonis-kvapas.lt/arbata/zalioji-arbata"]

    custom_settings = {
        'FEED_URI': 'All_Tea_Data.json',
        'FEED_FORMAT': 'json',
    }

    def parse(self, response):
        green_teas = response.css("div.products__item")
        green_tea_item = Green_Tea_Item()

        for tea in green_teas:
            green_tea_item["name"] = tea.css("h2::text").get().strip(),
            green_tea_item["price"] = tea.css("ins::text").get(),
            green_tea_item["url"] = tea.css("a.products__item-link").attrib["href"]
            green_tea_item["tea_type"] = "Green Tea"
            yield green_tea_item

        next_page = response.css("a[rel='next']").attrib.get("href")

        if next_page is not None:
            yield scrapy.Request(url=next_page, callback = self.parse)