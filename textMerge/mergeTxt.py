#! /usr/bin/env python3
# coding=utf-8

import natsort
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--path", type=str, default="/exper/textMerge/textFiles/", help="path of folder")
parser.add_argument("--output", type=str, default="merged", help="name of output file")
args = parser.parse_args()


if __name__ == "__main__":
    all_txt = []
    for filename in natsort.natsorted(os.listdir(args.path)):
        print("filename:", filename)

        with open(os.path.join(args.path, filename), 'r') as fread:
                for line in fread.readlines():
                        all_txt.append(line)

    with open(args.output + '.txt', 'w') as f:
        for line in all_txt:
            f.write(line)