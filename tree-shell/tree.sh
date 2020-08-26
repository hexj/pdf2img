#!/bin/bash
function listFiles()
{
        #1st param, the dir name
        #2nd param, the aligning space
        for file in `ls $1`;
        do
                echo "$2├── $file"
                if [ -d "$1/$file" ]; then
                    listFiles "$1/$file" "│   $2"
                fi
        done
}
echo $1
listFiles $1 ""
