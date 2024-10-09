import asyncio
import json
from collections import defaultdict

import datasets
import instructor
import pandas as pd
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from tqdm.asyncio import tqdm

client = instructor.from_openai(AsyncOpenAI())

input_files = [
    "data/example_logs/gpt-3.5_demographic.json",
    "data/example_logs/gpt-4_demographic.json",
    "data/example_logs/gpt-4o_demographic.json",
    "data/example_logs/llama-370b_demographic.json",
]


# load all of the input files
data = []
for file in input_files:
    with open(file) as f:
        data.append(json.load(f))


# there are two variables we want to compare
samples = list(map(lambda x: x["samples"], data))
attrs = defaultdict(list)

for file_name, sample in zip(input_files, samples):
    for s in sample:
        question = s["messages"][1]["content"]
        original_persona = s["metadata"]["persona"]
        persona_summary = s["metadata"]["pydantic_output"]["demographic_summary"]

        attrs[file_name].append(
            {
                "question": question,
                "original_persona": original_persona,
                "persona_summary": persona_summary,
            }
        )


class DifferenceObject(BaseModel):
    chain_of_thought: str = Field(
        ..., description="The chain of thought used to arrive at the answer"
    )
    difference: str = Field(
        ..., description="The difference between the original persona and the summary"
    )
    are_they_equivalent: bool = Field(
        ..., description="Whether the original persona and the summary are equivalent"
    )


async def get_difference(question, original_persona, persona_summary):
    """
    Determine, with respect to a particular question, if two personas are mostly equivalent. Highlight the differences.
    """
    return await client.chat.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at comparing two personas. Please highlight the differences, with respect to some question.",
            },
            {
                "role": "user",
                "content": f"Question: {question}\nOriginal: {original_persona}\nSummary: {persona_summary}",
            },
        ],
        response_model=DifferenceObject,
    )


# async map over the entire dataset, per model

differences = defaultdict(list)


async def main(save_every=100):
    sem = asyncio.Semaphore(30)
    steps = 0
    for file_name, sample in tqdm(attrs.items(), desc="Models"):
        for s in tqdm(sample, desc="Samples"):
            async with sem:
                diff = await get_difference(**s)
            differences[file_name].append(diff.model_dump())
            steps += 1
            if steps % save_every == 0:
                with open("differences.json", "w") as f:
                    json.dump(differences, f)


# create a pandas dataframe that has the follwoing columns:
# - question
# - original_persona
# - persona_summary
# - chain_of_thought
# - difference
# - are_they_equivalent
# - model


# read differences.json
with open("differences.json") as f:
    differences = json.load(f)


def create_pandas_df_from_differences(d) -> pd.DataFrame:
    """
    Create a pandas dataframe from the differences dictionary
    """

    data = []
    for filepath, diffs in d.items():
        attr = attrs[filepath]
        # get the model name from the file name
        model = filepath.split("/")[-1].split("_")[0]
        for idx, diff in enumerate(diffs):
            data.append(
                {
                    "question": attr[idx]["question"],
                    "original_persona": attr[idx]["original_persona"],
                    "persona_summary": attr[idx]["persona_summary"],
                    "chain_of_thought": diff["chain_of_thought"],
                    "difference": diff["difference"],
                    "are_they_equivalent": diff["are_they_equivalent"],
                    "model": model,
                }
            )

    return pd.DataFrame(data)


# asyncio.run(main())

# save output to csv
df = create_pandas_df_from_differences(differences)
df.to_csv("differences.csv")
