
from scrapy import cmdline


cmdline.execute("scrapy crawl counselchat -o dataset.csv -t csv".split())
