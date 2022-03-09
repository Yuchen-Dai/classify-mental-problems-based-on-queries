import scrapy
from scrapy.spiders import CrawlSpider
from data_scraping.items import DataScrapingItem


class CounselChatSpider(scrapy.Spider):
    name = 'counselchat'
    allowed_domains = ['counselchat.com']
    start_urls = ['https://counselchat.com/topics/depression']
    base_url = 'https://counselchat.com'

    def parse(self, response):
        label = response.url.split('/')[-1].split('?')[0]
        for i in response.css('.question-title'):
            item = DataScrapingItem()
            item['label'] = label
            item['text'] = i.css('::text').extract()
            yield item

        for item in response.css('.pagination li a'):
            yield scrapy.Request(self.base_url + item.css('::attr(href)').extract()[0], self.parse)

        for item in response.css('.list-topics li a'):
            yield scrapy.Request(self.base_url + item.css('::attr(href)').extract()[0], self.parse)


