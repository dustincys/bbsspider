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
        if re.search(u"租|卖|售|出", allEventTexts):
            for dataAfter, href, eventText in zip(dataAfters, hrefs, eventTexts):
                if re.search(u"租|卖|售|出",  eventText):
                    eventsQueue.append("{0}\nhttps://www.houstonbbs.com{1}\n{2}\n\n".format(
                        dataAfter, href, eventText))

        pickle.dump(eventsQueue, open("/home/dustin/temp/houstonbbs.cache.pkl", 'wb'))

        newsSet = set(eventsQueue).difference(set(oldsQueue))
        newsSet = sorted(newsSet, key = lambda item:int(item.split("\n")[1].split("/")[-1]), reverse=True)
        if len(newsSet) > 0:
            with open("/home/dustin/temp/houstonbbsNews.txt", 'w') as outputFile:
                for news in newsSet:
                    outputFile.write(news)
            subprocess.call(['/home/dustin/data/github/bbsSpider/bbsSpider/bin/report.sh'])
