# implements a scorer function using inspect ai's library
import os

import instructor
from inspect_ai.model import Model, get_model
from inspect_ai.scorer import Score, Target, accuracy, bootstrap_std, scorer
from inspect_ai.solver import TaskState
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

from persona_bench.tooling.prompts import (
    critique_template,
    format_critique,
    rewrite_prompt,
)

client = instructor.from_openai(AsyncOpenAI())


class CritiqueValidator(BaseModel):
    chain_of_thought: str = Field(
        ..., description="The chain of thought used to arrive at the answer"
    )
    personalization_critic: str = Field(..., description="The personalization critic")
    helpfulness_critic: str = Field(..., description="The helpfulness critic")
    conclusion: str = Field(..., description="The conclusion")
    needs_revision: bool = Field(..., description="Whether the answer needs revision")


async def extract_json_object_and_validate(
    llm_response: str,
) -> CritiqueValidator | None:
    # create the new prompt
    prompt = rewrite_prompt.format(json_object=llm_response) + format_critique
    # rewrite the json object
    rewrite_response = await client.chat.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting information from outputs and putting it into a json format.",
            },
            {"role": "user", "content": prompt},
        ],
        response_model=CritiqueValidator,
    )

    return rewrite_response


@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(100))
async def generate_and_validate(llm, prompt: str) -> CritiqueValidator:
    result = await llm.generate(prompt)
    return await extract_json_object_and_validate(result.completion)


@scorer(metrics=[accuracy(), bootstrap_std()])
def model_critique(template: str = critique_template, model: str | Model | None = None):
    grader_model = get_model(os.getenv("INSPECT_EVAL_MODEL"))

    async def score(state: TaskState, target: Target) -> Score:
        # format the model grading template
        score_prompt = (
            template.format(
                question=state.input_text,
                answer=state.output.completion,
                demographic=state.metadata["persona"],
            )
            + format_critique
        )

        # query the model for the score
        critique = await generate_and_validate(grader_model, score_prompt)

        if critique:
            return Score(
                value=1.0 if critique.needs_revision == False else 0.0,
                metadata={
                    "critique": critique.model_dump(),
                    "persona": state.metadata["persona"],
                    "_persona_idx": state.metadata["_persona_idx"],
                },
            )

    return score


@scorer(metrics=[accuracy(), bootstrap_std()])
def model_critique_pass_at_k(
    template: str = critique_template, model: str | Model | None = None
):
    grader_model = get_model(os.getenv("INSPECT_EVAL_MODEL"))

    async def score(state: TaskState, target: Target) -> Score:
        # format the model grading template
        critiques = []
        # yes I know you're not supposed to access this, no I do not care.
        for message in state._input:
            score_prompt = (
                template.format(
                    question=message.text,
                    answer=state.output.completion,
                    demographic=state.metadata["persona"],
                )
                + format_critique
            )

            # query the model for the score
            critique = await generate_and_validate(grader_model, score_prompt)
            if critique:
                critiques.append(critique)

        if critiques:
            score = Score(
                value=1.0 if any([not c.needs_revision for c in critiques]) else 0.0,
                metadata={
                    "critique": [critique.model_dump() for critique in critiques],
                    "persona": state.metadata["persona"],
                    "_persona_idx": state.metadata["_persona_idx"],
                },
            )
            return score

    return score
