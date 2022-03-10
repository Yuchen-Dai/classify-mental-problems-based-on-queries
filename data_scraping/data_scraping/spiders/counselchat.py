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
            title = i.css('::text').extract()[0]
            if title == '{{question.title}}':
                continue
            yield scrapy.Request(url = self.base_url + i.css('::attr(href)').extract()[0],
                                 meta={'label':label, 'title':title}, dont_filter = True, callback=self.parse_content)

        for item in response.css('.pagination li a'):
            yield scrapy.Request(self.base_url + item.css('::attr(href)').extract()[0], self.parse)

        for item in response.css('.list-topics li a'):
            yield scrapy.Request(self.base_url + item.css('::attr(href)').extract()[0], self.parse)


    def parse_content(self, response):
        item = DataScrapingItem()
        item['label'] = response.meta['label']
        item['title'] = response.meta['title']
        text = ''
        for i in response.css('.page-description p'):
            text += i.css('::text').extract()[0]
        item['text'] = text
        yield item