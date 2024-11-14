import logging

import scrapy.spiders
from scrapy.crawler import CrawlerProcess

from src import _config
from src.serivces.agrilla_sv import agrilla_sv
from src.serivces.crawler.crawler.spiders.huggingface_spider import HuggingfaceSpider
from src.utils import helpers, logger

logger.configure_logger(level="INFO")


def run_crawler(spider: type[scrapy.Spider]) -> None:
    process = CrawlerProcess({})
    process.crawl(spider)
    process.start()


def main(path: str = None) -> None:
    # 1. crawl and extract data
    run_crawler(HuggingfaceSpider)

    # 2. read data from crawled output
    outputs = helpers.read_json(path)
    documents = outputs["documents"]
    del outputs

    # 3. transform and load dataset to agrilla
    for _, document in enumerate(documents):
        dataset_name = document["data"]["dataset_name"]
        records = agrilla_sv.get_dataset(dataset_name)
        if records:
            try:
                records = agrilla_sv.transform(records)
                agrilla_sv.load(name=dataset_name.replace("/", "_"), records=records)
                logging.warning("Successfully create dataset")
            except Exception as e:
                logging.error(e)


if __name__ == "__main__":
    main(path=_config.PATH)
