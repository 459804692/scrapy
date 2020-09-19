import scrapy

from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

# 继承scrapy.Spider类
from scrapy_demo.qsbk.qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    # allowed_domains 指定域名，可以限制爬虫的范围
    allowed_domains = ['qiushibaike.com']
    # start_urls 开始链接 一般一个即可
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        # SelectorList
        duanzidivs = response.xpath("//div[@class = 'col1 old-style-col1']/div")
        for duanzidiv in duanzidivs:
            # Selector
            author = duanzidiv.xpath(".//h2//text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author, content=content)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)
