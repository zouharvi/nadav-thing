#!/usr/bin/env python3

import argparse
import csv
import evaluate

args = argparse.ArgumentParser()
args.add_argument("-i1", "--input-1", default="data/en.txt")
args.add_argument("-i2", "--input-2", default="data/nl.txt")
args.add_argument("-o", "--output", default="data/translations_c_google.csv")
args = args.parse_args()

# load everything (don't worry about efficiency)
with open(args.input_1, "r") as f:
    data = [{"original_en": x.rstrip("\n")} for x in f]

with open(args.input_1, "r") as f:
    data = [
        l | {"dutch_translation": x.rstrip("\n")}
        for l, x in list(zip(data, f))[:5]
    ]

print(len(data))

# WMT22 is also available but not from evaluate, so this is easier
comet_metric = evaluate.load('comet', config_name="wmt21-comet-qe-mqm")

# references=reference
scores_nl = comet_metric.compute(
    predictions=[x["dutch_translation"] for x in data],
    sources=[x["original_en"] for x in data],
    # this is a hack to satisfy evaluate
    # the model is not actually using the references
    references=["xxxxxxxxxxxxxxxxxxx"] * len(data),
    progress_bar=True,
)
print(f"Dutch avg: {scores_nl['mean_score']:.5f}")

data = [
    x | {
        "dutch_translation_score": score_nl,
    }
    for x, score_nl
    in zip(data, scores_nl["scores"])
]

with open(args.output, "w") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
