#!/usr/bin/env bash

cat /home/dustin/temp/houston.important.txt | /usr/bin/neomutt -s "Important! houstonbbs news $(/usr/bin/date +'%X')" hopejqq@163.com yanshuochu@qq.com qingqingjiang.huaduo@gmail.com

/home/dustin/bin/notmuchUpdate.sh

/usr/bin/notify-send "Important! Houston BBS" "$(/usr/bin/cat /home/dustin/temp/houston.important.txt)"

