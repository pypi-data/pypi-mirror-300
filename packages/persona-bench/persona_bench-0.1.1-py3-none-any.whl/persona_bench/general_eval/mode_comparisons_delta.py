import json
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# make sure example_logs/ exists. If it doesn't, throw an exception saying to run decompress_example_logs.sh
assert os.path.exists("data/example_logs/"), "Please run decompress_example_logs.sh"

# File names
files = [
    "data/example_logs/gpt-3.5_baseline.json",
    "data/example_logs/gpt-3.5_cot.json",
    "data/example_logs/gpt-3.5_no_cot.json",
    "data/example_logs/gpt-3.5_demographic.json",
    "data/example_logs/gpt-4_baseline.json",
    "data/example_logs/gpt-4_cot.json",
    "data/example_logs/gpt-4_no_cot.json",
    "data/example_logs/gpt-4_demographic.json",
    "data/example_logs/gpt-4o_baseline.json",
    "data/example_logs/gpt-4o_cot.json",
    "data/example_logs/gpt-4o_no_cot.json",
    "data/example_logs/gpt-4o_demographic.json",
    "data/example_logs/llama-370b_baseline.json",
    "data/example_logs/llama-370b_cot.json",
    "data/example_logs/llama-370b_no_cot.json",
    "data/example_logs/llama-370b_demographic.json",
]

# Loading data
data = []
for file in files:
    with open(file) as f:
        data.append(json.load(f))

# Extract accuracies and standard deviations
accuracies = {}
stds = {}
for file, d in zip(files, data):
    try:
        accuracies[file] = d["results"]["metrics"]["accuracy"]["value"]
        stds[file] = d["results"]["metrics"]["bootstrap_std"]["value"]
    except:
        accuracies[file] = d["results"]["scores"][0]["metrics"]["accuracy"]["value"]
        stds[file] = d["results"]["scores"][0]["metrics"]["bootstrap_std"]["value"]

# Calculate deltas
deltas = []
delta_stds = []
labels = []

for model in ["gpt-3.5", "gpt-4", "gpt-4o", "llama-370b"]:
    baseline = accuracies[f"data/example_logs/{model}_baseline.json"]
    baseline_std = stds[f"data/example_logs/{model}_baseline.json"]

    for usage in ["cot", "demographic", "no_cot"]:
        current = accuracies[f"data/example_logs/{model}_{usage}.json"]
        current_std = stds[f"data/example_logs/{model}_{usage}.json"]

        delta = (current - baseline) / baseline * 100
        delta_std = (current_std**2 + baseline_std**2) ** 0.5

        deltas.append(delta)
        delta_stds.append(delta_std)
        labels.append(f"{model}_{usage}")

        # print out al the stats
        print(f"{model}_{usage}: {delta:.2f} ± {delta_std:.2f}")

# Plotting
sns.set(style="whitegrid")
plt.figure(figsize=(14, 10))

# Create a color palette
palette = sns.color_palette("hls", 4)
shades = ["light", "dark"]

# Map each file to a color and shade
colors = []
for label in labels:
    llm = label.split("_")[0]
    usage = label.split("_")[1]

    if "gpt-3.5" in llm:
        color = palette[0]
    elif "gpt-4" in llm and "gpt-4o" not in llm:
        color = palette[1]
    elif "gpt-4o" in llm:
        color = palette[2]
    elif "llama-370b" in llm:
        color = palette[3]

    if usage == "cot":
        shade = sns.light_palette(color, 10)[3]
    elif usage == "demographic":
        shade = sns.light_palette(color, 10)[5]
    elif usage == "no":
        shade = sns.light_palette(color, 10)[7]

    colors.append(shade)

# Bar plot with error bars
x = np.arange(len(deltas))
bars = plt.bar(
    x,
    deltas,
    yerr=delta_stds,
    align="center",
    alpha=0.9,
    capsize=10,
    color=colors,
    edgecolor="black",
)

# Set labels and title
plt.ylabel("Percentage Improvement")
plt.axhline(0, color="grey", linewidth=0.8)
plt.xticks(x, labels, rotation=45)
plt.title("Percentage Improvement Over Baseline")

# Save the figure
plt.savefig("delta_comparison.png")
plt.show()
