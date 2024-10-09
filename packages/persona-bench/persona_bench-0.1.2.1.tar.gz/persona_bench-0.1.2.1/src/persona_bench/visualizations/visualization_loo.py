# load a log, given by the parser (default is to look through logs for the most recent one)

import argparse
import json
import logging
import os
from collections import defaultdict

from persona_bench.tooling.prompts import persona_keys
from persona_bench.tooling.utils import convert_to_dict

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

sample_scores = [sample["score"] for sample in log["samples"]]

# build up dictionaries of the personas and their respective scores
persona_loos = defaultdict(list)
persona_scores = defaultdict(list)
for score in sample_scores:
    persona_dict = convert_to_dict(score["metadata"]["persona"])
    persona_idx = score["metadata"]["_persona_idx"]
    score = score["value"]

    persona_loos[persona_idx].append(persona_dict)
    persona_scores[persona_idx].append(score)


attribute_wise_score = defaultdict(list)
max_length_loo = max(len(loos) for loos in persona_loos.values())

# we're going to group the scores by their loo attribute
for loos, scores in zip(persona_loos.values(), persona_scores.values()):
    # if we did not get all, just continue
    # if len(loos) != max_length_loo:
    #    continue

    # find the loo with the most keys
    base_persona_idx = argmax(len(loo) for loo in loos)

    loos_without_base = loos[:base_persona_idx] + loos[base_persona_idx + 1 :]
    scores_without_base = scores[:base_persona_idx] + scores[base_persona_idx + 1 :]

    # every loo is missing exactly 1 key from base persona. figure out what it is
    loo_keys = [set_persona_keys - set(loo.keys()) for loo in loos_without_base]
    loo_keys = list(set.union(*loo_keys))

    # add the base persona to the attribute wise score
    attribute_wise_score["baseline"].append(scores[base_persona_idx])

    for key, score in zip(loo_keys, scores_without_base):
        attribute_wise_score[key].append(score)

# alphabetize the keys, keep baseline first though
keys = list(attribute_wise_score.keys())
keys.remove("baseline")
keys.sort()
keys = ["baseline"] + keys

attribute_wise_score = {key: attribute_wise_score[key] for key in keys}

import matplotlib.pyplot as plt

# make a barplot
import seaborn as sns

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 15))

# make a graph of attribute wise score delta
sns.barplot(
    x=list(attribute_wise_score.keys()),
    y=[sum(scores) / len(scores) for scores in attribute_wise_score.values()],
    ax=ax,
)
plt.xticks(rotation=45)

# set the y label to accuracy
plt.ylabel("Accuracy after including attribute")
# set the x label to "LOO Attribute"
plt.xlabel("Persona attribute for measuring LLM capability")
# set the title to "Attribute wise score"
plt.title(f"Attribute wise score (n={n_samples}, model={log['eval']['model']})")

plt.savefig("attribute_wise_score.png")
