#!/usr/bin/env python3

import argparse
import csv

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/translations.csv")
args.add_argument("-o", "--output", default="data/en.txt")
args = args.parse_args()

# load everything (don't worry about efficiency)
with open(args.input, "r") as f:
    data = [x["original_en"] for x in csv.DictReader(f)]

with open(args.output, "w") as f:
    f.write("\n".join(data))