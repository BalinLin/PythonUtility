#!/usr/bin/python3
# coding=utf-8
"""
Merging multiple text files into single text file.
"""

import os
import argparse
import natsort

parser = argparse.ArgumentParser()

parser.add_argument("--input", type=str,
                    default="./input-files", help="path of input folder")
parser.add_argument("--output", type=str,
                    default="output.txt", help="path of output file")
args = parser.parse_args()


if __name__ == "__main__":
    all_txt = []
    for filename in natsort.natsorted(os.listdir(args.input)):
        print("filename:", filename)

        with open(os.path.join(args.input, filename), 'r', encoding="utf8") as fread:
            for line in fread.readlines():
                all_txt.append(line)

    with open(args.output, 'w', encoding="utf8") as f:
        for line in all_txt:
            f.write(line)
