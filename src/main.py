import logging

import argilla as rg

from src import _config
from src.serivces.agrilla_sv import agrilla_sv
from src.utils import helpers, logger

logger.configure_logger(level="INFO")


def main(path: str = None) -> None:
    documents = helpers.read_json(path)

    logging.info("Start processing documents...")
    for idx, document in enumerate(documents["documents"]):
        dataset_name = document["data"]["dataset_name"]
        logging.warning(f"\n\n{idx}. Processing Document: {dataset_name}")

        records = agrilla_sv.extract(dataset_name)
        records = agrilla_sv.transform(records)

        if not records:
            logging.warning("Failed to transform documents")
            continue

        fields = [
            rg.TextField(name="instruction"),
            rg.TextField(name="input"),
            rg.TextField(name="output"),
        ]
        questions = [
            rg.LabelQuestion(name="label", labels=["YES", "NO"], title="Is the sample correct?"),
            rg.TextQuestion(name="new_instruction", required=False),
            rg.TextQuestion(name="new_input", required=False),
            rg.TextQuestion(name="new_output", required=False),
        ]

        try:
            dataset_name = dataset_name.replace("/", "_")
            created_dataset = agrilla_sv.create(name=dataset_name, fields=fields, questions=questions)
            agrilla_sv.load(created_dataset, records=records[:10])
        except Exception as e:
            logging.error(e)
            continue

        logging.warning("Successfully create dataset")


if __name__ == "__main__":
    main(path=_config.PATH)
