#!/bin/bash

cd ./src/serivces/crawler || exit
scrapy crawl hug

export PYTHONPATH="${PYTHONPATH}:."

cd - > /dev/null
python3 src/main.py
