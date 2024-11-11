import logging
from typing import Any, Optional

import argilla as rg
import datasets
from datasets import load_dataset

from src._settings import _settings
from ._mapping import key_mapping_list
from src.utils import logger

logger.configure_logger(level="INFO")

REQUIRED_COLS = {"instruction", "input", "response"}
client = rg.Argilla(api_url=_settings.AGRILLA_API_URL, api_key=_settings.AGRILLA_API_KEY)


def extract(name: str) -> datasets.Dataset | None:
    try:
        dataset = load_dataset(name, trust_remote_code=True)
    except Exception as e:
        logging.warning(e)
        return None
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

        columns = set(records.features)
        if columns != REQUIRED_COLS:
            for column in columns:
                if column not in REQUIRED_COLS:
                    new_column = key_mapping_list.get(column.lower())
                    if new_column and new_column not in columns:
                        records = records.rename_column(column, new_column)

            common_columns = set(records.features) - columns
            if len(common_columns) <= 1:
                raise KeyError(f"The keys in the dataset do not match the required keys, with {columns}")

            for require_col in REQUIRED_COLS:
                if require_col not in records.features:
                    records = records.add_column(require_col, [""] * len(records))

        records = [
            rg.Record(
                fields={
                    "instruction": record["instruction"],
                    "input": record["input"],
                    "response": record["response"],
                }
            )
            for record in records
        ]
    except Exception as e:
        logging.error(e)
        return []

    return records


def create(
    workspace: str = "huggingface", name: str = None, fields: list[rg.Field] = None, questions: list[Optional[rg.TextQuestion|rg.LabelQuestion]] = None, **kwargs: dict[str, Any]
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
