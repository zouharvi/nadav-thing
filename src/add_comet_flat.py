#!/usr/bin/env python3

import argparse
import csv
import evaluate
import nltk

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/translations.csv")
args.add_argument("-o", "--output", default="data/translations_c_flat.csv")
args = args.parse_args()

# load everything (don't worry about efficiency)
with open(args.input, "r") as f:
    data = list(csv.DictReader(f))

data_new = []
for line in data:
    en_sents = nltk.tokenize.sent_tokenize(line["original_en"])
    nl_sents = nltk.tokenize.sent_tokenize(line["dutch_translation"])
    fr_sents = nltk.tokenize.sent_tokenize(line["french_translation"])
    if len(en_sents) != len(nl_sents) or len(en_sents) != len(fr_sents):
        continue

    for en_sent, nl_sent, fr_sent in zip(en_sents, nl_sents, fr_sents):
        data_new.append({
            "original_en": en_sent,
            "dutch_translation": nl_sent,
            "french_translation": fr_sent,
        })
data = data_new

# WMT22 is also available but not from evaluate, so this is easier
comet_metric = evaluate.load('comet', config_name="wmt21-comet-qe-mqm")

# references=reference
scores_nl = comet_metric.compute(
    predictions=[x["dutch_translation"] for x in data],
    sources=[x["original_en"] for x in data],
    # this is a hack to satisfy evaluate
    # the model is not actually using the references
    references=["xxxxxxxxxxxxxxxxxxx"]*len(data),
    progress_bar=True,
)

scores_fr = comet_metric.compute(
    predictions=[x["french_translation"] for x in data],
    sources=[x["original_en"] for x in data],
    # this is a hack to satisfy evaluate
    # the model is not actually using the references
    references=["xxxxxxxxxxxxxxxxxxx"]*len(data),
    progress_bar=True,
)

print(f"Dutch avg: {scores_nl['mean_score']:.5f}")
print(f"French avg: {scores_fr['mean_score']:.5f}")

data = [
    x | {
        "dutch_translation_score": score_nl,
        "french_translation_score": score_fr,
    }
    for x, score_nl, score_fr
    in zip(data, scores_nl["scores"], scores_fr["scores"])
]

with open(args.output, "w") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
