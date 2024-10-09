import asyncio
import json
import random
from collections import defaultdict

import datasets
import instructor
import pandas as pd
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from tqdm.asyncio import tqdm

client = instructor.from_openai(AsyncOpenAI())

arr1 = [
    "data/example_logs/cot_logs/gpt-3.5_cot.json",
    "data/example_logs/cot_logs/gpt-4_cot.json",
    "data/example_logs/cot_logs/gpt-4o_cot.json",
    "data/example_logs/cot_logs/llama-370b_cot.json",
]

arr2 = [
    "data/example_logs/direct_logs/gpt-3.5_direct.json",
    "data/example_logs/direct_logs/gpt-4_direct.json",
    "data/example_logs/direct_logs/gpt-4o_direct.json",
    "data/example_logs/direct_logs/llama-370b_direct.json",
]


# cot
data1 = []
for file in arr1:
    with open(file) as f:
        data1.append(json.load(f))


# direct
data2 = []
for file in arr1:
    with open(file) as f:
        data2.append(json.load(f))


def get_attrs(input_files, data):
    # there are two variables we want to compare
    samples = list(map(lambda x: x["samples"], data))
    attrs = defaultdict(list)

    for file_name, sample in zip(input_files, samples):
        for s in sample:
            question = s["messages"][1]["content"]
            original_persona = s["metadata"]["persona"]
            answer = s["metadata"]["pydantic_output"]["answer_to_question"]

            attrs[file_name].append(
                {
                    "question": question,
                    "answer": answer,
                    "original_persona": original_persona,
                }
            )

    return attrs


class SubtleObject(BaseModel):
    chain_of_thought: str = Field(
        ..., description="The chain of thought used to arrive at the answer"
    )
    is_it_subtle: bool = Field(
        ..., description="Is the question subtly personalized for the given persona?"
    )


async def get_subtle(question, answer, original_persona):
    """
    Determine, with respect to a particular question, if two personas are mostly equivalent. Highlight the differences.
    """
    return await client.chat.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "There is a system that generates an answer that is personalized for a specific persona.\
                    Your job is to determine if the answer is either *subtly* personalized for the persona or too on the nose. You are an expert at this task.",
            },
            {
                "role": "user",
                "content": f"Question: {question}\nAnswer: {answer}\nPersona: {original_persona}",
            },
        ],
        response_model=SubtleObject,
    )


# async map over the entire dataset, per model

with_cot_subtle_dict = defaultdict(list)
without_cot_subtle_dict = defaultdict(list)


async def main(save_every=100):
    sem = asyncio.Semaphore(30)
    steps = 0

    attrs1 = get_attrs(arr1, data1)
    attrs2 = get_attrs(arr2, data2)

    with_cot_count = 0
    without_cot_count = 0

    for file_name, sample in tqdm(attrs1.items(), desc="Models"):
        # take a random sample of 50 questions
        sample_new = random.sample(sample, 50)
        for s in tqdm(sample_new, desc="Samples"):
            async with sem:
                subtle = await get_subtle(**s)
            if subtle.is_it_subtle:
                with_cot_count += 1

            with_cot_subtle_dict[file_name].append(subtle.model_dump())
            steps += 1
            if steps % save_every == 0:
                with open("data/with_cot_subtle.json", "w") as f:
                    json.dump(with_cot_subtle_dict, f)

    for file_name, sample in tqdm(attrs2.items(), desc="Models"):
        # take a random sample of 50 questions
        sample_new = random.sample(sample, 50)
        for s in tqdm(sample_new, desc="Samples"):
            async with sem:
                subtle = await get_subtle(**s)

            if subtle.is_it_subtle:
                without_cot_count += 1

            without_cot_subtle_dict[file_name].append(subtle.model_dump())
            steps += 1
            if steps % save_every == 0:
                with open("data/without_cot_subtle.json", "w") as f:
                    json.dump(without_cot_subtle_dict, f)

    print(f"with_cot_count: {with_cot_count}")
    print(f"without_cot_count: {without_cot_count}")

    # print the proportions
    print(f"with_cot_proportion: {with_cot_count / len(attrs1)}")
    print(f"without_cot_proportion: {without_cot_count / len(attrs2)}")


if __name__ == "__main__":
    asyncio.run(main())
