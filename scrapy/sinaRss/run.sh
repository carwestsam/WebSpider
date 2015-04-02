#!/bin/bash

while true; do
    scrapy crawl sina2
    scrapy crawl renmin
    scrapy crawl xinhua2
    sleep 10m
done

