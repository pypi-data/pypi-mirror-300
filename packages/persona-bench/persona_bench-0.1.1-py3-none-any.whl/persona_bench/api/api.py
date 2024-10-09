import os
from typing import List, Literal

import pandas as pd
import requests as req

from persona_bench.api.interfaces import (
    InteractiveEvaluationRequest,
    Intersection,
    LooAttributes,
    PERSONAQuestionRequest,
)
from persona_bench.api.prompt_constructor import (
    BasePromptConstructor,
    DefaultPromptConstructor,
)
from persona_bench.api.utils import dataframe_to_questions, questions_to_dataframe

_VALID_EVALUATION_TYPES = frozenset(
    {
        "main",
        "loo",
        "intersectionality",
        "pass_at_k",
        "comparison",
    }
)


class PERSONAClient:
    def __init__(
        self,
        model_str: str,
        evaluation_type: Literal["main", "loo", "intersectionality", "pass_at_k"],
        N: int,
        intersection: list[Intersection] | None = None,
        loo_attributes: LooAttributes | None = None,
        seed: int | None = None,
        url: str = "https://synth-api-development.eastus.azurecontainer.io/api/v1/personas/v1/",
        api_key: str | None = None,
        prompt_constructor: BasePromptConstructor | None = DefaultPromptConstructor(),
    ) -> None:
        """
        Args:
            evaluation_type (str): The type of evaluation to perform
            model_str (str): The model to evaluate
            seed (int): Random seed for reproducibility
            N (int): Number of samples to use for evaluation
            intersection (list[Intersection]): Intersection attributes for evaluation
            loo_attributes (LooAttributes): Leave-one-out attributes for evaluation

        """

        if not (N is not None and N > 0):
            raise ValueError("N must be provided and greater than 0")

        if evaluation_type not in _VALID_EVALUATION_TYPES:
            raise ValueError(
                f"evaluation_type must be one of {_VALID_EVALUATION_TYPES}"
            )

        if api_key is None:
            api_key = os.getenv("SYNTH_API_KEY")

        if api_key is None:
            raise ValueError(
                """API key must be provided.
                Either set the SYNTH_API_KEY environment variable
                or pass the API key to the PERSONAClient constructor.
            """
            )

        if evaluation_type == "intersectionality" and intersection is None:
            raise ValueError(
                "Intersection attributes must be provided for intersectionality evaluation"
            )

        if evaluation_type == "loo" and loo_attributes is None:
            raise ValueError(
                "Leave-one-out attributes must be provided for loo evaluation"
            )

        self.evaluation_type = evaluation_type
        self.model_str = model_str
        self.seed = seed
        self.N = N
        self.intersection = intersection
        self.loo_attributes = loo_attributes
        self.url = url
        self.api_key = api_key

        req_obj = PERSONAQuestionRequest(
            model_str=model_str,
            evaluation_type=evaluation_type,
            seed=seed,
            N=N,
            intersection=intersection,
            loo_attributes=loo_attributes,
        )
        self.req_obj = req_obj

        ip = self.url + "questions"

        # make a request to IP
        self.data_dict = req.post(
            ip, headers={"X-API-Key": self.api_key}, json=req_obj.model_dump()
        )
        df, _ = questions_to_dataframe(self.data_dict.json(), prompt_constructor)
        self.data = df
        # add an answer row, and initialize it to None
        self.data["answer"] = None
        self.prompt_constructor = prompt_constructor
        self._iter_index = 0

    def __getitem__(self, idx):
        """
        Provides the row, but without the answer column
        """

        row_without_answer = self.data.drop(columns=["answer"]).iloc[idx]
        return row_without_answer

    def __index__(self, idx):
        """
        Provides the row, but without the answer column
        """

        return self.__getitem__(idx)

    def __iter__(self) -> "PERSONAClient":
        self._iter_index = 0

        return self

    def __next__(self):
        while self._iter_index < len(self.data):
            row = self.data.iloc[self._iter_index]
            self._iter_index += 1
            if pd.isna(row["answer"]):
                return row.drop("answer")
        raise StopIteration

    def __len__(self) -> int:
        return len(self.data)

    def log_answer(self, idx, answer) -> None:
        self.data.loc[idx, "answer"] = answer

    def set_answers(self, answers) -> None:
        if len(answers) != len(self.data):
            raise ValueError("Answers must be the same length as the dataset")

        self.data["answer"] = answers

    def evaluate(
        self,
        drop_answer_none: bool = False,
        save_scores: bool = False,
    ) -> dict:
        """
        Evaluates the answers using PERSONA-API

        Args:
            drop_answer_none (bool): Drop rows with no answers
            save_scores (bool): Save the scores in the dataset

        Returns:
            dict: The metrics for the evaluation (contains accuracy and std)
        """
        # make a request to IP
        ip = self.url + "evaluate"

        if drop_answer_none:
            dataset = self.data.dropna(subset=["answer"])
        evaluate_object = InteractiveEvaluationRequest(
            **self.req_obj.model_dump(),
            answered_questions=dataframe_to_questions(dataset),
        )

        response = req.post(
            ip, headers={"X-API-Key": self.api_key}, json=evaluate_object.model_dump()
        ).json()

        if save_scores:
            raw_scores = response.json()["raw_scores"]
            # add as column to the dataset. make sure the index matches the ones we sent (e.g. if we dropped some rows)
            # find a mapping from rows in the dataset to the original dataset
            mapping = dataset.index
            self.data["scores"] = [
                raw_scores[mapping.get_loc(idx)] for idx in self.data.index
            ]

        return response["metrics"]
