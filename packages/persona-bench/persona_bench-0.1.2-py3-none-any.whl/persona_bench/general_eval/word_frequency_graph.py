import re
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the CSV file
df = pd.read_csv("differences.csv")

# List of phrases to analyze
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


# Function to get related words
def get_related_words(phrase, nlp, threshold=0.5):
    phrase_vec = nlp(phrase)
    related = []
    for word in nlp.vocab:
        if word.has_vector:
            if (
                word.text.lower() != phrase.lower()
                and word.similarity(phrase_vec) > threshold
            ):
                related.append(word.text.lower())
    return related[:5]  # Return top 5 related words


# Generate related words for each phrase
related_words = {phrase: get_related_words(phrase, nlp) for phrase in persona_keys}


# Function to count occurrences of phrases and their related words
def count_phrases_and_related(text, phrases, related_words):
    text = text.lower()
    counts = defaultdict(int)
    for phrase in phrases:
        counts[phrase] += len(
            re.findall(r"\b" + re.escape(phrase.lower()) + r"\b", text)
        )
        for related in related_words[phrase]:
            counts[phrase] += len(re.findall(r"\b" + re.escape(related) + r"\b", text))
    return dict(counts)


# Models to analyze
models = ["gpt-3.5", "gpt-4", "gpt-4o", "llama-370b"]

# Compute frequency for each model
model_frequencies = {}
for model in models:
    model_text = " ".join(df[df["model"] == model]["difference"])
    model_frequencies[model] = count_phrases_and_related(
        model_text, persona_keys, related_words
    )

# Create a DataFrame from the frequencies
freq_df = pd.DataFrame(model_frequencies).reset_index()
freq_df.columns = ["Phrase"] + models
freq_df_melted = freq_df.melt(
    id_vars=["Phrase"], var_name="Model", value_name="Frequency"
)

# Set up the plot style
sns.set(style="whitegrid")

# Create a color palette
palette = sns.color_palette("hls", 4)

# Create the plot
plt.figure(figsize=(20, 6))
ax = sns.barplot(
    x="Phrase", y="Frequency", hue="Model", data=freq_df_melted, palette=palette
)

# Customize the plot
plt.title("Phrase and Related Words Frequency by Model", fontsize=20)
plt.xlabel("Phrases", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.legend(title="Model", title_fontsize="13", fontsize="12")

# Adjust layout and save
plt.tight_layout()
plt.savefig("phrase_frequency_all_models.png", dpi=300, bbox_inches="tight")
plt.close()

# Print the frequencies and related words
for model in models:
    print(f"\nFrequencies for {model}:")
    for phrase, count in model_frequencies[model].items():
        if count > 0:
            print(
                f"{phrase} (and related words: {', '.join(related_words[phrase])}): {count}"
            )

# Create individual plots for each model
for model in models:
    plt.figure(figsize=(15, 7))
    model_data = freq_df_melted[freq_df_melted["Model"] == model]
    sns.barplot(
        x="Phrase",
        y="Frequency",
        data=model_data,
        color=sns.color_palette()[models.index(model)],
    )

    plt.title(f"Phrase and Related Words Frequency for {model}", fontsize=20)
    plt.xlabel("Phrases", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{model}_phrase_frequency.png", dpi=300, bbox_inches="tight")
    plt.close()
