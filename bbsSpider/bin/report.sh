#!/usr/bin/env bash

cat /home/dustin/temp/houston.plain.txt | /usr/bin/neomutt -s "houstonbbs news $(/usr/bin/date +'%X')" yanshuochu@qq.com

/home/dustin/bin/notmuchUpdate.sh

/usr/bin/notify-send "Houston BBS" "$(/usr/bin/cat /home/dustin/temp/houston.plain.txt)"
