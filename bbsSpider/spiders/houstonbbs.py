# coding: utf8
import scrapy
import re
import os
import pickle
import subprocess
from collections import deque


class HoustonbbsSpider(scrapy.Spider):
    name = "houstonbbs"

    def start_requests(self):
        urls = [
            'https://www.houstonbbs.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        recentActs = response.css("section.items ul.even_odd_parent")[1]
        eventTexts = recentActs.css("ul li a::text").getall()
        eventObjs = recentActs.css("ul li").getall()
        hrefs = [re.search("(?<=href=\").+?(?=\")", eventText).group() for eventText in eventObjs]
        dataAfters = [re.search("(?<=data-after=\").+?(?=\")", eventText).group() for eventText in eventObjs]


        target = "/home/dustin/temp/houstonbbs.cache.pkl"

        try:
            if os.path.getsize(target) > 0:
                oldsQueue = pickle.load(open(target, 'rb'))
            else:
                oldsQueue = deque(maxlen = 20)
        except:
            oldsQueue = deque(maxlen = 20)

        eventsQueue = deque(maxlen = 20)

        allEventTexts = "\t".join(eventTexts)
        if "租" in allEventTexts or "售" in allEventTexts:
            for dataAfter, href, eventText in zip(dataAfters, hrefs, eventTexts):
                if "租" in eventText or "售" in eventText:
                    eventsQueue.append("{0}\thttps://www.houstonbbs.com{1}\t{2}\n".format(
                        dataAfter, href, eventText))

        pickle.dump(eventsQueue, open("/home/dustin/temp/houstonbbs.cache.pkl", 'wb'))

        newsSet = set(eventsQueue).difference(set(oldsQueue))
        if len(newsSet) > 0:
            with open("/home/dustin/temp/houstonbbsNews.txt", 'w') as outputFile:
                for news in newsSet:
                    outputFile.write(news)
            subprocess.call(['/home/dustin/data/github/bbsSpider/bbsSpider/bin/report.sh'])
