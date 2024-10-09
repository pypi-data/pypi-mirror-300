import os
from typing import Union

import instructor
import pandas as pd
from inspect_ai.model import CachePolicy, ChatMessageSystem, ChatMessageUser, get_model
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.solver._util import append_system_message
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential

from persona_bench.tooling.prompts import (
    format_prompt,
    format_prompt_demo_summary,
    format_prompt_no_cot,
    system_prompt,
    system_prompt_baseline,
    system_prompt_demo_summary,
    system_prompt_no_cot,
)

client = instructor.from_openai(AsyncOpenAI())


class OutputOnly(BaseModel):
    answer_to_question: str = Field(..., description="The answer to the question")


class CoTAndOutput(OutputOnly):
    chain_of_thought: str = Field(
        ..., description="The chain of thought used to arrive at the answer"
    )


class DemographicSummaryAndOutput(OutputOnly):
    demographic_summary: str = Field(..., description="The summary of the demographic")


modes = {
    "baseline": {
        "format": format_prompt_no_cot,
        "response_model": OutputOnly,
        "system_prompt": system_prompt_baseline,
    },
    "output_only": {
        "format": format_prompt_no_cot,
        "response_model": OutputOnly,
        "system_prompt": system_prompt_no_cot,
    },
    "chain_of_thought": {
        "format": format_prompt,
        "response_model": CoTAndOutput,
        "system_prompt": system_prompt,
    },
    "demographic_summary": {
        "format": format_prompt_demo_summary,
        "response_model": DemographicSummaryAndOutput,
        "system_prompt": system_prompt_demo_summary,
    },
}


async def extract_json_object_and_validate(
    llm_response: str, rewrite_model=None
) -> BaseModel:
    mode = os.getenv("GENERATE_MODE")
    # rewrite the json object
    rewrite_response = await client.chat.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"Extract the output from the following {llm_response}.",
            },
        ],
        response_model=modes[mode]["response_model"],
    )

    return rewrite_response


@solver
def generate_and_validate(cache: Union[bool, "CachePolicy"] = False) -> "Solver":
    # get the json rewrite model
    rewrite_model = get_model("openai/gpt-4o")

    # TODO: Generalize to arbitrary pydantic objects
    @retry(
        wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(1)
    )
    async def solve(state: TaskState, generate: Generate):
        try:
            result = await generate(state)
            # extract the json object from the response, and validate it
            pydantic_output = await extract_json_object_and_validate(
                result.output.completion, rewrite_model
            )
            result.output.completion = pydantic_output.answer_to_question
            result.metadata["pydantic_output"] = pydantic_output.model_dump()

            return result
        except Exception as e:
            # Log the error if needed
            print(f"Error during solving: {e}")
            print(result.output.completion)

            return None

    return solve


@solver
def validate_only(cache: Union[bool, "CachePolicy"] = False) -> "Solver":
    # get the json rewrite model
    rewrite_model = get_model("openai/gpt-4o")

    # TODO: Generalize to arbitrary pydantic objects
    @retry(
        wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(1)
    )
    async def solve(state: TaskState, generate: Generate):
        try:
            result = await generate(state)
            # extract the json object from the response, and validate it
            pydantic_output = await extract_json_object_and_validate(
                result.output.completion, rewrite_model
            )
            result.output.completion = pydantic_output.answer_to_question
            result.metadata["pydantic_output"] = pydantic_output.model_dump()

            return result
        except Exception as e:
            # Log the error if needed
            print(f"Error during solving: {e}")
            print(result.output.completion)

            return None

    return solve


@solver
def generate_and_validate_pass_at_k(
    cache: Union[bool, "CachePolicy"] = False, k: int = 1
) -> "Solver":
    # get the json rewrite model
    rewrite_model = get_model("openai/gpt-4o")

    # TODO: Generalize to arbitrary pydantic objects
    @retry(
        wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(100)
    )
    async def generate_single_answer(state: TaskState, generate: Generate):
        try:
            result = await generate(state)
            # extract the json object from the response, and validate it
            pydantic_object = await extract_json_object_and_validate(
                result.output.completion, rewrite_model
            )
            result.output.completion = pydantic_object.answer_to_question
            result.metadata["pydantic_output"] = pydantic_object.model_dump()

            return result

        except (ValidationError, Exception) as e:
            # Log the error if needed
            print(f"Error during solving: {e}")

            return None

    async def solve(state: TaskState, generate: Generate):
        solns = []
        for _ in range(k):
            answer = await generate_single_answer(state, generate)
            if answer:
                solns.append(ChatMessageUser(content=answer.output.completion))

        return TaskState(
            model=state.model,
            sample_id=state.sample_id,
            epoch=state.epoch,
            input=solns,
            messages=state.messages,
            tools=state.tools,
            tool_choice=state.tool_choice,
            output=state.output,
            completed=state.completed,
            metadata=state.metadata,
        )

    return solve


@solver
def prompt_template_from_metadata(template: str, format: str = None) -> Solver:
    """Parameterized prompt template, fills in with metadata from the taskstate.

    Prompt template containing a `{prompt}` placeholder and any
    number of additional `params`.

    Args:
      template (str | list[Message]):
          The conversation template to use. A simple string or
          a list of messages
      format (str):
          Optional format string to append to the template.

    Returns:
      A solver that uses the specified prompt template.
    """
    # determine the prompt template
    prompt_template = template

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        prompt = state.user_prompt

        filtered_metadata = {
            k: v for k, v in state.metadata.items() if not k.startswith("_")
        }
        content = prompt_template.format(prompt=prompt.text, **filtered_metadata)

        # remove "\n\n{prompt}\n" from the end of content
        content = content[: content.rfind("\n\n{prompt}\n")]
        append_system_message(state.messages, ChatMessageSystem(content=content))

        return state

    return solve
