# PERSONA-API SDK

## Quick Start

1. Install the package:
   ```bash
   pip install persona-bench
   ```

2. Set up your API key:
   - Sign up at [https://www.synthlabs.ai/research/persona](https://www.synthlabs.ai/research/persona) to get your API key and claim your free trial credits.
   - Set the API key as an environment variable:
     ```bash
     export SYNTH_API_KEY=your_api_key_here
     ```
   - Alternatively, you can pass the API key directly when initializing the client (see step 3).

3. Use in your Python script:
   ```python
   from persona_bench.api import PERSONAClient
   from persona_bench.api.prompt_constructor import ChainOfThoughtPromptConstructor

   client = PERSONAClient(
       model_str="your_identifier_name",
       evaluation_type="comparison", # Run a grounded evaluation, API exclusive!
       N=50,
       prompt_constructor=ChainOfThoughtPromptConstructor(),
       # If not set as an environment variable, pass the API key here:
       # api_key="your_api_key_here"
   )

   # Iterate through questions and log answers
   for idx, q in enumerate(client):
       answer = your_model_function(q["system"], q["user"])
       client.log_answer(idx, answer)

   # Evaluate the results
   results = client.evaluate(drop_answer_none=True)
   print(results)
   ```

## Key Features

### 📈 Evaluation Metrics
- **Personalized Response Generation**: Evaluate a model's capability to generate responses based on specific personas.
- **Leave One Out Analysis**: Measure the impact of individual attributes on model performance.
- **Intersectionality**: Analyze model behavior across various demographic intersections.
- **Pass@K**: Gauge the number of attempts needed for successful personalization.
- **Comparison Evaluation** (API-exclusive): Grounded personalization assessment.

### 🔧 Tools and API
- **API Integration**: Easily integrate with existing models to access a range of evaluation types.
- **Customizable Prompt Construction**: Personalize prompts with tools like ChainOfThoughtPromptConstructor.
- **InspectAI Compatibility**: Perform visualization using InspectAI's tools.


## Detailed Usage

### Initialization

Create a `PERSONAClient` instance with the following parameters:

- `model_str`: The identifier for this evaluation task
- `evaluation_type`: Type of evaluation ("main", "loo", "intersectionality", "pass_at_k")
- `N`: Number of samples for evaluation
- `prompt_constructor`: Custom prompt constructor (optional)
- `intersection`: List of intersection attributes (required for intersectionality evaluation)
- `loo_attributes`: Leave-one-out attributes (required for LOO evaluation)
- `seed`: Random seed for reproducibility (optional)
- `url`: API endpoint URL (optional, default is "https://synth-api-development.eastus.azurecontainer.io/api/v1/personas/v1/")
- `api_key`: Your SYNTH API key (optional if set as an environment variable)

Example:

```python
from persona_bench.api import PERSONAClient

client = PERSONAClient(
    model_str="your_identifier_name",
    evaluation_type="main",
    N=50,
    prompt_constructor=ChainOfThoughtPromptConstructor(),
    # If not set as an environment variable, pass the API key here:
    # api_key="your_api_key_here"
)
```

### Iterating Through Questions

Use the client as an iterable to access questions:

```python
for idx, question in enumerate(client):
    # Access question data
    system_prompt = question["system"]
    user_prompt = question["user"]
    # Generate answer using your model
    # Log the answer
    client.log_answer(idx, answer)
```

### Evaluation

Evaluate the logged answers:

```python
results = client.evaluate(drop_answer_none=True, save_scores=False)
```

- `drop_answer_none`: Drop rows with no answers (default: False)
- `save_scores`: Save individual scores in the dataset (default: False)

## Advanced Usage

### Custom Prompt Constructors

Create a custom prompt constructor by inheriting from `BasePromptConstructor`:

```python
from persona_bench.api.prompt_constructor import BasePromptConstructor

class MyCustomPromptConstructor(BasePromptConstructor):
    def construct_prompt(self, persona, question):
        # Implement your custom prompt construction logic
        pass
```

Use your custom constructor when initializing the client:

```python
client = PERSONAClient(
    # ... other parameters ...
    prompt_constructor=MyCustomPromptConstructor(),
)
```

### Accessing Raw Data

Access the underlying data using indexing:

```python
question = client[0]  # Get the first question
```

```python
answers = [generate_answer(q) for q in client]
client.set_answers(answers)
```

## Evaluation Types


### Comparison Evaluation (API-exclusive)

The comparison evaluation is our most advanced and grounded assessment,
exclusively available through the PERSONA API. It provides a robust measure of a
model's personalization capabilities using known gold truth answers.

<details>
<summary>Click to expand details</summary>

- Uses carefully curated persona pairs with known distinctions
- Presents models with questions that have objectively different answers for each persona
- Evaluates the model's ability to generate persona-appropriate responses
- Compares model outputs against gold truth answers for precise accuracy measurement
- Offers the most reliable and interpretable results among all evaluation types

This evaluation type stands out for its ground truth basis, allowing for a more
definitive assessment of a model's personalization performance. It's
particularly valuable for researchers and practitioners seeking a
high-confidence measure of their model's capabilities.

Example usage:


```python
from persona_bench.api import PERSONAClient
client = PERSONAClient(model_str="your_identifier_name" evaluation_type="comparison", N=50)
```
</details>

### Main Evaluation

The main evaluation assesses a model's ability to generate personalized responses based on given personas.

<details>
<summary>Click to expand details</summary>

```python
client = PERSONAClient(model_str="your_identifier_name", evaluation_type="main", N=50)
```
</details>

### Leave One Out (LOO) Analysis

Measures the impact of individual attributes on personalization performance.

<details>
<summary>Click to expand details</summary>

```python
from persona_bench.api.interfaces import LooAttributes

loo_attrs = LooAttributes(attributes=["age", "sex", "race", "education"])
client = PERSONAClient(model_str="your_identifier_name", evaluation_type="loo", N=50, loo_attributes=loo_attrs)
```

Full details on how to use leave one our analysis are available in the primary README.md
</details>

### Intersectionality

Evaluates model performance across different demographic intersections.

<details>
<summary>Click to expand details</summary>

```python
from persona_bench.api.interfaces import Intersection

intersections = [Intersection(attribute="race", value="White"), Intersection(attribute="sex", value="Male")]
client = PERSONAClient(model_str="your_identifier_name", evaluation_type="intersectionality", N=50, intersection=intersections)
```

Full details on how to use leave one our analysis are available in the primary README.md
</details>

### Pass@K

Determines how many attempts are required to successfully personalize for a given persona.

<details>
<summary>Click to expand details</summary>

```python
client = PERSONAClient(model_str="your_identifier_name", evaluation_type="pass_at_k", N=50)
```

WARNING! Pass@K is very credit intensive.
</details>
