import os

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
from inspect_ai import Task, task

from persona_bench.tooling.scorer import model_critique_pass_at_k
from persona_bench.tooling.solver import (
    generate_and_validate_pass_at_k,
    modes,
    prompt_template_from_metadata,
)
from persona_bench.tooling.utils import create_sample


@task
def persona_bench_pass_at_k():
    # get the mode
    mode = os.getenv("GENERATE_MODE")

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

    # create samples from prism_dataset['train']

    dataset = [
        create_sample(prism_row, persona)
        for prism_row, persona in zip(prism_dataset["train"], df.iterrows())
    ]

    # system_prompt = system_prompt.format(demographic=str(row_dict)) + format

    # take the first five of the dataset
    dataset = dataset[:300]

    return Task(
        dataset=dataset,
        plan=[
            prompt_template_from_metadata(
                modes[mode]["system_prompt"], modes[mode]["format"]
            ),
            generate_and_validate_pass_at_k(k=16),
        ],
        scorer=model_critique_pass_at_k(),
    )
