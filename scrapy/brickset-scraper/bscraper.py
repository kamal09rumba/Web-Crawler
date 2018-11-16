# https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
# Scrapy grabs data based on selector.
# Scrapy supports either css selector or xpath selectors
import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://brickset.com/sets/year-2019']

    def parse(self,response):
        SET_SELECTOR = '.set'

        for brikset in response.css(SET_SELECTOR):
            name_selector = 'h1 ::text'
            pieces_selector = './/dl[dt/text()="Pieces"]/dd/a/text()'
            minifigs_selector ='.//dl[dt/text()="Minifigs"]/dd[2]/a/text()'
            availability_selector = './/dl/dt[normalize-space(text())="Availability"]/following-sibling::dd[1]/text()'
            img_selector = 'img ::attr(src)'
            yield {
                'name': brikset.css(name_selector).extract_first(),
                'pieces' : brikset.xpath(pieces_selector).extract_first(),
                'minifigs' : brikset.xpath(minifigs_selector).extract_first(),
                'availability' : brikset.xpath(availability_selector).extract_first(),
                'img' : brikset.css(img_selector).extract_first()

            }
        ## Check if next page exist or not , if next page exist scrape all the datas

        next_page_selector = '.next a ::attr(href)'
        next_page = response.css(next_page_selector).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )