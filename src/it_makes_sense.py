#!/usr/bin/env python3

import evaluate

comet_metric = evaluate.load('comet', config_name="wmt21-comet-qe-mqm")

score = comet_metric.compute(
    predictions=["Ik ben nu al een paar uur buiten het bos aan het ronddwalen."],
    sources=["I've been wandering outside of the forest for a few hours now."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.13123
print(f"en to nl (correct translation): {score:.5f}")

score = comet_metric.compute(
    predictions=["I've been wandering outside of the forest for a few hours now."],
    sources=["Ik ben nu al een paar uur buiten het bos aan het ronddwalen."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.12696
print(f"nl to en (correct translation): {score:.5f}")


score = comet_metric.compute(
    predictions=["Ik heb veel te lang door het bos gezworven."],
    sources=["I've been wandering around the forest for far too long."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.11122 (less than correct translation!)
print(f"en to nl (incorrect translation): {score:.5f}")

score = comet_metric.compute(
    predictions=["I've been wandering around the forest for far too long."],
    sources=["Ik heb veel te lang door het bos gezworven."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.11496 (less than correct translation!)
print(f"nl to en (incorrect translation): {score:.5f}")



score = comet_metric.compute(
    predictions=["I've been wandering outside of the forest for a few hours now."],
    sources=["I've been wandering outside of the forest for a few hours now."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.13142
print(f"en to en: {score:.5f}")
score = comet_metric.compute(
    predictions=["Ik ben nu al een paar uur buiten het bos aan het ronddwalen."],
    sources=["Ik ben nu al een paar uur buiten het bos aan het ronddwalen."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.13089 (meaningless number but same as for nl)
print(f"nl to nl: {score:.5f}")



score = comet_metric.compute(
    predictions=["flkxvc xv rete xzocvij ewtlk zxcv lkwer Zv"],
    sources=["I've been wandering outside of the forest for a few hours now."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.04120 (very low number, as expected!)
print(f"en to nl (garbage): {score:.5f}")

score = comet_metric.compute(
    predictions=["flkxvc xv rete xzocvij ewtlk zxcv lkwer Zv"],
    sources=["Ik ben nu al een paar uur buiten het bos aan het ronddwalen."],
    references=["xxxxxxxxxxxxxxxxxxx"],
)["mean_score"]
# 0.03952 (very low number, as expected!)
print(f"nl to en (garbage): {score:.5f}")
