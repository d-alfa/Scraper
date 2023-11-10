import scrapy

class BlackteaspiderSpider(scrapy.Spider):
    name = "blackteaspider"
    allowed_domains = ["www.skonis-kvapas.lt"]
    start_urls = ["https://www.skonis-kvapas.lt/arbata/juodoji-arbata"]

    def parse(self, response):
        blackteas = response.css("div.products__item")

        for tea in blackteas:
            yield{
                "name" : tea.css("h2::text").get().strip(),
                "price" : tea.css("ins::text").replace("\xa0€","").replace(",",".").replace("€",""),
                "url" : tea.css("a.products__item-link").attrib["href"]
            }