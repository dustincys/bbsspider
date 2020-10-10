#!/usr/bin/env bash

cd /home/dustin/github/bbsSpider

DXML=/home/dustin/temp/houston.xml
IXML=/home/dustin/temp/houston.important.xml
DTEXT=/home/dustin/temp/houston.plain.txt
ITEXT=/home/dustin/temp/houston.important

/usr/bin/rm -f $DXML
/usr/bin/rm -f $IXML
/usr/bin/rm -f $DTEXT
/usr/bin/rm -f ${ITEXT}*

# /usr/bin/scrapy crawl houstonbbs -o /home/dustin/temp/houston.xml -t xml 2>&1 >/dev/null
/usr/bin/scrapy crawl houstonbbs 2>&1 >/dev/null

if [ -f ${DXML} ] && [ $(/usr/bin/cat ${DXML} | /usr/bin/wc -l) -gt 1 ] ; then
    /usr/bin/python2.7 /home/dustin/github/bbsSpider/bbsSpider/bin/xmlparse.py -i ${DXML} -o ${DTEXT}
    /home/dustin/github/bbsSpider/bbsSpider/bin/report.sh
fi

if [ -f ${IXML} ] && [ $(/usr/bin/cat ${IXML} | /usr/bin/wc -l) -gt 1 ] ; then
    /usr/bin/python2.7 /home/dustin/github/bbsSpider/bbsSpider/bin/xmlparseImportant.py -i ${IXML} -op ${ITEXT}
    /home/dustin/github/bbsSpider/bbsSpider/bin/reportImportant.sh
fi
