#!/usr/bin/env bash

files=$(ls /home/dustin/temp/houston.important*.txt)
for tempFile in $files
do
    /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" yanshuochu@qq.com qingqingjiang.huaduo@gmail.com
    /home/dustin/bin/notmuchUpdate.sh
    /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"

    # 艳华自行车 ##############################################################
    if /usr/bin/cat $tempFile | grep -E "(自行|山地)车"; then
        /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" tianyh@pku.edu.cn
        /home/dustin/bin/notmuchUpdate.sh
        /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
    fi

    if /usr/bin/cat $tempFile | grep -E "(渔|鱼)"; then
        /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" tianyh@pku.edu.cn bzhu80928@163.com
        /home/dustin/bin/notmuchUpdate.sh
        /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
    fi

    if /usr/bin/cat $tempFile | grep -E "(幼|婴|儿童|小孩)"; then
        /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" bzhu80928@163.com
        /home/dustin/bin/notmuchUpdate.sh
        /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
    fi
done

rm -rf $files
