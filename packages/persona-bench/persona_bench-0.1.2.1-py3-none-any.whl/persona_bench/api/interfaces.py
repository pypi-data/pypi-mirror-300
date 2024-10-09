from typing import Literal

from pydantic import BaseModel, Field

from persona_bench.tooling.utils import Intersection, LooAttributes


class Question(BaseModel):
    question: str = Field(..., description="The question to ask the language model")
    persona: dict = Field(default=None, description="The persona to use for evaluation")
    persona_idx: int = Field(
        default=None,
        description="The index of the persona in the dataframe (Do not edit.)",
    )
    intersection_attrs: list[Intersection] | None = Field(
        default=None,
        description="Intersection attributes for evaluation, if applicable",
    )
    loo_attrs: LooAttributes | None = Field(
        default=None,
        description="Leave-one-out attributes for evaluation, if applicable",
    )
    metadata: dict | None = Field(
        default=None, description="Extra metadata for the question. Do not edit."
    )


class AnsweredQuestion(Question):
    system: str | None = Field(
        ..., description="The system prompt to use for the evaluation"
    )
    user: str = Field(..., description="The question to ask the language model")
    answer: str = Field(..., description="The answer to the question")


class PERSONAQuestionRequest(BaseModel):
    model_str: str = Field(..., description="The model to evaluate")
    evaluation_type: Literal[
        "main", "loo", "intersectionality", "pass_at_k", "comparison"
    ] = Field(default="main", description="The type of evaluation to perform")
    seed: int | None = Field(
        default=None, description="Random seed for reproducibility"
    )
    N: int | None = Field(
        default=None, description="Number of samples to use for evaluation"
    )
    intersection: list[Intersection] | None = Field(
        default=None, description="Intersection attributes for evaluation"
    )
    loo_attributes: LooAttributes | None = Field(
        default=None, description="Leave-one-out attributes for evaluation"
    )

    # remove protected namespaces
    class Config:
        protected_namespaces = ()


class InteractiveEvaluationRequest(PERSONAQuestionRequest):
    answered_questions: list[AnsweredQuestion] = Field(
        ..., description="The questions and answers from the model"
    )
