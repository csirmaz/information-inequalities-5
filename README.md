# information-inequalities-5
Code and dataset for the paper "Information Inequalities for Five Random Variables" by E P Csirmaz and L Csirmaz

# Files

## pts.res

Contains the irreducible staircases for n<=60 in the form of a sequence of 0s and 1s denoting the decrease from the previous value.
`+` at the end of the line means that the corresponding triplet is extremal in the next generation as well (only these are present in this list).

## staircase.py

Generates a list of irreducible staircases. See `maxgen` in the script for the maximum number of generations to run to.
Usage: `python3 staircase.py > pts.res`

