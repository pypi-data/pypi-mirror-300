import asyncio
import os
from typing import Literal

from inspect_ai._eval.eval import eval_async
from inspect_ai.log import EvalLog

from persona_bench.main_evaluation import persona_bench_main as eval_main
from persona_bench.main_intersectionality import (
    persona_bench_intersectionality as eval_intersectionality,
)
from persona_bench.main_loo import persona_bench_loo as eval_loo
from persona_bench.main_pass_at_k import persona_bench_pass_at_k as eval_pass_at_k

_env = os.getenv


async def async_evaluate_model(
    model_str: str,
    evaluation_type: Literal["main", "loo", "intersectionality", "pass_at_k"] = "main",
    log_dir: str = "/tmp/",
    seed: int = None,
    N: int = None,
    OPENAI_API_KEY: str | None = None,
    GENERATE_MODE: (
        Literal["baseline", "output_only", "chain_of_thought", "demographic_summary"]
        | None
    ) = None,
    INTERSECTION_JSON: str | None = None,
    LOO_JSON: str | None = None,
    INSPECT_EVAL_MODEL: str = _env("INSPECT_EVAL_MODEL"),
) -> asyncio.Future:
    """
    Async. runs persona bench over the model specified by model_str

    Args:
        model_str: The model to evaluate
        evaluation_type: The evaluation type to run. Defaults to "main".
        log_dir: The directory to store the logs. Defaults to "/tmp/".
        seed: The seed to use for the evaluation. Defaults to None.
        N: The number of samples to use for the evaluation. Defaults to None (all samples).
        OPENAI_API_KEY: The openai used for rewriting the model output to be pydantic compliant.
            Defaults to env("OPENAI_API_KEY").
        GENERATE_MODE: The mode to use for generating the prompts. Defaults to env("GENERATE_MODE").
        INTERSECTION_JSON: The intersectionality json file. Defaults to env("INTERSECTION_JSON").
            See the readme on how to set this file up.
        LOO_JSON: The leave one out json file. Defaults to env("LOO_JSON"). See the readme on how to set this file up.
        INSPECT_EVAL_MODEL: The model to use for inspecting the evaluation. Defaults to env("INSPECT_EVAL_MODEL").
    Returns:
        asyncio.Future: The future object that will contain the result of the evaluation

    Usage:
        >>> from persona_bench import async_evaluate_model
        >>> from pprint import pprint
        >>> future = async_evaluate_model("gpt-3.5-turbo", evaluation_type="main")
        >>> eval = await future
        >>> pprint(eval[0].results.model_dump())
    """
    OPENAI_API_KEY = OPENAI_API_KEY or _env("OPENAI_API_KEY")
    GENERATE_MODE = GENERATE_MODE or _env("GENERATE_MODE")
    INSPECT_EVAL_MODEL = INSPECT_EVAL_MODEL or _env("INSPECT_EVAL_MODEL")
    LOO_JSON = LOO_JSON or _env("LOO_JSON")
    INTERSECTION_JSON = INTERSECTION_JSON or _env("INTERSECTION_JSON")

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    if not GENERATE_MODE:
        raise ValueError("GENERATE_MODE is not set")

    if not INSPECT_EVAL_MODEL:
        raise ValueError("INSPECT_EVAL_MODEL is not set")

    eval_fn = None

    if evaluation_type == "main":
        print("Running main evaluation")
        eval_fn = eval_main
    elif evaluation_type == "loo":
        eval_fn = eval_loo

        if not LOO_JSON:
            raise ValueError("LOO_JSON is not set")

    elif evaluation_type == "intersectionality":
        eval_fn = eval_intersectionality
        if not INTERSECTION_JSON:
            raise ValueError("INTERSECTION_JSON is not set")

    elif evaluation_type == "pass_at_k":
        print("Running pass at k")
        eval_fn = eval_pass_at_k
    else:
        raise ValueError(f"Invalid evaluation type: {evaluation_type}")

    # set all the environment variables
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["GENERATE_MODE"] = GENERATE_MODE
    os.environ["INTERSECTION_JSON"] = INTERSECTION_JSON
    os.environ["LOO_JSON"] = LOO_JSON
    os.environ["INSPECT_EVAL_MODEL"] = INSPECT_EVAL_MODEL

    return await eval_async(eval_fn, model_str, log_dir=log_dir, seed=seed, limit=N)


def evaluate_model(
    model_str: str,
    evaluation_type: Literal["main", "loo", "intersectionality", "pass_at_k"] = "main",
    log_dir: str = "/tmp/",
    seed: int = None,
    N: int = None,
    OPENAI_API_KEY: str = _env("OPENAI_API_KEY"),
    GENERATE_MODE: Literal[
        "baseline", "output_only", "chain_of_thought", "demographic_summary"
    ] = _env("GENERATE_MODE"),
    INTERSECTION_JSON: str = _env("INTERSECTION_JSON"),
    LOO_JSON: str = _env("LOO_JSON"),
    INSPECT_EVAL_MODEL: str = _env("INSPECT_EVAL_MODEL"),
) -> EvalLog:
    """
    Runs persona bench over the model specified by model_str

    Args:
        model_str: The model to evaluate
        evaluation_type: The evaluation type to run. Defaults to "main".
        log_dir: The directory to store the logs. Defaults to "/tmp/".
        seed: The seed to use for the evaluation. Defaults to None.
        N: The number of samples to use for the evaluation. Defaults to None (all samples).
        OPENAI_API_KEY: The openai used for rewriting the model output to be pydantic compliant.
            Defaults to env("OPENAI_API_KEY").
        GENERATE_MODE: The mode to use for generating the prompts. Defaults to env("GENERATE_MODE").
        INTERSECTION_JSON: The intersectionality json file. Defaults to env("INTERSECTION_JSON").
            See the readme on how to set this file up.
        LOO_JSON: The leave one out json file. Defaults to env("LOO_JSON"). See the readme on how to set this file up.
        INSPECT_EVAL_MODEL: The model to use for inspecting the evaluation. Defaults to env("INSPECT_EVAL_MODEL").

    Returns:
        list[EvalLog]: The result of the evaluation.

    Example:
        >>> from persona_bench import evaluate_model
        >>> from pprint import pprint
        >>> eval = evaluate_model("gpt-3.5-turbo", evaluation_type="main")
        >>> print(eval.results.model_dump())
    """
    return asyncio.run(
        async_evaluate_model(
            model_str,
            evaluation_type,
            log_dir,
            seed,
            N,
            OPENAI_API_KEY,
            GENERATE_MODE,
            INTERSECTION_JSON,
            LOO_JSON,
            INSPECT_EVAL_MODEL,
        )
    )[0]
