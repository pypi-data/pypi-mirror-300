# load a log, given by the parser (default is to look through logs for the most recent one)

import argparse
import json
import logging
import os
from collections import defaultdict

from persona_bench.tooling.utils import persona_keys

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

# if n_samples < 300, raise a warning
if n_samples < 300:
    logging.warning(
        f"Number of samples in log is less than 300. Visualization may be less effective."
    )

try:
    sample_scores = [sample["scores"] for sample in log["samples"]]
except:
    sample_scores = [sample["score"] for sample in log["samples"]]

to_graph = defaultdict(list)
# find the longest set of critiques
max_num_crits = (
    16  # max([len(score["metadata"]["critique"]) for score in sample_scores])
)


for score in sample_scores:
    for idx in range(max_num_crits):
        try:
            metadata = score["persona_bench/model_critique_pass_at_k"]["metadata"]
        except:
            metadata = score["metadata"]

        crit_length = len(metadata["critique"])

        try:
            check = metadata["critique"][idx]["needs_revision"]
        except:
            continue
        crit_list = [
            metadata["critique"][idx]["needs_revision"] == False
            for idx in range(0, min(idx + 1, crit_length))
        ]
        to_graph[idx + 1].append(1.0 if any(crit_list) else 0.0)


# get a list of xs and ys from to_graph
xs = list(to_graph.keys())
ys = list(to_graph.values())

# normalize
y_max = len(ys[-1])
ys = list(map(lambda x: sum(x) / y_max, ys))

import matplotlib.pyplot as plt

# make a barplot
import seaborn as sns

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 15))

# make a graph of pass at k
sns.barplot(x=xs, y=ys, ax=ax)

# ys to csv
import csv

model_name = log["eval"]["model"].split("/")[-1]
with open(f"pass_at_k_{model_name}.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["k", "cum_score"])
    for x, y in zip(xs, ys):
        writer.writerow([x, y])

# set title and labels
plt.title(f"Pass at k (n={n_samples}, model={log['eval']['model']})")
plt.xlabel("Number of attempts")
plt.ylabel("Cum score")

# save
plt.savefig("pass_at_k.png")
