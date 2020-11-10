# coding: utf8
import scrapy
import re
import os
import pickle
import subprocess
from collections import deque
from bbsSpider.items import BbsspiderItem
from bbsSpider import settings
from datetime import datetime


class HoustonbbsSpider(scrapy.Spider):
    name = "houstonbbs"

    def start_requests(self):
        urls = [
            'https://www.houstonbbs.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cacheLocal = settings.HOUSTONBBS_CACHE_LOCAL

        recentActs = response.css("section.home_items")[1]
        eventTexts = recentActs.css("div div a::text").getall()
        eventObjs = recentActs.css("div div").getall()
        hrefs = [re.search("(?<=href=\").+?(?=\")", eventText).group() for eventText in eventObjs]
        dateAftersTS = recentActs.css("div div time::attr(data-time)").getall()
        dateAfters = [ datetime.fromtimestamp(int(dats)).strftime("%m/%d/%Y-%H:%M:%S") for dats in dateAftersTS ]

        try:
            if os.path.getsize(cacheLocal) > 0:
                eventsQueue = pickle.load(open(cacheLocal, 'rb'))
                self.logger.info("eventsQueue read successfully!")
            else:
                eventsQueue = deque(maxlen = 200)
                self.logger.info("eventsQueue is empty!")
        except:
            eventsQueue = deque(maxlen = 200)
            self.logger.info("eventsQueue is error!")

        self.logger.info("eventsQueue size before this run: {}".format(len(eventsQueue)))
        self.logger.info("eventsQueue :")
        self.logger.info(eventsQueue)
        for dateAfter, href, eventText in zip(dateAfters, hrefs, eventTexts):
            urlFull = "https://www.houstonbbs.com{0}".format(href)

            cacheItem = "{0}\n{1}\n{2}\n\n".format(dateAfter, urlFull, eventText)

            self.logger.info("urlFull: {}".format(urlFull))
            self.logger.info("cacheItem: {}".format(cacheItem))

            if cacheItem not in eventsQueue:
                yield scrapy.Request(url=urlFull, meta={"dateAfter": dateAfter, "urlFull": urlFull, "eventText": eventText}, callback=self.detail_parse)
                eventsQueue.append(cacheItem)
        self.logger.info("eventsQueue size after this run: {}".format(len(eventsQueue)))
        self.logger.info("eventsQueue :")
        self.logger.info(eventsQueue)
        pickle.dump(eventsQueue, open(cacheLocal, 'wb'),  pickle.HIGHEST_PROTOCOL)

    def detail_parse(self, response):
        categoryList = response.css("header.content_header nav.breadcrumb a::text").getall()

        newsItem = BbsspiderItem()
        newsItem['date'] = response.meta["dateAfter"]
        newsItem['url'] = response.meta["urlFull"]
        newsItem['title'] = response.meta["eventText"]

        self.logger.info("newsItem:")
        self.logger.info(newsItem)


        articleUserNames = response.css("article header a::text").getall()
        articleUserCities = response.css("article header span.city::text").getall()

        articleUserResponseTimeTS = response.css("article header time::attr(data-time)").getall()
        articleUserResponseTime = [ datetime.fromtimestamp(int(dats)).strftime("%m/%d/%Y-%H:%M:%S") for dats in articleUserResponseTimeTS ]

        articleUserContent = []
        allArticleContent = response.css("article.message_list section div.article_content")
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
