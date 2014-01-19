#!/bin/bash
#sort --random-sort feature.f >> randomized.f
cd output/
shuf feature.f -o shuffled.f
split -l 398 shuffled.f group --numeric-suffixes=1 --additional-suffix=.f
