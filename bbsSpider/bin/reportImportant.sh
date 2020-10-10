#!/usr/bin/env bash

files=$(ls /home/dustin/temp/houston.important*.txt)
for tempFile in $files
do
    /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" yanshuochu@qq.com qingqingjiang.huaduo@gmail.com
    /home/dustin/bin/notmuchUpdate.sh
    /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
done

rm -rf $files
