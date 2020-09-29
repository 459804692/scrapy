# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from urllib import request

from scrapy.pipelines.images import ImagesPipeline

from scrapy_demo.bmw.bmw import settings


class BmwPipeline:
    def __init__(self):
        # 获取并创建当前目录,没有自行创建
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

        if not os.path.exists(self.path):
            os.mkdir(self.path)


    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']

        category_path = os.path.join(self.path,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name = url.split('_')[-1]
            request.urlretrieve(url,os.path.join(category_path,image_name))
        return item


# 重写一个新类，使其能够分类下载
class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用
        # 其实这个方法本身就是去发送下载请求的
        request_objs = super(BMWImagesPipeline, self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super(BMWImagesPipeline, self).file_path(request,response,info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        images_name = path.replace("full/","")
        images_path = os.path.join(category_path,images_name)
        return images_path

