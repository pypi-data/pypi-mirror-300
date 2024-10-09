# load a log, given by the parser (default is to look through logs for the most recent one)

import argparse
import json
import os
from collections import defaultdict

from persona_bench.tooling.prompts import persona_keys

set_persona_keys = set(persona_keys)


def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        type=str,
        default="logs/",
        help="Path to the log file. Unless a specific log is specified, the most recent log will be used.",
    )
    return parser.parse_args()


def dict_to_string(dictionary):
    out_str = ""
    for x in dictionary["attributes"]:
        out_str += x["attribute"] + ": " + str(x["values"]) + "\n"

    return out_str


args = parse_args()

# load the log. its a json file

# first check if they just gave a dir or a specific path
if os.path.isdir(args.log):
    logs = [
        os.path.join(args.log, log)
        for log in os.listdir(args.log)
        if log.endswith(".json")
    ]
    if not logs:
        raise ValueError(f"No logs found in {args.log}")
    log = max(logs, key=os.path.getctime)
else:
    log = args.log

# load the log
with open(log) as f:
    log = json.load(f)

# check if the log is empty
if not log:
    raise ValueError(f"Log is empty.")

# throw an error if "error" is a key in the log
if "error" in log:
    raise ValueError(f"Unable to use log with error for visualization.")

# assert that "samples"
if "samples" not in log:
    raise ValueError(f"Log does not contain samples.")


n_samples = log["eval"]["dataset"]["samples"]


sample_scores = [sample["score"] for sample in log["samples"]]
sample_metadatas = [sample["metadata"] for sample in log["samples"]]

intersection_dict = defaultdict(list)
for score, metadata in zip(sample_scores, sample_metadatas):
    for relevant in metadata["applicable_intersections"]:
        intersection_dict[
            dict_to_string(json.loads(relevant.replace("'", '"')))
        ].append(score["value"])

import matplotlib.pyplot as plt

# make a barplot
import seaborn as sns

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 15))

# make a graph of attribute wise score delta
sns.barplot(
    x=list(intersection_dict.keys()),
    y=[sum(scores) / len(scores) for scores in intersection_dict.values()],
    ax=ax,
)
plt.xticks(rotation=45)

# set the y label to accuracy
plt.ylabel("Accuracy of specific demographic intersection")
# set the x label to "LOO Attribute"
plt.xlabel("Intersection idx")
# set the title to "Attribute wise score"
plt.title(f"Intersection wise score (n={n_samples}, model={log['eval']['model']})")

plt.savefig("intersection_wise_score.png")
