#!/bin/bash

while true; do
    scrapy crawl sina
    scrapy crawl renmin
    scrapy crawl xinhua
    sleep 10m
done

