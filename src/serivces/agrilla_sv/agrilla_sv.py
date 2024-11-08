import logging
from typing import Any

import argilla as rg
import datasets
from datasets import load_dataset

from src._settings import _settings
from src.serivces.agrilla_sv._mapping import key_mapping_list
from src.utils import logger

logger.configure_logger(level="INFO")

REQUIRED_KEYS = ["instruction", "input", "output"]
client = rg.Argilla(api_url=_settings.AGRILLA_API_URL, api_key=_settings.AGRILLA_API_KEY)


def extract(name: str) -> datasets.Dataset:
    try:
        dataset = load_dataset(name, trust_remote_code=True)
    except Exception as e:
        logging.warning(e)
        return []
    return dataset


def transform(records: datasets.Dataset) -> list[rg.Record]:
    try:
        if isinstance(records, datasets.dataset_dict.DatasetDict):
            if "train" in records:
                records = records["train"]
            else:
                raise KeyError("Not found keyword 'train' in dataset")
        if not isinstance(records, datasets.arrow_dataset.Dataset):
            raise TypeError(f"Only support {datasets.arrow_dataset.Dataset}, got {type(records)}")

        keys = records.features.keys()
        if set(keys) != set(REQUIRED_KEYS):
            for key in keys:
                if key in REQUIRED_KEYS:
                    continue
                new_key = key_mapping_list.get(key.lower(), None)
                if new_key and new_key not in keys:
                    records = records.rename_column(key, new_key)

            result = set(records.features.keys()) - set(keys)
            if len(result) <= 1:
                raise KeyError(f"Not match keys, with {set(keys)}")

            for key in REQUIRED_KEYS:
                if key not in records.features.keys():
                    records = records.add_column(key, [""] * len(records))

        records = [
            rg.Record(
                fields={
                    "instruction": record["instruction"],
                    "input": record["input"],
                    "output": record["output"],
                }
            )
            for record in records
        ]
    except Exception as e:
        logging.error(e)
        return []

    return records


def create(
    workspace: str = "qna", name: str = None, fields: list[rg.Field] = None, questions: list[rg.TextQuestion] = None, **kwargs: dict[str, Any]
) -> rg.Dataset:
    settings = rg.Settings(fields=fields, questions=questions, **kwargs)
    dataset = rg.Dataset(name=name, workspace=workspace, settings=settings, client=client)
    dataset.create()
    return dataset


def load(dataset: rg.Dataset, records: list[rg.Record]) -> None:
    dataset.records.log(records)


def delete(name: str) -> None:
    dataset_to_delete = client.datasets(name=name)
    dataset_to_delete.delete()
    logging.warning(f"Dataset {name} deleted")
