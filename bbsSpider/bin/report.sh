#!/usr/bin/env bash

cat /home/dustin/temp/houstonbbsNews.txt | /usr/bin/neomutt -s "houstonbbs news $(/usr/bin/date +'%X')" hopejqq@163.com yanshuochu@qq.com

/home/dustin/bin/notmuchUpdate.sh
