#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

while true; do
    cd $DIR/daily/
    scrapy crawl baidu
    cd $DIR/parsePage
    python process.py
    cd $DIR/filter
    python filter.py
    sleep 10m
done

