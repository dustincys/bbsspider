# coding: utf8
import scrapy
import re
import os
import pickle
import subprocess
from collections import deque
from bbsSpider.items import BbsspiderItem


class HoustonbbsSpider(scrapy.Spider):
    name = "houstonbbs"

    def start_requests(self):
        urls = [
            'https://www.houstonbbs.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cacheLocal = "/home/dustin/temp/houstonbbs.cache.pkl"
        newsout = "/home/dustin/temp/houstonbbsNews.txt"

        recentActs = response.css("section.items ul.even_odd_parent")[1]
        eventTexts = recentActs.css("ul li a::text").getall()
        eventObjs = recentActs.css("ul li").getall()
        hrefs = [re.search("(?<=href=\").+?(?=\")", eventText).group() for eventText in eventObjs]
        dataAfters = [re.search("(?<=data-after=\").+?(?=\")", eventText).group() for eventText in eventObjs]

        try:
            if os.path.getsize(cacheLocal) > 0:
                oldsQueue = pickle.load(open(cacheLocal, 'rb'))
            else:
                oldsQueue = deque(maxlen = 20)
        except:
            oldsQueue = deque(maxlen = 20)

        eventsQueue = deque(maxlen = 20)
        for dataAfter, href, eventText in zip(dataAfters, hrefs, eventTexts):
            urlFull = "https://www.houstonbbs.com{0}".format(href)

            cacheItem = "{0}\n{1}\n{2}\n\n".format(dataAfter, urlFull, eventText)
            if cacheItem not in oldsQueue:
                yield scrapy.Request(url=urlFull, meta={"dataAfter": dataAfter, "urlFull": urlFull, "eventText": eventText}, callback=self.detail_parse)

            eventsQueue.append(cacheItem)
        pickle.dump(eventsQueue, open(cacheLocal, 'wb'))

    def detail_parse(self, response):
        categoryList = response.css("header.content_header nav.breadcrumb a::text").getall()
        if "生活资讯" in categoryList or "跳蚤" in categoryList:
            newsItem = BbsspiderItem()
            newsItem['date'] = response.meta["dataAfter"]
            newsItem['url'] = response.meta["urlFull"]
            newsItem['title'] = response.meta["eventText"]


            articleUserNames = response.css("article header a::text").getall()
            articleUserCities = response.css("article header span.city::text").getall()
            articleUserResponseTime = response.css("article header span.time::text").getall()

            articleUserContent = []
            allArticleContent = response.css("div.forum_post article div.article_content")
            for artC in allArticleContent:
                tempac = artC.css("div.article_content::text").getall()
                tempac = [item.strip() for item in tempac]
                tempac = re.sub('\n+', '\n', "\n".join(tempac)).strip("\n")
                articleUserContent.append(tempac)

            content = ""
            for un, uc, ur, auc in zip(articleUserNames,
                                       articleUserCities,
                                       articleUserResponseTime,
                                       articleUserContent):
                content = "{0}\n__________________\n{1}  \t{2}  \t{3}\n\n{4}\n\n".format(content, un, uc, ur, auc)

            newsItem['content'] = content

            yield newsItem
