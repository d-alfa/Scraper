import scrapy

class BlackteaspiderSpider(scrapy.Spider):
    name = "blackteaspider"
    allowed_domains = ["www.skonis-kvapas.lt"]
    start_urls = ["https://www.skonis-kvapas.lt/arbata/juodoji-arbata"]

    def parse(self, response):
        pass