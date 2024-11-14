# Data Pipeline Project

## Overview

This project implements a data pipeline for collecting, storing, processing, and uploading data from [Hugging Face's datasets page](https://huggingface.co/datasets) to Agrilla. The pipeline follows these primary steps:
1. Crawl data from Hugging Face using Scrapy.
2. Store the crawled data in a JSON file.
3. Run an ETL process to transform, load, and upload the data.

## Workflow

### Step 1: Run the Crawler
### Step 2: Run ETL Process and Upload Data
1. Reads the JSON file created by the crawler.
2. Transforms the data as needed.
3. Loads and uploads the transformed data to Agrilla.

### Running the Entire Pipeline

To run the entire pipeline (crawling, ETL, and upload), execute the `run.py` file.

## Getting Started

### Prerequisites

- Python 3.x
- Scrapy
- Agrilla 


