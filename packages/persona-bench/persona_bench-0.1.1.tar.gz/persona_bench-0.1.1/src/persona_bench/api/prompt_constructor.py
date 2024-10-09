import abc
import textwrap
import typing

from persona_bench.api.interfaces import Question


class Prompt(typing.TypedDict):
    system: str
    user: str


class BasePromptConstructor(abc.ABC):
    """
    Abstract class for prompt constructor
    """

    @abc.abstractmethod
    def __call__(self, question: Question) -> Prompt:
        raise NotImplementedError("Prompt constructor must be implemented")


class DefaultPromptConstructor(BasePromptConstructor):
    def __call__(self, question: Question) -> Prompt:
        system_prompt = textwrap.dedent(
            """
            You will be given a question and a persona. Write a response to the
            question befitting the persona.
        """
        )
        user_prompt = textwrap.dedent(
            f"""
            Persona: {question.persona}
            Question: {question.question}
        """
        )

        return {"system": system_prompt, "user": user_prompt}


class ChainOfThoughtPromptConstructor(DefaultPromptConstructor):
    def __call__(self, question: Question) -> Prompt:
        system_prompt = textwrap.dedent(
            """
            You will be given a question and a persona. Write a response to the
            question befitting the persona. Think step by step before providing
            an answer.
        """
        )

        return {"system": system_prompt, "user": super().__call__(question)["user"]}
