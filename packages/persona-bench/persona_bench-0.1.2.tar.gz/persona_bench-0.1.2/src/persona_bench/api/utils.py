import logging

import pandas as pd
from pydantic import ValidationError

from persona_bench.api.interfaces import AnsweredQuestion, Question
from persona_bench.api.prompt_constructor import BasePromptConstructor

_log = logging.getLogger(__name__)


def questions_to_dataframe(
    question_dicts: list[dict],
    prompt_constructor: BasePromptConstructor | None = None,
) -> tuple[pd.DataFrame, list[dict]]:
    """
    Validates and converts the given dictionaries to a pd.DataFrame[Question]
    """

    questions = []

    for q_dict in question_dicts:
        try:
            question = Question(**q_dict)
            question_dict = question.dict()

            # Add a prompt to the question dictionary
            if prompt_constructor is not None:
                prompt = prompt_constructor(question)
                question_dict.update(prompt)

            questions.append(question_dict)

        except ValidationError:
            _log.warning("Could not construct Question", exc_info=True)

    df = pd.DataFrame(questions)

    return df, questions


def dataframe_to_questions(df: pd.DataFrame) -> list[AnsweredQuestion]:
    """
    Convert each row of the DataFrame back into a Question object
    """

    questions = []

    for _, row in df.iterrows():
        question_dict = row.to_dict()

        try:
            question = AnsweredQuestion(**question_dict)
        except ValidationError:
            _log.warning("Could not construct AnsweredQuestion", exc_info=True)
            continue

        questions.append(question)

    return questions
