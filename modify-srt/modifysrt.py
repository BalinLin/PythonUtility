#!/usr/bin/python3
# coding=utf-8
"""
String processing to reformate subtitle.
"""

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input", type=str,
                    default="input.srt", help="path of input file")
parser.add_argument("--output", type=str,
                    default="output.srt", help="path of output file")
args = parser.parse_args()

if __name__ == '__main__':
    inputfile = open(args.input,
                     'r', encoding="utf8")
    PRE = None
    with open(args.output, 'w', encoding="utf8") as outputfile:
        for line in inputfile:
            if line and line[0].isdigit() and ':' not in line:
                if PRE and PRE != '\n':
                    outputfile.write('\n')
                outputfile.write(line)
            elif line and (line[0].islower() or line[0].isupper()):
                continue
            else:
                outputfile.write(line)
            PRE = line

    inputfile.close()
