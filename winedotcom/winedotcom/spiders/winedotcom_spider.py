from scrapy import Spider
from scrapy import Request
from winedotcom.items import WinedotcomItem

class WinedotcomSpider(Spider):
    name = 'winedotcom_spider'
    allowed_domains = ['www.wine.com']
    start_urls = ['https://www.wine.com/list/wine/7155?pricemax=80&ratingmin=94']
    # next is 'https://www.wine.com/list/wine/7155/2?pricemax=80&ratingmin=94'
    # we appear to have 25 results per page

    def parse(self, response):
        # Find the total number of results
        n = int(response.xpath('//span[@class="count"]/text()').extract_first())
        number_pages = n // 25 + 1
        result_urls = ['https://www.wine.com/list/wine/7155/{}?pricemax=80&ratingmin=94'.format(x) for x in range(1, number_pages + 1)]
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        wines = response.xpath('//li[@class="prodItem"]')
        for row in wines:
            ratings = row.xpath('.//li[@class="wineRatings_listItem"]')
            for rating in ratings:
                wine = WinedotcomItem()
                wine['name'] = row.xpath('.//span[@class="prodItemInfo_name"]/text()').extract_first()
                wine['varietal'] = row.xpath('.//span[@class="prodItemInfo_varietal"]/text()').extract_first()
                wine['origin'] = row.xpath('.//span[@class="prodItemInfo_originText"]/text()').extract_first()
                wine['price'] = row.xpath('.//meta[@itemprop="price"]/@content').extract_first()
                wine['type'] = row.xpath('.//ul[@class="prodAttr"]//@title').extract_first()
                wine['rating'] = rating.xpath('./@title').extract_first()
                yield wine
