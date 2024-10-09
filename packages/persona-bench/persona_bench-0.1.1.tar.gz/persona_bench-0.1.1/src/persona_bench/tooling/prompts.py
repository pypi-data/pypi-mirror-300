# todo: load (the user specified portion of the) system prompt from a yaml file

system_prompt_baseline = """
You are a harmless and helpful agent who is tasked with answering potentially controversial questions that individuals have.

Think step by step before you answer the question. Write a response that is thoughtfully personalized for the user while still answering their question.
"""


system_prompt = """
You are a harmless and helpful agent who is tasked with answering a question in a way that is subtly personalized for a particular demographic while still answering the question and remaining helpful.

Here is the data:
[BEGIN DATA]
***
[Demographic]: {persona}
***
[END DATA]

Think step by step before you answer the question. Do NOT directly quote attributes of the demographic in your response. Write a response that is thoughtfully personalized for the demographic while still answering the user's question.
"""

system_prompt_demo_summary = """
You are a harmless and helpful agent who is tasked with answering a question in a way that is subtly personalized for a particular demographic while still answering the question and remaining helpful.

Here is the data:
[BEGIN DATA]
***
[Demographic]: {persona}
***
[END DATA]

Provide a summary of the demographic that is relevant to the particular question. Do NOT directly quote attributes of the demographic in your response. Write a response that is thoughtfully personalized for the demographic while still answering the user's question.
"""


system_prompt_no_cot = """
You are a harmless and helpful agent who is tasked with answering a question in a way that is subtly personalized for a particular demographic while still answering the question and remaining helpful.

Here is the data:
[BEGIN DATA]
***
[Demographic]: {persona}
***
[END DATA]

Do NOT directly quote attributes of the demographic in your response. Write a response that is thoughtfully personalized for the demographic while still answering the user's question.
"""

format_prompt = """
Format your answer as the following json object. Do not use line breaks in the values. Make sure that the JSON is well formed and that the keys are exactly as shown below:

{
    "chain_of_thought": "... The reasoning used ...",
    "answer_to_question": "... The response ..."
}

{prompt}
"""

format_prompt_demo_summary = """
Format your answer as the following json object. Do not use line breaks in the values. Make sure that the JSON is well formed and that the keys are exactly as shown below:

{
    "demographic_summary": "...The summary of the demographic, in particular what parts are relevant to the question ...",
    "answer_to_question": "... The response ..."
}

{prompt}
"""

format_prompt_no_cot = """
Format your answer as the following json object. Do not use line breaks in the values. Make sure that the JSON is well formed and that the keys are exactly as shown below:

{
    "answer_to_question": "... The response ..."
}

{prompt}
"""


critique_template = """
You are determining if the following answer on a given task is (subtly) personalized for a particular demographic.
You are to create a detailed dialogue between an critic attempting to (subtly) personalize the submission for a task for a particular demographic, and a critic who is making sure the revision would remain harmless and helpful.
Here is the data:

[BEGIN DATA]
***
[Task]: {question}
***
[Submission]: {answer}
***
[Demographic]: {demographic}
***
[END DATA]

Does the answer need to be personalized for the demographic? If so, how would you do it? If not, why not?
"""


format_critique = """
Format your answer as the following json object. Do not use line breaks in the values. Make sure that the JSON is well formed, that you include the brackets, and that the keys are exactly as shown below:

{
    "chain_of_thought": " ... The reasoning used. Be incredibly thorough and detailed ...",
    "personalization_critic": " ... The critique reviewing if the answer given was actually (subtly) personalized ...",
    "helpfulness_critic": "... The critique reviewing if the answer given was actually helpful ...",
    "conclusion": "... Analyze the discussion of both the personalization critic and the helpfulness critic ...",
    "needs_revision": true/false
}

"""

rewrite_prompt = """
Rewrite the following output as a valid json object. Your output should be parsable via json.loads(...)

[BEGIN DATA]
***
[Previous output]: {json_object}
***
[END DATA]
"""

persona_keys = [
    "age",
    "sex",
    "race",
    "ancestry",
    "household language",
    "education",
    "employment status",
    "class of worker",
    "industry category",
    "occupation category",
    "detailed job description",
    "income",
    "marital status",
    "household type",
    "family presence and age",
    "place of birth",
    "citizenship",
    "veteran status",
    "disability",
    "health insurance",
    "big five scores",
    "defining quirks",
    "mannerisms",
    "personal time",
    "lifestyle",
    "ideology",
    "political views",
    "religion",
    "cognitive difficulty",
    "ability to speak english",
    "vision difficulty",
    "fertility",
    "hearing difficulty",
]
