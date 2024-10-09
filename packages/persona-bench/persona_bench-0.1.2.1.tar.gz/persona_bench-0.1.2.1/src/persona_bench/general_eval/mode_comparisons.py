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
        data.append((file, json.load(f)))

# Extract accuracies and standard deviations
accuracies = []
stds = []
for file, d in data:
    try:
        accuracies.append(d["results"]["metrics"]["accuracy"]["value"])
        stds.append(d["results"]["metrics"]["bootstrap_std"]["value"])
    except:
        accuracies.append(d["results"]["scores"][0]["metrics"]["accuracy"]["value"])
        stds.append(d["results"]["scores"][0]["metrics"]["bootstrap_std"]["value"])

    # print data
    model_usage = file.replace(".json", "").replace("data/example_logs/", "")

    print(f"{model_usage}: {accuracies[-1]:.2f} ± {stds[-1]:.2f}")

# Plotting
sns.set(style="whitegrid")
plt.figure(figsize=(14, 12))

# Create a color palette
palette = sns.color_palette("hls", 4)

# Map each file to a color and shade
colors = []
for i, file in enumerate(files):
    llm = file.split("_")[0]
    usage = file.split("_")[1]
    if "gpt-3.5" in llm:
        color = palette[0]
    elif "gpt-4" in llm and "gpt-4o" not in llm:
        color = palette[1]
    elif "gpt-4o" in llm:
        color = palette[2]
    elif "llama" in llm:
        color = palette[3]

    if usage == "cot.json":
        shade = sns.light_palette(color, 10)[3]
    elif usage == "no":
        shade = sns.light_palette(color, 10)[7]
    elif usage == "demographic.json":
        shade = sns.light_palette(color, 10)[5]
    elif usage == "baseline.json":
        shade = sns.light_palette(color, 10)[1]

    colors.append(shade)

# Bar plot with error bars
x = np.arange(len(accuracies))
bars = plt.bar(
    x,
    accuracies,
    yerr=stds,
    align="center",
    alpha=0.9,
    capsize=10,
    color=colors,
    edgecolor="black",
)

# Set labels and title
plt.ylabel("Accuracy")
ticks = [file.replace("data/example_logs/", "").replace(".json", "") for file in files]
plt.xticks(x, ticks, rotation=45)
plt.title("Comparison of LLMs with Different Usage Types")

# Save the figure
plt.savefig("comparison_no_cotvscot.png")
plt.show()
