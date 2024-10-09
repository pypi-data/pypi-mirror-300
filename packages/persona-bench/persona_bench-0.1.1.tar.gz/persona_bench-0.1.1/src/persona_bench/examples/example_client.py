# load our API key
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

from persona_bench.api import PERSONAClient
from persona_bench.api.prompt_constructor import ChainOfThoughtPromptConstructor

model = OpenAI()
# Create a PERSONAClient object
client = PERSONAClient(
    model_str="your_identifier_name",
    evaluation_type="main",  # Run a grounded evaluation, API exclusive!
    N=1,
    prompt_constructor=ChainOfThoughtPromptConstructor(),
    # If not set as an environment variable, pass the API key here:
    # api_key="your_api_key_here"
)

# Iterate through questions and log answers
for idx, q in enumerate(client):
    answer = model.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": q["system"]},
            {"role": "user", "content": q["user"]},
        ],
    )
    client.log_answer(idx, answer.choices[0].message.content)

# Evaluate the results
results = client.evaluate(drop_answer_none=True)
print(results)
