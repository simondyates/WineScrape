import scrapy

class WinedotcomItem(scrapy.Item):
     name = scrapy.Field()
     varietal = scrapy.Field()
     origin = scrapy.Field()
     price = scrapy.Field()
     type = scrapy.Field()
     rating = scrapy.Field()