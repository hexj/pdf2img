#!bin/bash

function handle(){
    # work_path=$(cd "$(dirname "$1")";pwd)
    for file in `ls $1`
    do
        newpath="$1/$file"
        if [ -d $newpath ];then
            if [ "${file##*-}"x = "set"x ];then
                handle "$newpath" $2
            else
                if [ -f "$newpath/.git/config" ];then
                    if [[ -n $(git -C $newpath diff --stat)  ]];then #是否有git 修改 ，or git diff --quiet || echo 'dirty'
                        echo "$newpath,"`git -C $newpath config --get remote.origin.url`",updated" #输出有修改的目录和远程url
                    else
                        echo "$newpath,"`git -C $newpath config --get remote.origin.url`
                    fi
                fi
            fi
        fi
    done
}

handle $1