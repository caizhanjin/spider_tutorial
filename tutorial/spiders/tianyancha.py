# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['www.tianyancha.com']
    base_url = 'https://www.tianyancha.com/search?key='
    start_urls = ['https://www.tianyancha.com/search?key=%E6%B7%B1%E5%9C%B3%E6%B0%94%E7%AB%8B%E5%8F%AF%E6%B0%94%E5%8A%A8%E8%AE%BE%E5%A4%87%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        df = pd.read_excel("E:\\code_storages\\tutorial\\tutorial\\data\\company_data.xls")
        self.company_dict = {}
        for item in zip(df["id"], df["name"]):
            # self.start_urls.append(self.base_url + item[1])
            self.company_dict[item[1]] = item[0]

    def parse(self, response):
        # scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")

        pass
