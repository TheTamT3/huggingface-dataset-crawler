# Data Pipeline Project

## Overview

This project implements a data pipeline for collecting, storing, processing, and uploading data from [Hugging Face's datasets page](https://huggingface.co/datasets) to Agrilla. The pipeline follows these primary steps:
1. Crawl data from Hugging Face using Scrapy.
2. Store the crawled data in a JSON file.
3. Run an ETL process to transform, load, and upload the data.

## Workflow

### Step 1: Run the Crawler

1. The crawler is implemented using Scrapy and is located in `src/services/crawler/crawler/spiders/huggingface_spider.py`.
2. To start crawling, run the crawler module. The crawler collects dataset information from Hugging Face's datasets page.
3. Once the crawl is complete, the output data will be saved in JSON format in the `/assets` directory.

### Step 2: Run ETL Process and Upload Data

The ETL process, defined in `/src/main.py`, performs the following tasks:
1. Reads the JSON file created by the crawler.
2. Transforms the data as needed.
3. Loads and uploads the transformed data to Agrilla.

### Running the Entire Pipeline

To run the entire pipeline (crawling, ETL, and upload), execute the `run_scripts.sh` file.

## Getting Started

### Prerequisites

- Python 3.x
- Scrapy
- Agrilla 


