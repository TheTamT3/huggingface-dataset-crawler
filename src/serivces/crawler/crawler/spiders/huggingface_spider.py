import json
import logging
import re
import timeit
from datetime import datetime, timedelta
from typing import Any

import scrapy
from scrapy.http import Response

ROOT = "https://huggingface.co"
PAGE = 30


class HuggingfaceSpider(scrapy.Spider):
    name = "hug"
    custom_settings = {"LOG_LEVEL": "WARNING"}
    start_urls = [ROOT + f"/datasets?p={i}&sort=modified&language=language:vi" for i in range(PAGE)]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.documents = []
        self.start_time = timeit.default_timer()

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.log(f"Processing PAGE: {response.url}", level=logging.WARNING)

        articles = response.css("article.overview-card-wrapper.group\\/repo")
        for article in articles:
            link = article.css("a::attr(href)").get()
            update_time = article.css("time::attr(datetime)").get()
            if self._is_valid_dataset_by_time(update_time):
                yield response.follow(ROOT + link, callback=self.process, cb_kwargs={"update_time": update_time.strip()})

    def process(self, response: Response, **kwargs: Any) -> Any:
        data, metadata = {}, {}

        dataset_name = response.url.split("datasets/")[-1]
        data["url"] = response.url
        data["dataset_name"] = dataset_name

        update_time = kwargs.get("update_time", "Unknown")
        metadata["update_time"] = update_time

        tags = response.css("div.mr-1.flex.flex-wrap.items-center")
        for tag in tags:
            attr = tag.css("span.mb-1.mr-1.p-1.text-sm ::text").get().replace(":", "").strip().lower()
            values = tag.css("div.tag.tag-white span::text").getall()
            metadata[attr] = values
            for value in values:
                pattern = r"Image|Audio|Video|Tabular|Geospatial|Speech|Visual"
                if re.search(pattern, value, re.IGNORECASE):
                    return

        self.documents.append({"data": data, "metadata": metadata})

    def close(self, data=None):
        data = {"documents": self.documents}
        self.save_to_json(data)
        self._cal_duration()

    def _cal_duration(self) -> None:
        run_time = timeit.default_timer() - self.start_time
        self.log(f"Spider run time: {run_time:.2f} seconds", level=logging.WARNING)

    def save_to_json(self, data, filename="assets/output.json") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.log("Saved documents", level=logging.WARNING)
        self.log(f"Number of documents: {len(self.documents)}")

    @staticmethod
    def _is_valid_dataset_by_time(article_time: str, weeks: int = 2) -> bool:
        article_date = datetime.fromisoformat(article_time)
        return datetime.now() - timedelta(weeks=weeks) <= article_date <= datetime.now()
