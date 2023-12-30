# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class Scraper_Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Name/Price --> strip all whitespaces from strings
        field_names = ["name","price"]
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value[0].strip()

        ## Name --> switch to lowercase
        lowercase_key = "name"
        value = adapter.get(lowercase_key)
        adapter[lowercase_key] = value.lower()

        ## Name --> replace unnecessary characters
        name = "name"
        unnecessary_characters = [
            "(stikl.) 40g",
            "(stikl.) 45 g",
            "(stikl.) 50 g",
            ", 50g (stikl.)",
            "sftgfop1 ff, 2022",
            "sftgfop1 ff 2023",
            "sftgfop1 ff",
            "sftgfop1",
            "sftgfop",
            "ftgfop1",
            "ftgfop",
            "ff, 2022",
            "ff 2023",
            ", 70g",
            ", 80 g",
            ", 1 vnt. vokelyje",
            ", 15 vnt.",
            ", 40 vnt.",
            ", 60g (stikl.)",
            ", 40g",
            ", 70g",
            ", 90g",
            "(stikl.) 60 g",
            ", 80g",
            ", 55g",
            ", 100g",
            ", 50g",
            ", 45g",
            ", 30g",
            ", 55 g",
            "(stikl.)"
        ]
        for u in unnecessary_characters:
            value = adapter.get(name)
            adapter[name] = value.replace(u,"").strip()

        ## Price --> convert to float
        price_key = "price"
        value = adapter.get(price_key)
        value = value.replace("\xa0€","").replace(",",".").replace("€","")
        adapter[price_key] = float(value)

        return item