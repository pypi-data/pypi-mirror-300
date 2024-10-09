import os

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
from inspect_ai import Task, task

from persona_bench.tooling.scorer import model_critique
from persona_bench.tooling.solver import (
    generate_and_validate,
    modes,
    prompt_template_from_metadata,
)
from persona_bench.tooling.utils import create_sample, load_intersections


@task
def persona_bench_intersectionality():
    # get the mode
    mode = os.getenv("GENERATE_MODE")

    # intersections is the INTERSECTION_JSON environment variable
    intersections = load_intersections(os.getenv("INTERSECTION_JSON"))

    # load our filtered prism dataset
    prism_dataset = load_dataset("SynthLabsAI/PRISM-Filter")

    # load our personas dataset. TODO make public
    splits = {
        "train": "data/train-00000-of-00001.parquet",
        "test": "data/test-00000-of-00001.parquet",
    }
    df = pd.read_parquet(
        "hf://datasets/SynthLabsAI/Synthetic-Personas/" + splits["train"]
    )

    # in Sample, input is "question" from prism_dataset and metadata is an entire row (expressed as a json string) from personas_dataset

    def create_intersectional_sample(prism_row, personas_row):
        """
        Takes a row from prism, which denotes a question, and a row from personas, which denotes a demographic
        Takes the persona and permutes over the attributes constructing a number of question LOO papers
        """
        persona = personas_row[1]

        applicable_intersections = []
        applicable_intersections_idx = []
        for idx, intersection in enumerate(intersections):
            contained = True
            for category in intersection.attributes:
                if persona[category.attribute] not in category.values:
                    contained = False
                    break

            if contained:
                applicable_intersections_idx.append(idx)
                applicable_intersections.append(str(intersection.model_dump()))

        if not applicable_intersections:
            return None

        return create_sample(
            prism_row,
            personas_row,
            extra_metadata={
                "applicable_intersections_idx": applicable_intersections,
                "applicable_intersections": applicable_intersections,
            },
        )

    dataset = [
        create_intersectional_sample(prism_row, persona)
        for prism_row, persona in zip(prism_dataset["train"], df.iterrows())
    ]

    # remove empty samples
    dataset = [d for d in dataset if d]

    return Task(
        dataset=dataset,
        plan=[
            prompt_template_from_metadata(
                modes[mode]["system_prompt"], modes[mode]["format"]
            ),
            generate_and_validate(),
        ],  # TODO better plan
        scorer=model_critique(),
    )
