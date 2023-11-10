import scrapy

class Black_Tea_Spider(scrapy.Spider):
    name = "Black_Tea_Spider"
    allowed_domains = ["www.skonis-kvapas.lt"]
    start_urls = ["https://www.skonis-kvapas.lt/arbata/juodoji-arbata"]

    def parse(self, response):
        blackteas = response.css("div.products__item")

        for tea in blackteas:
            yield{
                "name" : tea.css("h2::text").get().strip(),
                "price" : tea.css("ins::text").get().replace("\xa0€","").replace(",",".").replace("€",""),
                "url" : tea.css("a.products__item-link").attrib["href"]
            }

        next_page = response.css("a[rel='next']").attrib.get("href")

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)