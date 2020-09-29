import scrapy

from scrapy_demo.bmw.bmw.items import BmwItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    rules = (
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.+"),callback="parse_page",follow=True),
    )

    def parse_page(self, response):
        category = response.xpath("//div[@class='uibox']/div/text()").get()
        srcs = response.xpath('//div[contains(@class,"uibox-con")]/ul/li//img/@src').getall()
        srcs = list(map(lambda x:response.urljoin(x.replace("240x180_0_q95_c42_","")),srcs))

        # 得到整个状态列表
        # urls = []
        # for src in srcs:
        #     url = response.urljoin(src)
        #     urls.append(url)
        # srcs = list(map(lambda x:response.urljoin(x),srcs))

        yield BmwItem(category=category,image_urls = srcs)





    # 爬取缩略图用此部分
    def parse(self, response):
        # SelectorList -> list (可进行遍历)
        uiboxs = response.xpath("//div[@class='uibox']")[1:]  # 使用切片操作
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class = 'uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()

            # for url in urls:
            #     url = "https:"+url
            #     print(url)

            #  优化1：自动拼接成完整的URL
            # for url in urls:
            #     url = response.urljoin(url)
            #     print(url)

            # 优化2： 使用map()
            urls = list(map(lambda url:response.urljoin(url),urls))
            item = BmwItem(category  = category , image_urls = urls)
            yield item